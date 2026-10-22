<a id="usage"></a>

# שימוש

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
<a href="usage.md" lang="he" dir="rtl">עברית</a> ·
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
<a href="../uk/usage.md" lang="uk" dir="ltr">Українська</a> ·
<a href="../vi/usage.md" lang="vi" dir="ltr">Tiếng Việt</a> ·
<a href="../zh-Hans/usage.md" lang="zh-Hans" dir="ltr">简体中文</a> ·
<a href="../zh-Hant/usage.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->
<div lang="he" dir="rtl">

<a id="audit"></a>

## ביקורת

</div>

<div dir="ltr">

```sh
ha-meter-contracts check contract.json --json --lang en
ha-meter-contracts check examples/minimal.yaml --at 2026-01-01T12:00:05Z --lang es
```

</div>

<div lang="he" dir="rtl">

`--at` מקבל חותמת זמן ISO 8601 עם אזור זמן. ברירת המחדל היא זמן UTC הנוכחי. בהינתן אותם קלט, זמן ושפה, פלט JSON הוא דטרמיניסטי. דגימה נחשבת טרייה עד לגבול `freshness_seconds` כולל; רק לאחר הגבול היא נעשית ישנה מדי. דגימה מהעתיד אינה תקינה, ואין סבילות משתמעת לסטייה בין שעונים.

קודי יציאה: 0 = אין שגיאה או אזהרה; 1 = ממצא הקשור למשמעות או לאיכות הדגימה; 2 = שגיאת קלט או CLI. מידע כגון כינוי שאינו בשימוש אינו מכשיל בדיקה. `--json` כותב הן דוחות ביקורת והן אובייקטים של שגיאות קלט ל־stdout. בלעדיו, טקסט הביקורת נכתב ל־stdout ושגיאות הקלט ל־stderr. צינור פלט שנשבר מחזיר 2.

אין להשתמש ב־`|| true` ב־CI כדי להסתיר ממצאים. דוגמאות שאינן תקינות בכוונה צריכות לבדוק במפורש שקוד היציאה הוא 1. עזרה וגרסה יוצאות בקוד 0. `import-ha` תמיד כותב חוזה JSON; ‏`--json` אינו משנה את הסכמה שלו.

<a id="python-library"></a>

## ספריית Python

</div>

<div dir="ltr">

```python
from datetime import datetime, timezone
from ha_meter_contracts import audit, load_document, parse_contract

contract = parse_contract(load_document("examples/valid-three-meters.json"))
report = audit(contract, at=datetime(2026, 1, 1, 12, 0, 5, tzinfo=timezone.utc))
assert report["sums"][0]["value"] == 720
```

</div>

<div lang="he" dir="rtl">

`parse_contract` יוצר מחלקות נתונים קפואות; `InputError` חושף `code`, `path`, `params`. יש להשתמש במנתח הזה בכל גבול של קלט לא מהימן. `audit` מצפה ל־`Contract` שעבר אימות; הוא אינו מתרגם ממצאים. ה־CLI מוסיף ערכי `message` מתורגמים. בספרייה, הקורא בוחר במפורש את זמן ההערכה. אף אחד מהממשקים אינו משנה את הקלט או כותב קבצים.

<a id="offline-home-assistant-adapter"></a>

## מתאם Home Assistant לא מקוון

</div>

<div dir="ltr">

```sh
ha-meter-contracts import-ha examples/ha-contract.json --ha-states examples/ha-states.synthetic.json > /tmp/meter-contract.json
ha-meter-contracts check /tmp/meter-contract.json --at 2026-01-01T12:00:05Z --json
```

</div>

<div lang="he" dir="rtl">

יש למפות `entity_id` ו־`timestamp_attribute` בכל מד רצוי. הייצוא הוא מערך של אובייקטי מצב של HA עם `entity_id`, `state` ו־`attributes`. המאפיין הממופה חייב להכיל את זמן המדידה המקורי בפורמט ISO עם אזור זמן. ל־`attributes.unit_of_measurement` חייב להיות אותו ממד פיזיקלי; W/kW ו־Wh/kWh מומרים ליחידה שבחוזה.

רק ערכים ממופים וזמני מקור מועתקים. מתעלמים ממאפיינים אחרים, כולל שמות ידידותיים. דגימה חדשה יותר ממש מעבירה את הדגימה הקיימת ל־`previous`. העברה חוזרת של אותו ערך עם אותה חותמת זמן מקור אינה משנה את התוצאה; דגימה ישנה יותר או ערך סותר באותה חותמת זמן נדחים כ־`ha_sample_order`. ישויות חסרות ומצבים `unknown`/`unavailable` מנקים את הדגימה; הם אינם הופכים לאפס. חותמת זמן מקור חסרה, יחידה לא תואמת, ערך פגום או מזהה ישות כפול מכשילים את הייבוא בקוד יציאה 2. מדי מדידה שלא מופו נשארים ללא שינוי. מזהי ישויות יכולים להופיע בחוזה פרטי; דוגמאות ציבוריות משתמשות במזהים סינתטיים.

לייצוא HA רגיל לעיתים קרובות אין חותמת זמן מקורית של המקור. במקרה כזה המתאם מסרב במכוון להמציא אחת. יש להשיג נתוני התקן עם חותמת זמן או להשאיר את המד לא זמין. חותמות הזמן של קבלה או עדכון ב־HA אינן מוכיחות את זמן רכישת המדידה בהתקן. המתאם לעולם אינו מתחבר ל־`/api/states` או קורא אסימון. הוא אינו מעתיק סמני איפוס אנרגיה מ־HA; יש להוסיף בנפרד ראיות איפוס מאומתות לפני סכימת אנרגיה.

<a id="suggested-workflow"></a>

## תהליך עבודה מוצע

1. הצהירו על עץ התחומים הפיזיים ועל מקור הנתונים באמצעות תיעוד החיווט.
2. התחילו במד אחד ובדוגמה סינתטית קבועה.
3. ייצאו רק את התצפיות הדרושות לקובץ פרטי.
4. בצעו ביקורת ובחנו כל ממצא לפני שינוי אוטומציה במורד הזרם.
5. שמרו את זמני המקור המקוריים ואת ראיות הכיול בזמן העברות.

החבילה אינה מבצעת תיקונים, שינוי שמות של ישויות, איפוס התקנים או פריסת אוטומציה.

</div>
