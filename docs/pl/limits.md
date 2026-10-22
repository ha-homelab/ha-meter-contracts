<a id="limits-and-trust-boundary"></a>

# Ograniczenia i granica zaufania

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
<a href="../nl/limits.md" lang="nl" dir="ltr">Nederlands</a> ·
<a href="limits.md" lang="pl" dir="ltr">Polski</a> ·
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
To działający offline walidator deklaracji, a nie sterownik zabezpieczeń, przyrząd pomiarowy elektryka, usługa wykrywania okablowania ani integracja Home Assistant wykonująca działania.

- Jeden odczyt całkowity nie pozwala odtworzyć dokładnej jednoczesnej mocy trzech nieznanych odbiorników. Statystyczne przypuszczenia byłyby oszacowaniami, a nie pomiarami odpowiednimi dla zabezpieczeń.
- Zakres, pochodzenie, kierunek znaku oraz deklaracje kalibracji podaje operator. Fałszywe deklaracje mogą sprawić, że nieprawidłowy układ fizyczny będzie wyglądać na poprawny strukturalnie.
- `complete` oznacza kompletność względem zadeklarowanych liści, nie niezależnie sprawdzonego okablowania. Znacznik resetu źródła to dowód przyjmowany na zaufanie, a nie atestacja urządzenia.
- Obsługiwane są W, kW, Wh, kWh, V i A. Nie modelujemy mocy biernej/pozornej, algebry trójfazowej, nasycenia CT, przekładników napięciowych, przepełnienia licznika ani taryf.
- Składnikami sum są bezpośrednio mierniki, nie inne sumy. Sumy mocy wymagają zgodnych czasów. Sumy energii wymagają jawnego wspólnego początku liczników i zgodnych czasowo próbek.
- Wartości są skończonymi liczbami zmiennoprzecinkowymi. To nie jest dziesiętna księgowość do rozliczeń. Współczynniki kalibracji są zapisywane, nie stosowane.
- Sprawdzana jest tylko bieżąca próbka i opcjonalnie poprzednia. To nie baza historii, detektor anomalii lub dryfu ani pełny audyt integralności liczników.
- Czasy źródłowe HA muszą istnieć i rzeczywiście oznaczać akwizycję pomiaru. Czasy odbioru przez pamięć podręczną nie są po cichu akceptowane jako zamienniki.
- Wczytywanie JSON/YAML ma limity; API biblioteki `audit` oczekuje `Contract` utworzonego przez parser. Nie buduj dowolnych niepoprawnych klas danych z niezaufanych obiektów.
- Wejście plikowe przyjmuje tylko zwykłe pliki. Odrzuca dowiązania symboliczne w ostatnim elemencie ścieżki, FIFO, urządzenia i katalogi, otwiera bez blokowania i sprawdza otwarty deskryptor przed odczytem. Platformy bez `O_NOFOLLOW` i `O_NONBLOCK` odrzucają pliki; użyj tam `ha_meter_contracts.reader.loads_document` z już ograniczonym ciągiem. Dowiązania w katalogach nadrzędnych nie stanowią granicy piaskownicy. Limit bajtów obowiązuje także, gdy plik rośnie podczas odczytu.
- Wynik pozytywny nie dowodzi fizycznego działania przekaźnika, zaworu, silnika, przepływu pompy ani bezpieczeństwa elektrycznego. Nie są wykonywane automatyczne naprawy ani ponowienia.

Wejście i wyjście mogą zawierać identyfikatory encji i czasy podane przez operatora. Prawdziwe kontrakty/eksporty przechowuj prywatnie. Repozytorium zawiera wyłącznie przykłady syntetyczne. Program niczego nie wysyła, lecz przekierowanie raportu do zewnętrznej usługi jest decyzją operatora.
