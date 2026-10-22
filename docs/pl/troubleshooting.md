<a id="troubleshooting"></a>

# Rozwiązywanie problemów

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
<a href="../nl/troubleshooting.md" lang="nl" dir="ltr">Nederlands</a> ·
<a href="troubleshooting.md" lang="pl" dir="ltr">Polski</a> ·
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

## Listwa z trzema gniazdami nie daje trzech odczytów mocy

`scope_outside` oznacza, że żądany wynik indywidualny używa szerszego pomiaru. Zachowaj jedną encję dla całej listwy. Indywidualna moc wymaga niezależnych pomiarów właściwego zakresu. Włączony przekaźnik nie dowodzi poboru odbiornika; pompa pobierająca prąd nie dowodzi przepływu wody.

<a id="a-migrated-sensor-doubles-the-total"></a>

## Przeniesiony czujnik podwaja sumę

Samo `alias_stream` jest informacyjne. `duplicate_stream` oznacza, że obie kopie są w sumie. Kopiom tego samego CT nadaj to samo pochodzenie i zachowaj w sumie tylko jedną. Nie zmieniaj pochodzenia tylko po to, by uciszyć kontrolę.

![Jedno źródło i dwie reprezentacje](../images/duplicate-stream.svg)

<a id="no-numeric-sum-despite-individually-plausible-numbers"></a>

## Brak sumy liczbowej mimo wiarygodnych wartości

Sprawdź `sample_stale`, `sample_future`, `sample_skew`, `sample_missing`, `incomplete_coverage`, `unit_dimension`, `scope_overlap`. Odśwież rzeczywiste źródło i zachowaj czas akwizycji. Zwiększenie dozwolonego wieku zmienia politykę, nie naprawia pomiaru. Pełna suma jest oceniana względem zadeklarowanych liści: sprawdź też deklarację.

![Syntetyczna oś czasu jakości próbek](../images/sample-quality.svg)

<a id="energy-decreased-at-midnight"></a>

## Energia spadła o północy

Spadek może oznaczać prawdziwy reset, wymianę lub korektę. Zadeklaruj politykę i dodaj `reset_at` na podstawie rzeczywistych dowodów źródła. Czas powtórzenia HA nie jest znacznikiem resetu. `total_increasing` nie pasuje do energii netto ze znakiem. Liczniki o różnych początkach nie są sumowane.

<a id="voltage-looks-calibrated-but-watts-still-differ"></a>

## Napięcie wygląda na skalibrowane, ale waty się różnią

Kalibracja dotyczy konkretnej wielkości. Korekta napięcia nie potwierdza prądu, zależności fazowej, mocy ani zgromadzonej energii. Pole współczynnika jest tylko dokumentacją: wartości muszą już zawierać zamierzoną korektę.

<a id="yaml-fails-although-another-parser-accepts-it"></a>

## YAML nie działa, choć inny parser go przyjmuje

Ujmij czasy w cudzysłowy, usuń aliasy/kotwice/własne tagi i powielone klucze, użyj skończonych liczb. Nieznane pola są błędami, aby wykrywać literówki. Limity dotyczą obu formatów. Użyj JSON do wymiany, jeśli niejednoznaczne skalary YAML sprawiają problem.

<a id="ha-import-fails-on-timestamps"></a>

## Import HA odrzuca czasy

Ustaw `timestamp_attribute` na rzeczywisty atrybut czasu pomiaru. `last_reported` dowodzi tylko odbioru przez HA. Bez czasu źródła narzędzie nie może ustalić świeżości; pozostaw próbkę niedostępną. Nie ma tokenów ani połączeń do diagnozowania: import działa offline.

<a id="safe-issue-report"></a>

## Bezpieczne zgłoszenie problemu

Podaj wersje pakietu/Pythona, stałe kody, minimalny syntetyczny kontrakt, wybrane `--at`, wynik oczekiwany i rzeczywisty. Nie dołączaj pełnego eksportu HA, tokenów, prawdziwego adresu, harmonogramów domowych ani prywatnych ID urządzeń. W reprodukcji 0 W i niedostępna próbka muszą pozostać rozróżnione.
