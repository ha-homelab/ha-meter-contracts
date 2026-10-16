"""Validate declared topology and evidence, without claiming physical verification."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from .model import BASE_UNITS, UNITS, Contract, InputError, Meter


def audit(contract: Contract, *, at: datetime) -> dict[str, Any]:
    """Return deterministic machine findings and additive values at an explicit time."""
    if at.tzinfo is None or at.utcoffset() is None:
        raise InputError("input_timestamp", "$.at")
    findings: list[dict[str, Any]] = []

    def add(code: str, severity: str, path: str, **params: Any) -> None:
        findings.append({"code": code, "severity": severity, "path": path, "params": params})

    def index(items: tuple, path: str) -> dict:
        result = {}
        for i, item in enumerate(items):
            if item.id in result:
                add("duplicate_id", "error", f"{path}[{i}].id", id=item.id)
            result[item.id] = item
        return result

    scopes = index(contract.scopes, "$.scopes")
    meters = index(contract.meters, "$.meters")
    index(contract.sums, "$.sums")
    graph_valid = not findings
    for i, scope in enumerate(contract.scopes):
        if scope.parent is not None and scope.parent not in scopes:
            add("missing_scope", "error", f"$.scopes[{i}].parent", scope=scope.parent)
            graph_valid = False
        visited, current = set(), scope.id
        while current in scopes:
            if current in visited:
                add("scope_cycle", "error", f"$.scopes[{i}]", scope=scope.id)
                graph_valid = False
                break
            visited.add(current)
            current = scopes[current].parent

    def below(child: str, parent: str) -> bool:
        visited = set()
        while child in scopes and child not in visited:
            if child == parent:
                return True
            visited.add(child)
            child = scopes[child].parent
        return False

    children = {s.id: [] for s in contract.scopes}
    for scope in contract.scopes:
        if scope.parent in children:
            children[scope.parent].append(scope.id)

    def leaves(scope: str) -> set[str]:
        return {s for s in scopes if not children[s] and below(s, scope)}

    streams: dict[str, Meter] = {}
    ready: dict[str, bool] = {}
    for i, meter in enumerate(contract.meters):
        p = f"$.meters[{i}]"
        start = len(findings)
        if meter.scope not in scopes:
            add("missing_scope", "error", p + ".scope", scope=meter.scope)
        if UNITS[meter.unit][0] != meter.quantity:
            add("unit_dimension", "error", p + ".unit", quantity=meter.quantity, unit=meter.unit)
        if meter.kind == "estimated":
            add("estimated_value", "info", p, meter=meter.id)
        if meter.provenance in streams:
            original = streams[meter.provenance]
            if (original.scope, original.quantity, original.sign) != (
                meter.scope,
                meter.quantity,
                meter.sign,
            ):
                add("provenance_conflict", "error", p + ".provenance", meter=original.id)
                ready[original.id] = False
            else:
                add("alias_stream", "info", p + ".provenance", meter=original.id)
        else:
            streams[meter.provenance] = meter
        if meter.quantity == "energy":
            if meter.state_class == "measurement" or meter.reset == "not_applicable":
                add("energy_semantics", "error", p)
            if meter.state_class == "total_increasing" and meter.sign == "signed":
                add("signed_increasing", "error", p + ".state_class")
            if meter.reset == "unknown":
                add("reset_unknown", "warning", p + ".reset")
        elif meter.state_class != "measurement" or meter.reset != "not_applicable":
            add("instant_semantics", "error", p)
        if meter.calibration:
            if meter.calibration.quantity != meter.quantity:
                add("calibration_dimension", "error", p + ".calibration", quantity=meter.quantity)
            if meter.calibration.verified_at > at:
                add("calibration_future", "error", p + ".calibration.verified_at")
        if meter.sample is None or meter.sample.value is None:
            add("sample_missing", "warning", p + ".sample")
        if meter.sample:
            age = (at - meter.sample.measured_at).total_seconds()
            if age < 0:
                add("sample_future", "error", p + ".sample.measured_at")
            elif age > meter.freshness_seconds:
                add(
                    "sample_stale",
                    "warning",
                    p + ".sample.measured_at",
                    age_seconds=age,
                    limit_seconds=meter.freshness_seconds,
                )
        for label, sample in (("sample", meter.sample), ("previous", meter.previous)):
            if sample is None:
                continue
            if sample.value is not None and sample.value < 0 and meter.sign == "nonnegative":
                add("negative_value", "error", p + f".{label}.value")
            if sample.reset_at and (
                meter.quantity != "energy" or sample.reset_at > sample.measured_at
            ):
                add("reset_marker", "error", p + f".{label}.reset_at")
        if meter.previous and meter.sample:
            old, new = meter.previous, meter.sample
            if old.measured_at >= new.measured_at:
                add("sample_order", "error", p + ".previous.measured_at")
            if (
                meter.quantity == "energy"
                and old.value is not None
                and new.value is not None
                and new.value < old.value
                and meter.sign == "nonnegative"
            ):
                reset = (
                    new.reset_at is not None and old.measured_at < new.reset_at <= new.measured_at
                )
                if meter.reset == "never":
                    add("counter_decreased", "error", p + ".sample.value")
                elif not reset:
                    add("reset_unproven", "warning", p + ".sample.value")
            if old.reset_at and new.reset_at and new.reset_at < old.reset_at:
                add("reset_order", "error", p + ".sample.reset_at")
        ready[meter.id] = ready.get(meter.id, True) and not any(
            f["severity"] != "info" for f in findings[start:]
        )

    totals = []
    for i, total in enumerate(contract.sums):
        p, start = f"$.sums[{i}]", len(findings)
        selected = [meters[m] for m in total.meters if m in meters]
        if total.scope not in scopes:
            add("missing_scope", "error", p + ".scope", scope=total.scope)
        if len(set(total.meters)) != len(total.meters):
            add("duplicate_member", "error", p + ".meters")
        for member in total.meters:
            if member not in meters:
                add("missing_meter", "error", p + ".meters", meter=member)
        for j, meter in enumerate(selected):
            if meter.quantity != total.quantity:
                add("sum_dimension", "error", p + ".meters", meter=meter.id)
            if not below(meter.scope, total.scope):
                add("scope_outside", "error", p + ".meters", meter=meter.id, scope=total.scope)
            for other in selected[:j]:
                if meter.provenance == other.provenance:
                    add("duplicate_stream", "error", p + ".meters", meters=[other.id, meter.id])
                elif below(meter.scope, other.scope) or below(other.scope, meter.scope):
                    add("scope_overlap", "error", p + ".meters", meters=[other.id, meter.id])
        if graph_valid and total.scope in scopes and total.coverage == "complete":
            covered = set().union(*(leaves(m.scope) for m in selected))
            missing = sorted(leaves(total.scope) - covered)
            if missing:
                add("incomplete_coverage", "error", p + ".meters", scopes=missing)
        available = all(ready.get(m.id, False) for m in selected)
        if not available:
            add("sum_unavailable", "warning", p)
        times = [m.sample.measured_at for m in selected if m.sample]
        if len(times) > 1 and (max(times) - min(times)).total_seconds() > total.max_skew_seconds:
            add("sample_skew", "warning", p, limit_seconds=total.max_skew_seconds)
        if len({m.sign for m in selected}) > 1:
            add("sum_sign", "error", p)
        # Cumulative readings need an explicitly declared common counter origin.
        origins = {m.sample.reset_at for m in selected if m.sample}
        if total.quantity == "energy" and (len(origins) != 1 or None in origins):
            add("energy_sum_origin", "warning", p)
        valid = (
            graph_valid
            and bool(selected)
            and available
            and not any(f["severity"] != "info" for f in findings[start:])
        )
        value = sum(m.sample.value * UNITS[m.unit][1] for m in selected) if valid else None
        totals.append(
            {
                "id": total.id,
                "scope": total.scope,
                "quantity": total.quantity,
                "unit": BASE_UNITS[total.quantity],
                "value": value,
                "status": "available" if valid else "unavailable",
                "kind": "estimated" if any(m.kind == "estimated" for m in selected) else "measured",
                "coverage": total.coverage,
            }
        )
    findings.sort(key=lambda f: (f["path"], f["code"], str(f["params"])))
    summary = {
        level: sum(f["severity"] == level for f in findings)
        for level in ("error", "warning", "info")
    }
    return {
        "schema_version": 1,
        "at": at.astimezone(UTC).isoformat(),
        "summary": summary,
        "findings": findings,
        "sums": totals,
    }
