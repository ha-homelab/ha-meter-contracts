<a id="usage"></a>

# Використання

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
<a href="../pl/usage.md" lang="pl" dir="ltr">Polski</a> ·
<a href="../pt/usage.md" lang="pt" dir="ltr">Português</a> ·
<a href="../ru/usage.md" lang="ru" dir="ltr">Русский</a> ·
<a href="../th/usage.md" lang="th" dir="ltr">ไทย</a> ·
<a href="../tr/usage.md" lang="tr" dir="ltr">Türkçe</a> ·
<a href="usage.md" lang="uk" dir="ltr">Українська</a> ·
<a href="../vi/usage.md" lang="vi" dir="ltr">Tiếng Việt</a> ·
<a href="../zh-Hans/usage.md" lang="zh-Hans" dir="ltr">简体中文</a> ·
<a href="../zh-Hant/usage.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->
<a id="audit"></a>

## Аудит

```sh
ha-meter-contracts check contract.json --json --lang en
ha-meter-contracts check examples/minimal.yaml --at 2026-01-01T12:00:05Z --lang es
```

`--at` приймає час ISO 8601 із часовим поясом. Типове значення — поточний UTC. За однакових введення, часу та мови JSON детермінований. Відлік залишається свіжим до межі `freshness_seconds` включно; застаріває лише після неї. Відлік із майбутнього некоректний, без неявного допуску розбіжності годинників.

Коди завершення: 0 = немає помилок/попереджень; 1 = семантична проблема або проблема якості відліку; 2 = помилка введення/CLI. Інформаційні знахідки, як-от невикористаний псевдонім, не спричиняють неуспіху. `--json` записує звіти й об’єкти помилок введення до stdout. Без цієї опції текст аудиту йде до stdout, а помилки введення — до stderr. Розірваний канал виведення повертає 2.

Не використовуйте `|| true` у CI для приховування знахідок. Навмисно некоректні приклади мають явно перевіряти код 1. Довідка й версія повертають 0. `import-ha` завжди записує контракт JSON; `--json` не змінює його схему.

<a id="python-library"></a>

## Бібліотека Python

```python
from datetime import datetime, timezone
from ha_meter_contracts import audit, load_document, parse_contract

contract = parse_contract(load_document("examples/valid-three-meters.json"))
report = audit(contract, at=datetime(2026, 1, 1, 12, 0, 5, tzinfo=timezone.utc))
assert report["sums"][0]["value"] == 720
```

`parse_contract` створює незмінні класи даних; `InputError` надає `code`, `path`, `params`. Використовуйте парсер на кожній межі недовіреного введення. `audit` очікує перевірений `Contract` і не перекладає знахідок. CLI додає локалізовані значення `message`. У бібліотеці викликач явно вибирає час оцінювання. Жоден API не змінює введення й не записує файлів.

<a id="offline-home-assistant-adapter"></a>

## Автономний адаптер Home Assistant

```sh
ha-meter-contracts import-ha examples/ha-contract.json --ha-states examples/ha-states.synthetic.json > /tmp/meter-contract.json
ha-meter-contracts check /tmp/meter-contract.json --at 2026-01-01T12:00:05Z --json
```

Зіставте `entity_id` та `timestamp_attribute` на кожному потрібному вимірювачі. Експорт — масив станів HA з `entity_id`, `state` та `attributes`. Зіставлений атрибут має містити початковий час вимірювання ISO з часовим поясом. `attributes.unit_of_measurement` має мати ту саму розмірність; W/kW та Wh/kWh перетворюються на одиницю контракту.

Копіюються лише зіставлені значення та час джерела. Інші атрибути, зокрема зручні назви, ігноруються. Строго новіший відлік переміщує наявний до `previous`. Повторення того самого значення з тим самим часом джерела ідемпотентне; старіший відлік чи суперечливе значення в той самий час відхиляється як `ha_sample_order`. Відсутні сутності й стани `unknown`/`unavailable` очищають відлік; вони не стають нулем. Відсутній час, несумісна одиниця, некоректне значення чи повторний ID сутності завершують імпорт кодом 2. Незіставлені вимірювачі не змінюються. Приватні контракти можуть містити ID сутностей; публічні приклади використовують синтетичні ідентифікатори.

Звичайний експорт HA часто не містить початкового часу. У такому разі адаптер навмисно відмовляється його вигадувати. Отримайте дані пристрою з часовими позначками або залиште вимірювач недоступним. Час отримання/оновлення HA не доводить отримання вимірювання пристроєм. Адаптер ніколи не під’єднується до `/api/states` і не читає токенів. Він не копіює позначок скидання енергії з HA; перед додаванням енергії окремо додайте перевірені свідчення.

<a id="suggested-workflow"></a>

## Рекомендований порядок роботи

1. Задекларуйте дерево фізичних областей і походження джерел за документацією проводки.
2. Почніть з одного вимірювача та фіксованого синтетичного прикладу.
3. Експортуйте лише потрібні спостереження до приватного файлу.
4. Запустіть аудит і перевірте кожну знахідку до зміни залежної автоматизації.
5. Зберігайте початкові часові позначки й свідчення калібрування під час міграцій.

Пакет не виконує виправлень, не перейменовує сутностей, не скидає пристроїв і не розгортає автоматизацій.
