from __future__ import annotations

import copy
import json
import os
import subprocess
import sys
from datetime import UTC, datetime
from itertools import permutations
from pathlib import Path

import pytest

from ha_meter_contracts import InputError, audit, load_document, parse_contract
from ha_meter_contracts.ha_export import overlay_states
from ha_meter_contracts.reader import MAX_BYTES, loads_document

ROOT = Path(__file__).resolve().parents[1]
AT = datetime(2026, 1, 1, 12, 0, 5, tzinfo=UTC)


def fixture(name="valid-three-meters.json"):
    return load_document(ROOT / "examples" / name)


def check(document, at=AT):
    return audit(parse_contract(document), at=at)


def codes(report):
    return {f["code"] for f in report["findings"]}


def test_valid_units_and_true_zero():
    result = check(fixture())
    assert result["findings"] == []
    assert result["sums"][0]["value"] == 720
    assert result["sums"][0]["unit"] == "W"


def test_aggregate_cannot_be_used_as_individual_pump():
    result = check(fixture("kmc-shared-meter.json"))
    assert "scope_outside" in codes(result)
    assert result["sums"][0]["value"] is None


def test_aliases_allowed_but_not_added():
    document = fixture("duplicate-emporia.json")
    result = check(document)
    assert {"alias_stream", "duplicate_stream"} <= codes(result)
    assert result["sums"][0]["value"] is None
    document["sums"] = []
    result = check(document)
    assert result["summary"] == {"error": 0, "warning": 0, "info": 1}


def test_parent_plus_child_double_count():
    document = fixture()
    document["meters"][0]["scope"] = "strip"
    assert "scope_overlap" in codes(check(document))


def test_complete_coverage_missing_child_but_partial_is_allowed():
    document = fixture()
    document["sums"][0]["meters"].pop()
    assert "incomplete_coverage" in codes(check(document))
    document["sums"][0]["coverage"] = "partial"
    result = check(document)
    assert result["sums"][0]["value"] == 720


@pytest.mark.parametrize(
    "change,expected",
    [
        ({"sample": None}, "sample_missing"),
        ({"unit": "V"}, "unit_dimension"),
        ({"state_class": "total"}, "instant_semantics"),
        ({"scope": "absent"}, "missing_scope"),
        ({"sample": {"value": -1, "measured_at": "2026-01-01T12:00:00Z"}}, "negative_value"),
        ({"sample": {"value": 1, "measured_at": "2026-01-01T12:01:00Z"}}, "sample_future"),
        ({"sample": {"value": 1, "measured_at": "2026-01-01T11:59:00Z"}}, "sample_stale"),
    ],
)
def test_invalid_member_disables_sum(change, expected):
    document = fixture()
    document["meters"][0].update(change)
    result = check(document)
    assert expected in codes(result)
    assert result["sums"][0]["value"] is None


def test_skew_blocks_sum_even_when_all_members_fresh():
    document = fixture()
    document["meters"][0]["sample"]["measured_at"] = "2026-01-01T11:59:55Z"
    result = check(document)
    assert "sample_stale" not in codes(result)
    assert "sample_skew" in codes(result)
    assert result["sums"][0]["value"] is None


def test_estimate_is_preserved_in_sum():
    document = fixture()
    document["meters"][1]["kind"] = "estimated"
    result = check(document)
    assert result["sums"][0]["kind"] == "estimated"
    assert result["sums"][0]["value"] == 720


def test_cycle_and_missing_parent_do_not_crash():
    document = fixture()
    document["scopes"][0]["parent"] = "outlet_a"
    result = check(document)
    assert "scope_cycle" in codes(result)
    assert result["sums"][0]["value"] is None
    document["scopes"][0]["parent"] = "absent"
    assert "missing_scope" in codes(check(document))


def test_duplicate_ids_and_missing_members():
    document = fixture()
    document["meters"][1]["id"] = "meter_a"
    result = check(document)
    assert {"duplicate_id", "missing_meter"} <= codes(result)
    assert result["sums"][0]["value"] is None


def test_provenance_must_have_one_physical_meaning():
    document = fixture()
    document["meters"][1]["provenance"] = "meter_a"
    result = check(document)
    assert "provenance_conflict" in codes(result)
    assert result["sums"][0]["value"] is None


@pytest.mark.parametrize("order", list(permutations(range(3))))
def test_provenance_conflict_disables_every_alias_in_any_order(order):
    document = fixture()
    original = copy.deepcopy(document["meters"][0])
    alias = copy.deepcopy(original)
    alias["id"] = "alias_a"
    conflict = copy.deepcopy(document["meters"][1])
    conflict["provenance"] = original["provenance"]
    members = [original, alias, conflict]
    document["meters"] = [members[i] for i in order]
    document["sums"] = [
        dict(
            id="sum_" + meter["id"],
            scope=meter["scope"],
            meters=[meter["id"]],
            quantity="power",
            coverage="complete",
        )
        for meter in members
    ]
    report = check(document)
    assert "provenance_conflict" in codes(report)
    assert all(total["value"] is None for total in report["sums"])
    assert all(total["status"] == "unavailable" for total in report["sums"])


def test_voltage_calibration_does_not_calibrate_watts():
    document = fixture()
    document["meters"][0]["calibration"] = dict(
        quantity="voltage",
        factor=0.95,
        reference="reference_meter",
        verified_at="2025-12-31T12:00:00Z",
    )
    assert "calibration_dimension" in codes(check(document))
    document["meters"][0]["calibration"]["quantity"] = "power"
    assert check(document)["sums"][0]["value"] == 720  # Never apply the factor a second time.


def energy():
    document = fixture()
    for meter in document["meters"]:
        meter.update(quantity="energy", unit="Wh", state_class="total_increasing", reset="periodic")
        meter["sample"].update(value=10, reset_at="2026-01-01T00:00:00Z")
    document["sums"][0]["quantity"] = "energy"
    return document


def test_aligned_energy_periods_can_be_summed():
    assert check(energy())["sums"][0]["value"] == 30


def test_unlike_energy_origins_are_not_summed():
    document = energy()
    document["meters"][0]["sample"].pop("reset_at")
    result = check(document)
    assert "energy_sum_origin" in codes(result)
    assert result["sums"][0]["value"] is None


def test_counter_drop_needs_reset_evidence():
    document = energy()
    meter = document["meters"][0]
    meter["previous"] = {"value": 50, "measured_at": "2026-01-01T11:59:59Z"}
    assert "reset_unproven" in codes(check(document))
    meter["sample"]["reset_at"] = "2026-01-01T12:00:00Z"
    assert "reset_unproven" not in codes(check(document))
    meter["reset"] = "never"
    assert "counter_decreased" in codes(check(document))


def test_signed_net_energy_is_not_increasing():
    document = energy()
    document["meters"][0].update(sign="signed")
    assert "signed_increasing" in codes(check(document))
    document["meters"][0].update(state_class="total")
    document["meters"][0]["sample"]["value"] = -10
    assert "negative_value" not in codes(check(document))
    assert "sum_sign" in codes(check(document))


@pytest.mark.parametrize(
    "field,value", [("schema_version", True), ("schema_version", 2), ("unknown", "private")]
)
def test_strict_root_schema(field, value):
    document = fixture()
    document[field] = value
    with pytest.raises(InputError):
        parse_contract(document)


@pytest.mark.parametrize("value", [True, "0", float("nan"), float("inf"), 10**400])
def test_numeric_types_and_bounds(value):
    document = fixture()
    document["meters"][0]["sample"]["value"] = value
    with pytest.raises(InputError):
        parse_contract(document)


@pytest.mark.parametrize(
    "text,fmt",
    [
        ('{"a": 1, "a": 2}', "json"),
        ('{"a": NaN}', "json"),
        ("a: 1\na: 2", "yaml"),
        ("a: &a [1]\nb: *a", "yaml"),
        ("a: !!str value", "yaml"),
        ("true: value", "yaml"),
        ("[" * 40 + "0" + "]" * 40, "json"),
    ],
)
def test_reader_rejects_ambiguous_or_deep_input(text, fmt):
    with pytest.raises(InputError):
        loads_document(text, fmt)


def test_oversized_input():
    with pytest.raises(InputError, match="input_size"):
        loads_document(" " * (MAX_BYTES + 1))


def test_file_reader_rejects_fifo_without_waiting(tmp_path):
    pipe = tmp_path / "input.json"
    os.mkfifo(pipe)
    script = """
import sys
from ha_meter_contracts import InputError, load_document
try:
    load_document(sys.argv[1])
except InputError as exc:
    assert exc.code == "input_read"
else:
    raise AssertionError("FIFO accepted")
"""
    result = subprocess.run(
        [sys.executable, "-c", script, str(pipe)],
        capture_output=True,
        text=True,
        timeout=5,
        check=False,
    )
    assert result.returncode == 0, result.stderr


def test_file_reader_rejects_symlink_directory_device_and_missing_file(tmp_path):
    target = tmp_path / "target.json"
    target.write_text("{}")
    link = tmp_path / "link.json"
    link.symlink_to(target)
    for path in (link, tmp_path, Path(os.devnull), tmp_path / "missing.json"):
        with pytest.raises(InputError, match="input_read"):
            load_document(path)


def test_file_reader_enforces_size_after_open_and_when_file_grows(tmp_path, monkeypatch):
    path = tmp_path / "large.json"
    path.write_bytes(b" " * (MAX_BYTES + 1))
    with pytest.raises(InputError, match="input_size"):
        load_document(path)
    real_stat = os.fstat

    def earlier_size(fd):
        # Model growth after the size check: the read bound must still apply.
        info = list(real_stat(fd))
        info[6] = 0
        return os.stat_result(info)

    monkeypatch.setattr(os, "fstat", earlier_size)
    with pytest.raises(InputError, match="input_size"):
        load_document(path)


def test_json_and_yaml_equivalent():
    document = fixture("minimal.yaml")
    assert check(document)["findings"] == []
    assert document == loads_document(json.dumps(document))


def test_naive_timestamp_rejected():
    document = fixture()
    document["meters"][0]["sample"]["measured_at"] = "2026-01-01T12:00:00"
    with pytest.raises(InputError, match="input_timestamp"):
        check(document)


def test_ha_overlay_converts_units_without_copying_private_attributes():
    contract, states = fixture("ha-contract.json"), fixture("ha-states.synthetic.json")
    original = copy.deepcopy(contract)
    states[0]["attributes"]["private_note"] = "do-not-copy-this"
    result = overlay_states(contract, states)
    assert result["meters"][0]["sample"]["value"] == 720
    assert "do-not-copy-this" not in json.dumps(result)
    assert contract == original
    assert check(result)["summary"]["error"] == 0


def test_ha_cached_state_time_never_substitutes_for_source_time():
    contract, states = fixture("ha-contract.json"), fixture("ha-states.synthetic.json")
    states[0]["last_updated"] = "2026-01-01T12:00:00Z"
    del states[0]["attributes"]["source_measured_at"]
    with pytest.raises(InputError, match="input_timestamp"):
        overlay_states(contract, states)


def test_ha_replay_is_idempotent_and_conflicting_old_data_rejected():
    contract, states = fixture("ha-contract.json"), fixture("ha-states.synthetic.json")
    result = overlay_states(contract, states)
    assert overlay_states(result, states) == result
    states[0]["state"] = "0.99"
    with pytest.raises(InputError, match="ha_sample_order"):
        overlay_states(result, states)


def test_ha_missing_or_unavailable_never_becomes_zero():
    contract = fixture("ha-contract.json")
    result = overlay_states(contract, [])
    assert result["meters"][0]["sample"] is None
    assert "sample_missing" in codes(check(result))


@pytest.mark.parametrize("state", [{}, [], True, "nan", "infinity"])
def test_ha_malformed_state_returns_input_error(state):
    contract, states = fixture("ha-contract.json"), fixture("ha-states.synthetic.json")
    states[0]["state"] = state
    with pytest.raises(InputError):
        overlay_states(contract, states)
