<a id="limits-and-trust-boundary"></a>

# Limits and trust boundary

<!-- language-navigation:start -->
<p dir="ltr">
<a href="limits.md" lang="en" dir="ltr">English</a> ·
<a href="ar/limits.md" lang="ar" dir="rtl">العربية</a> ·
<a href="bn/limits.md" lang="bn" dir="ltr">বাংলা</a> ·
<a href="cs/limits.md" lang="cs" dir="ltr">Čeština</a> ·
<a href="de/limits.md" lang="de" dir="ltr">Deutsch</a> ·
<a href="es/limits.md" lang="es" dir="ltr">Español</a> ·
<a href="fa/limits.md" lang="fa" dir="rtl">فارسی</a> ·
<a href="fr/limits.md" lang="fr" dir="ltr">Français</a> ·
<a href="he/limits.md" lang="he" dir="rtl">עברית</a> ·
<a href="hi/limits.md" lang="hi" dir="ltr">हिन्दी</a> ·
<a href="id/limits.md" lang="id" dir="ltr">Bahasa Indonesia</a> ·
<a href="it/limits.md" lang="it" dir="ltr">Italiano</a> ·
<a href="ja/limits.md" lang="ja" dir="ltr">日本語</a> ·
<a href="ko/limits.md" lang="ko" dir="ltr">한국어</a> ·
<a href="nl/limits.md" lang="nl" dir="ltr">Nederlands</a> ·
<a href="pl/limits.md" lang="pl" dir="ltr">Polski</a> ·
<a href="pt/limits.md" lang="pt" dir="ltr">Português</a> ·
<a href="ru/limits.md" lang="ru" dir="ltr">Русский</a> ·
<a href="th/limits.md" lang="th" dir="ltr">ไทย</a> ·
<a href="tr/limits.md" lang="tr" dir="ltr">Türkçe</a> ·
<a href="uk/limits.md" lang="uk" dir="ltr">Українська</a> ·
<a href="vi/limits.md" lang="vi" dir="ltr">Tiếng Việt</a> ·
<a href="zh-Hans/limits.md" lang="zh-Hans" dir="ltr">简体中文</a> ·
<a href="zh-Hant/limits.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->
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
- File input accepts regular files only. It rejects final-component symlinks, FIFOs, devices and directories, opening nonblocking and checking the opened descriptor before reading. Platforms without `O_NOFOLLOW` and `O_NONBLOCK` reject file input; use `ha_meter_contracts.reader.loads_document` with an already bounded string there. Parent-directory symlinks are not a sandbox boundary. The byte limit is enforced even if a file grows during reading.
- No proof of physical relay, valve, motor, pump flow or electrical safety follows from a passing result. No automatic repair or retries are performed.

Inputs and outputs may contain operator-supplied entity IDs and times. Keep real contracts/exports private. The repository includes synthetic examples only. The program does not upload data, but redirecting its report to an external service is the operator's choice.
