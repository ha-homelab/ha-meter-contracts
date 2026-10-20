# Changelog

## Unreleased

No pending changes.

## 0.1.1b1 — 2026-10-20

- Publish the first GitHub beta packages with matching source/package versions and SHA-256 checksums.
- Document the prerelease process and use the pinned build configuration as the source of truth.

- Update CI to pytest 9.0.3 (GHSA-6w46-j5rx-g56g) and the build backend to setuptools 83.0.0 (upstream fix for GHSA-h35f-9h28-mq5c).
- Document private reporting, review/release responsibilities, contribution rules and the current continuity limitation; include these policies in source distributions.

- Make every alias of a conflicting physical provenance unavailable to sums, independent of input order.
- Reject non-regular file inputs and final symlinks before reading; retain the byte limit when a file grows.

## 0.1.0 — initial source release

- Typed offline contract parser and auditor for meter topology, provenance, additive scope, quantity and unit semantics.
- Freshness, time skew, reset evidence and calibration-per-quantity checks; unavailable values never become zero.
- Bounded strict JSON/YAML loading and allowlisted import from saved Home Assistant state exports.
- Stable machine reports and English, Russian, German and Spanish CLI messages/help.
- Synthetic regression fixtures, reproducible SVG illustrations, structural JSON Schema, EN/RU guides and checked-in wiki sources.

Physical hardware behavior is not tested by this package. Publication and deployment are separate from source validation.
