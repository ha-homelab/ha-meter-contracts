"""Small explicit catalogs; machine codes and parameter names never translate."""

from __future__ import annotations

import json
from importlib.resources import files

LANGUAGES = ("en", "ru", "de", "es")


def catalog(lang: str) -> dict[str, str]:
    if lang not in LANGUAGES:
        raise ValueError("unsupported language")
    return json.loads(files("ha_meter_contracts").joinpath("locales", lang + ".json").read_text())
