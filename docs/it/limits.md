<a id="limits-and-trust-boundary"></a>

# Limiti e confine di fiducia

<!-- language-navigation:start -->
<p dir="ltr">
<a href="../limits.md" lang="en" dir="ltr">English</a> ·
<a href="../ar/limits.md" lang="ar" dir="rtl">العربية</a> ·
<a href="../bn/limits.md" lang="bn" dir="ltr">বাংলা</a> ·
<a href="../cs/limits.md" lang="cs" dir="ltr">Čeština</a> ·
<a href="../de/limits.md" lang="de" dir="ltr">Deutsch</a> ·
<a href="../es/limits.md" lang="es" dir="ltr">Español</a> ·
<a href="../fa/limits.md" lang="fa" dir="rtl">فارسی</a> ·
<a href="../fr/limits.md" lang="fr" dir="ltr">Français</a> ·
<a href="../he/limits.md" lang="he" dir="rtl">עברית</a> ·
<a href="../hi/limits.md" lang="hi" dir="ltr">हिन्दी</a> ·
<a href="../id/limits.md" lang="id" dir="ltr">Bahasa Indonesia</a> ·
<a href="limits.md" lang="it" dir="ltr">Italiano</a> ·
<a href="../ja/limits.md" lang="ja" dir="ltr">日本語</a> ·
<a href="../ko/limits.md" lang="ko" dir="ltr">한국어</a> ·
<a href="../nl/limits.md" lang="nl" dir="ltr">Nederlands</a> ·
<a href="../pl/limits.md" lang="pl" dir="ltr">Polski</a> ·
<a href="../pt/limits.md" lang="pt" dir="ltr">Português</a> ·
<a href="../ru/limits.md" lang="ru" dir="ltr">Русский</a> ·
<a href="../th/limits.md" lang="th" dir="ltr">ไทย</a> ·
<a href="../tr/limits.md" lang="tr" dir="ltr">Türkçe</a> ·
<a href="../uk/limits.md" lang="uk" dir="ltr">Українська</a> ·
<a href="../vi/limits.md" lang="vi" dir="ltr">Tiếng Việt</a> ·
<a href="../zh-Hans/limits.md" lang="zh-Hans" dir="ltr">简体中文</a> ·
<a href="../zh-Hant/limits.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->
Questo è un validatore offline di dichiarazioni, non un controllore di protezione, uno strumento di prova per elettricisti, un servizio di rilevamento del cablaggio o un’integrazione Home Assistant che esegue azioni.

- Una misura totale non consente di ricostruire l’esatta potenza simultanea di tre carichi sconosciuti. Le ipotesi statistiche sarebbero stime, non misure adatte alla protezione.
- Ambito, provenienza, direzione del segno e dichiarazioni di calibrazione provengono dall’operatore. Dichiarazioni false possono far apparire strutturalmente valido un sistema fisico non valido.
- `complete` significa completo rispetto alle foglie dichiarate, non a un cablaggio verificato indipendentemente. Un marcatore di azzeramento della fonte è una prova attendibile, non un’attestazione del dispositivo.
- Sono supportati W, kW, Wh, kWh, V e A. Non modelliamo potenza reattiva/apparente, algebra trifase, saturazione dei CT, trasformatori di tensione, overflow dei contatori o tariffe.
- I membri di una somma sono misuratori diretti, non altre somme. Le somme di potenza richiedono timestamp allineati. Quelle di energia richiedono un’origine esplicita comune del contatore e campioni allineati.
- I valori sono numeri finiti in virgola mobile. Non è un sistema contabile decimale adatto alla fatturazione. I fattori di calibrazione sono registrati, non applicati.
- Vengono controllati solo un campione corrente e uno precedente facoltativo. Non è un database storico, un rilevatore di anomalie o deriva né un audit completo dell’integrità dei contatori.
- I timestamp della fonte HA devono esistere e rappresentare davvero l’acquisizione. I tempi di ricezione della cache non vengono accettati implicitamente come sostituti.
- Il caricamento JSON/YAML è limitato; l’API di libreria `audit` si aspetta un `Contract` prodotto dal parser. Non costruire dataclass arbitrarie malformate da oggetti non attendibili.
- L’input da file accetta solo file regolari. Rifiuta symlink nell’ultimo componente, FIFO, dispositivi e directory, apre senza blocco e verifica il descrittore aperto prima della lettura. Le piattaforme prive di `O_NOFOLLOW` e `O_NONBLOCK` rifiutano i file; usare lì `ha_meter_contracts.reader.loads_document` con una stringa già limitata. I symlink nelle directory superiori non sono un confine di sandbox. Il limite di byte vale anche se il file cresce durante la lettura.
- Un risultato positivo non dimostra il funzionamento fisico di relè, valvole, motori, flusso di pompe o sicurezza elettrica. Non vengono eseguiti riparazioni o tentativi automatici.

Input e output possono contenere ID di entità e tempi forniti dall’operatore. Conservare privatamente contratti/esportazioni reali. Il repository contiene solo esempi sintetici. Il programma non carica dati, ma inoltrare il rapporto a un servizio esterno è una scelta dell’operatore.
