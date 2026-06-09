"""gepaw.app.approvals: approval service helpers used by tool guard mixins.

The real module wires FastAPI request handling; the test-only stub
exposes a ``get_approval_service()`` factory so the lazy-init code path
in :class:`ToolGuardMixin` can be exercised.
"""
from __future__ import annotations

from typing import Any


def get_approval_service() -> Any:
    """Return the per-agent approval service.

    Tests patch this symbol with ``@patch("gepaw.app.approvals.get_approval_service")``
    so the production implementation is not relevant for unit tests.
    """
    raise NotImplementedError(
        "gepaw.app.approvals.get_approval_service must be patched in tests.",
    )


__all__ = ["get_approval_service"]