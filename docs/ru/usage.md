<a id="usage"></a>

# Использование

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
<a href="usage.md" lang="ru" dir="ltr">Русский</a> ·
<a href="../th/usage.md" lang="th" dir="ltr">ไทย</a> ·
<a href="../tr/usage.md" lang="tr" dir="ltr">Türkçe</a> ·
<a href="../uk/usage.md" lang="uk" dir="ltr">Українська</a> ·
<a href="../vi/usage.md" lang="vi" dir="ltr">Tiếng Việt</a> ·
<a href="../zh-Hans/usage.md" lang="zh-Hans" dir="ltr">简体中文</a> ·
<a href="../zh-Hant/usage.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->
<a id="audit"></a>

## Проверка

```sh
ha-meter-contracts check contract.json --json --lang en
ha-meter-contracts check examples/minimal.yaml --at 2026-01-01T12:00:05Z --lang es
```

`--at` принимает временную метку ISO 8601 с часовым поясом. По умолчанию используется текущее UTC. При одинаковом вводе, времени и языке JSON детерминирован. Отсчёт свежий до границы `freshness_seconds` включительно; устаревает только после неё. Будущий отсчёт недопустим; неявного допуска на расхождение часов нет.

Коды выхода: 0 — нет ошибок/предупреждений; 1 — семантическая проблема или проблема качества отсчёта; 2 — ошибка ввода/CLI. Информация, например неиспользуемый псевдоним, не проваливает проверку. `--json` выводит отчёты и объекты ошибок ввода в stdout. Без него текст отчёта идёт в stdout, ошибки ввода — в stderr. Разрыв выходного канала возвращает 2.

Не используйте `|| true` в CI для сокрытия находок. Намеренно неверные примеры должны явно проверять код 1. Справка и версия возвращают 0. `import-ha` всегда выводит JSON-контракт; `--json` не меняет его схему.

<a id="python-library"></a>

## Библиотека Python

```python
from datetime import datetime, timezone
from ha_meter_contracts import audit, load_document, parse_contract

contract = parse_contract(load_document("examples/valid-three-meters.json"))
report = audit(contract, at=datetime(2026, 1, 1, 12, 0, 5, tzinfo=timezone.utc))
assert report["sums"][0]["value"] == 720
```

`parse_contract` создаёт неизменяемые dataclass; `InputError` предоставляет `code`, `path`, `params`. Применяйте парсер на каждой границе недоверенного ввода. `audit` ожидает проверенный `Contract` и не переводит находки. CLI добавляет локализованные `message`. При использовании библиотеки вызывающая сторона явно выбирает время оценки. Ни один API не меняет ввод и не записывает файлы.

<a id="offline-home-assistant-adapter"></a>

## Офлайн-адаптер Home Assistant

```sh
ha-meter-contracts import-ha examples/ha-contract.json --ha-states examples/ha-states.synthetic.json > /tmp/meter-contract.json
ha-meter-contracts check /tmp/meter-contract.json --at 2026-01-01T12:00:05Z --json
```

Сопоставьте `entity_id` и `timestamp_attribute` у каждого нужного измерителя. Экспорт — массив объектов состояния HA с `entity_id`, `state` и `attributes`. Сопоставленный атрибут должен содержать исходное ISO-время измерения с часовым поясом. `attributes.unit_of_measurement` должен иметь ту же размерность; W/kW и Wh/kWh переводятся в единицу контракта.

Копируются только сопоставленные значения и исходное время. Остальные атрибуты, включая понятные имена, игнорируются. Строго более новый отсчёт переносит существующий в `previous`. Повтор того же значения с той же исходной меткой времени идемпотентен; старый отсчёт или конфликтующее значение с той же меткой отклоняются с `ha_sample_order`. Отсутствующие сущности и состояния `unknown`/`unavailable` очищают отсчёт, а не превращаются в ноль. Отсутствующее исходное время, несовместимая единица, некорректное значение или повторный ID сущности завершают импорт с кодом 2. Несопоставленные измерители неизменны. ID сущностей могут быть в приватном контракте; публичные примеры используют синтетические идентификаторы.

В обычном экспорте HA часто нет исходной метки времени. Тогда адаптер намеренно отказывается её выдумывать. Получите данные устройства с временем или оставьте измеритель недоступным. Время получения/обновления HA не доказывает время измерения устройством. Адаптер не подключается к `/api/states` и не читает токен. Он не копирует метки сброса энергии из HA; перед суммированием энергии отдельно добавьте проверенное свидетельство сброса.

<a id="suggested-workflow"></a>

## Рекомендуемый порядок

1. Объявите дерево физических областей и происхождение источников по документации проводки.
2. Начните с одного измерителя и фиксированного синтетического примера.
3. Экспортируйте только необходимые наблюдения в приватный файл.
4. Проверьте и разберите каждую находку до изменения зависимой автоматизации.
5. При миграции сохраняйте исходное время и свидетельства калибровки.

Пакет не выполняет исправление, переименование сущностей, сброс устройств или развёртывание автоматизации.
