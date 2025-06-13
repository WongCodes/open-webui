from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from typing import Dict

from open_webui.utils.auth import get_admin_user

router = APIRouter()


class PluginConfigForm(BaseModel):
    config: Dict


@router.get("/", response_model=list[str])
async def list_plugins(request: Request, user=Depends(get_admin_user)):
    return list(getattr(request.app.state, "plugins", {}).keys())


@router.get("/{plugin}/config", response_model=dict)
async def get_plugin_config(plugin: str, request: Request, user=Depends(get_admin_user)):
    return getattr(request.app.state, "plugin_configs", {}).get(plugin, {})


@router.post("/{plugin}/config", response_model=dict)
async def set_plugin_config(
    plugin: str,
    form: PluginConfigForm,
    request: Request,
    user=Depends(get_admin_user),
):
    if not hasattr(request.app.state, "plugin_configs"):
        request.app.state.plugin_configs = {}
    request.app.state.plugin_configs[plugin] = form.config
    return request.app.state.plugin_configs[plugin]
