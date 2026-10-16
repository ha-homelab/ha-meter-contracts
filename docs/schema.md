# Contract schema v1

The machine-readable [schema.json](../schema.json) describes structure. The Python parser is authoritative for bounds; `audit` adds physical and temporal semantics that JSON Schema cannot prove. Generate the structural file with `python3 scripts/generate_schema.py`.

## Root and limits

Required: integer `schema_version: 1`, `scopes`, `meters`. Optional: `sums` (default empty). Unknown fields are rejected at every contract level. Up to 512 scopes, 512 meters and 128 sums; scopes and meters must not be empty. Each sum has 1–512 members. Input is UTF-8, at most 1,048,576 bytes, nesting depth 16 and 20,000 value nodes. JSON duplicate keys, NaN/Infinity, and YAML aliases/anchors/explicit tags are rejected. Quote timestamps in YAML so they remain strings.

Identifiers are 1–96 ASCII characters, beginning with a letter/digit and then letters, digits, `.`, `_`, `-`. IDs are unique within each collection; scope and meter namespaces are separate. All times include `T` and a timezone. Numbers are finite, not booleans, and within ±10^15 unless a narrower bound is given.

## Physical scopes

Each scope has `id`, `kind` (`site`, `circuit`, `strip`, `outlet`, `load`) and optional `parent`. Parents must exist and form an acyclic forest. A meter on a parent covers all its descendants. Scope kinds are descriptive; they do not infer voltage, phases, ratings, wiring or permitted parents. You declare the true topology.

## Meters

Required fields:

- `id`, `scope`: unique measurement identifier and declared physical scope.
- `quantity`: `power`, `energy`, `voltage`, `current`.
- `unit`: respectively W/kW, Wh/kWh, V, A. The parser accepts the vocabulary; the auditor checks the dimension.
- `kind`: `measured` or `estimated`. This is a declaration, not laboratory verification.
- `provenance`: stable identity of the physical measurement stream, **not** its HA/MQTT representation. Alias readings share it. Different sign/quantity/scope with one provenance is a conflict; every alias of that conflicted stream becomes unavailable for sums, regardless of input order. Choose separate provenance for genuinely distinct flow channels.
- `sign`: `nonnegative` for consumption-only/import-only/export-only magnitude; `signed` for a declared bidirectional flow. This release does not infer which physical direction is positive.
- `state_class`: `measurement`, `total`, `total_increasing`.
- `freshness_seconds`: positive age budget, 0.001–604800 seconds.

Optional `reset`: `never`, `periodic`, `device_restart`, `unknown`, `not_applicable` (default). Energy needs an explicit non-`not_applicable` policy and total-style state class. Signed energy cannot use `total_increasing`. Other quantities need `measurement` and `not_applicable`.

Optional `sample`, `previous`: null or an object containing `value` (number or null), `measured_at`, optional `reset_at`. Previous must be older. A nonnegative counter decrease requires a reset marker between samples; `never` rejects it. `reset_at` must not be later than its sample and applies only to energy. Unknown counter reset semantics produce a warning. A signed net counter may legitimately decrease; its correct baseline remains the producer's responsibility.

Optional `calibration`: `quantity`, positive `factor` (10^-12–10^12), synthetic/private `reference` identifier, `verified_at`. It records evidence for exactly that quantity. Sample values are **already calibrated**: the validator never reapplies the factor. A future calibration or a voltage calibration on a power meter is invalid. Absence of calibration does not prove accuracy and is not automatically an error.

Optional `entity_id`, `timestamp_attribute`: offline HA mapping; see [usage](usage.md#offline-home-assistant-adapter).

## Sums

Required: `id`, target `scope`, list of meter IDs in `meters`, `quantity` (`power` or `energy`), `coverage` (`partial` or `complete`). Optional `max_skew_seconds`: 0–604800, default 2.

Members must lie within the target scope, have matching dimensions and sign semantics, use different physical streams, and not overlap each other as parent/child or identical scopes. A complete sum must cover every **declared leaf scope** under its target. Undeclared wiring cannot be detected. A partial sum explicitly reports its coverage as partial. Nested sums are not supported; members always reference meters.

Every member must have valid, fresh data; their acquisition times must lie within the allowed skew. Energy additionally requires identical explicit `reset_at` origins. This checks declared alignment, not the accuracy of historical counter accumulation. Sums convert to W or Wh. Current and voltage sums are intentionally unsupported because their meaning depends on circuit topology.

A numeric sum is unavailable when any required evidence or semantic check fails. Estimates are propagated as `kind: estimated`. Two aliases may coexist in the inventory, but cannot both contribute to a sum. No total is inferred for unmeasured individual outlets.

## Report v1

Root: `schema_version`, evaluation `at` normalized to UTC, severity counts in `summary`, sorted `findings`, and `sums`. Each finding contains `code`, `severity`, JSON-style `path`, structured `params`; the CLI adds `message`. Each sum contains `id`, `scope`, `quantity`, base `unit`, `value`, `status`, `kind`, `coverage`. Unknown values are JSON null, never NaN.
