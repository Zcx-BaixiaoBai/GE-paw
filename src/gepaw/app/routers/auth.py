"""/api/auth 路由：登录、刷新、登出、me。"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Cookie, Depends, HTTPException, Request, Response, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..audit import write_audit
from ..db import get_db
from ..deps import Principal, get_current_principal
from ...exceptions import AuthError
from ...models import RefreshToken, User
from ...security.jwt import create_access_token, create_refresh_token, decode_token
from ...security.passwords import verify_password
from ..settings import get_settings
from ..auth import has_registered_users, is_auth_enabled

router = APIRouter(prefix="/api/auth", tags=["auth"])


class LoginReq(BaseModel):
    username: str
    password: str
    org_id: Optional[str] = None


class RefreshReq(BaseModel):
    refresh_token: str


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class MeResp(BaseModel):
    id: str
    username: str
    display_name: Optional[str] = None
    is_super_admin: bool
    orgs: List[Dict[str, Any]]
    current_org: Dict[str, Any]
    role: str

class AuthStatusResponse(BaseModel):
    enabled: bool
    has_users: bool


def _build_pair(user: User, org_id: str, role: str) -> TokenPair:
    s = get_settings()
    org_ids = [m.org_id for m in user.memberships]
    roles = {m.org_id: m.role for m in user.memberships}
    access = create_access_token(user_id=user.id, org_ids=org_ids, roles_by_org=roles, ttl=s.access_ttl)
    refresh, _jti = create_refresh_token(user_id=user.id, ttl=s.refresh_ttl)
    return TokenPair(access_token=access, refresh_token=refresh, expires_in=s.access_ttl)


@router.post("/login", response_model=TokenPair)
def login(req: LoginReq, response: Response, request: Request, db: Session = Depends(get_db)) -> TokenPair:
    user: Optional[User] = db.query(User).filter(User.username == req.username).first()
    if user is None or not user.is_active or not verify_password(req.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")
    target_org_id = req.org_id
    if target_org_id is None:
        if not user.memberships:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="用户未关联任何组织")
        target_org_id = user.memberships[0].org_id
    m = next((mm for mm in user.memberships if mm.org_id == target_org_id), None)
    if m is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="用户未关联该组织")

    pair = _build_pair(user, m.org_id, m.role)
    s = get_settings()
    refresh_payload = decode_token(pair.refresh_token, expected_type="refresh")
    db.add(RefreshToken(
        jti=refresh_payload["jti"],
        user_id=user.id,
        expires_at=datetime.fromtimestamp(refresh_payload["exp"], tz=timezone.utc).replace(tzinfo=None),
    ))
    user.last_login_at = datetime.now(timezone.utc).replace(tzinfo=None)
    db.commit()
    write_audit(
        db,
        action="auth.login",
        actor_id=user.id,
        org_id=m.org_id,
        ip=request.client.host if request.client else None,
    )
    response.set_cookie("gepaw_access", pair.access_token, max_age=s.access_ttl, httponly=True, samesite="lax")
    response.set_cookie("gepaw_refresh", pair.refresh_token, max_age=s.refresh_ttl, httponly=True, samesite="lax")
    return pair


@router.post("/refresh", response_model=TokenPair)
def refresh(req: RefreshReq, response: Response, db: Session = Depends(get_db)) -> TokenPair:
    try:
        payload = decode_token(req.refresh_token, expected_type="refresh")
    except AuthError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    jti = payload.get("jti")
    rt: Optional[RefreshToken] = db.query(RefreshToken).filter(RefreshToken.jti == jti).first()
    if rt is None or rt.revoked:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="refresh token 已撤销")
    user: Optional[User] = db.get(User, payload.get("sub"))
    if user is None or not user.is_active or not user.memberships:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户无效")
    m = user.memberships[0]
    pair = _build_pair(user, m.org_id, m.role)
    s = get_settings()
    new_payload = decode_token(pair.refresh_token, expected_type="refresh")
    rt.revoked = True
    db.add(RefreshToken(
        jti=new_payload["jti"],
        user_id=user.id,
        expires_at=datetime.fromtimestamp(new_payload["exp"], tz=timezone.utc).replace(tzinfo=None),
    ))
    db.commit()
    response.set_cookie("gepaw_access", pair.access_token, max_age=s.access_ttl, httponly=True, samesite="lax")
    response.set_cookie("gepaw_refresh", pair.refresh_token, max_age=s.refresh_ttl, httponly=True, samesite="lax")
    return pair


@router.post("/logout")
def logout(response: Response, db: Session = Depends(get_db),
           gepaw_refresh: Optional[str] = Cookie(default=None)) -> Dict[str, bool]:
    if gepaw_refresh:
        try:
            payload = decode_token(gepaw_refresh, expected_type="refresh")
            jti = payload.get("jti")
            rt = db.query(RefreshToken).filter(RefreshToken.jti == jti).first()
            if rt is not None:
                rt.revoked = True
                db.commit()
        except AuthError:
            pass
    response.delete_cookie("gepaw_access")
    response.delete_cookie("gepaw_refresh")
    return {"ok": True}


@router.get("/me", response_model=MeResp)
def me(principal: Principal = Depends(get_current_principal)) -> MeResp:
    return MeResp(
        id=principal.user.id,
        username=principal.user.username,
        display_name=principal.user.display_name,
        is_super_admin=principal.user.is_super_admin,
        orgs=[{"id": m.org_id, "name": m.org.name, "slug": m.org.slug, "role": m.role} for m in principal.user.memberships],
        current_org={"id": principal.org.id, "name": principal.org.name, "slug": principal.org.slug},
        role=principal.role,
    )

@router.get("/status", response_model=AuthStatusResponse)
def auth_status() -> AuthStatusResponse:
    """Check whether authentication is enabled and whether any
    user has registered."""
    return AuthStatusResponse(
        enabled=is_auth_enabled(),
        has_users=has_registered_users(),
    )
