<a id="troubleshooting"></a>

# פתרון תקלות

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
<a href="troubleshooting.md" lang="he" dir="rtl">עברית</a> ·
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
<a href="../uk/troubleshooting.md" lang="uk" dir="ltr">Українська</a> ·
<a href="../vi/troubleshooting.md" lang="vi" dir="ltr">Tiếng Việt</a> ·
<a href="../zh-Hans/troubleshooting.md" lang="zh-Hans" dir="ltr">简体中文</a> ·
<a href="../zh-Hant/troubleshooting.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->
<div lang="he" dir="rtl">

<a id="a-three-outlet-strip-cannot-produce-three-power-readings"></a>

## מפצל בעל שלושה שקעים אינו יכול להפיק שלוש קריאות הספק

`scope_outside` פירושו שתוצאה פרטנית מבוקשת משתמשת במדידה רחבה יותר. יש להשאיר ישות אחת לכל המפצל. אם נדרש הספק פרטני, יש להוסיף מדידות עצמאיות בעלות תחומי מדידה נכונים. ממסר מופעל אינו מוכיח שהעומס שלו צורך הספק; משאבה שצורכת חשמל אינה מוכיחה שמים זורמים.

<a id="a-migrated-sensor-doubles-the-total"></a>

## חיישן שהועבר מכפיל את הסכום

`alias_stream` לבדו הוא מידע בלבד. `duplicate_stream` פירושו ששני העותקים נכללים בסכום. יש לתת לעותקים של אותו שנאי זרם את אותו מקור נתונים ולהשאיר רק אחד מהם בסכום. אין לשנות את מקור הנתונים רק כדי להשתיק את הבדיקה.

![מקור אחד ושני ייצוגים](../images/duplicate-stream.svg)

<a id="no-numeric-sum-despite-individually-plausible-numbers"></a>

## אין סכום מספרי אף שכל מספר בפני עצמו נראה סביר

בדקו `sample_stale`, `sample_future`, `sample_skew`, `sample_missing`, `incomplete_coverage`, `unit_dimension`, `scope_overlap`. יש לרענן את המקור המקורי ולשמור את זמן רכישת המדידה שלו. הגדלת סף הטריות היא שינוי מדיניות, ולא תיקון המדידה. סכום מלא נבחן מול תחומי העלים המוצהרים, לכן יש לבחון גם את ההצהרה.

![ציר זמן סינתטי של איכות דגימות](../images/sample-quality.svg)

<a id="energy-decreased-at-midnight"></a>

## האנרגיה ירדה בחצות

ירידה עשויה להיות איפוס אמיתי, החלפה או תיקון. יש להצהיר על המדיניות ולהוסיף `reset_at` מתוך ראיות אמיתיות מהמקור. חותמת הזמן שבה HA העביר מחדש את הערך אינה סמן איפוס. `total_increasing` אינו מתאים לאנרגיית נטו עם סימן. שני מונים בעלי נקודות מוצא שונות אינם נסכמים.

<a id="voltage-looks-calibrated-but-watts-still-differ"></a>

## המתח נראה מכויל אך הוואטים עדיין שונים

כיול הוא לכל גודל פיזיקלי בנפרד. תיקון מתח אינו מאמת זרם, יחס מופע, הספק או אנרגיה מצטברת. שדה המקדם הוא תיעוד בלבד: הערכים חייבים כבר לכלול את התיקון המיועד.

<a id="yaml-fails-although-another-parser-accepts-it"></a>

## YAML נכשל אף שמנתח אחר מקבל אותו

יש להקיף חותמות זמן במירכאות, להסיר כינויים, עוגנים ותגים מותאמים אישית, להסיר מפתחות כפולים ולהשתמש במספרים סופיים. שדות לא מוכרים הם שגיאות כדי לתפוס שגיאות הקלדה. המגבלות חלות על שני הפורמטים. השתמשו ב־JSON להעברת נתונים כאשר ערכים סקלריים דו־משמעיים של YAML אינם נוחים.

<a id="ha-import-fails-on-timestamps"></a>

## ייבוא HA נכשל בגלל חותמות זמן

הגדירו את `timestamp_attribute` למאפיין שמייצג זמן מדידה אמיתי. `last_reported` מוכיח רק קבלה בידי HA. אם אין זמן מקור זמין, הכלי אינו יכול לקבוע טריות; יש להשאיר את הדגימה לא זמינה. אין בעיית אסימון או קישוריות רשת לאבחן, כי הייבוא אינו מקוון.

<a id="safe-issue-report"></a>

## דיווח תקלה בטוח

יש לכלול את גרסת החבילה וגרסת Python, קודי ממצאים יציבים, חוזה סינתטי מינימלי, ערך `--at` שנבחר, תוצאה צפויה ותוצאה בפועל. אין לצרף ייצוא HA מלא, אסימון, כתובת אמיתית, לוח זמנים של משק הבית או מזהים פרטיים של התקנים. בדוגמה לשחזור חייבים להמשיך להבחין בין ערך של 0 W לבין דגימה לא זמינה.

</div>
