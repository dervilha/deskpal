from . import resources
import importlib.resources as pkgres

def load_resource(resource_path: str) -> str:
    with pkgres.files(resources).joinpath(resource_path).open("r", encoding="utf-8") as file:
        data = file.read()
    return data

def write_resource(resource_path: str, data: str):
    with pkgres.files(resources).joinpath(resource_path).open("w", encoding="utf-8") as file:
        file.write(data)


def load_language(language_file_path: str) -> dict[str, str]:
    out = {}
    res = load_resource(language_file_path)
    items = res.split('\n')
    for i in items:
        if len(i) < 1:
            continue
        key, value = i.split(':', 1)
        out[key.strip()] = value.strip()
    return out