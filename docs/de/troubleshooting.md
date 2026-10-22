<a id="troubleshooting"></a>

# Fehlerbehebung

<!-- language-navigation:start -->
<p dir="ltr">
<a href="../troubleshooting.md" lang="en" dir="ltr">English</a> ·
<a href="../ar/troubleshooting.md" lang="ar" dir="rtl">العربية</a> ·
<a href="../bn/troubleshooting.md" lang="bn" dir="ltr">বাংলা</a> ·
<a href="../cs/troubleshooting.md" lang="cs" dir="ltr">Čeština</a> ·
<a href="troubleshooting.md" lang="de" dir="ltr">Deutsch</a> ·
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

## Eine Dreifachsteckdose liefert nicht drei Leistungsmessungen

`scope_outside` bedeutet, dass ein angefordertes Einzelergebnis eine umfassendere Messung verwendet. Behalten Sie eine Entität für die gesamte Leiste. Für individuelle Leistung brauchen Sie unabhängige, korrekt abgegrenzte Messungen. Ein eingeschaltetes Relais beweist keinen Verbrauch seiner Last; eine elektrisch betriebene Pumpe beweist keinen Wasserfluss.

<a id="a-migrated-sensor-doubles-the-total"></a>

## Ein migrierter Sensor verdoppelt die Summe

`alias_stream` allein ist informativ. `duplicate_stream` bedeutet, dass beide Kopien in einer Summe stehen. Geben Sie Kopien desselben CT dieselbe Herkunft und behalten Sie nur eine in der Summe. Ändern Sie die Herkunft nicht nur zum Unterdrücken der Prüfung.

![Eine Quelle und zwei Darstellungen](../images/duplicate-stream.svg)

<a id="no-numeric-sum-despite-individually-plausible-numbers"></a>

## Keine numerische Summe trotz einzeln plausibler Werte

Prüfen Sie `sample_stale`, `sample_future`, `sample_skew`, `sample_missing`, `incomplete_coverage`, `unit_dimension`, `scope_overlap`. Aktualisieren Sie die ursprüngliche Quelle und bewahren Sie ihre Erfassungszeit. Ein größeres Altersbudget ist eine Richtlinienänderung, keine Messreparatur. Vollständigkeit wird anhand deklarierter Blattbereiche bewertet; prüfen Sie daher auch die Deklaration.

![Synthetischer Zeitverlauf der Messwertqualität](../images/sample-quality.svg)

<a id="energy-decreased-at-midnight"></a>

## Energie ist um Mitternacht gesunken

Ein Rückgang kann ein echter Reset, Austausch oder eine Korrektur sein. Deklarieren Sie die Richtlinie und ergänzen Sie `reset_at` aus tatsächlichen Quellnachweisen. Die Zeit, zu der HA einen Wert erneut abspielte, ist keine Rücksetzmarkierung. `total_increasing` passt nicht zu vorzeichenbehafteter Nettoenergie. Zwei Zähler mit verschiedenen Ursprüngen werden nicht summiert.

<a id="voltage-looks-calibrated-but-watts-still-differ"></a>

## Spannung wirkt kalibriert, Watt unterscheiden sich weiterhin

Kalibrierung gilt je Größe. Eine Spannungskorrektur validiert weder Strom, Phasenbeziehung, Leistung noch akkumulierte Energie. Das Faktorfeld dokumentiert nur: Die Werte müssen die beabsichtigte Korrektur bereits enthalten.

<a id="yaml-fails-although-another-parser-accepts-it"></a>

## YAML scheitert, obwohl ein anderer Parser es akzeptiert

Setzen Sie Zeitstempel in Anführungszeichen, entfernen Sie Aliasse/Anker/eigene Tags und doppelte Schlüssel, und verwenden Sie endliche Zahlen. Unbekannte Felder gelten zur Erkennung von Tippfehlern als Fehler. Die Grenzen gelten für beide Formate. Verwenden Sie JSON zum Austausch, wenn mehrdeutige YAML-Skalare stören.

<a id="ha-import-fails-on-timestamps"></a>

## HA-Import scheitert an Zeitstempeln

Setzen Sie `timestamp_attribute` auf ein echtes Messzeit-Attribut. `last_reported` beweist nur den Empfang durch HA. Ohne Quellzeit kann dieses Werkzeug keine Aktualität feststellen; belassen Sie den Messwert als nicht verfügbar. Token oder Netzwerkverbindung müssen nicht untersucht werden, da der Import offline erfolgt.

<a id="safe-issue-report"></a>

## Sicherer Fehlerbericht

Nennen Sie Paket-/Python-Version, stabile Befundcodes, einen minimalen synthetischen Vertrag, gewähltes `--at`, erwartetes und tatsächliches Ergebnis. Fügen Sie keinen vollständigen HA-Export, Token, echte Adresse, Haushaltszeitplan oder private Gerätekennung bei. 0 W und ein nicht verfügbarer Messwert müssen im Reproduktionsbeispiel unterscheidbar bleiben.
