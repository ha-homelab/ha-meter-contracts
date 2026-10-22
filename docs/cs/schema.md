<a id="contract-schema-v1"></a>

# Schéma kontraktu v1

<!-- language-navigation:start -->
<p dir="ltr">
<a href="../schema.md" lang="en" dir="ltr">English</a> ·
<a href="../ar/schema.md" lang="ar" dir="rtl">العربية</a> ·
<a href="../bn/schema.md" lang="bn" dir="ltr">বাংলা</a> ·
<a href="schema.md" lang="cs" dir="ltr">Čeština</a> ·
<a href="../de/schema.md" lang="de" dir="ltr">Deutsch</a> ·
<a href="../es/schema.md" lang="es" dir="ltr">Español</a> ·
<a href="../fa/schema.md" lang="fa" dir="rtl">فارسی</a> ·
<a href="../fr/schema.md" lang="fr" dir="ltr">Français</a> ·
<a href="../he/schema.md" lang="he" dir="rtl">עברית</a> ·
<a href="../hi/schema.md" lang="hi" dir="ltr">हिन्दी</a> ·
<a href="../id/schema.md" lang="id" dir="ltr">Bahasa Indonesia</a> ·
<a href="../it/schema.md" lang="it" dir="ltr">Italiano</a> ·
<a href="../ja/schema.md" lang="ja" dir="ltr">日本語</a> ·
<a href="../ko/schema.md" lang="ko" dir="ltr">한국어</a> ·
<a href="../nl/schema.md" lang="nl" dir="ltr">Nederlands</a> ·
<a href="../pl/schema.md" lang="pl" dir="ltr">Polski</a> ·
<a href="../pt/schema.md" lang="pt" dir="ltr">Português</a> ·
<a href="../ru/schema.md" lang="ru" dir="ltr">Русский</a> ·
<a href="../th/schema.md" lang="th" dir="ltr">ไทย</a> ·
<a href="../tr/schema.md" lang="tr" dir="ltr">Türkçe</a> ·
<a href="../uk/schema.md" lang="uk" dir="ltr">Українська</a> ·
<a href="../vi/schema.md" lang="vi" dir="ltr">Tiếng Việt</a> ·
<a href="../zh-Hans/schema.md" lang="zh-Hans" dir="ltr">简体中文</a> ·
<a href="../zh-Hant/schema.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->
Strojově čitelný [schema.json](../../schema.json) popisuje strukturu. Pro limity je rozhodující parser Pythonu; `audit` doplňuje fyzikální a časovou sémantiku, kterou JSON Schema nedokáže prokázat. Strukturální soubor vytvoříte pomocí `python3 scripts/generate_schema.py`.

<a id="root-and-limits"></a>

## Kořen a limity

Povinné: celé číslo `schema_version: 1`, `scopes`, `meters`. Volitelné: `sums` (ve výchozím stavu prázdné). Neznámá pole se odmítají na každé úrovni. Nejvýše 512 rozsahů, 512 měřidel a 128 součtů; rozsahy ani měřidla nesmějí být prázdné. Každý součet má 1–512 členů. Vstup UTF-8, nejvýše 1 048 576 bajtů, hloubka 16 a 20 000 hodnotových uzlů. Duplicitní klíče JSON, NaN/Infinity a aliasy/kotvy/výslovné tagy YAML se odmítají. Časy v YAML uzavřete do uvozovek, aby zůstaly řetězci.

Identifikátory mají 1–96 znaků ASCII: nejprve písmeno/číslice, potom písmena, číslice, `.`, `_`, `-`. ID jsou jedinečná v každé kolekci; rozsahy a měřidla mají oddělené jmenné prostory. Všechny časy obsahují `T` a časové pásmo. Čísla jsou konečná, ne booleovská, v mezích ±10^15, pokud není stanovena přísnější mez.

<a id="physical-scopes"></a>

## Fyzické rozsahy

Každý rozsah má `id`, `kind` (`site`, `circuit`, `strip`, `outlet`, `load`) a volitelné `parent`. Rodiče musí existovat a tvořit acyklický les. Měřidlo na rodiči pokrývá všechny potomky. Typy rozsahů jsou popisné: neodvozují napětí, fáze, jmenovité hodnoty, zapojení ani povolené rodiče. Skutečnou topologii deklaruje uživatel.

<a id="meters"></a>

## Měřidla

Povinná pole:

- `id`, `scope`: jedinečný identifikátor měření a deklarovaný fyzický rozsah.
- `quantity`: `power`, `energy`, `voltage`, `current`.
- `unit`: příslušně W/kW, Wh/kWh, V, A. Parser přijímá slovník; auditor kontroluje rozměr.
- `kind`: `measured` nebo `estimated`. Jde o deklaraci, ne laboratorní ověření.
- `provenance`: stálá identita fyzického toku měření, **nikoli** jeho reprezentace HA/MQTT. Aliasové údaje ji sdílejí. Rozdílná znaménka/veličiny/rozsahy s jedním původem tvoří konflikt; všechny aliasy toku se stanou nedostupnými pro součty bez ohledu na pořadí vstupu. Pro skutečně různé fyzické kanály volte různé původy.
- `sign`: `nonnegative` pro velikosti pouze spotřeby/importu/exportu; `signed` pro deklarovaný obousměrný tok. Tato verze neodvozuje, který fyzický směr je kladný.
- `state_class`: `measurement`, `total`, `total_increasing`.
- `freshness_seconds`: kladné maximální stáří, 0.001–604800 sekund.

Volitelné `reset`: `never`, `periodic`, `device_restart`, `unknown`, `not_applicable` (výchozí). Energie vyžaduje výslovnou politiku jinou než `not_applicable` a stavovou třídu typu total. Energie se znaménkem nesmí používat `total_increasing`. Ostatní veličiny vyžadují `measurement` a `not_applicable`.

Volitelné `sample`, `previous`: null nebo objekt s `value` (číslo či null), `measured_at`, volitelným `reset_at`. Předchozí vzorek musí být starší. Pokles nezáporného čítače vyžaduje značku resetu mezi vzorky; `never` ji odmítá. `reset_at` nesmí být pozdější než jeho vzorek a platí jen pro energii. Neznámá sémantika resetu vyvolá varování. Čistý čítač se znaménkem může legitimně klesat; správný základ zůstává odpovědností producenta.

Volitelné `calibration`: `quantity`, kladný `factor` (10^-12–10^12), syntetický/soukromý identifikátor `reference`, `verified_at`. Zaznamenává podklady pro právě tuto veličinu. Hodnoty jsou **již kalibrované**: validátor nikdy nepoužívá koeficient znovu. Kalibrace z budoucnosti nebo kalibrace napětí u měřidla výkonu je neplatná. Chybějící kalibrace nedokazuje přesnost a není automaticky chybou.

Volitelné `entity_id`, `timestamp_attribute`: offline mapování HA; viz [použití](usage.md#offline-home-assistant-adapter).

<a id="sums"></a>

## Součty

Povinné: `id`, cílový `scope`, seznam ID měřidel v `meters`, `quantity` (`power` nebo `energy`), `coverage` (`partial` nebo `complete`). Volitelné `max_skew_seconds`: 0–604800, výchozí 2.

Členové musí patřit do cílového rozsahu, mít slučitelné rozměry a sémantiku znaménka, používat různé fyzické toky a nepřekrývat se jako rodič/potomek či totožné rozsahy. Úplný součet pokrývá každý **deklarovaný listový rozsah** pod cílem. Nedeklarované zapojení nelze zjistit. Částečný součet výslovně deklaruje částečné pokrytí. Vnořené součty nejsou podporovány; členové vždy odkazují na měřidla.

Každý člen musí mít platná čerstvá data; časy měření musí ležet v povolené odchylce. Energie navíc vyžaduje totožné výslovné počátky `reset_at`. Ověřuje se deklarované sladění, ne přesnost historické akumulace. Součty se převádějí na W nebo Wh. Součty proudu a napětí záměrně nejsou podporovány, protože závisejí na topologii obvodu.

Číselný součet je nedostupný, pokud chybí požadovaný podklad nebo selže sémantická kontrola. Odhady se propagují jako `kind: estimated`. Dva aliasy mohou být současně v inventáři, ale nemohou oba přispívat do součtu. Neodvozuje se žádný součet pro jednotlivé neměřené zásuvky.

<a id="report-v1"></a>

## Zpráva v1

Kořen: `schema_version`, čas vyhodnocení `at` normalizovaný na UTC, počty závažností v `summary`, seřazené `findings` a `sums`. Každý nález obsahuje `code`, `severity`, `path` ve stylu JSON, strukturované `params`; CLI přidává `message`. Každý součet obsahuje `id`, `scope`, `quantity`, základní `unit`, `value`, `status`, `kind`, `coverage`. Neznámé hodnoty jsou JSON null, nikdy NaN.
