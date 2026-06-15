"""GE-paw FastAPI 应用入口。"""

from __future__ import annotations



import os

from contextlib import asynccontextmanager

from pathlib import Path



from fastapi import FastAPI, Request

from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import JSONResponse

from fastapi.staticfiles import StaticFiles



from gepaw import __version__

from ..exceptions import AuthError, PermissionDeniedError

from ..constant import LOG_FILE_PATH, PROJECT_NAME

from ..utils.logging import get_logger, setup_logger

from .cors import WikiNoStoreMiddleware, build_cors_options

from .db import init_db

from .routers import auth as auth_router
from .routers import gateway as gateway_router_module

from .routers.admin import admin_router

from .routers.client import client_router

from .routers.client_extras import extras_router

from .routers.webhook import webhook_router

from .settings import get_settings



logger = get_logger("app")





@asynccontextmanager

async def lifespan(app: FastAPI):

    s = get_settings()

    setup_logger(s.log_level, log_path=LOG_FILE_PATH)

    logger.info("%s v%s 启动", PROJECT_NAME, __version__)

    init_db()

    from .scheduler import start_scheduler, stop_scheduler

    # Skip channel startup when disabled via env (tests / no-channel mode).

    _skip_channels = os.environ.get("GEPAW_DISABLE_CHANNEL_STARTUP") == "1"

    if not _skip_channels:

        from .channels.manager import ChannelManager

        async def _noop_process(*_a, **_k):

            if False:

                yield None

        try:

            channel_manager = ChannelManager.from_env(_noop_process)

            await channel_manager.start_all()

        except NotImplementedError:

            logger.warning("channels unavailable; skipping startup")

            channel_manager = None

    else:

        channel_manager = None

    start_scheduler()

    try:

        yield

    finally:

        if channel_manager is not None:

            await channel_manager.stop_all()

        stop_scheduler()

        logger.info("已退出")





def create_app() -> FastAPI:

    s = get_settings()

    app = FastAPI(

        title=PROJECT_NAME,

        version=__version__,

        docs_url="/api/docs" if s.docs_enabled else None,

        redoc_url=None,

        lifespan=lifespan,

    )



    cors = build_cors_options()

    app.add_middleware(CORSMiddleware, **cors)

    app.add_middleware(WikiNoStoreMiddleware)



    @app.exception_handler(PermissionError)

    async def _on_perm(request: Request, exc: PermissionError):

        logger.warning("permission denied at %s: %s", request.url.path, exc)

        return JSONResponse(status_code=403, content={"detail": "forbidden", "message": str(exc)})



    @app.exception_handler(AuthError)

    async def _on_auth(request: Request, exc: AuthError):

        return JSONResponse(status_code=401, content={"detail": "unauthorized", "message": str(exc)})



    @app.exception_handler(PermissionDeniedError)

    async def _on_pd(request: Request, exc: PermissionDeniedError):

        return JSONResponse(status_code=403, content={"detail": "forbidden", "message": str(exc)})



    @app.exception_handler(FileNotFoundError)

    async def _on_404(request: Request, exc: FileNotFoundError):

        return JSONResponse(status_code=404, content={"detail": "not_found", "message": str(exc)})



    @app.exception_handler(Exception)

    async def _on_error(request: Request, exc: Exception):

        if isinstance(exc, PermissionError):

            return JSONResponse(status_code=403, content={"detail": "forbidden", "message": str(exc)})

        if isinstance(exc, FileNotFoundError):

            return JSONResponse(status_code=404, content={"detail": "not_found", "message": str(exc)})

        logger.exception("unhandled error at %s: %s", request.url.path, exc)

        return JSONResponse(status_code=500, content={"detail": "internal_error", "message": str(exc)})



    @app.get("/api/health")

    def health() -> dict:

        return {"ok": True, "version": __version__, "project": PROJECT_NAME}



    app.include_router(auth_router.router)

    app.include_router(admin_router)

    app.include_router(client_router)

    app.include_router(extras_router)

    app.include_router(webhook_router)
    app.include_router(gateway_router_module.router, prefix='/api')



    static_dir = Path(__file__).resolve().parents[3] / "web" / "dist"

    if static_dir.exists():

        # Serve /assets/* and other static files directly, fall back to index.html for SPA routes.

        from fastapi.responses import FileResponse

        @app.get("/assets/{file_path:path}", include_in_schema=False)

        def _static_asset(file_path: str):

            full = (static_dir / "assets" / file_path).resolve()

            if not str(full).startswith(str((static_dir / "assets").resolve())) or not full.is_file():

                return JSONResponse(status_code=404, content={"detail": "asset not found"})

            return FileResponse(str(full))



        # SPA fallback: any non-API GET that doesn't match a static file returns index.html

        @app.get("/{full_path:path}", include_in_schema=False)

        def spa_fallback(full_path: str):

            # Try to serve a real file first (vite.svg, favicon.ico, etc.)

            if full_path and "." in full_path.split("/")[-1]:

                candidate = (static_dir / full_path).resolve()

                if str(candidate).startswith(str(static_dir.resolve())) and candidate.is_file():

                    return FileResponse(str(candidate))

            index = static_dir / "index.html"

            if not index.exists():

                return JSONResponse(status_code=404, content={"detail": "index not built"})

            return FileResponse(str(index), media_type="text/html")

    else:

        @app.get("/")

        def index() -> dict:

            return {

                "project": PROJECT_NAME, "version": __version__,

                "static_dir": str(static_dir),

                "hint": "请先构建 web 端: cd web && pnpm build",

            }



    return app





app = create_app()

