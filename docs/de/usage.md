<a id="usage"></a>

# Verwendung

<!-- language-navigation:start -->
<p dir="ltr">
<a href="../usage.md" lang="en" dir="ltr">English</a> ·
<a href="../ar/usage.md" lang="ar" dir="rtl">العربية</a> ·
<a href="../bn/usage.md" lang="bn" dir="ltr">বাংলা</a> ·
<a href="../cs/usage.md" lang="cs" dir="ltr">Čeština</a> ·
<a href="usage.md" lang="de" dir="ltr">Deutsch</a> ·
<a href="../es/usage.md" lang="es" dir="ltr">Español</a> ·
<a href="../fa/usage.md" lang="fa" dir="rtl">فارسی</a> ·
<a href="../fr/usage.md" lang="fr" dir="ltr">Français</a> ·
<a href="../he/usage.md" lang="he" dir="rtl">עברית</a> ·
<a href="../hi/usage.md" lang="hi" dir="ltr">हिन्दी</a> ·
<a href="../id/usage.md" lang="id" dir="ltr">Bahasa Indonesia</a> ·
<a href="../it/usage.md" lang="it" dir="ltr">Italiano</a> ·
<a href="../ja/usage.md" lang="ja" dir="ltr">日本語</a> ·
<a href="../ko/usage.md" lang="ko" dir="ltr">한국어</a> ·
<a href="../nl/usage.md" lang="nl" dir="ltr">Nederlands</a> ·
<a href="../pl/usage.md" lang="pl" dir="ltr">Polski</a> ·
<a href="../pt/usage.md" lang="pt" dir="ltr">Português</a> ·
<a href="../ru/usage.md" lang="ru" dir="ltr">Русский</a> ·
<a href="../th/usage.md" lang="th" dir="ltr">ไทย</a> ·
<a href="../tr/usage.md" lang="tr" dir="ltr">Türkçe</a> ·
<a href="../uk/usage.md" lang="uk" dir="ltr">Українська</a> ·
<a href="../vi/usage.md" lang="vi" dir="ltr">Tiếng Việt</a> ·
<a href="../zh-Hans/usage.md" lang="zh-Hans" dir="ltr">简体中文</a> ·
<a href="../zh-Hant/usage.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->
<a id="audit"></a>

## Prüfung

```sh
ha-meter-contracts check contract.json --json --lang en
ha-meter-contracts check examples/minimal.yaml --at 2026-01-01T12:00:05Z --lang es
```

`--at` akzeptiert einen ISO-8601-Zeitstempel mit Zeitzone. Standard ist die aktuelle UTC-Zeit. Bei gleicher Eingabe, Zeit und Sprache ist JSON deterministisch. Ein Messwert bleibt bis einschließlich seiner `freshness_seconds`-Grenze aktuell und wird erst danach veraltet. Ein zukünftiger Wert ist ungültig; es gibt keinen impliziten Toleranzbereich für Uhrabweichungen.

Exitcodes: 0 = kein Fehler/keine Warnung; 1 = semantischer Befund oder Qualitätsbefund zum Messwert; 2 = Eingabe-/CLI-Fehler. Informationen wie ein ungenutzter Alias lassen eine Prüfung nicht fehlschlagen. `--json` schreibt Prüfberichte und Eingabefehlerobjekte nach stdout. Ohne diese Option gehen Berichtstext nach stdout und Eingabefehler nach stderr. Eine unterbrochene Ausgabepipe liefert 2.

Verwenden Sie in CI kein `|| true`, um Befunde zu verstecken. Absichtlich ungültige Beispiele sollten Exitcode 1 explizit prüfen. Hilfe und Version liefern 0. `import-ha` schreibt immer einen JSON-Vertrag; `--json` verändert dessen Schema nicht.

<a id="python-library"></a>

## Python-Bibliothek

```python
from datetime import datetime, timezone
from ha_meter_contracts import audit, load_document, parse_contract

contract = parse_contract(load_document("examples/valid-three-meters.json"))
report = audit(contract, at=datetime(2026, 1, 1, 12, 0, 5, tzinfo=timezone.utc))
assert report["sums"][0]["value"] == 720
```

`parse_contract` erzeugt unveränderliche Dataclasses; `InputError` stellt `code`, `path`, `params` bereit. Verwenden Sie diesen Parser an jeder Grenze für nicht vertrauenswürdige Eingaben. `audit` erwartet einen validierten `Contract` und übersetzt keine Befunde. Die CLI ergänzt lokalisierte `message`-Werte. In der Bibliothek wählt der Aufrufer die Auswertungszeit explizit. Keine API verändert die Eingabe oder schreibt Dateien.

<a id="offline-home-assistant-adapter"></a>

## Offline-Adapter für Home Assistant

```sh
ha-meter-contracts import-ha examples/ha-contract.json --ha-states examples/ha-states.synthetic.json > /tmp/meter-contract.json
ha-meter-contracts check /tmp/meter-contract.json --at 2026-01-01T12:00:05Z --json
```

Ordnen Sie jedem gewünschten Messgerät `entity_id` und `timestamp_attribute` zu. Der Export ist ein Array von HA-Zustandsobjekten mit `entity_id`, `state` und `attributes`. Das zugeordnete Attribut muss die ursprüngliche ISO-Messzeit mit Zeitzone enthalten. `attributes.unit_of_measurement` muss dieselbe Dimension besitzen; W/kW und Wh/kWh werden in die Vertragseinheit umgerechnet.

Kopiert werden nur zugeordnete Werte und Quellzeiten. Andere Attribute einschließlich Anzeigenamen werden ignoriert. Ein strikt neuerer Messwert verschiebt den bestehenden nach `previous`. Derselbe Wert mit demselben Quellzeitstempel ist idempotent; ein älterer Wert oder ein widersprüchlicher Wert zum selben Zeitpunkt wird als `ha_sample_order` abgelehnt. Fehlende Entitäten und Zustände `unknown`/`unavailable` löschen den Messwert; sie werden nicht null Watt. Fehlende Quellzeit, inkompatible Einheit, fehlerhafter Wert oder doppelte Entitäts-ID lassen den Import mit 2 scheitern. Nicht zugeordnete Messgeräte bleiben unverändert. Entitäts-IDs dürfen in privaten Verträgen stehen; öffentliche Beispiele verwenden synthetische Kennungen.

Gewöhnlichen HA-Exporten fehlt oft die ursprüngliche Quellzeit. Der Adapter weigert sich dann absichtlich, eine zu erfinden. Beschaffen Sie zeitgestempelte Gerätedaten oder belassen Sie den Messwert als nicht verfügbar. HA-Empfangs-/Aktualisierungszeiten beweisen nicht die Erfassungszeit des Geräts. Der Adapter verbindet sich nie mit `/api/states` und liest kein Token. Er kopiert keine Energie-Rücksetzmarkierungen aus HA; ergänzen Sie geprüfte Rücksetznachweise vor Energiesummen separat.

<a id="suggested-workflow"></a>

## Empfohlener Ablauf

1. Deklarieren Sie den physischen Bereichsbaum und die Quellenherkunft anhand der Verkabelungsdokumentation.
2. Beginnen Sie mit einem Messgerät und einem festen synthetischen Beispiel.
3. Exportieren Sie nur notwendige Beobachtungen in eine private Datei.
4. Prüfen und bewerten Sie jeden Befund, bevor Sie nachgelagerte Automatisierung ändern.
5. Bewahren Sie bei Migrationen ursprüngliche Quellzeiten und Kalibrierungsnachweise auf.

Dieses Paket führt weder Reparaturen noch Entitätsumbenennungen, Geräteresets oder Automatisierungsbereitstellungen aus.
