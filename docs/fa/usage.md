<a id="usage"></a>

# کاربرد

<!-- language-navigation:start -->
<p dir="ltr">
<a href="../usage.md" lang="en" dir="ltr">English</a> ·
<a href="../ar/usage.md" lang="ar" dir="rtl">العربية</a> ·
<a href="../bn/usage.md" lang="bn" dir="ltr">বাংলা</a> ·
<a href="../cs/usage.md" lang="cs" dir="ltr">Čeština</a> ·
<a href="../de/usage.md" lang="de" dir="ltr">Deutsch</a> ·
<a href="../es/usage.md" lang="es" dir="ltr">Español</a> ·
<a href="usage.md" lang="fa" dir="rtl">فارسی</a> ·
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
<a href="../uk/usage.md" lang="uk" dir="ltr">Українська</a> ·
<a href="../vi/usage.md" lang="vi" dir="ltr">Tiếng Việt</a> ·
<a href="../zh-Hans/usage.md" lang="zh-Hans" dir="ltr">简体中文</a> ·
<a href="../zh-Hant/usage.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->
<div lang="fa" dir="rtl">

<a id="audit"></a>

## ممیزی

</div>

<div dir="ltr">

```sh
ha-meter-contracts check contract.json --json --lang en
ha-meter-contracts check examples/minimal.yaml --at 2026-01-01T12:00:05Z --lang es
```

</div>

<div lang="fa" dir="rtl">

`--at` زمان ISO 8601 با منطقهٔ زمانی می‌پذیرد. پیش‌فرض، UTC فعلی است. با ورودی، زمان و زبان یکسان، خروجی JSON قطعی است. نمونه تا خود مرز `freshness_seconds` تازه است و فقط پس از آن کهنه می‌شود. نمونهٔ آینده نامعتبر است و هیچ ارفاق ضمنی اختلاف ساعت وجود ندارد.

کد خروج: 0 یعنی بدون خطا/هشدار؛ 1 یعنی یافتهٔ معنایی یا کیفیت نمونه؛ 2 یعنی خطای ورودی/CLI. اطلاعاتی مانند نام مستعار استفاده‌نشده بررسی را ناموفق نمی‌کند. `--json` هم گزارش ممیزی و هم شیء خطای ورودی را روی stdout می‌گذارد. بدون آن، متن ممیزی به stdout و خطای ورودی به stderr می‌رود. شکستن لولهٔ خروجی کد 2 می‌دهد.

در CI برای پنهان‌کردن یافته‌ها از `|| true` استفاده نکنید. مثال‌های عمداً نامعتبر باید کد خروج 1 را صریح بررسی کنند. راهنما و نسخه کد 0 می‌دهند. `import-ha` همیشه قرارداد JSON می‌نویسد؛ `--json` طرح‌واره‌اش را تغییر نمی‌دهد.

<a id="python-library"></a>

## کتابخانهٔ Python

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

<div lang="fa" dir="rtl">

`parse_contract`، dataclassهای منجمد می‌سازد؛ `InputError`، `code`، `path` و `params` را ارائه می‌کند. در هر مرز ورودی نامطمئن از این پارسر استفاده کنید. `audit` یک `Contract` تأییدشده می‌خواهد و یافته‌ها را ترجمه نمی‌کند. CLI مقادیر محلی‌شدهٔ `message` را می‌افزاید. در کتابخانه فراخواننده زمان ارزیابی را صریح انتخاب می‌کند. هیچ‌یک از دو API ورودی را تغییر نمی‌دهد یا فایل نمی‌نویسد.

<a id="offline-home-assistant-adapter"></a>

## سازگارکنندهٔ آفلاین Home Assistant

</div>

<div dir="ltr">

```sh
ha-meter-contracts import-ha examples/ha-contract.json --ha-states examples/ha-states.synthetic.json > /tmp/meter-contract.json
ha-meter-contracts check /tmp/meter-contract.json --at 2026-01-01T12:00:05Z --json
```

</div>

<div lang="fa" dir="rtl">

روی هر کنتور موردنظر `entity_id` و `timestamp_attribute` را نگاشت کنید. خروجی، آرایه‌ای از اشیای وضعیت HA با `entity_id`، `state` و `attributes` است. ویژگی نگاشت‌شده باید زمان اصلی اندازه‌گیری ISO با منطقهٔ زمانی را داشته باشد. `attributes.unit_of_measurement` باید بُعد یکسان داشته باشد؛ W/kW و Wh/kWh به واحد قرارداد تبدیل می‌شوند.

فقط مقادیر نگاشت‌شده و زمان منبع کپی می‌شوند. سایر ویژگی‌ها، از جمله نام‌های خوانا، نادیده گرفته می‌شوند. نمونهٔ واقعاً جدیدتر، نمونهٔ موجود را به `previous` می‌برد. بازپخش همان مقدار با همان زمان منبع نتیجه را تغییر نمی‌دهد؛ نمونهٔ قدیمی‌تر یا مقدار متعارض در همان زمان با `ha_sample_order` رد می‌شود. موجودیت مفقود و حالت‌های `unknown`/`unavailable` نمونه را پاک می‌کنند؛ صفر نمی‌شوند. زمان منبع مفقود، واحد ناسازگار، مقدار بدساخت یا شناسهٔ موجودیت تکراری، واردکردن را با کد 2 ناموفق می‌کند. کنتورهای نگاشت‌نشده تغییر نمی‌کنند. قرارداد خصوصی می‌تواند شناسهٔ موجودیت داشته باشد؛ مثال عمومی شناسهٔ ساختگی دارد.

خروجی عادی HA اغلب زمان اصلی منبع ندارد. در این حالت سازگارکننده عمداً از ساختن زمان خودداری می‌کند. دادهٔ زمان‌دار دستگاه بگیرید یا کنتور را ناموجود نگه دارید. زمان دریافت/به‌روزرسانی HA زمان اخذ دستگاه را ثابت نمی‌کند. سازگارکننده هرگز به `/api/states` وصل نمی‌شود و توکنی نمی‌خواند. نشانگرهای بازنشانی انرژی را از HA کپی نمی‌کند؛ پیش از جمع انرژی، مدرک تأییدشدهٔ بازنشانی را جداگانه اضافه کنید.

<a id="suggested-workflow"></a>

## گردش کار پیشنهادی

1. درخت دامنهٔ فیزیکی و منشأ منابع را از روی مستندات سیم‌کشی اعلام کنید.
2. با یک کنتور و مثال ساختگی ثابت شروع کنید.
3. فقط مشاهدات ضروری را به فایل خصوصی صادر کنید.
4. پیش از تغییر اتوماسیون پایین‌دستی، ممیزی و تک‌تک یافته‌ها را بررسی کنید.
5. در مهاجرت، زمان‌های اصلی منبع و شواهد کالیبراسیون را نگه دارید.

این بسته هیچ اصلاح خودکار، تغییر نام موجودیت، بازنشانی دستگاه یا استقرار اتوماسیونی انجام نمی‌دهد.

</div>
