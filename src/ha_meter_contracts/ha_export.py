"""Allowlisted extraction from an existing HA JSON export, never live access."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from .model import UNITS, InputError, array, number, parse_contract, timestamp


def overlay_states(document: dict, states: Any) -> dict:
    """Copy only mapped value/unit/source-time fields into a contract.

    HA last_changed/last_updated/last_reported are deliberately not substituted
    for the device's sample time. The user must map a source-time attribute.
    """
    contract = parse_contract(document)
    by_id = {}
    for state in array(states, "$ha", 4096):
        if not isinstance(state, dict) or not isinstance(state.get("entity_id"), str):
            raise InputError("ha_format", "$ha")
        if state["entity_id"] in by_id:
            raise InputError("ha_duplicate", "$ha")
        by_id[state["entity_id"]] = state
    result = deepcopy(document)
    for i, meter in enumerate(contract.meters):
        if meter.entity_id is None:
            continue
        p = f"$.meters[{i}]"
        if meter.timestamp_attribute is None:
            raise InputError("ha_timestamp", p)
        target = result["meters"][i]
        state = by_id.get(meter.entity_id)
        raw = state.get("state") if state else None
        if (
            state is None
            or raw is None
            or (isinstance(raw, str) and raw in {"unknown", "unavailable"})
        ):
            target["sample"] = None
            continue
        attributes = state.get("attributes")
        if not isinstance(attributes, dict):
            raise InputError("ha_format", p)
        unit = attributes.get("unit_of_measurement")
        if (
            not isinstance(unit, str)
            or unit not in UNITS
            or UNITS[unit][0] != meter.quantity
            or UNITS[meter.unit][0] != meter.quantity
        ):
            raise InputError("ha_unit", p)
        measured = timestamp(attributes.get(meter.timestamp_attribute), p + ".source_time")
        value = state.get("state")
        if isinstance(value, str):
            try:
                value = float(value)
            except (ValueError, OverflowError):
                raise InputError("input_number", p + ".state") from None
        value = number(value, p + ".state") * UNITS[unit][1] / UNITS[meter.unit][1]
        number(value, p + ".converted_value")
        if meter.sample and measured <= meter.sample.measured_at:
            if measured == meter.sample.measured_at and value == meter.sample.value:
                continue  # A replay does not renew time or create a new previous sample.
            raise InputError("ha_sample_order", p)
        if target.get("sample") is not None:
            target["previous"] = target["sample"]
        target["sample"] = {"value": value, "measured_at": measured.isoformat()}
    parse_contract(result)
    return result
