<a id="troubleshooting"></a>

# Troubleshooting

<!-- language-navigation:start -->
<p dir="ltr">
<a href="troubleshooting.md" lang="en" dir="ltr">English</a> ·
<a href="ar/troubleshooting.md" lang="ar" dir="rtl">العربية</a> ·
<a href="bn/troubleshooting.md" lang="bn" dir="ltr">বাংলা</a> ·
<a href="cs/troubleshooting.md" lang="cs" dir="ltr">Čeština</a> ·
<a href="de/troubleshooting.md" lang="de" dir="ltr">Deutsch</a> ·
<a href="es/troubleshooting.md" lang="es" dir="ltr">Español</a> ·
<a href="fa/troubleshooting.md" lang="fa" dir="rtl">فارسی</a> ·
<a href="fr/troubleshooting.md" lang="fr" dir="ltr">Français</a> ·
<a href="he/troubleshooting.md" lang="he" dir="rtl">עברית</a> ·
<a href="hi/troubleshooting.md" lang="hi" dir="ltr">हिन्दी</a> ·
<a href="id/troubleshooting.md" lang="id" dir="ltr">Bahasa Indonesia</a> ·
<a href="it/troubleshooting.md" lang="it" dir="ltr">Italiano</a> ·
<a href="ja/troubleshooting.md" lang="ja" dir="ltr">日本語</a> ·
<a href="ko/troubleshooting.md" lang="ko" dir="ltr">한국어</a> ·
<a href="nl/troubleshooting.md" lang="nl" dir="ltr">Nederlands</a> ·
<a href="pl/troubleshooting.md" lang="pl" dir="ltr">Polski</a> ·
<a href="pt/troubleshooting.md" lang="pt" dir="ltr">Português</a> ·
<a href="ru/troubleshooting.md" lang="ru" dir="ltr">Русский</a> ·
<a href="th/troubleshooting.md" lang="th" dir="ltr">ไทย</a> ·
<a href="tr/troubleshooting.md" lang="tr" dir="ltr">Türkçe</a> ·
<a href="uk/troubleshooting.md" lang="uk" dir="ltr">Українська</a> ·
<a href="vi/troubleshooting.md" lang="vi" dir="ltr">Tiếng Việt</a> ·
<a href="zh-Hans/troubleshooting.md" lang="zh-Hans" dir="ltr">简体中文</a> ·
<a href="zh-Hant/troubleshooting.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->
<a id="a-three-outlet-strip-cannot-produce-three-power-readings"></a>

## A three-outlet strip cannot produce three power readings

`scope_outside` means a requested individual result uses a broader measurement. Keep one whole-strip entity. Add independent, correctly scoped measurements if individual power is needed. A relay being on does not prove that its load is consuming power; a pump consuming electricity does not prove that water is flowing.

<a id="a-migrated-sensor-doubles-the-total"></a>

## A migrated sensor doubles the total

`alias_stream` alone is informational. `duplicate_stream` means both copies occur in a sum. Give copies of the same CT the same provenance and keep only one in the sum. Do not change provenance just to silence the check.

![One source and two representations](images/duplicate-stream.svg)

<a id="no-numeric-sum-despite-individually-plausible-numbers"></a>

## No numeric sum despite individually plausible numbers

Check `sample_stale`, `sample_future`, `sample_skew`, `sample_missing`, `incomplete_coverage`, `unit_dimension`, `scope_overlap`. Refresh the original source and preserve its acquisition time. Extending a freshness budget is a policy change, not a measurement repair. A complete sum is judged against declared leaf scopes, so review the declaration too.

![Synthetic sample-quality timeline](images/sample-quality.svg)

<a id="energy-decreased-at-midnight"></a>

## Energy decreased at midnight

A drop may be a real reset, replacement or correction. Declare the policy and add `reset_at` from actual source evidence. A timestamp from when HA replayed the value is not a reset marker. `total_increasing` is inappropriate for signed net energy. Two counters with different origins are not summed.

<a id="voltage-looks-calibrated-but-watts-still-differ"></a>

## Voltage looks calibrated but watts still differ

Calibration is per quantity. A voltage correction does not validate current, phase relationship, power or accumulated energy. The factor field is documentation only: values must already contain the intended correction.

<a id="yaml-fails-although-another-parser-accepts-it"></a>

## YAML fails although another parser accepts it

Quote timestamps, remove aliases/anchors/custom tags, remove duplicate keys, and use finite numbers. Unknown fields are errors to catch typos. The limits apply to both formats. Use JSON for interchange when ambiguous YAML scalars are inconvenient.

<a id="ha-import-fails-on-timestamps"></a>

## HA import fails on timestamps

Set `timestamp_attribute` to a real measurement-time attribute. `last_reported` only proves receipt by HA. If no source time is available, this tool cannot establish freshness; leave the sample unavailable. There is no token or network connectivity issue to debug because import is offline.

<a id="safe-issue-report"></a>

## Safe issue report

Include package/Python version, stable finding codes, a minimal synthetic contract, chosen `--at`, expected result and actual result. Do not attach a full HA export, token, real address, household schedule or private device identifiers. A value of 0 W and an unavailable sample must remain distinguishable in a reproducer.
