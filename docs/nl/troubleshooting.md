<a id="troubleshooting"></a>

# Problemen oplossen

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
<a href="../it/troubleshooting.md" lang="it" dir="ltr">Italiano</a> ·
<a href="../ja/troubleshooting.md" lang="ja" dir="ltr">日本語</a> ·
<a href="../ko/troubleshooting.md" lang="ko" dir="ltr">한국어</a> ·
<a href="troubleshooting.md" lang="nl" dir="ltr">Nederlands</a> ·
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

## Een stekkerdoos met drie aansluitingen levert geen drie vermogensmetingen

`scope_outside` betekent dat een aangevraagd individueel resultaat een bredere meting gebruikt. Houd één entiteit voor de hele stekkerdoos. Voor individueel vermogen hebt u onafhankelijke metingen met het juiste bereik nodig. Een ingeschakeld relais bewijst geen verbruik; elektrisch verbruik van een pomp bewijst geen waterstroming.

<a id="a-migrated-sensor-doubles-the-total"></a>

## Een gemigreerde sensor verdubbelt het totaal

`alias_stream` alleen is informatief. `duplicate_stream` betekent dat beide kopieën in de som staan. Geef kopieën van dezelfde CT dezelfde herkomst en houd slechts één in de som. Verander de herkomst niet alleen om de controle te onderdrukken.

![Eén bron en twee weergaven](../images/duplicate-stream.svg)

<a id="no-numeric-sum-despite-individually-plausible-numbers"></a>

## Geen numerieke som ondanks aannemelijke waarden

Controleer `sample_stale`, `sample_future`, `sample_skew`, `sample_missing`, `incomplete_coverage`, `unit_dimension`, `scope_overlap`. Vernieuw de werkelijke bron en behoud de meettijd. De toegestane leeftijd verhogen verandert het beleid, maar repareert geen meting. Een volledige som wordt tegen opgegeven bladeren beoordeeld: controleer ook de verklaring.

![Synthetische tijdlijn van monsterkwaliteit](../images/sample-quality.svg)

<a id="energy-decreased-at-midnight"></a>

## Energie daalde om middernacht

Een daling kan een echte reset, vervanging of correctie zijn. Geef het beleid op en voeg `reset_at` toe op basis van werkelijke brononderbouwing. Een tijdstip van een HA-herhaling is geen resetmarkering. `total_increasing` past niet bij netto energie met teken. Tellers met verschillende oorsprongen worden niet opgeteld.

<a id="voltage-looks-calibrated-but-watts-still-differ"></a>

## Spanning lijkt gekalibreerd maar watts verschillen

Kalibratie is specifiek voor de grootheid. Een spanningscorrectie valideert geen stroom, faserelatie, vermogen of opgetelde energie. Het factorveld is alleen documentatie: waarden moeten de bedoelde correctie al bevatten.

<a id="yaml-fails-although-another-parser-accepts-it"></a>

## YAML faalt hoewel een andere parser het accepteert

Zet tijdstippen tussen aanhalingstekens, verwijder aliassen/ankers/aangepaste tags en dubbele sleutels, gebruik eindige getallen. Onbekende velden zijn fouten om typefouten op te sporen. De grenzen gelden voor beide formaten. Gebruik JSON voor uitwisseling wanneer dubbelzinnige YAML-scalars problemen veroorzaken.

<a id="ha-import-fails-on-timestamps"></a>

## HA-import faalt op tijdstippen

Stel `timestamp_attribute` in op een echt meettijdattribuut. `last_reported` bewijst alleen ontvangst door HA. Zonder brontijd kan het hulpmiddel de actualiteit niet bepalen; laat het monster onbeschikbaar. Er zijn geen tokens of verbindingen te onderzoeken: import werkt offline.

<a id="safe-issue-report"></a>

## Veilig een probleem melden

Vermeld pakket-/Python-versies, stabiele codes, een minimaal synthetisch contract, gekozen `--at`, verwacht en werkelijk resultaat. Voeg geen volledige HA-export, tokens, echt adres, huishoudschema's of privéapparaat-ID's toe. In de reproductie moeten 0 W en een onbeschikbaar monster onderscheiden blijven.
