# =============================================================
# main.py — App factory i uključivanje routera
# =============================================================

import logging
from fastapi import FastAPI
from app.core.config import settings
from app.core.errors import AppError, app_error_handler
from app.core.logging import setup_logging
from app.routers.health import router as health_router
from app.routers.auth import router as auth_router
from app.routers.teams import router as teams_router

logger = logging.getLogger(__name__)

def create_app() -> FastAPI:
    # 1. Konfiguracija logiranja.
    setup_logging()

    # 2. Kreiranje FastAPI instance.
    app = FastAPI(
        title="E-sports Tournament API",
        version="0.1.0",
        description="Sustav za upravljanje e-sport turnirima i igračima",
        docs_url="/docs" if settings.ENV == "dev" else None,
        redoc_url=None,
    )

    # 3. Registracija globalnog error handlera.
    app.add_exception_handler(AppError, app_error_handler)

    # 4. Uključivanje routera.
    app.include_router(health_router, prefix="/health", tags=["health"])
    app.include_router(auth_router, prefix="/auth", tags=["auth"])
    app.include_router(teams_router, prefix="/teams", tags=["teams"])

    logger.info("Aplikacija kreirana (env=%s)", settings.ENV)
    return app

app = create_app()
