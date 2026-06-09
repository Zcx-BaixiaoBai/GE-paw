"""FastAPI 依赖：当前用户、当前组织、RBAC。"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from fastapi import Depends, Header, HTTPException, Request, status
from sqlalchemy.orm import Session

from ..exceptions import AuthError, PermissionDeniedError
from ..models import Membership, Org, User
from ..security.jwt import decode_token
from .db import get_db


@dataclass
class Principal:
    user: User
    org: Org
    role: str

    @property
    def is_admin(self) -> bool:
        return self.role == "admin" or self.user.is_super_admin


def _extract_token(request: Request, authorization: Optional[str]) -> str:
    if authorization:
        if authorization.lower().startswith("bearer "):
            return authorization.split(" ", 1)[1].strip()
        return authorization.strip()
    cookie = request.cookies.get("gepaw_access")
    if cookie:
        return cookie
    raise AuthError("缺少访问令牌")


def get_current_principal(
    request: Request,
    db: Session = Depends(get_db),
    x_org_id: Optional[str] = Header(default=None, alias="X-Org-Id"),
    authorization: Optional[str] = Header(default=None, alias="Authorization"),
) -> Principal:
    token = _extract_token(request, authorization)
    payload = decode_token(token, expected_type="access")
    user_id = payload.get("sub")
    if not user_id:
        raise AuthError("token 缺少 sub")
    user: Optional[User] = db.get(User, user_id)
    if user is None or not user.is_active:
        raise AuthError("用户不存在或已停用")

    org_ids = payload.get("org_ids") or []
    roles = payload.get("roles") or {}
    target_org_id = x_org_id or (org_ids[0] if org_ids else None)
    if not target_org_id:
        raise AuthError("用户未关联任何组织")
    if target_org_id not in org_ids:
        raise PermissionDeniedError("无权访问该组织")

    m: Optional[Membership] = (
        db.query(Membership)
        .filter(Membership.user_id == user.id, Membership.org_id == target_org_id)
        .first()
    )
    if m is None:
        raise PermissionDeniedError("用户与组织无关联")

    org: Optional[Org] = db.get(Org, target_org_id)
    if org is None:
        raise AuthError("组织不存在")

    role = roles.get(target_org_id) or m.role
    return Principal(user=user, org=org, role=role)


def require_user(principal: Principal = Depends(get_current_principal)) -> Principal:
    return principal


def require_admin(principal: Principal = Depends(get_current_principal)) -> Principal:
    if not principal.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="需要管理员权限")
    return principal
