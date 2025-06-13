import importlib.util
import logging
from pathlib import Path
from fastapi import FastAPI, APIRouter

log = logging.getLogger(__name__)


def load_plugins(app: FastAPI, plugins_path: Path | None = None) -> None:
    """Dynamically load plugins from plugins_path and register their routers."""
    if plugins_path is None:
        plugins_path = Path(__file__).resolve().parents[2] / "plugins"

    app.state.plugins = {}
    app.state.plugin_configs = {}

    if not plugins_path.exists():
        log.warning("Plugins directory not found: %s", plugins_path)
        return

    for file in plugins_path.iterdir():
        if file.is_dir():
            init_file = file / "__init__.py"
            if not init_file.exists():
                continue
            module_path = init_file
            name = file.name
        elif file.suffix == ".py":
            module_path = file
            name = file.stem
        else:
            continue

        spec = importlib.util.spec_from_file_location(f"plugins.{name}", module_path)
        if not spec or not spec.loader:
            continue
        module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)
        except Exception as e:
            log.exception("Failed to load plugin %s: %s", name, e)
            continue

        router = getattr(module, "router", None)
        if isinstance(router, APIRouter):
            prefix = getattr(module, "PLUGIN_PREFIX", f"/plugins/{name}")
            app.include_router(router, prefix=prefix, tags=[name])
            app.state.plugins[name] = {"prefix": prefix}
            app.state.plugin_configs[name] = getattr(module, "DEFAULT_CONFIG", {})
            if hasattr(module, "init"):
                try:
                    module.init(app)
                except Exception as e:
                    log.exception("Error initializing plugin %s: %s", name, e)
        else:
            log.warning("Plugin %s does not define a router", name)
