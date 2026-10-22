<a id="contract-schema-v1"></a>

# Schemat kontraktu v1

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
<a href="../it/schema.md" lang="it" dir="ltr">Italiano</a> ·
<a href="../ja/schema.md" lang="ja" dir="ltr">日本語</a> ·
<a href="../ko/schema.md" lang="ko" dir="ltr">한국어</a> ·
<a href="../nl/schema.md" lang="nl" dir="ltr">Nederlands</a> ·
<a href="schema.md" lang="pl" dir="ltr">Polski</a> ·
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
Czytelny maszynowo [schema.json](../../schema.json) opisuje strukturę. Parser Pythona rozstrzyga o limitach; `audit` dodaje semantykę fizyczną i czasową, której JSON Schema nie może dowieść. Plik strukturalny generuj przez `python3 scripts/generate_schema.py`.

<a id="root-and-limits"></a>

## Korzeń i limity

Wymagane: liczba całkowita `schema_version: 1`, `scopes`, `meters`. Opcjonalne: `sums` (domyślnie puste). Nieznane pola są odrzucane na każdym poziomie. Maksymalnie 512 zakresów, 512 mierników i 128 sum; zakresy i mierniki nie mogą być puste. Każda suma ma 1–512 składników. Wejście UTF-8, maksymalnie 1 048 576 bajtów, głębokość 16 i 20 000 węzłów wartości. Duplikaty kluczy JSON, NaN/Infinity oraz aliasy/kotwice/jawne tagi YAML są odrzucane. Czasy YAML ujmuj w cudzysłowy, aby pozostały ciągami.

Identyfikatory mają 1–96 znaków ASCII: najpierw litera/cyfra, potem litery, cyfry, `.`, `_`, `-`. ID są unikatowe w każdej kolekcji; zakresy i mierniki mają odrębne przestrzenie nazw. Wszystkie czasy zawierają `T` i strefę czasową. Liczby są skończone, nie są wartościami logicznymi i mieszczą się w ±10^15, o ile nie ma ciaśniejszego limitu.

<a id="physical-scopes"></a>

## Zakresy fizyczne

Każdy zakres ma `id`, `kind` (`site`, `circuit`, `strip`, `outlet`, `load`) i opcjonalne `parent`. Rodzice muszą istnieć i tworzyć acykliczny las. Miernik na rodzicu obejmuje wszystkich potomków. Typy zakresów są opisowe: nie wyznaczają napięcia, faz, wartości znamionowych, okablowania ani dozwolonych rodziców. Prawdziwą topologię deklaruje użytkownik.

<a id="meters"></a>

## Mierniki

Pola wymagane:

- `id`, `scope`: unikatowy identyfikator odczytu i zadeklarowany zakres fizyczny.
- `quantity`: `power`, `energy`, `voltage`, `current`.
- `unit`: odpowiednio W/kW, Wh/kWh, V, A. Parser przyjmuje słownik; audytor sprawdza wymiar.
- `kind`: `measured` lub `estimated`. To deklaracja, nie weryfikacja laboratoryjna.
- `provenance`: stała tożsamość fizycznego strumienia pomiarów, **nie** jego reprezentacji HA/MQTT. Odczyty będące aliasami ją współdzielą. Różne znaki/wielkości/zakresy dla jednego pochodzenia tworzą konflikt; wszystkie aliasy strumienia stają się niedostępne dla sum niezależnie od kolejności wejścia. Dla rzeczywiście różnych kanałów fizycznych wybieraj różne pochodzenie.
- `sign`: `nonnegative` dla wartości wyłącznie poboru/importu/eksportu; `signed` dla zadeklarowanego przepływu dwukierunkowego. Ta wersja nie wnioskuje, który kierunek fizyczny jest dodatni.
- `state_class`: `measurement`, `total`, `total_increasing`.
- `freshness_seconds`: dodatni maksymalny wiek, 0.001–604800 sekund.

Opcjonalne `reset`: `never`, `periodic`, `device_restart`, `unknown`, `not_applicable` (domyślnie). Energia wymaga jawnej polityki innej niż `not_applicable` i klasy stanu typu total. Energia ze znakiem nie może używać `total_increasing`. Pozostałe wielkości wymagają `measurement` i `not_applicable`.

Opcjonalne `sample`, `previous`: null lub obiekt z `value` (liczba lub null), `measured_at`, opcjonalnie `reset_at`. Poprzednia próbka musi być starsza. Spadek licznika nieujemnego wymaga znacznika resetu pomiędzy próbkami; `never` go odrzuca. `reset_at` nie może być późniejsze niż jego próbka i dotyczy tylko energii. Nieznana semantyka resetu daje ostrzeżenie. Licznik netto ze znakiem może prawidłowo maleć; właściwa podstawa pozostaje odpowiedzialnością producenta.

Opcjonalne `calibration`: `quantity`, dodatnie `factor` (10^-12–10^12), syntetyczny/prywatny identyfikator `reference`, `verified_at`. Rejestruje dowód dla dokładnie tej wielkości. Wartości są **już skalibrowane**: walidator nigdy nie stosuje współczynnika ponownie. Kalibracja z przyszłości lub kalibracja napięcia dla miernika mocy jest nieprawidłowa. Brak kalibracji nie dowodzi dokładności i nie jest automatycznie błędem.

Opcjonalne `entity_id`, `timestamp_attribute`: mapowanie offline HA; patrz [użycie](usage.md#offline-home-assistant-adapter).

<a id="sums"></a>

## Sumy

Wymagane: `id`, docelowe `scope`, lista ID mierników w `meters`, `quantity` (`power` lub `energy`), `coverage` (`partial` lub `complete`). Opcjonalne `max_skew_seconds`: 0–604800, domyślnie 2.

Składniki muszą należeć do docelowego zakresu, mieć zgodne wymiary i semantykę znaku, używać różnych strumieni fizycznych oraz nie nakładać się jako rodzic/dziecko albo identyczne zakresy. Pełna suma obejmuje każdy **zadeklarowany zakres liściowy** pod celem. Niezadeklarowanego okablowania nie można wykryć. Suma częściowa jawnie deklaruje częściowe pokrycie. Zagnieżdżone sumy nie są obsługiwane; składniki zawsze wskazują mierniki.

Każdy składnik musi mieć poprawne, świeże dane; czasy akwizycji muszą mieścić się w dozwolonym odchyleniu. Energia wymaga również identycznych jawnych początków `reset_at`. Sprawdzana jest deklarowana zgodność, nie dokładność historycznej akumulacji. Sumy są przeliczane na W lub Wh. Sumy prądu i napięcia celowo nie są obsługiwane, ponieważ zależą od topologii obwodu.

Suma liczbowa jest niedostępna, gdy brak wymaganych dowodów lub nie przejdzie kontrola semantyczna. Oszacowania propagują się jako `kind: estimated`. Dwa aliasy mogą współistnieć w inwentarzu, lecz nie mogą oba wejść do sumy. Nie wyznacza się żadnej sumy dla indywidualnych niemierzonych gniazd.

<a id="report-v1"></a>

## Raport v1

Korzeń: `schema_version`, czas oceny `at` znormalizowany do UTC, liczności według wagi w `summary`, uporządkowane `findings` i `sums`. Każde ustalenie zawiera `code`, `severity`, `path` w stylu JSON, strukturalne `params`; CLI dodaje `message`. Każda suma zawiera `id`, `scope`, `quantity`, bazowe `unit`, `value`, `status`, `kind`, `coverage`. Nieznane wartości to JSON null, nigdy NaN.
