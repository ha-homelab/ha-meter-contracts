<a id="usage"></a>

# الاستخدام

<!-- language-navigation:start -->
<p dir="ltr">
<a href="../usage.md" lang="en" dir="ltr">English</a> ·
<a href="usage.md" lang="ar" dir="rtl">العربية</a> ·
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
<a href="../uk/usage.md" lang="uk" dir="ltr">Українська</a> ·
<a href="../vi/usage.md" lang="vi" dir="ltr">Tiếng Việt</a> ·
<a href="../zh-Hans/usage.md" lang="zh-Hans" dir="ltr">简体中文</a> ·
<a href="../zh-Hant/usage.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->
<div lang="ar" dir="rtl">

<a id="audit"></a>

## التدقيق

</div>

<div dir="ltr">

```sh
ha-meter-contracts check contract.json --json --lang en
ha-meter-contracts check examples/minimal.yaml --at 2026-01-01T12:00:05Z --lang es
```

</div>

<div lang="ar" dir="rtl">

تقبل `--at` طابعاً زمنياً ISO 8601 مع منطقة زمنية. الافتراضي UTC الحالي. عند ثبات الإدخال والوقت واللغة يكون JSON حتمياً. تظل العينة حديثة حتى حد `freshness_seconds` شاملاً؛ ولا تصبح قديمة إلا بعده. العينة المستقبلية غير صالحة، دون سماح ضمني بانحراف الساعة.

رموز الخروج: 0 = لا أخطاء/تحذيرات؛ 1 = مشكلة دلالية أو جودة عينة؛ 2 = خطأ إدخال/CLI. النتائج المعلوماتية مثل بديل غير مستخدم لا تسبب فشلاً. تكتب `--json` التقارير وكائنات أخطاء الإدخال إلى stdout. بدونها يذهب نص التدقيق إلى stdout وأخطاء الإدخال إلى stderr. الأنبوب المقطوع للإخراج يعيد 2.

لا تستعمل `|| true` في CI لإخفاء النتائج. يجب أن تتحقق الأمثلة غير الصالحة عمداً صراحة من رمز الخروج 1. تعيد المساعدة والنسخة 0. تكتب `import-ha` دائماً عقد JSON؛ ولا تغيّر `--json` مخططه.

<a id="python-library"></a>

## مكتبة Python

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

<div lang="ar" dir="rtl">

تنشئ `parse_contract` فئات بيانات غير قابلة للتغيير؛ وتكشف `InputError` الحقول `code` و`path` و`params`. استخدم المحلل عند كل حد إدخال غير موثوق. تتوقع `audit` كائن `Contract` متحققاً منه ولا تترجم النتائج. تضيف CLI قيم `message` المحلية. يختار مستدعي المكتبة وقت التقييم صراحة. لا تغيّر أي واجهة الإدخال ولا تكتب ملفات.

<a id="offline-home-assistant-adapter"></a>

## محوّل Home Assistant دون اتصال

</div>

<div dir="ltr">

```sh
ha-meter-contracts import-ha examples/ha-contract.json --ha-states examples/ha-states.synthetic.json > /tmp/meter-contract.json
ha-meter-contracts check /tmp/meter-contract.json --at 2026-01-01T12:00:05Z --json
```

</div>

<div lang="ar" dir="rtl">

اربط `entity_id` و`timestamp_attribute` على كل عداد مطلوب. التصدير مصفوفة حالات HA فيها `entity_id` و`state` و`attributes`. يجب أن تتضمن السمة المربوطة وقت القياس ISO الأصلي مع المنطقة الزمنية. يجب أن تكون `attributes.unit_of_measurement` من البُعد نفسه؛ وتُحوّل W/kW وWh/kWh إلى وحدة العقد.

تُنسخ القيم المربوطة وأوقات المصدر فقط. تُهمل السمات الأخرى بما فيها الأسماء المقروءة. تنقل عينة أحدث فعلاً العينة الموجودة إلى `previous`. تكرار القيمة نفسها بوقت المصدر نفسه لا يغير النتيجة؛ وتُرفض عينة أقدم أو قيمة متعارضة عند الوقت نفسه باسم `ha_sample_order`. تمسح الكيانات المفقودة وحالات `unknown`/`unavailable` العينة؛ ولا تصبح صفراً. غياب الوقت أو وحدة غير متوافقة أو قيمة مشوهة أو معرّف كيان مكرر يُفشل الاستيراد بالرمز 2. لا تتغير العدادات غير المربوطة. قد تحتوي العقود الخاصة معرّفات كيانات؛ وتستعمل الأمثلة العامة معرّفات اصطناعية.

كثيراً ما لا يتضمن تصدير HA العادي الطابع الزمني الأصلي. يرفض المحوّل عمداً اختراعه حينئذ. احصل على بيانات جهاز ذات طوابع زمنية أو اترك العداد غير متاح. لا تثبت أوقات استلام/تحديث HA وقت قياس الجهاز. لا يتصل المحوّل أبداً بـ`/api/states` ولا يقرأ رموز وصول. ولا ينسخ علامات تصفير الطاقة من HA؛ أضف أدلة متحققاً منها منفصلة قبل جمع الطاقة.

<a id="suggested-workflow"></a>

## سير عمل مقترح

1. صرّح بشجرة النطاقات الفيزيائية ومصادر البيانات استناداً إلى وثائق التوصيل.
2. ابدأ بعداد واحد ومثال اصطناعي ثابت.
3. صدّر الملاحظات اللازمة فقط إلى ملف خاص.
4. شغّل التدقيق وراجع كل نتيجة قبل تعديل الأتمتة التي تعتمد عليها.
5. احتفظ بأوقات المصدر وأدلة المعايرة أثناء الترحيل.

لا تنفذ الحزمة إصلاحات أو تعيد تسمية كيانات أو تصفّر أجهزة أو تنشر أتمتة.

</div>
