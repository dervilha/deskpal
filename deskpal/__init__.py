from . import directory
from . import terminal
from . import resources
import importlib.resources as pkgres

def load_resource(resource_path: str) -> str:
    with pkgres.files(resources).joinpath(resource_path).open("r", encoding="utf-8") as file:
        data = file.read()
    return data

def write_resource(resource_path: str, data: str):
    with pkgres.files(resources).joinpath(resource_path).open("w", encoding="utf-8") as file:
        file.write(data)

