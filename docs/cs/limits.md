<a id="limits-and-trust-boundary"></a>

# Omezení a hranice důvěry

<!-- language-navigation:start -->
<p dir="ltr">
<a href="../limits.md" lang="en" dir="ltr">English</a> ·
<a href="../ar/limits.md" lang="ar" dir="rtl">العربية</a> ·
<a href="../bn/limits.md" lang="bn" dir="ltr">বাংলা</a> ·
<a href="limits.md" lang="cs" dir="ltr">Čeština</a> ·
<a href="../de/limits.md" lang="de" dir="ltr">Deutsch</a> ·
<a href="../es/limits.md" lang="es" dir="ltr">Español</a> ·
<a href="../fa/limits.md" lang="fa" dir="rtl">فارسی</a> ·
<a href="../fr/limits.md" lang="fr" dir="ltr">Français</a> ·
<a href="../he/limits.md" lang="he" dir="rtl">עברית</a> ·
<a href="../hi/limits.md" lang="hi" dir="ltr">हिन्दी</a> ·
<a href="../id/limits.md" lang="id" dir="ltr">Bahasa Indonesia</a> ·
<a href="../it/limits.md" lang="it" dir="ltr">Italiano</a> ·
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
Jde o offline validátor deklarací, nikoli o ochranný řadič, zkušební přístroj elektrikáře, službu zjišťující zapojení ani integraci Home Assistant provádějící akce.

- Z jediného celkového údaje nelze obnovit přesný současný příkon tří neznámých zátěží. Statistické dohady by byly odhady, ne měření vhodná pro ochranu.
- Rozsah, původ, směr znaménka a deklarace kalibrace dodává obsluha. Nepravdivé deklarace mohou způsobit, že fyzicky neplatný systém vypadá strukturálně platný.
- `complete` znamená úplnost vzhledem k deklarovaným listům, ne nezávisle ověřenému zapojení. Značka resetu ze zdroje je důvěryhodný podklad, nikoli atestace zařízení.
- Podporovány jsou W, kW, Wh, kWh, V a A. Nemodelujeme jalový/zdánlivý výkon, třífázovou algebru, saturaci CT, transformátory napětí, přetečení čítače ani tarify.
- Členy součtu jsou přímo měřidla, nikoli jiné součty. Součty výkonu vyžadují časově sladěné údaje. Součty energie vyžadují výslovný společný počátek čítačů a sladěné vzorky.
- Hodnoty jsou konečná čísla s plovoucí desetinnou čárkou. Nejde o desetinné účetnictví pro fakturaci. Kalibrační koeficienty se zaznamenávají, nikoli aplikují.
- Kontroluje se pouze aktuální a volitelně předchozí vzorek. Nejde o historickou databázi, detektor anomálií či driftu ani úplný audit integrity čítačů.
- Zdrojové časy HA musí existovat a skutečně označovat pořízení měření. Časy příjmu do mezipaměti se tiše nepřijímají jako náhrada.
- Načítání JSON/YAML je omezené; knihovní API `audit` očekává `Contract` vytvořený parserem. Nevytvářejte libovolné chybně strukturované datové třídy z nedůvěryhodných objektů.
- Souborový vstup přijímá pouze běžné soubory. Odmítá symbolické odkazy v poslední složce cesty, FIFO, zařízení a adresáře, otevírá neblokujícím způsobem a před čtením ověřuje otevřený deskriptor. Platformy bez `O_NOFOLLOW` a `O_NONBLOCK` soubory odmítají; tam použijte `ha_meter_contracts.reader.loads_document` s již omezeným řetězcem. Symbolické odkazy v nadřazených adresářích nejsou hranicí sandboxu. Limit bajtů platí i při růstu souboru během čtení.
- Úspěšný výsledek nedokazuje fyzickou funkci relé, ventilů, motorů, průtok čerpadla ani elektrickou bezpečnost. Neprovádějí se automatické opravy ani opakované pokusy.

Vstup i výstup mohou obsahovat ID entit a časy dodané obsluhou. Skutečné kontrakty/exporty uchovávejte soukromě. Repozitář obsahuje pouze syntetické příklady. Program nic neodesílá, ale přesměrování zprávy do externí služby je rozhodnutí obsluhy.
