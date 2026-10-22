<a id="troubleshooting"></a>

# Risoluzione dei problemi

<!-- language-navigation:start -->
<p dir="ltr">
<a href="../troubleshooting.md" lang="en" dir="ltr">English</a> ·
<a href="../ar/troubleshooting.md" lang="ar" dir="rtl">العربية</a> ·
<a href="../bn/troubleshooting.md" lang="bn" dir="ltr">বাংলা</a> ·
<a href="../cs/troubleshooting.md" lang="cs" dir="ltr">Čeština</a> ·
<a href="../de/troubleshooting.md" lang="de" dir="ltr">Deutsch</a> ·
<a href="../es/troubleshooting.md" lang="es" dir="ltr">Español</a> ·
<a href="../fa/troubleshooting.md" lang="fa" dir="rtl">فارسی</a> ·
<a href="../fr/troubleshooting.md" lang="fr" dir="ltr">Français</a> ·
<a href="../he/troubleshooting.md" lang="he" dir="rtl">עברית</a> ·
<a href="../hi/troubleshooting.md" lang="hi" dir="ltr">हिन्दी</a> ·
<a href="../id/troubleshooting.md" lang="id" dir="ltr">Bahasa Indonesia</a> ·
<a href="troubleshooting.md" lang="it" dir="ltr">Italiano</a> ·
<a href="../ja/troubleshooting.md" lang="ja" dir="ltr">日本語</a> ·
<a href="../ko/troubleshooting.md" lang="ko" dir="ltr">한국어</a> ·
<a href="../nl/troubleshooting.md" lang="nl" dir="ltr">Nederlands</a> ·
<a href="../pl/troubleshooting.md" lang="pl" dir="ltr">Polski</a> ·
<a href="../pt/troubleshooting.md" lang="pt" dir="ltr">Português</a> ·
<a href="../ru/troubleshooting.md" lang="ru" dir="ltr">Русский</a> ·
<a href="../th/troubleshooting.md" lang="th" dir="ltr">ไทย</a> ·
<a href="../tr/troubleshooting.md" lang="tr" dir="ltr">Türkçe</a> ·
<a href="../uk/troubleshooting.md" lang="uk" dir="ltr">Українська</a> ·
<a href="../vi/troubleshooting.md" lang="vi" dir="ltr">Tiếng Việt</a> ·
<a href="../zh-Hans/troubleshooting.md" lang="zh-Hans" dir="ltr">简体中文</a> ·
<a href="../zh-Hant/troubleshooting.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->
<a id="a-three-outlet-strip-cannot-produce-three-power-readings"></a>

## Una multipresa a tre uscite non produce tre letture di potenza

`scope_outside` significa che un risultato individuale richiesto usa una misura più ampia. Mantenere un’entità per l’intera multipresa. Per la potenza individuale servono misure indipendenti di ambito corretto. Un relè acceso non dimostra che il carico consumi; una pompa che consuma elettricità non dimostra flusso d’acqua.

<a id="a-migrated-sensor-doubles-the-total"></a>

## Un sensore migrato raddoppia il totale

`alias_stream` da solo è informativo. `duplicate_stream` significa che entrambe le copie sono nella somma. Dare alle copie dello stesso CT la stessa provenienza e tenerne solo una nella somma. Non cambiare provenienza solo per silenziare il controllo.

![Una fonte e due rappresentazioni](../images/duplicate-stream.svg)

<a id="no-numeric-sum-despite-individually-plausible-numbers"></a>

## Nessuna somma numerica nonostante valori plausibili

Controllare `sample_stale`, `sample_future`, `sample_skew`, `sample_missing`, `incomplete_coverage`, `unit_dimension`, `scope_overlap`. Aggiornare la fonte originale e conservarne il tempo di acquisizione. Aumentare l’età consentita cambia la politica, non ripara la misura. Una somma completa è valutata rispetto alle foglie dichiarate: verificare anche la dichiarazione.

![Cronologia sintetica della qualità dei campioni](../images/sample-quality.svg)

<a id="energy-decreased-at-midnight"></a>

## L’energia è diminuita a mezzanotte

Il calo può essere un vero azzeramento, sostituzione o correzione. Dichiarare la politica e aggiungere `reset_at` da prove reali della fonte. Il timestamp di una ripetizione HA non è un marcatore di azzeramento. `total_increasing` non è adatto all’energia netta con segno. Contatori con origini diverse non vengono sommati.

<a id="voltage-looks-calibrated-but-watts-still-differ"></a>

## La tensione sembra calibrata ma i watt differiscono

La calibrazione è specifica della grandezza. Una correzione di tensione non valida corrente, relazione di fase, potenza o energia accumulata. Il campo fattore documenta soltanto: i valori devono già contenere la correzione desiderata.

<a id="yaml-fails-although-another-parser-accepts-it"></a>

## YAML fallisce anche se un altro parser lo accetta

Mettere timestamp tra virgolette, eliminare alias/ancore/tag personalizzati e chiavi duplicate, usare numeri finiti. I campi sconosciuti sono errori per rilevare refusi. I limiti valgono per entrambi i formati. Usare JSON per lo scambio se gli scalari YAML ambigui creano problemi.

<a id="ha-import-fails-on-timestamps"></a>

## L’importazione HA fallisce sui timestamp

Impostare `timestamp_attribute` su un vero attributo del tempo di misura. `last_reported` dimostra solo ricezione da parte di HA. Senza tempo della fonte, lo strumento non può stabilire freschezza; lasciare il campione indisponibile. Non ci sono token o connessioni da diagnosticare: l’importazione è offline.

<a id="safe-issue-report"></a>

## Segnalazione sicura

Includere versioni pacchetto/Python, codici stabili, contratto sintetico minimo, `--at` scelto, risultato atteso ed effettivo. Non allegare export HA completo, token, indirizzo reale, orari domestici o ID privati dei dispositivi. Nel riproduttore, 0 W e campione indisponibile devono restare distinti.
