"""GE-paw 命令行入口。"""
from __future__ import annotations

import argparse
import os
import secrets
import string
import sys
from pathlib import Path
from typing import Optional

from gepaw import __version__
from ..constant import PROJECT_NAME
from ..utils.logging import get_logger, setup_logger

logger = get_logger("cli")


def _gen_password(n: int = 16) -> str:
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(n))


def _ensure_secret_key() -> None:
    if os.environ.get("GEPAW_SECRET_KEY"):
        return
    key = secrets.token_urlsafe(48)
    os.environ["GEPAW_SECRET_KEY"] = key
    env_path = Path(".env")
    if not env_path.exists():
        env_path.write_text(f"GEPAW_SECRET_KEY={key}\n", encoding="utf-8")
    else:
        with env_path.open("a", encoding="utf-8") as f:
            f.write(f"\nGEPAW_SECRET_KEY={key}\n")


def cmd_init(args: argparse.Namespace) -> int:
    from ..app.db import init_db, session_scope
    from ..app.settings import get_settings
    from ..models import Membership, Org, User
    from ..security.passwords import hash_password

    _ensure_secret_key()
    s = get_settings()
    init_db()
    setup_logger(s.log_level)
    username = args.username or s.admin_username
    password = args.password or s.admin_password or _gen_password()
    org_name = args.org_name or s.org_name
    org_slug = args.org_slug or "default"

    with session_scope() as db:
        org: Optional[Org] = db.query(Org).filter(Org.slug == org_slug).first()
        if org is None:
            org = Org(name=org_name, slug=org_slug)
            db.add(org); db.flush()
        user: Optional[User] = db.query(User).filter(User.username == username).first()
        if user is None:
            user = User(
                username=username,
                display_name=username,
                password_hash=hash_password(password),
                is_super_admin=True,
            )
            db.add(user); db.flush()
            db.add(Membership(user_id=user.id, org_id=org.id, role="admin"))
        else:
            user.is_super_admin = True
            user.password_hash = hash_password(password)
            existing = next((m for m in user.memberships if m.org_id == org.id), None)
            if existing is None:
                db.add(Membership(user_id=user.id, org_id=org.id, role="admin"))
    print()
    print(f"== {PROJECT_NAME} 初始化完成 ==")
    print(f"  管理员用户名: {username}")
    print(f"  管理员密码 : {password}")
    print(f"  默认组织   : {org_name} (slug: {org_slug})")
    print(f"  数据目录   : {s.data_dir}")
    print(f"  数据库     : {s.database_url}")
    print()
    return 0


def cmd_serve(args: argparse.Namespace) -> int:
    from ..app.settings import get_settings
    import uvicorn

    _ensure_secret_key()
    s = get_settings()
    setup_logger(s.log_level)
    uvicorn.run(
        "gepaw.app._app:app",
        host=args.host or s.host,
        port=args.port or s.port,
        reload=args.reload,
        log_level=s.log_level,
    )
    return 0


def cmd_health(args: argparse.Namespace) -> int:
    import httpx
    base = args.base
    try:
        r = httpx.get(f"{base.rstrip('/')}/api/health", timeout=5.0)
        r.raise_for_status()
        print(r.json())
        return 0
    except Exception as e:
        print(f"health check failed: {e}")
        return 1


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="gepaw", description=f"{PROJECT_NAME} CLI")
    p.add_argument("--version", action="version", version=f"{PROJECT_NAME} v{__version__}")
    sub = p.add_subparsers(dest="cmd", required=True)

    p_init = sub.add_parser("init", help="初始化首位管理员与默认组织")
    p_init.add_argument("--username", default=None)
    p_init.add_argument("--password", default=None)
    p_init.add_argument("--org-name", default=None)
    p_init.add_argument("--org-slug", default="default")
    p_init.set_defaults(func=cmd_init)

    p_serve = sub.add_parser("serve", help="启动 API 服务（默认 0.0.0.0:8765）")
    p_serve.add_argument("--host", default=None)
    p_serve.add_argument("--port", type=int, default=None)
    p_serve.add_argument("--reload", action="store_true")
    p_serve.set_defaults(func=cmd_serve)

    p_health = sub.add_parser("health", help="探测 /api/health")
    p_health.add_argument("--base", default="http://127.0.0.1:8765")
    p_health.set_defaults(func=cmd_health)

    return p


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


def cli() -> None:
    sys.exit(main())


if __name__ == "__main__":
    cli()
