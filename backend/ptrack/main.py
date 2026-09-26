"""FastAPI application entry point."""

from typing import Annotated

from fastapi import Depends, FastAPI

from ptrack import __version__
from ptrack.config import Settings, get_settings

SettingsDep = Annotated[Settings, Depends(get_settings)]

app = FastAPI(
    title="PTrack API",
    version=__version__,
    description="Multi-carrier shipment visibility: tracking, route maps and delay prediction.",
)


@app.get("/health", tags=["system"])
def health(settings: SettingsDep) -> dict:
    """Liveness check. Lists which carriers have credentials configured."""
    return {
        "status": "ok",
        "version": __version__,
        "carriers_configured": settings.configured_carriers(),
    }
