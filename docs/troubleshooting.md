# Troubleshooting

## A three-outlet strip cannot produce three power readings

`scope_outside` means a requested individual result uses a broader measurement. Keep one whole-strip entity. Add independent, correctly scoped measurements if individual power is needed. A relay being on does not prove that its load is consuming power; a pump consuming electricity does not prove that water is flowing.

## A migrated sensor doubles the total

`alias_stream` alone is informational. `duplicate_stream` means both copies occur in a sum. Give copies of the same CT the same provenance and keep only one in the sum. Do not change provenance just to silence the check.

![One source and two representations](images/duplicate-stream.svg)

## No numeric sum despite individually plausible numbers

Check `sample_stale`, `sample_future`, `sample_skew`, `sample_missing`, `incomplete_coverage`, `unit_dimension`, `scope_overlap`. Refresh the original source and preserve its acquisition time. Extending a freshness budget is a policy change, not a measurement repair. A complete sum is judged against declared leaf scopes, so review the declaration too.

![Synthetic sample-quality timeline](images/sample-quality.svg)

## Energy decreased at midnight

A drop may be a real reset, replacement or correction. Declare the policy and add `reset_at` from actual source evidence. A timestamp from when HA replayed the value is not a reset marker. `total_increasing` is inappropriate for signed net energy. Two counters with different origins are not summed.

## Voltage looks calibrated but watts still differ

Calibration is per quantity. A voltage correction does not validate current, phase relationship, power or accumulated energy. The factor field is documentation only: values must already contain the intended correction.

## YAML fails although another parser accepts it

Quote timestamps, remove aliases/anchors/custom tags, remove duplicate keys, and use finite numbers. Unknown fields are errors to catch typos. The limits apply to both formats. Use JSON for interchange when ambiguous YAML scalars are inconvenient.

## HA import fails on timestamps

Set `timestamp_attribute` to a real measurement-time attribute. `last_reported` only proves receipt by HA. If no source time is available, this tool cannot establish freshness; leave the sample unavailable. There is no token or network connectivity issue to debug because import is offline.

## Safe issue report

Include package/Python version, stable finding codes, a minimal synthetic contract, chosen `--at`, expected result and actual result. Do not attach a full HA export, token, real address, household schedule or private device identifiers. A value of 0 W and an unavailable sample must remain distinguishable in a reproducer.
