<a id="limits-and-trust-boundary"></a>

# Grenzen und Vertrauensgrenze

<!-- language-navigation:start -->
<p dir="ltr">
<a href="../limits.md" lang="en" dir="ltr">English</a> ·
<a href="../ar/limits.md" lang="ar" dir="rtl">العربية</a> ·
<a href="../bn/limits.md" lang="bn" dir="ltr">বাংলা</a> ·
<a href="../cs/limits.md" lang="cs" dir="ltr">Čeština</a> ·
<a href="limits.md" lang="de" dir="ltr">Deutsch</a> ·
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
Dies ist ein Offline-Prüfer für deklarierte Daten, keine Schutzsteuerung, kein elektrisches Prüfgerät, keine automatische Erkennung der Verkabelung und keine Home-Assistant-Integration, die Aktionen ausführt.

- Aus einem Gesamtmesswert lässt sich nicht die genaue gleichzeitige Leistung dreier unbekannter Lasten rekonstruieren. Statistische Vermutungen wären Schätzungen, keine für Schutzfunktionen geeigneten Messungen.
- Bereiche, Herkunft, Vorzeichenrichtung und Kalibrierungsangaben stammen vom Betreiber. Falsche Angaben können ein physikalisch ungültiges System strukturell gültig erscheinen lassen.
- `complete` bedeutet vollständig gegenüber den deklarierten Blättern, nicht gegenüber unabhängig geprüfter Verkabelung. Eine Rücksetzmarkierung der Quelle ist ein vertrauter Nachweis, keine Geräteattestierung.
- Unterstützt werden W, kW, Wh, kWh, V und A. Nicht modelliert werden Blind-/Scheinleistung, Dreiphasenrechnung, CT-Sättigung, Spannungswandler, Zählerüberläufe oder Tarife.
- Summenmitglieder sind direkte Messgeräte, keine anderen Summen. Leistungssummen benötigen zeitlich abgestimmte Werte. Energiesummen benötigen einen gemeinsamen expliziten Zählerursprung und abgestimmte Messwerte.
- Werte sind endliche Gleitkommazahlen. Dies ist kein abrechnungsgeeignetes dezimales Buchhaltungssystem. Kalibrierungsfaktoren werden dokumentiert, nicht angewendet.
- Geprüft werden nur ein aktueller und optional ein vorheriger Messwert. Dies ist keine Verlaufsdatenbank, Anomalie- oder Drift-Erkennung und kein vollständiges Integritätsaudit eines Zählers.
- HA-Quellzeitstempel müssen vorhanden sein und tatsächlich die Erfassung repräsentieren. Empfangszeitstempel eines Caches werden nicht stillschweigend als Ersatz akzeptiert.
- Das Laden von JSON/YAML ist begrenzt; die Bibliotheks-API `audit` erwartet einen vom Parser erzeugten `Contract`. Erstellen Sie keine beliebigen fehlerhaften Dataclasses aus nicht vertrauenswürdigen Objekten.
- Dateieingaben akzeptieren nur reguläre Dateien. Symlinks in der letzten Pfadkomponente, FIFOs, Geräte und Verzeichnisse werden abgelehnt; das Öffnen erfolgt nicht blockierend, und vor dem Lesen wird der geöffnete Deskriptor geprüft. Plattformen ohne `O_NOFOLLOW` und `O_NONBLOCK` lehnen Dateieingaben ab; verwenden Sie dort `ha_meter_contracts.reader.loads_document` mit einer bereits größenbegrenzten Zeichenfolge. Symlinks in übergeordneten Verzeichnissen sind keine Sandbox-Grenze. Die Bytegrenze gilt auch, wenn eine Datei während des Lesens wächst.
- Ein bestandener Test beweist weder die physische Funktion eines Relais, Ventils oder Motors noch Pumpendurchfluss oder elektrische Sicherheit. Es erfolgen keine automatischen Reparaturen oder Wiederholungen.

Ein- und Ausgaben können vom Betreiber angegebene Entitäts-IDs und Zeiten enthalten. Halten Sie echte Verträge/Exporte privat. Das Repository enthält nur synthetische Beispiele. Das Programm lädt keine Daten hoch; die Weiterleitung seines Berichts an einen externen Dienst entscheidet der Betreiber.
