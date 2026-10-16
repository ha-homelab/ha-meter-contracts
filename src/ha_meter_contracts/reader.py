"""Read bounded JSON or YAML, rejecting duplicate keys, aliases and custom tags."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from .model import InputError

MAX_BYTES = 1_048_576
MAX_NODES = 20_000
MAX_DEPTH = 16


def _pairs(pairs: list) -> dict:
    result = {}
    for key, value in pairs:
        if not isinstance(key, str) or key in result:
            raise InputError("input_duplicate")
        result[key] = value
    return result


class StrictLoader(yaml.SafeLoader):
    pass


def _mapping(loader: StrictLoader, node: yaml.Node) -> dict:
    return _pairs([(loader.construct_object(k), loader.construct_object(v)) for k, v in node.value])


StrictLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _mapping)


def _bounds(value: Any) -> None:
    stack, count = [(value, 0)], 0
    while stack:
        node, depth = stack.pop()
        count += 1
        if depth > MAX_DEPTH or count > MAX_NODES:
            raise InputError("input_bounds")
        if isinstance(node, dict):
            stack.extend((v, depth + 1) for v in node.values())
        elif isinstance(node, list):
            stack.extend((v, depth + 1) for v in node)


def loads_document(text: str, format: str = "json") -> Any:
    if len(text.encode("utf-8")) > MAX_BYTES:
        raise InputError("input_size", limit=MAX_BYTES)
    try:
        if format == "json":

            def reject_constant(_: str) -> None:
                raise InputError("input_number")

            value = json.loads(text, object_pairs_hook=_pairs, parse_constant=reject_constant)
        elif format == "yaml":
            for token in yaml.scan(text):
                if isinstance(token, (yaml.AliasToken, yaml.AnchorToken, yaml.TagToken)):
                    raise InputError("input_yaml_features")
            value = yaml.load(text, Loader=StrictLoader)
        else:
            raise InputError("input_format")
    except (json.JSONDecodeError, yaml.YAMLError, RecursionError, ValueError) as exc:
        if isinstance(exc, InputError):
            raise
        raise InputError("input_parse") from None
    _bounds(value)
    return value


def load_document(path: str | Path) -> Any:
    p = Path(path)
    try:
        with p.open("rb") as stream:
            content = stream.read(MAX_BYTES + 1)
        if len(content) > MAX_BYTES:
            raise InputError("input_size", limit=MAX_BYTES)
        text = content.decode("utf-8")
    except (OSError, UnicodeError):
        raise InputError("input_read") from None
    return loads_document(text, "yaml" if p.suffix.lower() in {".yaml", ".yml"} else "json")
