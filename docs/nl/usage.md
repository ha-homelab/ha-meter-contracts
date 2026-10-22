<a id="usage"></a>

# Gebruik

<!-- language-navigation:start -->
<p dir="ltr">
<a href="../usage.md" lang="en" dir="ltr">English</a> ·
<a href="../ar/usage.md" lang="ar" dir="rtl">العربية</a> ·
<a href="../bn/usage.md" lang="bn" dir="ltr">বাংলা</a> ·
<a href="../cs/usage.md" lang="cs" dir="ltr">Čeština</a> ·
<a href="../de/usage.md" lang="de" dir="ltr">Deutsch</a> ·
<a href="../es/usage.md" lang="es" dir="ltr">Español</a> ·
<a href="../fa/usage.md" lang="fa" dir="rtl">فارسی</a> ·
<a href="../fr/usage.md" lang="fr" dir="ltr">Français</a> ·
<a href="../he/usage.md" lang="he" dir="rtl">עברית</a> ·
<a href="../hi/usage.md" lang="hi" dir="ltr">हिन्दी</a> ·
<a href="../id/usage.md" lang="id" dir="ltr">Bahasa Indonesia</a> ·
<a href="../it/usage.md" lang="it" dir="ltr">Italiano</a> ·
<a href="../ja/usage.md" lang="ja" dir="ltr">日本語</a> ·
<a href="../ko/usage.md" lang="ko" dir="ltr">한국어</a> ·
<a href="usage.md" lang="nl" dir="ltr">Nederlands</a> ·
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

## Audit

```sh
ha-meter-contracts check contract.json --json --lang en
ha-meter-contracts check examples/minimal.yaml --at 2026-01-01T12:00:05Z --lang es
```

`--at` accepteert een ISO 8601-tijdstip met tijdzone. Standaard is de huidige UTC-tijd. Bij gelijke invoer, tijd en taal is de JSON deterministisch. Een monster blijft recent tot en met de grens `freshness_seconds`; pas daarna is het verouderd. Een toekomstig monster is ongeldig, zonder impliciete tolerantie voor klokafwijking.

Exitcodes: 0 = geen fouten/waarschuwingen; 1 = semantisch probleem of probleem met monsterkwaliteit; 2 = invoer-/CLI-fout. Informatieve bevindingen zoals een ongebruikte alias laten de controle niet mislukken. `--json` schrijft rapporten en invoerfoutobjecten naar stdout. Zonder deze optie gaat audittekst naar stdout en gaan invoerfouten naar stderr. Een verbroken uitvoerpijp geeft 2 terug.

Gebruik geen `|| true` in CI om bevindingen te verbergen. Bewust ongeldige voorbeelden moeten expliciet exitcode 1 controleren. Help en versie geven 0 terug. `import-ha` schrijft altijd een JSON-contract; `--json` verandert dat schema niet.

<a id="python-library"></a>

## Python-bibliotheek

```python
from datetime import datetime, timezone
from ha_meter_contracts import audit, load_document, parse_contract

contract = parse_contract(load_document("examples/valid-three-meters.json"))
report = audit(contract, at=datetime(2026, 1, 1, 12, 0, 5, tzinfo=timezone.utc))
assert report["sums"][0]["value"] == 720
```

`parse_contract` maakt onveranderlijke dataclasses; `InputError` biedt `code`, `path`, `params`. Gebruik de parser op elke niet-vertrouwde invoergrens. `audit` verwacht een gevalideerd `Contract` en vertaalt geen bevindingen. De CLI voegt gelokaliseerde `message`-waarden toe. Bij bibliotheekgebruik kiest de aanroeper expliciet de evaluatietijd. Geen van beide API's wijzigt de invoer of schrijft bestanden.

<a id="offline-home-assistant-adapter"></a>

## Offline Home Assistant-adapter

```sh
ha-meter-contracts import-ha examples/ha-contract.json --ha-states examples/ha-states.synthetic.json > /tmp/meter-contract.json
ha-meter-contracts check /tmp/meter-contract.json --at 2026-01-01T12:00:05Z --json
```

Koppel `entity_id` en `timestamp_attribute` op elke gewenste meter. De export is een array van HA-toestanden met `entity_id`, `state` en `attributes`. Het gekoppelde attribuut moet de oorspronkelijke ISO-meettijd met tijdzone bevatten. `attributes.unit_of_measurement` moet dezelfde dimensie hebben; W/kW en Wh/kWh worden naar de contracteenheid omgerekend.

Alleen gekoppelde waarden en brontijden worden gekopieerd. Andere attributen, waaronder gebruiksvriendelijke namen, worden genegeerd. Een strikt nieuwer monster verplaatst het bestaande naar `previous`. Dezelfde waarde met hetzelfde brontijdstip opnieuw importeren is idempotent; een ouder monster of een conflicterende waarde op hetzelfde tijdstip wordt als `ha_sample_order` geweigerd. Ontbrekende entiteiten en toestanden `unknown`/`unavailable` wissen het monster; ze worden geen nul. Ontbrekende tijd, incompatibele eenheid, misvormde waarde of dubbel entiteits-ID laat de import met 2 mislukken. Niet-gekoppelde meters blijven ongewijzigd. Privécontracten kunnen entiteits-ID's bevatten; openbare voorbeelden gebruiken synthetische identificatoren.

Een gewone HA-export bevat vaak niet het oorspronkelijke tijdstip. In dat geval weigert de adapter dit bewust te verzinnen. Verkrijg apparaatgegevens met tijdstippen of laat de meter onbeschikbaar. HA-ontvangst-/bijwerktijden bewijzen geen meting door het apparaat. De adapter maakt nooit verbinding met `/api/states` en leest geen tokens. Hij kopieert geen energieresetmarkeringen uit HA; voeg afzonderlijk geverifieerde onderbouwing toe voordat u energie optelt.

<a id="suggested-workflow"></a>

## Voorgestelde werkwijze

1. Geef de fysieke bereikboom en bronherkomst op aan de hand van bedradingsdocumentatie.
2. Begin met één meter en een vast synthetisch voorbeeld.
3. Exporteer alleen noodzakelijke waarnemingen naar een privébestand.
4. Voer de audit uit en beoordeel elke bevinding voordat u afhankelijke automatisering wijzigt.
5. Bewaar brontijden en kalibratieonderbouwing tijdens migraties.

Het pakket voert geen reparaties uit, hernoemt geen entiteiten, reset geen apparaten en implementeert geen automatisering.
