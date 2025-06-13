import importlib
import logging
import pkgutil
from pathlib import Path
from fastapi import FastAPI
from open_webui.config import save_config

log = logging.getLogger(__name__)


def load_plugins(app: FastAPI):
    """Discover and load plugins from the ``plugins`` package."""
    try:
        pkg = importlib.import_module("plugins")
    except ModuleNotFoundError:
        log.info("No plugins directory found")
        app.state.loaded_plugins = []
        return []

    plugin_path = Path(pkg.__file__).parent
    loaded = []

    for _, name, _ in pkgutil.iter_modules([str(plugin_path)]):
        module = importlib.import_module(f"plugins.{name}")

        # Register router if available
        if hasattr(module, "router"):
            prefix = getattr(module, "PREFIX", f"/plugins/{name}")
            app.include_router(module.router, prefix=prefix, tags=["plugins"])

        # Run custom setup if defined
        if hasattr(module, "setup"):
            try:
                module.setup(app)
            except Exception as exc:
                log.exception("Error setting up plugin %s: %s", name, exc)

        # Persist default configuration
        if hasattr(module, "default_config"):
            cfg = app.state.config.PLUGINS
            if name not in cfg:
                cfg[name] = module.default_config
                app.state.config.PLUGINS = cfg
        loaded.append(name)

    app.state.loaded_plugins = loaded
    return loaded
