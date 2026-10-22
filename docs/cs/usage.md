<a id="usage"></a>

# Použití

<!-- language-navigation:start -->
<p dir="ltr">
<a href="../usage.md" lang="en" dir="ltr">English</a> ·
<a href="../ar/usage.md" lang="ar" dir="rtl">العربية</a> ·
<a href="../bn/usage.md" lang="bn" dir="ltr">বাংলা</a> ·
<a href="usage.md" lang="cs" dir="ltr">Čeština</a> ·
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

## Audit

```sh
ha-meter-contracts check contract.json --json --lang en
ha-meter-contracts check examples/minimal.yaml --at 2026-01-01T12:00:05Z --lang es
```

`--at` přijímá čas ISO 8601 s časovým pásmem. Výchozí je aktuální UTC. Při stejném vstupu, čase a jazyce je JSON deterministický. Vzorek zůstává čerstvý včetně hranice `freshness_seconds`; zastaralý je až po ní. Budoucí vzorek je neplatný, bez implicitní tolerance odchylky hodin.

Návratové kódy: 0 = žádné chyby/varování; 1 = sémantický problém nebo problém kvality vzorku; 2 = chyba vstupu/CLI. Informace jako nepoužitý alias nezpůsobují neúspěch. `--json` zapisuje zprávy a objekty vstupních chyb na stdout. Bez této volby jde text auditu na stdout a vstupní chyby na stderr. Přerušená výstupní roura vrací 2.

Nepoužívejte v CI `|| true` ke skrytí nálezů. Záměrně neplatné příklady mají výslovně ověřovat kód 1. Nápověda a verze vracejí 0. `import-ha` vždy zapisuje kontrakt JSON; `--json` nemění jeho schéma.

<a id="python-library"></a>

## Knihovna Pythonu

```python
from datetime import datetime, timezone
from ha_meter_contracts import audit, load_document, parse_contract

contract = parse_contract(load_document("examples/valid-three-meters.json"))
report = audit(contract, at=datetime(2026, 1, 1, 12, 0, 5, tzinfo=timezone.utc))
assert report["sums"][0]["value"] == 720
```

`parse_contract` vytváří neměnné datové třídy; `InputError` zpřístupňuje `code`, `path`, `params`. Parser používejte na každé hranici nedůvěryhodného vstupu. `audit` očekává validovaný `Contract` a nepřekládá nálezy. CLI přidává lokalizované hodnoty `message`. V knihovně volající výslovně vybírá čas vyhodnocení. Žádné API nemění vstup ani nezapisuje soubory.

<a id="offline-home-assistant-adapter"></a>

## Offline adaptér Home Assistant

```sh
ha-meter-contracts import-ha examples/ha-contract.json --ha-states examples/ha-states.synthetic.json > /tmp/meter-contract.json
ha-meter-contracts check /tmp/meter-contract.json --at 2026-01-01T12:00:05Z --json
```

Na každém požadovaném měřidle namapujte `entity_id` a `timestamp_attribute`. Export je pole stavů HA s `entity_id`, `state` a `attributes`. Mapovaný atribut musí obsahovat původní čas měření ISO s časovým pásmem. `attributes.unit_of_measurement` musí mít stejný rozměr; W/kW a Wh/kWh se převedou na jednotku kontraktu.

Kopírují se jen mapované hodnoty a zdrojové časy. Jiné atributy včetně uživatelských názvů se ignorují. Striktně novější vzorek přesune stávající do `previous`. Opakování stejné hodnoty se stejným zdrojovým časem je idempotentní; starší vzorek nebo konfliktní hodnota ve stejném čase se odmítne jako `ha_sample_order`. Chybějící entity a stavy `unknown`/`unavailable` vzorek vymažou; nemění se na nulu. Chybějící čas, neslučitelná jednotka, chybná hodnota nebo duplicitní ID entity způsobí selhání importu s 2. Nemapovaná měřidla zůstanou beze změny. Soukromé kontrakty mohou obsahovat ID entit; veřejné příklady používají syntetické identifikátory.

Běžný export HA často neobsahuje původní čas. V takovém případě ho adaptér záměrně odmítá vymyslet. Získejte data zařízení s časy nebo ponechte měřidlo nedostupné. Časy příjmu/aktualizace HA nedokazují pořízení měření zařízením. Adaptér se nikdy nepřipojuje k `/api/states` ani nečte tokeny. Nekopíruje značky resetu energie z HA; před součtem energie přidejte zvlášť ověřené podklady.

<a id="suggested-workflow"></a>

## Doporučený postup

1. Deklarujte strom fyzických rozsahů a původ zdrojů podle dokumentace zapojení.
2. Začněte jedním měřidlem a pevným syntetickým příkladem.
3. Exportujte pouze potřebná pozorování do soukromého souboru.
4. Spusťte audit a posuďte každý nález před změnou navazující automatizace.
5. Při migracích zachovejte původní časy a podklady kalibrace.

Balíček neprovádí nápravy, nepřejmenovává entity, neresetuje zařízení ani nenasazuje automatizace.
