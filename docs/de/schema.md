<a id="contract-schema-v1"></a>

# Vertragsschema v1

<!-- language-navigation:start -->
<p dir="ltr">
<a href="../schema.md" lang="en" dir="ltr">English</a> ·
<a href="../ar/schema.md" lang="ar" dir="rtl">العربية</a> ·
<a href="../bn/schema.md" lang="bn" dir="ltr">বাংলা</a> ·
<a href="../cs/schema.md" lang="cs" dir="ltr">Čeština</a> ·
<a href="schema.md" lang="de" dir="ltr">Deutsch</a> ·
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
Die maschinenlesbare [schema.json](../../schema.json) beschreibt die Struktur. Für Grenzwerte ist der Python-Parser maßgeblich; `audit` ergänzt physikalische und zeitliche Semantik, die JSON Schema nicht beweisen kann. Erzeugen Sie die Strukturdatei mit `python3 scripts/generate_schema.py`.

<a id="root-and-limits"></a>

## Wurzel und Grenzen

Erforderlich: ganzzahliges `schema_version: 1`, `scopes`, `meters`. Optional: `sums` (standardmäßig leer). Unbekannte Felder werden auf jeder Vertragsebene abgelehnt. Höchstens 512 Bereiche, 512 Messgeräte und 128 Summen; Bereiche und Messgeräte dürfen nicht leer sein. Jede Summe umfasst 1–512 Mitglieder. Eingabe: UTF-8, höchstens 1.048.576 Bytes, Verschachtelungstiefe 16 und 20.000 Werteknoten. Doppelte JSON-Schlüssel, NaN/Infinity sowie YAML-Aliasse/-Anker/-explizite Tags werden abgelehnt. Setzen Sie YAML-Zeitstempel in Anführungszeichen, damit sie Zeichenfolgen bleiben.

Kennungen bestehen aus 1–96 ASCII-Zeichen: zuerst Buchstabe/Ziffer, danach Buchstaben, Ziffern, `.`, `_`, `-`. IDs sind innerhalb jeder Sammlung eindeutig; Bereiche und Messgeräte haben getrennte Namensräume. Alle Zeiten enthalten `T` und eine Zeitzone. Zahlen sind endlich, keine booleschen Werte, und liegen innerhalb ±10^15, sofern keine engere Grenze angegeben ist.

<a id="physical-scopes"></a>

## Physische Bereiche

Jeder Bereich besitzt `id`, `kind` (`site`, `circuit`, `strip`, `outlet`, `load`) und optional `parent`. Übergeordnete Bereiche müssen existieren und einen azyklischen Wald bilden. Ein Messgerät auf einem übergeordneten Bereich erfasst alle Nachkommen. Bereichstypen sind beschreibend; sie leiten keine Spannung, Phasen, Nennwerte, Verkabelung oder erlaubten Eltern ab. Sie deklarieren die tatsächliche Topologie.

<a id="meters"></a>

## Messgeräte

Erforderliche Felder:

- `id`, `scope`: eindeutige Messkennung und deklarierter physischer Bereich.
- `quantity`: `power`, `energy`, `voltage`, `current`.
- `unit`: entsprechend W/kW, Wh/kWh, V, A. Der Parser akzeptiert das Vokabular; der Prüfer kontrolliert die Dimension.
- `kind`: `measured` oder `estimated`. Dies ist eine Angabe, keine Laborprüfung.
- `provenance`: stabile Identität des physischen Messdatenstroms, **nicht** seiner HA/MQTT-Darstellung. Aliaswerte teilen diese Identität. Unterschiedliches Vorzeichen/Größe/Bereich bei gleicher Herkunft ist ein Konflikt; jeder Alias des betroffenen Stroms wird unabhängig von der Eingabereihenfolge für Summen unbrauchbar. Verwenden Sie getrennte Herkunftskennungen für tatsächlich getrennte Flusskanäle.
- `sign`: `nonnegative` für reine Verbrauchs-/Import-/Exportbeträge; `signed` für einen deklarierten bidirektionalen Fluss. Diese Version leitet nicht ab, welche physische Richtung positiv ist.
- `state_class`: `measurement`, `total`, `total_increasing`.
- `freshness_seconds`: positives Altersbudget, 0.001–604800 Sekunden.

Optionales `reset`: `never`, `periodic`, `device_restart`, `unknown`, `not_applicable` (Standard). Energie benötigt eine explizite Richtlinie ungleich `not_applicable` und eine Total-Zustandsklasse. Vorzeichenbehaftete Energie darf nicht `total_increasing` verwenden. Andere Größen benötigen `measurement` und `not_applicable`.

Optionale `sample`, `previous`: null oder ein Objekt mit `value` (Zahl oder null), `measured_at` und optional `reset_at`. Der vorherige Wert muss älter sein. Ein Rückgang eines nichtnegativen Zählers erfordert eine Rücksetzmarkierung zwischen den Messwerten; `never` lehnt ihn ab. `reset_at` darf nicht nach seinem Messwert liegen und gilt nur für Energie. Unbekannte Rücksetzsemantik erzeugt eine Warnung. Ein vorzeichenbehafteter Nettozähler darf rechtmäßig sinken; sein korrekter Ausgangspunkt bleibt Verantwortung des Erzeugers.

Optionale `calibration`: `quantity`, positiver `factor` (10^-12–10^12), synthetische/private Kennung `reference`, `verified_at`. Sie dokumentiert Nachweise genau für diese Größe. Messwerte sind **bereits kalibriert**: der Prüfer wendet den Faktor nie erneut an. Eine zukünftige Kalibrierung oder Spannungskalibrierung an einem Leistungsmesser ist ungültig. Fehlende Kalibrierung beweist keine Genauigkeit und ist nicht automatisch ein Fehler.

Optionale `entity_id`, `timestamp_attribute`: Offline-HA-Zuordnung; siehe [Verwendung](usage.md#offline-home-assistant-adapter).

<a id="sums"></a>

## Summen

Erforderlich: `id`, Ziel-`scope`, Messgeräte-IDs in `meters`, `quantity` (`power` oder `energy`), `coverage` (`partial` oder `complete`). Optionales `max_skew_seconds`: 0–604800, Standard 2.

Mitglieder müssen im Zielbereich liegen, passende Dimensionen und Vorzeichensemantik besitzen, unterschiedliche physische Ströme nutzen und dürfen sich weder als Eltern/Kind noch durch identische Bereiche überlappen. Eine vollständige Summe muss jeden **deklarierten Blattbereich** unter dem Ziel abdecken. Nicht deklarierte Verkabelung ist nicht erkennbar. Eine Teilsumme weist ihre Abdeckung ausdrücklich als teilweise aus. Verschachtelte Summen werden nicht unterstützt; Mitglieder verweisen immer auf Messgeräte.

Jedes Mitglied benötigt gültige, aktuelle Daten; die Erfassungszeiten müssen innerhalb des erlaubten Versatzes liegen. Energie benötigt außerdem identische explizite `reset_at`-Ursprünge. Geprüft wird deklarierte Abstimmung, nicht die Genauigkeit historischer Zählerakkumulation. Summen werden in W oder Wh umgerechnet. Strom- und Spannungssummen sind bewusst nicht unterstützt, weil ihre Bedeutung von der Schaltungstopologie abhängt.

Eine numerische Summe ist nicht verfügbar, sobald erforderliche Nachweise fehlen oder eine semantische Prüfung scheitert. Schätzungen werden als `kind: estimated` weitergegeben. Zwei Aliasse dürfen im Inventar bestehen, aber nicht beide zu einer Summe beitragen. Für ungemessene einzelne Steckdosen wird kein Gesamtwert abgeleitet.

<a id="report-v1"></a>

## Bericht v1

Wurzel: `schema_version`, nach UTC normalisierter Auswertungszeitpunkt `at`, Schweregradzähler in `summary`, sortierte `findings` und `sums`. Jeder Befund enthält `code`, `severity`, JSON-artigen `path` und strukturierte `params`; die CLI ergänzt `message`. Jede Summe enthält `id`, `scope`, `quantity`, Basis-`unit`, `value`, `status`, `kind`, `coverage`. Unbekannte Werte sind JSON null, niemals NaN.
