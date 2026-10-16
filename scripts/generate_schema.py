"""Generate the public structural JSON Schema; semantic rules remain in audit()."""

import json
from pathlib import Path


def object_schema(properties, required):
    return {
        "type": "object",
        "additionalProperties": False,
        "properties": properties,
        "required": required,
    }


def array_schema(items, maximum, minimum=0):
    return {"type": "array", "items": items, "maxItems": maximum, "minItems": minimum}


def build_schema():
    identity = {"type": "string", "pattern": "^[A-Za-z0-9][A-Za-z0-9_.-]{0,95}$"}
    time = {"type": "string", "format": "date-time", "maxLength": 40}
    number = {"type": "number", "minimum": -1e15, "maximum": 1e15}
    quantity = {"enum": ["power", "energy", "voltage", "current"]}
    sample = object_schema(
        {"value": {"anyOf": [number, {"type": "null"}]}, "measured_at": time, "reset_at": time},
        ["value", "measured_at"],
    )
    calibration = object_schema(
        {
            "quantity": quantity,
            "factor": {"type": "number", "minimum": 1e-12, "maximum": 1e12},
            "reference": identity,
            "verified_at": time,
        },
        ["quantity", "factor", "reference", "verified_at"],
    )
    scope = object_schema(
        {
            "id": identity,
            "kind": {"enum": ["site", "circuit", "strip", "outlet", "load"]},
            "parent": identity,
        },
        ["id", "kind"],
    )
    meter = object_schema(
        {
            "id": identity,
            "scope": identity,
            "quantity": quantity,
            "unit": {"enum": ["W", "kW", "Wh", "kWh", "V", "A"]},
            "kind": {"enum": ["measured", "estimated"]},
            "provenance": identity,
            "sign": {"enum": ["nonnegative", "signed"]},
            "state_class": {"enum": ["measurement", "total", "total_increasing"]},
            "reset": {"enum": ["not_applicable", "never", "periodic", "device_restart", "unknown"]},
            "freshness_seconds": {"type": "number", "minimum": 0.001, "maximum": 604800},
            "sample": {"anyOf": [sample, {"type": "null"}]},
            "previous": {"anyOf": [sample, {"type": "null"}]},
            "calibration": {"anyOf": [calibration, {"type": "null"}]},
            "entity_id": identity,
            "timestamp_attribute": identity,
        },
        [
            "id",
            "scope",
            "quantity",
            "unit",
            "kind",
            "provenance",
            "sign",
            "state_class",
            "freshness_seconds",
        ],
    )
    total = object_schema(
        {
            "id": identity,
            "scope": identity,
            "meters": array_schema(identity, 512, 1),
            "quantity": {"enum": ["power", "energy"]},
            "coverage": {"enum": ["partial", "complete"]},
            "max_skew_seconds": {"type": "number", "minimum": 0, "maximum": 604800},
        },
        ["id", "scope", "meters", "quantity", "coverage"],
    )
    schema = object_schema(
        {
            "schema_version": {"type": "integer", "const": 1},
            "scopes": array_schema(scope, 512, 1),
            "meters": array_schema(meter, 512, 1),
            "sums": array_schema(total, 128),
        },
        ["schema_version", "scopes", "meters"],
    )
    schema.update(
        {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "title": "HA Meter Contracts v1",
            "description": (
                "Structural schema only; run the CLI for physical and sample-quality rules."
            ),
        }
    )
    return schema


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    (root / "schema.json").write_text(json.dumps(build_schema(), indent=2) + "\n")
