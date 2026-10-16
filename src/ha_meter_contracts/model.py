"""Strict, bounded contract schema. Samples contain already calibrated values."""

from __future__ import annotations

import math
import re
from dataclasses import dataclass
from datetime import datetime
from typing import Any

UNITS = {
    "W": ("power", 1.0),
    "kW": ("power", 1000.0),
    "Wh": ("energy", 1.0),
    "kWh": ("energy", 1000.0),
    "V": ("voltage", 1.0),
    "A": ("current", 1.0),
}
BASE_UNITS = {"power": "W", "energy": "Wh", "voltage": "V", "current": "A"}
ID = re.compile(r"[a-zA-Z0-9][a-zA-Z0-9_.-]{0,95}\Z")


class InputError(ValueError):
    """Safe structured input failure; never includes raw document content."""

    def __init__(self, code: str, path: str = "$", **params: Any):
        self.code, self.path, self.params = code, path, params
        super().__init__(code)


def obj(value: Any, path: str, required: set[str], optional: set[str] | None = None) -> dict:
    if not isinstance(value, dict) or any(not isinstance(k, str) for k in value):
        raise InputError("input_object", path)
    if not required <= value.keys():
        raise InputError("input_missing", path, fields=sorted(required - value.keys()))
    if value.keys() - required - (optional or set()):
        # Unknown field names may contain private material; do not echo them.
        raise InputError("input_unknown", path)
    return value


def choice(value: Any, options: set[str], path: str) -> str:
    if not isinstance(value, str) or value not in options:
        raise InputError("input_choice", path, options=sorted(options))
    return value


def identifier(value: Any, path: str) -> str:
    if not isinstance(value, str) or ID.fullmatch(value) is None:
        raise InputError("input_identifier", path)
    return value


def number(value: Any, path: str, minimum: float = -1e15, maximum: float = 1e15) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise InputError("input_number", path)
    try:
        valid = math.isfinite(value) and minimum <= value <= maximum
    except OverflowError:
        valid = False
    if not valid:
        raise InputError("input_number", path)
    return float(value)


def timestamp(value: Any, path: str) -> datetime:
    if not isinstance(value, str) or len(value) > 40 or "T" not in value:
        raise InputError("input_timestamp", path)
    try:
        result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        raise InputError("input_timestamp", path) from None
    if result.tzinfo is None or result.utcoffset() is None:
        raise InputError("input_timestamp", path)
    return result


def array(value: Any, path: str, limit: int, nonempty: bool = False) -> list:
    if not isinstance(value, list) or len(value) > limit or (nonempty and not value):
        raise InputError("input_array", path, limit=limit)
    return value


@dataclass(frozen=True)
class Scope:
    id: str
    kind: str
    parent: str | None


@dataclass(frozen=True)
class Sample:
    value: float | None
    measured_at: datetime
    reset_at: datetime | None = None


@dataclass(frozen=True)
class Calibration:
    quantity: str
    factor: float
    reference: str
    verified_at: datetime


@dataclass(frozen=True)
class Meter:
    id: str
    scope: str
    quantity: str
    unit: str
    kind: str
    provenance: str
    sign: str
    state_class: str
    reset: str
    freshness_seconds: float
    sample: Sample | None
    previous: Sample | None
    calibration: Calibration | None
    entity_id: str | None = None
    timestamp_attribute: str | None = None


@dataclass(frozen=True)
class Sum:
    id: str
    scope: str
    meters: tuple[str, ...]
    quantity: str
    coverage: str
    max_skew_seconds: float


@dataclass(frozen=True)
class Contract:
    scopes: tuple[Scope, ...]
    meters: tuple[Meter, ...]
    sums: tuple[Sum, ...]


def parse_sample(value: Any, path: str) -> Sample | None:
    if value is None:
        return None
    o = obj(value, path, {"value", "measured_at"}, {"reset_at"})
    return Sample(
        None if o["value"] is None else number(o["value"], path + ".value"),
        timestamp(o["measured_at"], path + ".measured_at"),
        timestamp(o["reset_at"], path + ".reset_at") if "reset_at" in o else None,
    )


def parse_calibration(value: Any, path: str) -> Calibration | None:
    if value is None:
        return None
    o = obj(value, path, {"quantity", "factor", "reference", "verified_at"})
    return Calibration(
        choice(o["quantity"], set(BASE_UNITS), path + ".quantity"),
        number(o["factor"], path + ".factor", 1e-12, 1e12),
        identifier(o["reference"], path + ".reference"),
        timestamp(o["verified_at"], path + ".verified_at"),
    )


def parse_contract(value: Any) -> Contract:
    o = obj(value, "$", {"schema_version", "scopes", "meters"}, {"sums"})
    if type(o["schema_version"]) is not int or o["schema_version"] != 1:
        raise InputError("input_version", "$.schema_version")
    scopes = []
    for i, raw in enumerate(array(o["scopes"], "$.scopes", 512, True)):
        p = f"$.scopes[{i}]"
        s = obj(raw, p, {"id", "kind"}, {"parent"})
        scopes.append(
            Scope(
                identifier(s["id"], p + ".id"),
                choice(s["kind"], {"site", "circuit", "strip", "outlet", "load"}, p + ".kind"),
                identifier(s["parent"], p + ".parent") if "parent" in s else None,
            )
        )
    meters = []
    required = {
        "id",
        "scope",
        "quantity",
        "unit",
        "kind",
        "provenance",
        "sign",
        "state_class",
        "freshness_seconds",
    }
    for i, raw in enumerate(array(o["meters"], "$.meters", 512, True)):
        p = f"$.meters[{i}]"
        m = obj(
            raw,
            p,
            required,
            {"sample", "previous", "calibration", "reset", "entity_id", "timestamp_attribute"},
        )
        meters.append(
            Meter(
                identifier(m["id"], p + ".id"),
                identifier(m["scope"], p + ".scope"),
                choice(m["quantity"], set(BASE_UNITS), p + ".quantity"),
                choice(m["unit"], set(UNITS), p + ".unit"),
                choice(m["kind"], {"measured", "estimated"}, p + ".kind"),
                identifier(m["provenance"], p + ".provenance"),
                choice(m["sign"], {"nonnegative", "signed"}, p + ".sign"),
                choice(
                    m["state_class"],
                    {"measurement", "total", "total_increasing"},
                    p + ".state_class",
                ),
                choice(
                    m.get("reset", "not_applicable"),
                    {"not_applicable", "never", "periodic", "device_restart", "unknown"},
                    p + ".reset",
                ),
                number(m["freshness_seconds"], p + ".freshness_seconds", 0.001, 604800),
                parse_sample(m.get("sample"), p + ".sample"),
                parse_sample(m.get("previous"), p + ".previous"),
                parse_calibration(m.get("calibration"), p + ".calibration"),
                identifier(m["entity_id"], p + ".entity_id") if "entity_id" in m else None,
                identifier(m["timestamp_attribute"], p + ".timestamp_attribute")
                if "timestamp_attribute" in m
                else None,
            )
        )
    sums = []
    for i, raw in enumerate(array(o.get("sums", []), "$.sums", 128)):
        p = f"$.sums[{i}]"
        s = obj(raw, p, {"id", "scope", "meters", "quantity", "coverage"}, {"max_skew_seconds"})
        members = tuple(
            identifier(m, p + f".meters[{j}]")
            for j, m in enumerate(array(s["meters"], p + ".meters", 512, True))
        )
        sums.append(
            Sum(
                identifier(s["id"], p + ".id"),
                identifier(s["scope"], p + ".scope"),
                members,
                choice(s["quantity"], {"power", "energy"}, p + ".quantity"),
                choice(s["coverage"], {"partial", "complete"}, p + ".coverage"),
                number(s.get("max_skew_seconds", 2), p + ".max_skew_seconds", 0, 604800),
            )
        )
    return Contract(tuple(scopes), tuple(meters), tuple(sums))
