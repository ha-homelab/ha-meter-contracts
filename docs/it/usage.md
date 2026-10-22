<a id="usage"></a>

# Uso

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
<a href="usage.md" lang="it" dir="ltr">Italiano</a> ·
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

`--at` accetta un timestamp ISO 8601 con fuso orario. Il valore predefinito è l’UTC corrente. A parità di input, tempo e lingua, il JSON è deterministico. Un campione resta recente fino al limite incluso di `freshness_seconds`; diventa obsoleto solo dopo. Un campione futuro non è valido, senza tolleranza implicita allo scarto degli orologi.

Codici di uscita: 0 = nessun errore/avviso; 1 = problema semantico o di qualità del campione; 2 = errore input/CLI. Informazioni come un alias inutilizzato non fanno fallire il controllo. `--json` scrive rapporti e oggetti di errore input su stdout. Senza l’opzione, il testo di audit va su stdout e gli errori input su stderr. Una pipe di output interrotta restituisce 2.

Non usare `|| true` in CI per nascondere risultati. Gli esempi intenzionalmente non validi devono verificare esplicitamente l’uscita 1. Aiuto e versione restituiscono 0. `import-ha` scrive sempre un contratto JSON; `--json` non ne cambia lo schema.

<a id="python-library"></a>

## Libreria Python

```python
from datetime import datetime, timezone
from ha_meter_contracts import audit, load_document, parse_contract

contract = parse_contract(load_document("examples/valid-three-meters.json"))
report = audit(contract, at=datetime(2026, 1, 1, 12, 0, 5, tzinfo=timezone.utc))
assert report["sums"][0]["value"] == 720
```

`parse_contract` crea dataclass immutabili; `InputError` espone `code`, `path`, `params`. Usare il parser a ogni confine di input non fidato. `audit` richiede un `Contract` validato e non traduce i risultati. La CLI aggiunge valori `message` localizzati. Nella libreria il chiamante sceglie esplicitamente l’istante di valutazione. Nessuna API modifica l’input o scrive file.

<a id="offline-home-assistant-adapter"></a>

## Adattatore offline Home Assistant

```sh
ha-meter-contracts import-ha examples/ha-contract.json --ha-states examples/ha-states.synthetic.json > /tmp/meter-contract.json
ha-meter-contracts check /tmp/meter-contract.json --at 2026-01-01T12:00:05Z --json
```

Mappare `entity_id` e `timestamp_attribute` su ogni misuratore desiderato. L’export è un array di stati HA con `entity_id`, `state` e `attributes`. L’attributo mappato deve contenere l’istante ISO originale della misura con fuso orario. `attributes.unit_of_measurement` deve avere la stessa dimensione; W/kW e Wh/kWh vengono convertiti nell’unità del contratto.

Si copiano solo valori mappati e tempi della fonte. Gli altri attributi, compresi i nomi descrittivi, sono ignorati. Un campione strettamente più recente sposta quello esistente in `previous`. Ripetere lo stesso valore con lo stesso timestamp sorgente è idempotente; un campione più vecchio o un valore in conflitto allo stesso istante viene rifiutato come `ha_sample_order`. Entità mancanti e stati `unknown`/`unavailable` cancellano il campione; non diventano zero. Timestamp mancante, unità incompatibile, valore malformato o ID entità duplicato fanno fallire l’importazione con 2. I misuratori non mappati restano invariati. I contratti privati possono contenere ID entità; gli esempi pubblici usano identificatori sintetici.

Un normale export HA spesso non contiene il timestamp originale. In quel caso l’adattatore si rifiuta deliberatamente di inventarlo. Ottenere dati del dispositivo con timestamp o lasciare il misuratore indisponibile. I tempi di ricezione/aggiornamento HA non provano l’acquisizione del dispositivo. L’adattatore non si collega mai a `/api/states` né legge token. Non copia marcatori di azzeramento energia da HA; aggiungere separatamente prove verificate prima di sommare energia.

<a id="suggested-workflow"></a>

## Procedura consigliata

1. Dichiarare albero degli ambiti fisici e provenienza delle fonti usando la documentazione del cablaggio.
2. Iniziare con un misuratore e un esempio sintetico fisso.
3. Esportare solo le osservazioni necessarie in un file privato.
4. Eseguire l’audit e valutare ogni risultato prima di modificare un’automazione a valle.
5. Conservare tempi originali e prove di calibrazione durante le migrazioni.

Il pacchetto non esegue riparazioni, rinomina entità, azzera dispositivi o distribuisce automazioni.
