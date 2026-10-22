<a id="contract-schema-v1"></a>

# סכמת חוזה v1

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
<a href="schema.md" lang="he" dir="rtl">עברית</a> ·
<a href="../hi/schema.md" lang="hi" dir="ltr">हिन्दी</a> ·
<a href="../id/schema.md" lang="id" dir="ltr">Bahasa Indonesia</a> ·
<a href="../it/schema.md" lang="it" dir="ltr">Italiano</a> ·
<a href="../ja/schema.md" lang="ja" dir="ltr">日本語</a> ·
<a href="../ko/schema.md" lang="ko" dir="ltr">한국어</a> ·
<a href="../nl/schema.md" lang="nl" dir="ltr">Nederlands</a> ·
<a href="../pl/schema.md" lang="pl" dir="ltr">Polski</a> ·
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
<div lang="he" dir="rtl">

הקובץ הקריא למכונה [schema.json](../../schema.json) מתאר את המבנה. מנתח Python הוא המקור הקובע לגבי מגבלות; `audit` מוסיף משמעות פיזית וזמנית ש־JSON Schema אינו יכול להוכיח. יש ליצור את קובץ המבנה באמצעות `python3 scripts/generate_schema.py`.

<a id="root-and-limits"></a>

## שורש ומגבלות

חובה: המספר השלם `schema_version: 1`, וכן `scopes` ו־`meters`. רשות: `sums` (ריק כברירת מחדל). שדות לא מוכרים נדחים בכל רמות החוזה. מותר לכל היותר 512 תחומי מדידה, 512 מדי מדידה ו־128 סכומים; תחומי המדידה ומדי המדידה אינם רשאים להיות ריקים. לכל סכום יש 1–512 איברים. הקלט הוא UTF-8, בגודל של עד 1,048,576 בתים, עומק קינון 16 ו־20,000 צומתי ערכים. מפתחות כפולים ו־NaN/Infinity ב־JSON, וכן כינויים, עוגנים ותגים מפורשים ב־YAML, נדחים. יש להקיף חותמות זמן ב־YAML במירכאות כדי שיישארו מחרוזות.

מזהים כוללים 1–96 תווי ASCII, מתחילים באות או בספרה, ואחריהם אותיות, ספרות, `.`, `_`, `-`. המזהים ייחודיים בתוך כל אוסף; מרחבי השמות של תחומי המדידה ושל מדי המדידה נפרדים. כל הזמנים כוללים `T` ואזור זמן. מספרים חייבים להיות סופיים, לא בוליאניים, ובטווח ±10^15 אלא אם ניתנה מגבלה צרה יותר.

<a id="physical-scopes"></a>

## תחומי מדידה פיזיים

לכל תחום יש `id`, וכן `kind` (`site`, `circuit`, `strip`, `outlet`, `load`) ו־`parent` אופציונלי. ההורים חייבים להתקיים וליצור יער ללא מעגלים. מדידה על הורה מכסה את כל צאצאיו. סוגי התחומים הם תיאוריים; הם אינם מסיקים מתח, פאזות, ערכים נקובים, חיווט או הורים מותרים. עליכם להצהיר על הטופולוגיה האמיתית.

<a id="meters"></a>

## מדי מדידה

שדות חובה:

- `id`, `scope`: מזהה מדידה ייחודי ותחום פיזי מוצהר.
- `quantity`: `power`, `energy`, `voltage`, `current`.
- `unit`: בהתאמה W/kW, Wh/kWh, V, A. המנתח מקבל את המונחים; הביקורת בודקת את הממד הפיזיקלי.
- `kind`: `measured` או `estimated`. זו הצהרה, ולא אימות מעבדתי.
- `provenance`: זהות יציבה של זרם המדידה הפיזי, **ולא** של הייצוג שלו ב־HA/MQTT. קריאות שהן כינויים חולקות את אותה זהות. סימן, גודל פיזיקלי או תחום שונים תחת אותו מקור יוצרים סתירה; כל כינוי של הזרם הסותר נעשה לא זמין לסכומים, בלי קשר לסדר הקלט. יש לבחור מקורות נפרדים לערוצי זרימה שבאמת נפרדים פיזית.
- `sign`: `nonnegative` לגודל של צריכה בלבד, יבוא בלבד או יצוא בלבד; `signed` לזרימה דו־כיוונית מוצהרת. גרסה זו אינה מסיקה איזה כיוון פיזי הוא חיובי.
- `state_class`: `measurement`, `total`, `total_increasing`.
- `freshness_seconds`: סף גיל חיובי, 0.001–604800 שניות.

השדה האופציונלי `reset`: `never`, `periodic`, `device_restart`, `unknown`, `not_applicable` (ברירת המחדל). אנרגיה מחייבת מדיניות מפורשת שאינה `not_applicable` ומחלקת מצב של ערך מצטבר. אנרגיה עם סימן אינה יכולה להשתמש ב־`total_increasing`. גדלים אחרים מחייבים `measurement` ו־`not_applicable`.

השדות האופציונליים `sample`, `previous`: null או אובייקט המכיל `value` (מספר או null), `measured_at` ו־`reset_at` אופציונלי. הדגימה הקודמת חייבת להיות ישנה יותר. ירידה במונה לא שלילי מחייבת סמן איפוס בין הדגימות; `never` דוחה אותה. `reset_at` אינו רשאי להיות מאוחר מהדגימה שלו וחל על אנרגיה בלבד. משמעות לא ידועה של איפוס המונה יוצרת אזהרה. מונה נטו עם סימן רשאי לרדת באופן תקין; האחריות לנקודת הבסיס הנכונה שלו נשארת בידי יצרן הנתונים.

השדה האופציונלי `calibration`: `quantity`, מקדם `factor` חיובי (10^-12–10^12), מזהה `reference` סינתטי או פרטי, וכן `verified_at`. הוא מתעד ראיות עבור אותו גודל פיזיקלי בדיוק. ערכי הדגימה **כבר מכוילים**: המאמת לעולם אינו מחיל שוב את המקדם. כיול עתידי או כיול מתח על מד הספק אינם תקינים. היעדר כיול אינו מוכיח דיוק, ואינו שגיאה אוטומטית.

השדות האופציונליים `entity_id`, `timestamp_attribute`: מיפוי HA לא מקוון; ראו [שימוש](usage.md#offline-home-assistant-adapter).

<a id="sums"></a>

## סכומים

חובה: `id`, תחום יעד `scope`, רשימת מזהי מדי מדידה ב־`meters`, גודל `quantity` (`power` או `energy`), וכן `coverage` (`partial` או `complete`). השדה האופציונלי `max_skew_seconds`: ‏0–604800, ברירת מחדל 2.

האיברים חייבים להימצא בתוך תחום היעד, להיות בעלי ממדים ומשמעות סימן תואמים, להשתמש בזרמים פיזיים שונים, ולא לחפוף זה לזה כהורה וילד או כתחומים זהים. סכום מלא חייב לכסות כל **תחום עלה מוצהר** מתחת ליעד שלו. אי אפשר לזהות חיווט שלא הוצהר. סכום חלקי מדווח במפורש שהכיסוי שלו חלקי. סכומים מקוננים אינם נתמכים; איברים תמיד מפנים למדי מדידה.

לכל איבר חייבים להיות נתונים תקינים וטריים; זמני רכישת המדידות חייבים להיות בתוך הסטייה המותרת. אנרגיה מחייבת בנוסף נקודות מוצא מפורשות וזהות של `reset_at`. הדבר בודק יישור מוצהר, ולא את הדיוק של הצטברות המונה בעבר. סכומים מומרים ל־W או ל־Wh. סכומי זרם ומתח אינם נתמכים במכוון, משום שמשמעותם תלויה בטופולוגיית המעגל.

סכום מספרי אינו זמין אם ראיה נדרשת כלשהי חסרה או בדיקת משמעות כלשהי נכשלת. אומדנים מועברים הלאה כ־`kind: estimated`. שני כינויים יכולים להתקיים יחד במלאי, אך אינם יכולים לתרום שניהם לאותו סכום. אין הסקה של סך כלשהו עבור שקעים בודדים שלא נמדדו.

<a id="report-v1"></a>

## דוח v1

ברמת השורש: `schema_version`, זמן ההערכה `at` מנורמל ל־UTC, ספירות לפי חומרה ב־`summary`, ממצאי `findings` ממוינים, וכן `sums`. כל ממצא מכיל `code`, `severity`, נתיב `path` בסגנון JSON ו־`params` מובנים; ה־CLI מוסיף `message`. כל סכום מכיל `id`, `scope`, `quantity`, יחידת בסיס `unit`, וכן `value`, `status`, `kind`, `coverage`. ערכים לא ידועים הם null ב־JSON, ולעולם לא NaN.

</div>
