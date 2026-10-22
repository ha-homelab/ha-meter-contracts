<a id="usage"></a>

# Użycie

<!-- language-navigation:start -->
<p dir="ltr">
<a href="../usage.md" lang="en" dir="ltr">English</a> ·
<a href="../ar/usage.md" lang="ar" dir="rtl">العربية</a> ·
<a href="../bn/usage.md" lang="bn" dir="ltr">বাংলা</a> ·
<a href="../cs/usage.md" lang="cs" dir="ltr">Čeština</a> ·
<a href="../de/usage.md" lang="de" dir="ltr">Deutsch</a> ·
<a href="../es/usage.md" lang="es" dir="ltr">Español</a> ·
<a href="../fa/usage.md" lang="fa" dir="rtl">فارسی</a> ·
<a href="../fr/usage.md" lang="fr" dir="ltr">Français</a> ·
<a href="../he/usage.md" lang="he" dir="rtl">עברית</a> ·
<a href="../hi/usage.md" lang="hi" dir="ltr">हिन्दी</a> ·
<a href="../id/usage.md" lang="id" dir="ltr">Bahasa Indonesia</a> ·
<a href="../it/usage.md" lang="it" dir="ltr">Italiano</a> ·
<a href="../ja/usage.md" lang="ja" dir="ltr">日本語</a> ·
<a href="../ko/usage.md" lang="ko" dir="ltr">한국어</a> ·
<a href="../nl/usage.md" lang="nl" dir="ltr">Nederlands</a> ·
<a href="usage.md" lang="pl" dir="ltr">Polski</a> ·
<a href="../pt/usage.md" lang="pt" dir="ltr">Português</a> ·
<a href="../ru/usage.md" lang="ru" dir="ltr">Русский</a> ·
<a href="../th/usage.md" lang="th" dir="ltr">ไทย</a> ·
<a href="../tr/usage.md" lang="tr" dir="ltr">Türkçe</a> ·
<a href="../uk/usage.md" lang="uk" dir="ltr">Українська</a> ·
<a href="../vi/usage.md" lang="vi" dir="ltr">Tiếng Việt</a> ·
<a href="../zh-Hans/usage.md" lang="zh-Hans" dir="ltr">简体中文</a> ·
<a href="../zh-Hant/usage.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->
<a id="audit"></a>

## Audyt

```sh
ha-meter-contracts check contract.json --json --lang en
ha-meter-contracts check examples/minimal.yaml --at 2026-01-01T12:00:05Z --lang es
```

`--at` przyjmuje czas ISO 8601 ze strefą czasową. Domyślny jest bieżący UTC. Przy tym samym wejściu, czasie i języku JSON jest deterministyczny. Próbka pozostaje świeża do granicy `freshness_seconds` włącznie; jest nieaktualna dopiero po niej. Próbka z przyszłości jest nieprawidłowa, bez domyślnej tolerancji przesunięcia zegara.

Kody wyjścia: 0 = brak błędów/ostrzeżeń; 1 = problem semantyczny lub jakości próbki; 2 = błąd wejścia/CLI. Informacje, takie jak nieużywany alias, nie powodują niepowodzenia. `--json` zapisuje raporty i obiekty błędów wejścia na stdout. Bez tej opcji tekst audytu trafia na stdout, a błędy wejścia na stderr. Przerwany potok wyjściowy zwraca 2.

Nie używaj `|| true` w CI do ukrywania ustaleń. Celowo nieprawidłowe przykłady powinny jawnie sprawdzać kod 1. Pomoc i wersja zwracają 0. `import-ha` zawsze zapisuje kontrakt JSON; `--json` nie zmienia jego schematu.

<a id="python-library"></a>

## Biblioteka Pythona

```python
from datetime import datetime, timezone
from ha_meter_contracts import audit, load_document, parse_contract

contract = parse_contract(load_document("examples/valid-three-meters.json"))
report = audit(contract, at=datetime(2026, 1, 1, 12, 0, 5, tzinfo=timezone.utc))
assert report["sums"][0]["value"] == 720
```

`parse_contract` tworzy niemodyfikowalne klasy danych; `InputError` udostępnia `code`, `path`, `params`. Używaj parsera na każdej granicy niezaufanego wejścia. `audit` oczekuje zwalidowanego `Contract` i nie tłumaczy ustaleń. CLI dodaje przetłumaczone wartości `message`. W bibliotece wywołujący jawnie wybiera czas oceny. Żadne API nie modyfikuje wejścia ani nie zapisuje plików.

<a id="offline-home-assistant-adapter"></a>

## Adapter offline Home Assistant

```sh
ha-meter-contracts import-ha examples/ha-contract.json --ha-states examples/ha-states.synthetic.json > /tmp/meter-contract.json
ha-meter-contracts check /tmp/meter-contract.json --at 2026-01-01T12:00:05Z --json
```

Zmapuj `entity_id` i `timestamp_attribute` na każdym potrzebnym mierniku. Eksport jest tablicą stanów HA z `entity_id`, `state` i `attributes`. Mapowany atrybut musi zawierać oryginalny czas pomiaru ISO ze strefą. `attributes.unit_of_measurement` musi mieć ten sam wymiar; W/kW i Wh/kWh są przeliczane na jednostkę kontraktu.

Kopiowane są tylko mapowane wartości i czasy źródła. Inne atrybuty, w tym przyjazne nazwy, są ignorowane. Ściśle nowsza próbka przenosi istniejącą do `previous`. Powtórzenie tej samej wartości z tym samym czasem źródłowym jest idempotentne; starsza próbka lub sprzeczna wartość w tym samym czasie jest odrzucana jako `ha_sample_order`. Brak encji oraz stany `unknown`/`unavailable` usuwają próbkę; nie zmieniają jej w zero. Brak czasu, niezgodna jednostka, nieprawidłowa wartość lub powielony ID encji kończą import kodem 2. Niemapowane mierniki pozostają bez zmian. Prywatne kontrakty mogą zawierać ID encji; publiczne przykłady używają syntetycznych identyfikatorów.

Zwykły eksport HA często nie zawiera oryginalnego czasu. Adapter celowo odmawia wówczas jego wymyślenia. Uzyskaj dane urządzenia z czasem lub pozostaw miernik niedostępny. Czasy odbioru/aktualizacji HA nie dowodzą akwizycji urządzenia. Adapter nigdy nie łączy się z `/api/states` ani nie czyta tokenów. Nie kopiuje znaczników resetu energii z HA; dodaj oddzielnie zweryfikowane dowody przed sumowaniem energii.

<a id="suggested-workflow"></a>

## Zalecany przebieg pracy

1. Zadeklaruj drzewo fizycznych zakresów i pochodzenie źródeł na podstawie dokumentacji okablowania.
2. Zacznij od jednego miernika i stałego syntetycznego przykładu.
3. Wyeksportuj tylko potrzebne obserwacje do prywatnego pliku.
4. Uruchom audyt i sprawdź każde ustalenie przed zmianą automatyzacji korzystającej z danych.
5. Zachowaj oryginalne czasy i dowody kalibracji podczas migracji.

Pakiet nie wykonuje napraw, nie zmienia nazw encji, nie resetuje urządzeń ani nie wdraża automatyzacji.
