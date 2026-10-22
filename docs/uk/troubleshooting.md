<a id="troubleshooting"></a>

# Усунення несправностей

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
<a href="../pl/troubleshooting.md" lang="pl" dir="ltr">Polski</a> ·
<a href="../pt/troubleshooting.md" lang="pt" dir="ltr">Português</a> ·
<a href="../ru/troubleshooting.md" lang="ru" dir="ltr">Русский</a> ·
<a href="../th/troubleshooting.md" lang="th" dir="ltr">ไทย</a> ·
<a href="../tr/troubleshooting.md" lang="tr" dir="ltr">Türkçe</a> ·
<a href="troubleshooting.md" lang="uk" dir="ltr">Українська</a> ·
<a href="../vi/troubleshooting.md" lang="vi" dir="ltr">Tiếng Việt</a> ·
<a href="../zh-Hans/troubleshooting.md" lang="zh-Hans" dir="ltr">简体中文</a> ·
<a href="../zh-Hant/troubleshooting.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->
<a id="a-three-outlet-strip-cannot-produce-three-power-readings"></a>

## Подовжувач із трьома розетками не дає трьох показників потужності

`scope_outside` означає, що запитаний індивідуальний результат використовує ширше вимірювання. Залиште одну сутність для всього подовжувача. Для індивідуальної потужності потрібні незалежні вимірювання належної області. Увімкнене реле не доводить споживання навантаження; споживання електрики насосом не доводить потоку води.

<a id="a-migrated-sensor-doubles-the-total"></a>

## Перенесений датчик подвоює підсумок

Саме `alias_stream` інформаційне. `duplicate_stream` означає, що обидві копії входять до суми. Дайте копіям одного CT однакове походження й залиште в сумі лише одну. Не змінюйте походження лише заради вимкнення перевірки.

![Одне джерело та два представлення](../images/duplicate-stream.svg)

<a id="no-numeric-sum-despite-individually-plausible-numbers"></a>

## Немає числової суми попри правдоподібні значення

Перевірте `sample_stale`, `sample_future`, `sample_skew`, `sample_missing`, `incomplete_coverage`, `unit_dimension`, `scope_overlap`. Оновіть справжнє джерело й збережіть час вимірювання. Збільшення дозволеного віку змінює політику, а не виправляє вимірювання. Повна сума оцінюється щодо задекларованих листків: перевірте й декларацію.

![Синтетична часова шкала якості відліків](../images/sample-quality.svg)

<a id="energy-decreased-at-midnight"></a>

## Енергія зменшилася опівночі

Зменшення може бути справжнім скиданням, заміною або корекцією. Задекларуйте політику й додайте `reset_at` зі справжніх свідчень джерела. Час повторного відтворення HA — не позначка скидання. `total_increasing` не підходить для чистої енергії зі знаком. Лічильники з різними початками не додаються.

<a id="voltage-looks-calibrated-but-watts-still-differ"></a>

## Напруга здається відкаліброваною, але вати відрізняються

Калібрування специфічне для величини. Корекція напруги не підтверджує струм, фазовий зв’язок, потужність чи накопичену енергію. Поле коефіцієнта лише документальне: значення вже повинні містити бажану корекцію.

<a id="yaml-fails-although-another-parser-accepts-it"></a>

## YAML не проходить, хоча інший парсер його приймає

Беріть час у лапки, видаліть псевдоніми/якорі/власні теги та повторні ключі, використовуйте скінченні числа. Невідомі поля є помилками для виявлення друкарських похибок. Обмеження діють для обох форматів. Використовуйте JSON для обміну, якщо неоднозначні скаляри YAML спричиняють проблеми.

<a id="ha-import-fails-on-timestamps"></a>

## Імпорт HA не проходить через часові позначки

Встановіть `timestamp_attribute` на справжній атрибут часу вимірювання. `last_reported` доводить лише отримання HA. Без часу джерела інструмент не може визначити свіжість; залиште відлік недоступним. Тут немає токенів чи підключень для діагностики: імпорт автономний.

<a id="safe-issue-report"></a>

## Безпечне повідомлення про проблему

Додайте версії пакета/Python, стабільні коди, мінімальний синтетичний контракт, вибраний `--at`, очікуваний і фактичний результат. Не додавайте повного експорту HA, токенів, справжньої адреси, домашніх розкладів чи приватних ID пристроїв. У відтворенні 0 W і недоступний відлік мають залишатися різними.
