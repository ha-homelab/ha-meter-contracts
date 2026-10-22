<a id="contract-schema-v1"></a>

# Schema del contratto v1

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
<a href="schema.md" lang="it" dir="ltr">Italiano</a> ·
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
Lo [schema.json](../../schema.json) leggibile dalle macchine descrive la struttura. Il parser Python è autorevole per i limiti; `audit` aggiunge semantica fisica e temporale che JSON Schema non può dimostrare. Generare il file strutturale con `python3 scripts/generate_schema.py`.

<a id="root-and-limits"></a>

## Radice e limiti

Obbligatori: intero `schema_version: 1`, `scopes`, `meters`. Facoltativo: `sums` (vuoto per impostazione predefinita). I campi sconosciuti sono rifiutati a ogni livello. Massimo 512 ambiti, 512 misuratori e 128 somme; ambiti e misuratori non devono essere vuoti. Ogni somma ha 1–512 membri. Input UTF-8, massimo 1.048.576 byte, profondità 16 e 20.000 nodi di valore. Sono rifiutati chiavi JSON duplicate, NaN/Infinity e alias/ancore/tag espliciti YAML. Mettere tra virgolette i timestamp YAML perché restino stringhe.

Gli identificatori hanno 1–96 caratteri ASCII: prima lettera/cifra, poi lettere, cifre, `.`, `_`, `-`. Gli ID sono univoci in ogni raccolta; ambiti e misuratori hanno namespace separati. Tutti i tempi includono `T` e fuso orario. I numeri sono finiti, non booleani, entro ±10^15 salvo limiti più stretti.

<a id="physical-scopes"></a>

## Ambiti fisici

Ogni ambito ha `id`, `kind` (`site`, `circuit`, `strip`, `outlet`, `load`) e `parent` facoltativo. I genitori devono esistere e formare una foresta aciclica. Un misuratore su un genitore copre tutti i discendenti. I tipi di ambito sono descrittivi: non deducono tensione, fasi, valori nominali, cablaggio o genitori consentiti. La topologia reale viene dichiarata dall’utente.

<a id="meters"></a>

## Misuratori

Campi obbligatori:

- `id`, `scope`: identificatore univoco della misura e ambito fisico dichiarato.
- `quantity`: `power`, `energy`, `voltage`, `current`.
- `unit`: rispettivamente W/kW, Wh/kWh, V, A. Il parser accetta il vocabolario; l’auditor verifica la dimensione.
- `kind`: `measured` o `estimated`. È una dichiarazione, non una verifica di laboratorio.
- `provenance`: identità stabile del flusso fisico di misure, **non** della sua rappresentazione HA/MQTT. Le letture alias la condividono. Segno/grandezza/ambito diversi con una provenienza unica creano conflitto; tutti gli alias del flusso diventano indisponibili per le somme, indipendentemente dall’ordine di input. Scegliere provenienze distinte per canali di flusso realmente distinti.
- `sign`: `nonnegative` per magnitudini solo consumo/importazione/esportazione; `signed` per un flusso bidirezionale dichiarato. Questa versione non deduce quale direzione fisica sia positiva.
- `state_class`: `measurement`, `total`, `total_increasing`.
- `freshness_seconds`: età massima positiva, 0.001–604800 secondi.

`reset` facoltativo: `never`, `periodic`, `device_restart`, `unknown`, `not_applicable` (predefinito). L’energia richiede una politica esplicita diversa da `not_applicable` e una classe di stato di tipo total. L’energia con segno non può usare `total_increasing`. Le altre grandezze richiedono `measurement` e `not_applicable`.

`sample`, `previous` facoltativi: null o oggetto con `value` (numero o null), `measured_at`, `reset_at` facoltativo. Il precedente deve essere più vecchio. Un calo di contatore non negativo richiede un marcatore di azzeramento tra campioni; `never` lo rifiuta. `reset_at` non deve essere successivo al suo campione e riguarda solo l’energia. Semantiche di azzeramento sconosciute producono un avviso. Un contatore netto con segno può diminuire legittimamente; la base corretta resta responsabilità del produttore.

`calibration` facoltativa: `quantity`, `factor` positivo (10^-12–10^12), identificatore sintetico/privato `reference`, `verified_at`. Registra prove per quella precisa grandezza. I valori sono **già calibrati**: il validatore non riapplica mai il fattore. Una calibrazione futura o di tensione su un misuratore di potenza non è valida. L’assenza di calibrazione non prova accuratezza e non è automaticamente un errore.

`entity_id`, `timestamp_attribute` facoltativi: mappatura HA offline; vedere [uso](usage.md#offline-home-assistant-adapter).

<a id="sums"></a>

## Somme

Obbligatori: `id`, `scope` di destinazione, elenco di ID misuratori in `meters`, `quantity` (`power` o `energy`), `coverage` (`partial` o `complete`). `max_skew_seconds` facoltativo: 0–604800, predefinito 2.

I membri devono appartenere all’ambito di destinazione, avere dimensioni e semantica del segno coerenti, usare flussi fisici diversi e non sovrapporsi come genitore/figlio o ambiti identici. Una somma completa copre ogni **ambito foglia dichiarato** sotto la destinazione. Il cablaggio non dichiarato non è rilevabile. Una somma parziale dichiara esplicitamente copertura parziale. Le somme annidate non sono supportate; i membri fanno sempre riferimento a misuratori.

Ogni membro deve avere dati validi e recenti; i tempi di acquisizione devono rientrare nello scarto consentito. L’energia richiede inoltre origini `reset_at` esplicite identiche. Si verifica l’allineamento dichiarato, non l’accuratezza dell’accumulo storico. Le somme sono convertite in W o Wh. Le somme di corrente e tensione non sono intenzionalmente supportate, perché dipendono dalla topologia del circuito.

Una somma numerica è indisponibile quando manca una prova richiesta o fallisce un controllo semantico. Le stime si propagano come `kind: estimated`. Due alias possono coesistere nell’inventario, ma non contribuire entrambi a una somma. Non viene dedotto alcun totale per singole prese non misurate.

<a id="report-v1"></a>

## Rapporto v1

Radice: `schema_version`, istante di valutazione `at` normalizzato in UTC, conteggi di gravità in `summary`, `findings` ordinati e `sums`. Ogni risultato contiene `code`, `severity`, `path` in stile JSON, `params` strutturati; la CLI aggiunge `message`. Ogni somma contiene `id`, `scope`, `quantity`, `unit` di base, `value`, `status`, `kind`, `coverage`. I valori sconosciuti sono JSON null, mai NaN.
