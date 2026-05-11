from typing import Any
import httpx
import yaml


def load_resource(filename: str) -> Any:
    from importlib import resources
    ref = resources.files("wbmcp") / "data" / filename
    with ref.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_local(filename: str) -> Any:
    with open("data/" + filename, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_http(url: str) -> Any:
    data = httpx.get(url)
    return yaml.safe_load(data.content)
