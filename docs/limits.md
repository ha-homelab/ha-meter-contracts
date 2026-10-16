# Limits and trust boundary

This is an offline declaration validator, not a protection controller, electrician's test instrument, wiring discovery service or Home Assistant integration that executes actions.

- One total measurement cannot recover exact simultaneous power for three unknown loads. Statistical guesses would be estimates, not protection-grade measurements.
- Scope, provenance, sign direction and calibration statements come from the operator. Lying declarations can make an invalid physical system look structurally valid.
- `complete` means complete against declared leaves, not independently verified wiring. A source reset marker is trusted evidence, not device attestation.
- We support W, kW, Wh, kWh, V and A. We do not model reactive/apparent power, three-phase algebra, CT saturation, voltage transformers, counter rollover or tariffs.
- Sum members are direct meters, not other sums. Power sums require aligned timestamps. Energy sums require a common explicit counter origin and aligned samples.
- Values are finite floating-point numbers. This is not a billing-grade decimal accounting system. Calibration factors are recorded, not applied.
- Only a current and optional previous sample are checked. This is not a history database, anomaly detector, drift detector or complete counter-integrity audit.
- HA source timestamps must exist and must actually represent acquisition. Cache receipt timestamps are not silently accepted as substitutes.
- JSON/YAML loading is bounded; the library's `audit` API expects a `Contract` produced by the parser. Do not construct arbitrary malformed dataclasses from untrusted objects.
- No proof of physical relay, valve, motor, pump flow or electrical safety follows from a passing result. No automatic repair or retries are performed.

Inputs and outputs may contain operator-supplied entity IDs and times. Keep real contracts/exports private. The repository includes synthetic examples only. The program does not upload data, but redirecting its report to an external service is the operator's choice.
