"""审计日志写入助手。"""
from __future__ import annotations

import json
from typing import Any, Optional

from sqlalchemy.orm import Session

from ..models import AuditLog


def write_audit(
    db: Session,
    *,
    action: str,
    actor_id: Optional[str] = None,
    org_id: Optional[str] = None,
    target: Optional[str] = None,
    detail: Optional[dict[str, Any]] = None,
    ip: Optional[str] = None,
) -> None:
    entry = AuditLog(
        org_id=org_id,
        actor_id=actor_id,
        action=action,
        target=target,
        detail_json=json.dumps(detail, ensure_ascii=False) if detail else None,
        ip=ip,
    )
    db.add(entry)
    db.flush()
