"""中间件：CORS + 严格 wiki no-store 缓存策略。"""
from __future__ import annotations

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from .settings import get_settings


class WikiNoStoreMiddleware(BaseHTTPMiddleware):
    """对 /api/client/wiki/* 与 /api/admin/wiki/* 强制 no-store + no-cache。"""

    def __init__(self, app, prefixes=("/api/client/wiki", "/api/admin/wiki")) -> None:
        super().__init__(app)
        # NOTE: extras (diff / preview-data / plan) all read wiki content server-side,
        # so they are part of the no-store contract as well. Other client/admin
        # routes (chat, sessions, crons, tokens, ...) stay cacheable by default.
        self.prefixes = (
            '/api/client/wiki',
            '/api/admin/wiki',
            '/api/client/diff',
            '/api/client/preview-data',
            '/api/client/plan',
        )

    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)
        path = request.url.path
        if any(path.startswith(p) for p in self.prefixes):
            response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"
        return response


def build_cors_options() -> dict:
    s = get_settings()
    return {
        "allow_origins": s.cors_origins,
        "allow_credentials": True,
        "allow_methods": ["*"],
        "allow_headers": ["*"],
    }
