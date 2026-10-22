<a id="contract-schema-v1"></a>

# مخطط العقد v1

<!-- language-navigation:start -->
<p dir="ltr">
<a href="../schema.md" lang="en" dir="ltr">English</a> ·
<a href="schema.md" lang="ar" dir="rtl">العربية</a> ·
<a href="../bn/schema.md" lang="bn" dir="ltr">বাংলা</a> ·
<a href="../cs/schema.md" lang="cs" dir="ltr">Čeština</a> ·
<a href="../de/schema.md" lang="de" dir="ltr">Deutsch</a> ·
<a href="../es/schema.md" lang="es" dir="ltr">Español</a> ·
<a href="../fa/schema.md" lang="fa" dir="rtl">فارسی</a> ·
<a href="../fr/schema.md" lang="fr" dir="ltr">Français</a> ·
<a href="../he/schema.md" lang="he" dir="rtl">עברית</a> ·
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
<div lang="ar" dir="rtl">

يصف [schema.json](../../schema.json) القابل للقراءة آلياً البنية. محلل Python هو المرجع للحدود؛ وتضيف `audit` دلالات فيزيائية وزمنية لا يستطيع JSON Schema إثباتها. ولّد ملف البنية باستخدام `python3 scripts/generate_schema.py`.

<a id="root-and-limits"></a>

## الجذر والحدود

المطلوب: العدد الصحيح `schema_version: 1` و`scopes` و`meters`. الاختياري: `sums` (فارغ افتراضياً). تُرفض الحقول المجهولة في كل مستوى. الحد الأقصى 512 نطاقاً و512 عداداً و128 مجموعاً؛ ويجب ألا تكون النطاقات والعدادات فارغة. لكل مجموع 1–512 عضواً. الإدخال UTF-8 بحد أقصى 1,048,576 بايت وعمق 16 و20,000 عقدة قيمة. تُرفض مفاتيح JSON المكررة وNaN/Infinity وأسماء YAML المستعارة ومراسيه ووسومه الصريحة. ضع طوابع YAML الزمنية بين علامتي اقتباس لتبقى سلاسل.

المعرّفات من 1–96 محرف ASCII: حرف أو رقم أولاً ثم حروف وأرقام و`.` و`_` و`-`. المعرّفات فريدة داخل كل مجموعة؛ وللنطاقات والعدادات فضاءا أسماء منفصلان. تتضمن جميع الأوقات `T` ومنطقة زمنية. الأعداد منتهية وليست منطقية، وضمن ±10^15 ما لم ينطبق حد أشد.

<a id="physical-scopes"></a>

## النطاقات الفيزيائية

لكل نطاق `id` و`kind` (`site` أو `circuit` أو `strip` أو `outlet` أو `load`) و`parent` اختياري. يجب أن تكون الآباء موجودة وأن تشكل غابة لا دورية. يغطي عداد الأب كل نسله. أنواع النطاقات وصفية: لا تستنتج الجهد أو الأطوار أو القيم المقننة أو التوصيلات أو الآباء المسموحين. يصرّح المستخدم بالطوبولوجيا الحقيقية.

<a id="meters"></a>

## العدادات

الحقول المطلوبة:

- `id` و`scope`: معرّف قراءة فريد ونطاق فيزيائي مصرّح به.
- `quantity`: `power` أو `energy` أو `voltage` أو `current`.
- `unit`: بالترتيب W/kW وWh/kWh وV وA. يقبل المحلل المفردات؛ ويتحقق المدقق من البُعد.
- `kind`: `measured` أو `estimated`. هذا تصريح، وليس تحققاً مخبرياً.
- `provenance`: الهوية الثابتة لتدفق القياس الفيزيائي، **لا** لتمثيله في HA/MQTT. تشترك القراءات البديلة فيها. اختلاف الإشارة/الكمية/النطاق مع مصدر واحد تعارض؛ وتصبح جميع بدائل التدفق غير متاحة للمجاميع بغض النظر عن ترتيب الإدخال. اختر مصادر مختلفة للقنوات الفيزيائية المختلفة فعلاً.
- `sign`: القيمة `nonnegative` لمقادير الاستهلاك/الاستيراد/التصدير فقط؛ و`signed` لتدفق ثنائي الاتجاه مصرّح به. لا تستنتج هذه النسخة أي الاتجاهين الفيزيائيين موجب.
- `state_class`: `measurement` أو `total` أو `total_increasing`.
- `freshness_seconds`: أقصى عمر موجب، 0.001–604800 ثانية.

الحقل الاختياري `reset`: `never` أو `periodic` أو `device_restart` أو `unknown` أو `not_applicable` (الافتراضي). تتطلب الطاقة سياسة صريحة غير `not_applicable` وفئة حالة من نوع total. لا يجوز للطاقة ذات الإشارة استعمال `total_increasing`. وتتطلب الكميات الأخرى `measurement` و`not_applicable`.

الحقول الاختيارية `sample` و`previous`: null أو كائن يحتوي `value` (عدد أو null) و`measured_at` و`reset_at` اختيارياً. يجب أن تكون العينة السابقة أقدم. يتطلب انخفاض عداد غير سالب علامة تصفير بين العينتين؛ وترفضها `never`. يجب ألا تتجاوز `reset_at` وقت عينتها، وتنطبق على الطاقة فقط. دلالات التصفير المجهولة تُصدر تحذيراً. يجوز لعداد صافٍ ذي إشارة أن ينخفض بصورة صحيحة؛ ويظل خط الأساس الصحيح مسؤولية المنتج.

الحقل الاختياري `calibration`: `quantity` و`factor` موجب (10^-12–10^12) ومعرّف اصطناعي/خاص `reference` و`verified_at`. يسجّل دليلاً لتلك الكمية تحديداً. القيم **معايرة مسبقاً**: لا يعيد المدقق تطبيق المعامل مطلقاً. المعايرة المستقبلية أو معايرة الجهد على عداد قدرة غير صحيحة. غياب المعايرة لا يثبت الدقة وليس خطأ تلقائياً.

الحقول الاختيارية `entity_id` و`timestamp_attribute`: ربط HA دون اتصال؛ انظر [الاستخدام](usage.md#offline-home-assistant-adapter).

<a id="sums"></a>

## المجاميع

المطلوب: `id` و`scope` الهدف وقائمة معرّفات عدادات في `meters` و`quantity` (`power` أو `energy`) و`coverage` (`partial` أو `complete`). الاختياري `max_skew_seconds`: من 0–604800، والافتراضي 2.

يجب أن تقع الأعضاء ضمن نطاق الهدف، وتتوافق أبعادها ودلالات إشاراتها، وتستعمل تدفقات فيزيائية مختلفة، ولا تتداخل كأب/ابن أو نطاقات متطابقة. يغطي المجموع الكامل كل **نطاق طرفي مصرّح به (ورقة في شجرة النطاقات)** أسفل الهدف. لا يمكن اكتشاف التوصيلات غير المصرّح بها. يصرّح المجموع الجزئي صراحة بتغطية جزئية. لا تُدعم المجاميع المتداخلة؛ وتشير الأعضاء دوماً إلى عدادات.

يجب أن يكون لكل عضو بيانات صحيحة وحديثة؛ وأن تقع أوقات القياس ضمن الفارق المسموح. تتطلب الطاقة أيضاً أصول `reset_at` صريحة ومتطابقة. هذا يتحقق من المحاذاة المصرّح بها، لا من دقة التراكم التاريخي. تُحوّل المجاميع إلى W أو Wh. لا تُدعم مجاميع التيار والجهد عمداً لأنها تعتمد على طوبولوجيا الدائرة.

لا يتاح مجموع رقمي حين يغيب دليل مطلوب أو يفشل تحقق دلالي. تنتقل التقديرات بصفتها `kind: estimated`. يمكن لبديلين التعايش في الجرد، لكن لا يجوز أن يسهما معاً في مجموع واحد. لا يُستنتج أي إجمالي للمقابس الفردية غير المقاسة.

<a id="report-v1"></a>

## التقرير v1

الجذر: `schema_version` ووقت التقييم `at` الموحّد إلى UTC وعدد الحالات حسب الشدة في `summary` و`findings` مرتبة و`sums`. كل نتيجة تحتوي `code` و`severity` و`path` بأسلوب JSON و`params` مهيكلة؛ وتضيف CLI الحقل `message`. كل مجموع يحتوي `id` و`scope` و`quantity` و`unit` الأساسية و`value` و`status` و`kind` و`coverage`. القيم المجهولة JSON null، وليست NaN مطلقاً.

</div>
