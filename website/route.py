import os
from fastapi import APIRouter
import importlib
from pathlib import Path
from typing import List
from .config import BASE_DIR, ROOT_DIR, logger
from main import app

# BASE_DIR= os.getcwd()
# ROOT= Path(__file__).parent.name
# ROOT_PATH= Path(f"{BASE_DIR}/{ROOT}")
print( 'ROOT_PATH', BASE_DIR, ROOT_DIR / "domain")

def load_domain_routers(basedir, suffix: str) -> List[APIRouter]:
    # print('basedir', basedir)
    routers = []
    for subdir in Path(basedir).iterdir():
        if subdir.is_dir() and not subdir.name.startswith("__"):
            router_filename = f"{subdir.name}{suffix}.py"
            router_path = subdir / router_filename

            if router_path.exists():
                relative_path = subdir.relative_to(BASE_DIR)
                module_base = relative_path.as_posix().replace("/", ".")
                # print('router_path', relative_path, module_base, subdir.name)
                module_name= f"{module_base}.{subdir.name}{suffix}"
                try:
                    module = importlib.import_module(module_name)
                    router = getattr(module, "router", None)
                    if isinstance(router, APIRouter):
                        routers.append(router)
                except Exception as e:
                    print(f"❌ Error importing {module_name}: {e}")

    return routers

routers= load_domain_routers(ROOT_DIR / "domain", "_router")
for route in routers:
    app.include_router(route)
