# Changelog

## Unreleased

- Make every alias of a conflicting physical provenance unavailable to sums, independent of input order.
- Reject non-regular file inputs and final symlinks before reading; retain the byte limit when a file grows.

## 0.1.0 — initial source release

- Typed offline contract parser and auditor for meter topology, provenance, additive scope, quantity and unit semantics.
- Freshness, time skew, reset evidence and calibration-per-quantity checks; unavailable values never become zero.
- Bounded strict JSON/YAML loading and allowlisted import from saved Home Assistant state exports.
- Stable machine reports and English, Russian, German and Spanish CLI messages/help.
- Synthetic regression fixtures, reproducible SVG illustrations, structural JSON Schema, EN/RU guides and checked-in wiki sources.

Physical hardware behavior is not tested by this package. Publication and deployment are separate from source validation.
