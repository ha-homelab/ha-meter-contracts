<a id="troubleshooting"></a>

# Řešení problémů

<!-- language-navigation:start -->
<p dir="ltr">
<a href="../troubleshooting.md" lang="en" dir="ltr">English</a> ·
<a href="../ar/troubleshooting.md" lang="ar" dir="rtl">العربية</a> ·
<a href="../bn/troubleshooting.md" lang="bn" dir="ltr">বাংলা</a> ·
<a href="troubleshooting.md" lang="cs" dir="ltr">Čeština</a> ·
<a href="../de/troubleshooting.md" lang="de" dir="ltr">Deutsch</a> ·
<a href="../es/troubleshooting.md" lang="es" dir="ltr">Español</a> ·
<a href="../fa/troubleshooting.md" lang="fa" dir="rtl">فارسی</a> ·
<a href="../fr/troubleshooting.md" lang="fr" dir="ltr">Français</a> ·
<a href="../he/troubleshooting.md" lang="he" dir="rtl">עברית</a> ·
<a href="../hi/troubleshooting.md" lang="hi" dir="ltr">हिन्दी</a> ·
<a href="../id/troubleshooting.md" lang="id" dir="ltr">Bahasa Indonesia</a> ·
<a href="../it/troubleshooting.md" lang="it" dir="ltr">Italiano</a> ·
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

## Lišta se třemi zásuvkami neposkytuje tři údaje o výkonu

`scope_outside` znamená, že požadovaný individuální výsledek používá širší měření. Ponechte jednu entitu pro celou lištu. Individuální výkon vyžaduje nezávislá měření správného rozsahu. Sepnuté relé nedokazuje spotřebu zátěže; čerpadlo odebírající elektřinu nedokazuje průtok vody.

<a id="a-migrated-sensor-doubles-the-total"></a>

## Migrovaný senzor zdvojnásobuje součet

Samotné `alias_stream` je informativní. `duplicate_stream` znamená, že v součtu jsou obě kopie. Kopiím stejného CT dejte stejný původ a v součtu ponechte pouze jednu. Neměňte původ jen kvůli umlčení kontroly.

![Jeden zdroj a dvě reprezentace](../images/duplicate-stream.svg)

<a id="no-numeric-sum-despite-individually-plausible-numbers"></a>

## Žádný číselný součet navzdory věrohodným hodnotám

Zkontrolujte `sample_stale`, `sample_future`, `sample_skew`, `sample_missing`, `incomplete_coverage`, `unit_dimension`, `scope_overlap`. Obnovte skutečný zdroj a zachovejte čas měření. Zvýšení dovoleného stáří mění politiku, neopravuje měření. Úplný součet se hodnotí vůči deklarovaným listům: zkontrolujte i deklaraci.

![Syntetická časová osa kvality vzorků](../images/sample-quality.svg)

<a id="energy-decreased-at-midnight"></a>

## Energie o půlnoci klesla

Pokles může být skutečný reset, výměna nebo oprava. Deklarujte politiku a přidejte `reset_at` ze skutečných podkladů zdroje. Čas přehrání HA není značka resetu. `total_increasing` není vhodné pro čistou energii se znaménkem. Čítače s různými počátky se nesčítají.

<a id="voltage-looks-calibrated-but-watts-still-differ"></a>

## Napětí vypadá kalibrovaně, ale watty se liší

Kalibrace je specifická pro veličinu. Oprava napětí nepotvrzuje proud, fázový vztah, výkon ani akumulovanou energii. Pole koeficientu je jen dokumentační: hodnoty již musí obsahovat zamýšlenou opravu.

<a id="yaml-fails-although-another-parser-accepts-it"></a>

## YAML selhává, přestože jej jiný parser přijímá

Uzavřete časy do uvozovek, odstraňte aliasy/kotvy/vlastní tagy a duplicitní klíče, použijte konečná čísla. Neznámá pole jsou chyby, aby se zachytily překlepy. Limity platí pro oba formáty. Pokud vadí nejednoznačné skaláry YAML, pro výměnu použijte JSON.

<a id="ha-import-fails-on-timestamps"></a>

## Import HA selhává na časech

Nastavte `timestamp_attribute` na skutečný atribut času měření. `last_reported` dokazuje pouze příjem do HA. Bez zdrojového času nástroj nemůže určit čerstvost; ponechte vzorek nedostupný. Nejsou tu tokeny ani spojení k diagnostice: import je offline.

<a id="safe-issue-report"></a>

## Bezpečné hlášení problému

Uveďte verze balíčku/Pythonu, stabilní kódy, minimální syntetický kontrakt, zvolený `--at`, očekávaný a skutečný výsledek. Nepřikládejte úplný export HA, tokeny, skutečnou adresu, domácí rozvrhy ani soukromá ID zařízení. V reprodukci musí zůstat rozlišeny 0 W a nedostupný vzorek.
