<a id="usage"></a>

# Usage

<!-- language-navigation:start -->
<p dir="ltr">
<a href="usage.md" lang="en" dir="ltr">English</a> ·
<a href="ar/usage.md" lang="ar" dir="rtl">العربية</a> ·
<a href="bn/usage.md" lang="bn" dir="ltr">বাংলা</a> ·
<a href="cs/usage.md" lang="cs" dir="ltr">Čeština</a> ·
<a href="de/usage.md" lang="de" dir="ltr">Deutsch</a> ·
<a href="es/usage.md" lang="es" dir="ltr">Español</a> ·
<a href="fa/usage.md" lang="fa" dir="rtl">فارسی</a> ·
<a href="fr/usage.md" lang="fr" dir="ltr">Français</a> ·
<a href="he/usage.md" lang="he" dir="rtl">עברית</a> ·
<a href="hi/usage.md" lang="hi" dir="ltr">हिन्दी</a> ·
<a href="id/usage.md" lang="id" dir="ltr">Bahasa Indonesia</a> ·
<a href="it/usage.md" lang="it" dir="ltr">Italiano</a> ·
<a href="ja/usage.md" lang="ja" dir="ltr">日本語</a> ·
<a href="ko/usage.md" lang="ko" dir="ltr">한국어</a> ·
<a href="nl/usage.md" lang="nl" dir="ltr">Nederlands</a> ·
<a href="pl/usage.md" lang="pl" dir="ltr">Polski</a> ·
<a href="pt/usage.md" lang="pt" dir="ltr">Português</a> ·
<a href="ru/usage.md" lang="ru" dir="ltr">Русский</a> ·
<a href="th/usage.md" lang="th" dir="ltr">ไทย</a> ·
<a href="tr/usage.md" lang="tr" dir="ltr">Türkçe</a> ·
<a href="uk/usage.md" lang="uk" dir="ltr">Українська</a> ·
<a href="vi/usage.md" lang="vi" dir="ltr">Tiếng Việt</a> ·
<a href="zh-Hans/usage.md" lang="zh-Hans" dir="ltr">简体中文</a> ·
<a href="zh-Hant/usage.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->
<a id="audit"></a>

## Audit

```sh
ha-meter-contracts check contract.json --json --lang en
ha-meter-contracts check examples/minimal.yaml --at 2026-01-01T12:00:05Z --lang es
```

`--at` accepts an ISO 8601 timestamp with a timezone. The default is current UTC. Given the same input, time and language, JSON output is deterministic. A sample is fresh through its inclusive `freshness_seconds` boundary; it becomes stale only after that boundary. A future sample is invalid, with no implicit clock-skew allowance.

Exit codes: 0 = no error/warning; 1 = semantic or sample-quality finding; 2 = input/CLI error. Information such as an unused alias does not fail a check. `--json` puts both audit reports and input-error objects on stdout. Without it, audit text goes to stdout and input errors to stderr. A broken output pipe returns 2.

Do not use `|| true` in CI to hide findings. Intentionally invalid examples should explicitly assert exit 1. Help and version exit 0. `import-ha` always writes a JSON contract; `--json` does not change its schema.

<a id="python-library"></a>

## Python library

```python
from datetime import datetime, timezone
from ha_meter_contracts import audit, load_document, parse_contract

contract = parse_contract(load_document("examples/valid-three-meters.json"))
report = audit(contract, at=datetime(2026, 1, 1, 12, 0, 5, tzinfo=timezone.utc))
assert report["sums"][0]["value"] == 720
```

`parse_contract` creates frozen dataclasses; `InputError` exposes `code`, `path`, `params`. Use this parser at every untrusted input boundary. `audit` expects a validated `Contract`; it does not translate findings. The CLI adds localized `message` values. The caller chooses evaluation time explicitly in the library. Neither API mutates the input or writes files.

<a id="offline-home-assistant-adapter"></a>

## Offline Home Assistant adapter

```sh
ha-meter-contracts import-ha examples/ha-contract.json --ha-states examples/ha-states.synthetic.json > /tmp/meter-contract.json
ha-meter-contracts check /tmp/meter-contract.json --at 2026-01-01T12:00:05Z --json
```

Map `entity_id` and `timestamp_attribute` on each desired meter. The export is an array of HA state objects with `entity_id`, `state`, and `attributes`. The mapped attribute must contain the original, timezone-aware ISO measurement time. `attributes.unit_of_measurement` must have the same dimension; W/kW and Wh/kWh are converted to the contract unit.

Only mapped values and source times are copied. Other attributes are ignored, including friendly names. A strictly newer sample moves the existing sample to `previous`. Replaying the same value with the same source timestamp is idempotent; an older sample or a conflicting value at the same timestamp is rejected as `ha_sample_order`. Missing entities and `unknown`/`unavailable` states clear the sample; they do not become zero. A missing source timestamp, incompatible unit, malformed value or duplicate entity ID fails the import with exit 2. Unmapped meters are unchanged. Entity IDs may exist in a private contract; public examples use synthetic identifiers.

An ordinary HA export often lacks an original source timestamp. In that case this adapter intentionally refuses to invent one. Obtain timestamped device data or retain the meter as unavailable. HA receipt/update timestamps do not prove device acquisition time. The adapter never connects to `/api/states` or reads a token. It does not copy energy reset markers from HA; add verified reset evidence separately before summing energy.

<a id="suggested-workflow"></a>

## Suggested workflow

1. Declare the physical scope tree and source provenance using wiring documentation.
2. Start with one meter and a fixed synthetic example.
3. Export only necessary observations to a private file.
4. Audit and review each finding before changing a downstream automation.
5. Keep the original source times and calibration evidence during migrations.

No remediation, entity rename, device reset or automation deployment is performed by this package.
