<a id="limits-and-trust-boundary"></a>

# Beperkingen en vertrouwensgrens

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
<a href="../it/limits.md" lang="it" dir="ltr">Italiano</a> ·
<a href="../ja/limits.md" lang="ja" dir="ltr">日本語</a> ·
<a href="../ko/limits.md" lang="ko" dir="ltr">한국어</a> ·
<a href="limits.md" lang="nl" dir="ltr">Nederlands</a> ·
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
Dit is een offline validator van verklaringen, geen beveiligingsregelaar, testinstrument voor elektriciens, dienst die bedrading ontdekt of Home Assistant-integratie die acties uitvoert.

- Uit één totale meting kan de exacte gelijktijdige belasting van drie onbekende verbruikers niet worden afgeleid. Statistische gissingen zouden schattingen zijn, geen metingen die voor beveiliging geschikt zijn.
- Bereik, herkomst, tekenrichting en kalibratieverklaringen komen van de beheerder. Onjuiste verklaringen kunnen een fysiek ongeldig systeem structureel geldig laten lijken.
- `complete` betekent volledig ten opzichte van de opgegeven bladeren, niet ten opzichte van onafhankelijk gecontroleerde bedrading. Een resetmarkering van de bron is vertrouwde onderbouwing, geen apparaatattestatie.
- W, kW, Wh, kWh, V en A worden ondersteund. We modelleren geen blind-/schijnvermogen, driefasenalgebra, CT-verzadiging, spanningstransformatoren, telleroverloop of tarieven.
- Leden van een som zijn rechtstreekse meters, geen andere sommen. Vermogenssommen vereisen uitgelijnde tijdstippen. Energiesommen vereisen een expliciete gemeenschappelijke telleroorsprong en uitgelijnde monsters.
- Waarden zijn eindige drijvendekommagetallen. Dit is geen decimale boekhouding voor facturatie. Kalibratiefactoren worden geregistreerd, niet toegepast.
- Alleen één huidig en eventueel één vorig monster worden gecontroleerd. Dit is geen historische database, anomalie- of driftdetector of volledige integriteitsaudit van tellers.
- HA-brontijdstippen moeten bestaan en daadwerkelijk het meetmoment aangeven. Ontvangsttijden van de cache worden niet stilzwijgend als vervanging geaccepteerd.
- JSON/YAML-invoer is begrensd; de bibliotheek-API `audit` verwacht een door de parser gemaakte `Contract`. Bouw geen willekeurige misvormde dataclasses uit niet-vertrouwde objecten.
- Bestandsinvoer accepteert alleen gewone bestanden. Symbolische links in het laatste padonderdeel, FIFO's, apparaten en mappen worden geweigerd; het bestand wordt niet-blokkerend geopend en de geopende descriptor wordt vóór het lezen gecontroleerd. Platforms zonder `O_NOFOLLOW` en `O_NONBLOCK` weigeren bestanden; gebruik daar `ha_meter_contracts.reader.loads_document` met een al begrensde tekenreeks. Symbolische links in bovenliggende mappen vormen geen sandboxgrens. De bytegrens geldt ook wanneer het bestand tijdens het lezen groeit.
- Een geslaagde controle bewijst geen fysieke werking van relais, kleppen, motoren, pompdebiet of elektrische veiligheid. Er worden geen automatische reparaties of herhaalde pogingen uitgevoerd.

Invoer en uitvoer kunnen door de beheerder verstrekte entiteits-ID's en tijden bevatten. Houd echte contracten/exports privé. De repository bevat alleen synthetische voorbeelden. Het programma uploadt niets, maar een rapport naar een externe dienst doorsturen is een keuze van de beheerder.
