<a id="contract-schema-v1"></a>

# Contractschema v1

<!-- language-navigation:start -->
<p dir="ltr">
<a href="../schema.md" lang="en" dir="ltr">English</a> ·
<a href="../ar/schema.md" lang="ar" dir="rtl">العربية</a> ·
<a href="../bn/schema.md" lang="bn" dir="ltr">বাংলা</a> ·
<a href="../cs/schema.md" lang="cs" dir="ltr">Čeština</a> ·
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
<a href="schema.md" lang="nl" dir="ltr">Nederlands</a> ·
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
Het machinaal leesbare [schema.json](../../schema.json) beschrijft de structuur. De Python-parser is leidend voor grenzen; `audit` voegt fysieke en tijdsemantiek toe die JSON Schema niet kan bewijzen. Genereer het structuurbestand met `python3 scripts/generate_schema.py`.

<a id="root-and-limits"></a>

## Hoofdniveau en grenzen

Verplicht: geheel getal `schema_version: 1`, `scopes`, `meters`. Optioneel: `sums` (standaard leeg). Onbekende velden worden op elk niveau geweigerd. Maximaal 512 bereiken, 512 meters en 128 sommen; bereiken en meters mogen niet leeg zijn. Iedere som heeft 1–512 leden. Invoer is UTF-8, maximaal 1.048.576 bytes, diepte 16 en 20.000 waardeknooppunten. Dubbele JSON-sleutels, NaN/Infinity en expliciete YAML-aliassen/ankers/tags worden geweigerd. Zet YAML-tijdstippen tussen aanhalingstekens zodat ze tekenreeksen blijven.

Identificatoren hebben 1–96 ASCII-tekens: eerst letter/cijfer, daarna letters, cijfers, `.`, `_`, `-`. ID's zijn uniek binnen elke verzameling; bereiken en meters hebben afzonderlijke naamruimten. Alle tijden bevatten `T` en een tijdzone. Getallen zijn eindig, geen booleans, binnen ±10^15 tenzij een strengere grens geldt.

<a id="physical-scopes"></a>

## Fysieke bereiken

Elk bereik heeft `id`, `kind` (`site`, `circuit`, `strip`, `outlet`, `load`) en optioneel `parent`. Ouders moeten bestaan en een acyclisch bos vormen. Een meter op een ouder omvat alle nakomelingen. Bereiktypen zijn beschrijvend: ze leiden geen spanning, fasen, nominale waarden, bedrading of toegestane ouders af. De gebruiker geeft de werkelijke topologie op.

<a id="meters"></a>

## Meters

Verplichte velden:

- `id`, `scope`: unieke meetidentificator en opgegeven fysiek bereik.
- `quantity`: `power`, `energy`, `voltage`, `current`.
- `unit`: respectievelijk W/kW, Wh/kWh, V, A. De parser accepteert de woordenschat; de auditor controleert de dimensie.
- `kind`: `measured` of `estimated`. Dit is een verklaring, geen laboratoriumverificatie.
- `provenance`: stabiele identiteit van de fysieke meetstroom, **niet** van de HA/MQTT-weergave. Aliasmetingen delen deze. Verschillende tekens/grootheden/bereiken met één herkomst vormen een conflict; alle aliassen van die stroom worden onbeschikbaar voor sommen, ongeacht de invoervolgorde. Kies verschillende herkomsten voor werkelijk verschillende fysieke kanalen.
- `sign`: `nonnegative` voor uitsluitend verbruiks-/import-/exportgroottes; `signed` voor een opgegeven tweerichtingsstroom. Deze versie leidt niet af welke fysieke richting positief is.
- `state_class`: `measurement`, `total`, `total_increasing`.
- `freshness_seconds`: positieve maximumleeftijd, 0.001–604800 seconden.

Optioneel `reset`: `never`, `periodic`, `device_restart`, `unknown`, `not_applicable` (standaard). Energie vereist een expliciet beleid anders dan `not_applicable` en een total-achtige toestandsklasse. Energie met teken mag niet `total_increasing` gebruiken. Andere grootheden vereisen `measurement` en `not_applicable`.

Optioneel `sample`, `previous`: null of object met `value` (getal of null), `measured_at`, optioneel `reset_at`. Het vorige monster moet ouder zijn. Een daling van een niet-negatieve teller vereist een resetmarkering tussen monsters; `never` weigert die. `reset_at` mag niet later zijn dan zijn monster en geldt alleen voor energie. Onbekende resetsemantiek geeft een waarschuwing. Een netto teller met teken mag terecht dalen; de juiste basis blijft de verantwoordelijkheid van de producent.

Optioneel `calibration`: `quantity`, positieve `factor` (10^-12–10^12), synthetische/private identificator `reference`, `verified_at`. Dit registreert onderbouwing voor precies die grootheid. Waarden zijn **al gekalibreerd**: de validator past de factor nooit nogmaals toe. Toekomstige kalibratie of spanningskalibratie op een vermogensmeter is ongeldig. Ontbrekende kalibratie bewijst geen nauwkeurigheid en is niet automatisch een fout.

Optioneel `entity_id`, `timestamp_attribute`: offline HA-koppeling; zie [gebruik](usage.md#offline-home-assistant-adapter).

<a id="sums"></a>

## Sommen

Verplicht: `id`, doel-`scope`, lijst meter-ID's in `meters`, `quantity` (`power` of `energy`), `coverage` (`partial` of `complete`). Optioneel `max_skew_seconds`: 0–604800, standaard 2.

Leden moeten binnen het doelbereik vallen, compatibele dimensies en tekensemantiek hebben, verschillende fysieke stromen gebruiken en niet overlappen als ouder/kind of identieke bereiken. Een volledige som dekt elk **opgegeven bladbereik** onder het doel. Niet-opgegeven bedrading kan niet worden ontdekt. Een gedeeltelijke som verklaart expliciet gedeeltelijke dekking. Geneste sommen worden niet ondersteund; leden verwijzen altijd naar meters.

Ieder lid moet geldige recente gegevens hebben; meettijden moeten binnen de toegestane afwijking vallen. Energie vereist ook identieke expliciete `reset_at`-oorsprongen. Dit controleert de opgegeven uitlijning, niet de nauwkeurigheid van historische accumulatie. Sommen worden omgezet naar W of Wh. Stroom- en spanningssommen worden bewust niet ondersteund omdat ze van de schakelingstopologie afhangen.

Een numerieke som is onbeschikbaar wanneer vereiste onderbouwing ontbreekt of een semantische controle faalt. Schattingen werken door als `kind: estimated`. Twee aliassen mogen in de inventaris naast elkaar bestaan, maar mogen niet beide aan een som bijdragen. Er wordt geen totaal voor afzonderlijke ongemeten stopcontacten afgeleid.

<a id="report-v1"></a>

## Rapport v1

Hoofdniveau: `schema_version`, evaluatietijd `at` genormaliseerd naar UTC, aantallen per ernst in `summary`, gesorteerde `findings` en `sums`. Elke bevinding bevat `code`, `severity`, JSON-achtig `path`, gestructureerde `params`; de CLI voegt `message` toe. Elke som bevat `id`, `scope`, `quantity`, basis-`unit`, `value`, `status`, `kind`, `coverage`. Onbekende waarden zijn JSON null, nooit NaN.
