<a id="troubleshooting"></a>

# عیب‌یابی

<!-- language-navigation:start -->
<p dir="ltr">
<a href="../troubleshooting.md" lang="en" dir="ltr">English</a> ·
<a href="../ar/troubleshooting.md" lang="ar" dir="rtl">العربية</a> ·
<a href="../bn/troubleshooting.md" lang="bn" dir="ltr">বাংলা</a> ·
<a href="../cs/troubleshooting.md" lang="cs" dir="ltr">Čeština</a> ·
<a href="../de/troubleshooting.md" lang="de" dir="ltr">Deutsch</a> ·
<a href="../es/troubleshooting.md" lang="es" dir="ltr">Español</a> ·
<a href="troubleshooting.md" lang="fa" dir="rtl">فارسی</a> ·
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
<a href="../uk/troubleshooting.md" lang="uk" dir="ltr">Українська</a> ·
<a href="../vi/troubleshooting.md" lang="vi" dir="ltr">Tiếng Việt</a> ·
<a href="../zh-Hans/troubleshooting.md" lang="zh-Hans" dir="ltr">简体中文</a> ·
<a href="../zh-Hant/troubleshooting.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->
<div lang="fa" dir="rtl">

<a id="a-three-outlet-strip-cannot-produce-three-power-readings"></a>

## سه خروجی یک چندراهی، سه قرائت توان ایجاد نمی‌کنند

`scope_outside` یعنی نتیجهٔ تکیِ درخواست‌شده از اندازه‌گیری گسترده‌تر استفاده می‌کند. یک موجودیت برای کل چندراهی نگه دارید. اگر توان تکی لازم است، اندازه‌گیری مستقل در دامنهٔ درست اضافه کنید. روشن‌بودن رله مصرف توان بار را ثابت نمی‌کند؛ مصرف برق پمپ هم جاری‌بودن آب را ثابت نمی‌کند.

<a id="a-migrated-sensor-doubles-the-total"></a>

## حسگر مهاجرت‌کرده مجموع را دوبرابر می‌کند

`alias_stream` به‌تنهایی اطلاعاتی است. `duplicate_stream` یعنی هر دو نسخه در یک جمع آمده‌اند. نسخه‌های همان CT را با منشأ یکسان معرفی کنید و فقط یکی را در جمع نگه دارید. منشأ را صرفاً برای خاموش‌کردن بررسی عوض نکنید.

![یک منبع و دو نمایش](../images/duplicate-stream.svg)

<a id="no-numeric-sum-despite-individually-plausible-numbers"></a>

## با وجود اعداد تکی معقول، جمع عددی وجود ندارد

`sample_stale`، `sample_future`، `sample_skew`، `sample_missing`، `incomplete_coverage`، `unit_dimension` و `scope_overlap` را بررسی کنید. منبع اصلی را تازه و زمان اخذ آن را حفظ کنید. افزایش بودجهٔ تازگی، تغییر سیاست است نه تعمیر اندازه‌گیری. جمع کامل بر اساس دامنه‌های برگ اعلام‌شده داوری می‌شود؛ پس اظهار را نیز بررسی کنید.

![خط زمانی ساختگی کیفیت نمونه](../images/sample-quality.svg)

<a id="energy-decreased-at-midnight"></a>

## انرژی در نیمه‌شب کاهش یافت

کاهش می‌تواند بازنشانی واقعی، تعویض یا اصلاح باشد. سیاست را اعلام کنید و `reset_at` را از مدرک واقعی منبع اضافه کنید. زمان بازپخش مقدار توسط HA نشانگر بازنشانی نیست. `total_increasing` برای انرژی خالص علامت‌دار نامناسب است. دو شمارنده با مبدأ متفاوت جمع نمی‌شوند.

<a id="voltage-looks-calibrated-but-watts-still-differ"></a>

## ولتاژ کالیبره به نظر می‌رسد اما وات‌ها متفاوت‌اند

کالیبراسیون برای هر کمیت جداست. اصلاح ولتاژ، جریان، رابطهٔ فاز، توان یا انرژی انباشته را تأیید نمی‌کند. فیلد ضریب فقط مستندات است؛ مقادیر باید از قبل اصلاح موردنظر را داشته باشند.

<a id="yaml-fails-although-another-parser-accepts-it"></a>

## YAML با وجود پذیرش پارسر دیگر شکست می‌خورد

زمان‌ها را نقل‌قول‌گذاری کنید، نام مستعار/لنگر/برچسب سفارشی و کلید تکراری را حذف کنید و اعداد متناهی به کار ببرید. فیلد ناشناخته برای کشف غلط تایپی خطاست. محدودیت‌ها برای هر دو قالب‌اند. اگر اسکالر مبهم YAML مزاحم است، برای تبادل JSON به کار ببرید.

<a id="ha-import-fails-on-timestamps"></a>

## واردکردن HA روی زمان‌ها شکست می‌خورد

`timestamp_attribute` را به ویژگی واقعی زمان اندازه‌گیری نگاشت کنید. `last_reported` فقط دریافت توسط HA را ثابت می‌کند. بدون زمان منبع، ابزار نمی‌تواند تازگی را تعیین کند؛ نمونه را ناموجود بگذارید. مشکل توکن یا اتصال شبکه‌ای برای عیب‌یابی وجود ندارد چون واردکردن آفلاین است.

<a id="safe-issue-report"></a>

## گزارش امن مشکل

نسخهٔ بسته/Python، کد پایدار یافته، حداقل قرارداد ساختگی، `--at` انتخاب‌شده، نتیجهٔ موردانتظار و واقعی را بنویسید. خروجی کامل HA، توکن، نشانی واقعی، برنامهٔ زندگی خانه یا شناسهٔ خصوصی دستگاه را پیوست نکنید. بازتولید باید 0 W را از نمونهٔ ناموجود متمایز نگه دارد.

</div>
