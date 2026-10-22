<a id="troubleshooting"></a>

# استكشاف المشكلات

<!-- language-navigation:start -->
<p dir="ltr">
<a href="../troubleshooting.md" lang="en" dir="ltr">English</a> ·
<a href="troubleshooting.md" lang="ar" dir="rtl">العربية</a> ·
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
<a href="../uk/troubleshooting.md" lang="uk" dir="ltr">Українська</a> ·
<a href="../vi/troubleshooting.md" lang="vi" dir="ltr">Tiếng Việt</a> ·
<a href="../zh-Hans/troubleshooting.md" lang="zh-Hans" dir="ltr">简体中文</a> ·
<a href="../zh-Hant/troubleshooting.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->
<div lang="ar" dir="rtl">

<a id="a-three-outlet-strip-cannot-produce-three-power-readings"></a>

## المشترك ذو ثلاثة مخارج لا ينتج ثلاث قراءات قدرة

تعني `scope_outside` أن نتيجة فردية مطلوبة تستخدم قياساً أوسع. احتفظ بكيان واحد للمشترك كله. تحتاج القدرة الفردية إلى قياسات مستقلة صحيحة النطاق. تشغيل مرحّل لا يثبت استهلاك الحمل؛ واستهلاك المضخة للكهرباء لا يثبت تدفق الماء.

<a id="a-migrated-sensor-doubles-the-total"></a>

## مستشعر جرى ترحيله يضاعف الإجمالي

تكون `alias_stream` وحدها معلوماتية. تعني `duplicate_stream` أن النسختين داخل المجموع. أعطِ نسخ CT نفسه المصدر نفسه واحتفظ بواحدة فقط داخل المجموع. لا تغيّر المصدر لمجرد إسكات التحقق.

![مصدر واحد وتمثيلان](../images/duplicate-stream.svg)

<a id="no-numeric-sum-despite-individually-plausible-numbers"></a>

## لا يوجد مجموع رقمي رغم معقولية القيم

تحقق من `sample_stale` و`sample_future` و`sample_skew` و`sample_missing` و`incomplete_coverage` و`unit_dimension` و`scope_overlap`. جدّد المصدر الحقيقي واحتفظ بوقت قياسه. زيادة العمر المسموح تغيّر السياسة ولا تصلح القياس. يُقيّم المجموع الكامل مقابل الأوراق المصرّح بها: تحقق من التصريح أيضاً.

![خط زمني اصطناعي لجودة العينات](../images/sample-quality.svg)

<a id="energy-decreased-at-midnight"></a>

## انخفضت الطاقة عند منتصف الليل

قد يكون الانخفاض تصفيراً حقيقياً أو استبدالاً أو تصحيحاً. صرّح بالسياسة وأضف `reset_at` من دليل حقيقي للمصدر. وقت إعادة تشغيل بيانات HA ليس علامة تصفير. لا تناسب `total_increasing` الطاقة الصافية ذات الإشارة. لا تُجمع عدادات مختلفة الأصل.

<a id="voltage-looks-calibrated-but-watts-still-differ"></a>

## يبدو الجهد معايراً لكن الواط مختلف

المعايرة خاصة بالكمية. تصحيح الجهد لا يتحقق من التيار أو علاقة الطور أو القدرة أو الطاقة المتراكمة. حقل المعامل توثيقي فقط؛ يجب أن تتضمن القيم التصحيح المقصود مسبقاً.

<a id="yaml-fails-although-another-parser-accepts-it"></a>

## يفشل YAML رغم أن محللاً آخر يقبله

ضع الأوقات بين علامات اقتباس، وأزل الأسماء المستعارة والمراسي والوسوم المخصصة والمفاتيح المكررة، واستعمل أعداداً منتهية. الحقول المجهولة أخطاء لالتقاط أخطاء الكتابة. تسري الحدود على التنسيقين. استخدم JSON للتبادل إذا سببت قيم YAML المفردة الملتبسة مشكلات.

<a id="ha-import-fails-on-timestamps"></a>

## يفشل استيراد HA عند الطوابع الزمنية

اضبط `timestamp_attribute` إلى سمة حقيقية لوقت القياس. لا تثبت `last_reported` إلا استلام HA. بدون وقت المصدر لا تستطيع الأداة تحديد الحداثة؛ اترك العينة غير متاحة. لا توجد رموز وصول أو اتصالات لتشخيصها: الاستيراد دون اتصال.

<a id="safe-issue-report"></a>

## الإبلاغ الآمن عن مشكلة

أدرج نسخ الحزمة/Python والرموز الثابتة وعقداً اصطناعياً أدنى و`--at` المختار والنتيجة المتوقعة والفعلية. لا ترفق تصدير HA كاملاً أو رموز وصول أو عنواناً حقيقياً أو جداول المنزل أو معرّفات الأجهزة الخاصة. يجب أن يظل 0 W والعينة غير المتاحة مختلفين في مثال إعادة الإنتاج.

</div>
