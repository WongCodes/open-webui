from datetime import datetime
from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/", response_model=dict)
async def get_time(request: Request):
    """Return the current server time."""
    return {"time": datetime.utcnow().isoformat() + "Z"}


# Default configuration for this plugin
default_config = {"enabled": True}

# Example setup function showing how a plugin can modify the app


def setup(app):
    if default_config.get("enabled"):

        @app.middleware("http")
        async def add_time_header(request: Request, call_next):
            response = await call_next(request)
            response.headers["X-Time-Plugin"] = "1"
            return response
