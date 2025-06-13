from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from open_webui.utils.auth import get_admin_user, get_verified_user

router = APIRouter()


@router.get("/", response_model=list[str])
async def list_plugins(request: Request, user=Depends(get_verified_user)):
    """Return list of loaded plugin names."""
    return getattr(request.app.state, "loaded_plugins", [])


class PluginConfigForm(BaseModel):
    config: dict


@router.get("/{plugin}/config", response_model=dict)
async def get_plugin_config(
    plugin: str, request: Request, user=Depends(get_admin_user)
):
    return request.app.state.config.PLUGINS.get(plugin, {})


@router.post("/{plugin}/config", response_model=dict)
async def set_plugin_config(
    plugin: str, form: PluginConfigForm, request: Request, user=Depends(get_admin_user)
):
    cfg = request.app.state.config.PLUGINS
    cfg[plugin] = form.config
    request.app.state.config.PLUGINS = cfg
    return cfg[plugin]
