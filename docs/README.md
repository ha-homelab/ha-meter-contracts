# Documentation

Guides for the offline checker that validates what a meter measures, how readings may
be combined, and whether a sample is usable. It reads JSON or YAML exports and never
uses a Home Assistant token, network connection or device command.

## Getting started

- [Usage](usage.md) — install the package, run the validator on an export, and read its verdict and exit code.

## The contract

- [Contract schema v1](schema.md) — the declared topology, measurement and sample fields the validator accepts.
- [Limits and trust boundary](limits.md) — which mistakes are caught, which are out of scope, and what the operator still has to confirm.

## Reference

- [Troubleshooting](troubleshooting.md) — diagnoses for schema, graph, unit and freshness failures.
- [Sources and design references](sources.md) — the HA, JSON Schema and ESPHome documentation the rules follow.

## Translations

- [Complete guide translations](translations.md) — every guide and checked-in wiki page in each of the 24 documentation languages, with links per language.
