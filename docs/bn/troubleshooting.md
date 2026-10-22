<a id="troubleshooting"></a>

# সমস্যা সমাধান

<!-- language-navigation:start -->
<p dir="ltr">
<a href="../troubleshooting.md" lang="en" dir="ltr">English</a> ·
<a href="../ar/troubleshooting.md" lang="ar" dir="rtl">العربية</a> ·
<a href="troubleshooting.md" lang="bn" dir="ltr">বাংলা</a> ·
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
<a id="a-three-outlet-strip-cannot-produce-three-power-readings"></a>

## তিন সকেটের মাল্টিপ্লাগ তিনটি ক্ষমতার পাঠ দেয় না

`scope_outside` মানে চাওয়া পৃথক ফল আরও বড় পরিসরের পরিমাপ ব্যবহার করছে। পুরো মাল্টিপ্লাগের জন্য একটি এনটিটি রাখুন। পৃথক ক্ষমতার জন্য সঠিক পরিসরের স্বাধীন পরিমাপ চাই। চালু রিলে লোডের খরচ প্রমাণ করে না; বিদ্যুৎ খরচ করা পাম্প পানির প্রবাহ প্রমাণ করে না।

<a id="a-migrated-sensor-doubles-the-total"></a>

## স্থানান্তরিত সেন্সর মোট দ্বিগুণ করছে

শুধু `alias_stream` তথ্যমূলক। `duplicate_stream` মানে দুই কপিই যোগফলে আছে। একই CT-র কপিতে একই উৎসপরিচয় দিন এবং যোগফলে কেবল একটি রাখুন। শুধু পরীক্ষা চুপ করাতে উৎসপরিচয় বদলাবেন না।

![একটি উৎস ও দুটি উপস্থাপনা](../images/duplicate-stream.svg)

<a id="no-numeric-sum-despite-individually-plausible-numbers"></a>

## গ্রহণযোগ্য মান থাকা সত্ত্বেও সাংখ্যিক যোগফল নেই

`sample_stale`, `sample_future`, `sample_skew`, `sample_missing`, `incomplete_coverage`, `unit_dimension`, `scope_overlap` পরীক্ষা করুন। প্রকৃত উৎস তাজা করুন এবং পরিমাপের সময় রাখুন। অনুমোদিত বয়স বাড়ালে নীতি বদলায়, পরিমাপ ঠিক হয় না। পূর্ণ যোগফল ঘোষিত পাতার বিপরীতে মূল্যায়িত: ঘোষণাও পরীক্ষা করুন।

![নমুনার মানের কৃত্রিম সময়রেখা](../images/sample-quality.svg)

<a id="energy-decreased-at-midnight"></a>

## মধ্যরাতে শক্তি কমেছে

কমা সত্যিকারের রিসেট, প্রতিস্থাপন বা সংশোধন হতে পারে। নীতি ঘোষণা করুন এবং বাস্তব উৎসপ্রমাণ থেকে `reset_at` যোগ করুন। HA রিপ্লের সময় রিসেট চিহ্ন নয়। চিহ্নযুক্ত নিট শক্তির জন্য `total_increasing` উপযুক্ত নয়। ভিন্ন সূচনার কাউন্টার যোগ করা হয় না।

<a id="voltage-looks-calibrated-but-watts-still-differ"></a>

## ভোল্টেজ ক্যালিব্রেটেড মনে হয়, কিন্তু ওয়াট আলাদা

ক্যালিব্রেশন রাশিনির্দিষ্ট। ভোল্টেজ সংশোধন তড়িৎপ্রবাহ, ফেজ সম্পর্ক, ক্ষমতা বা সঞ্চিত শক্তি যাচাই করে না। গুণকের ক্ষেত্র শুধু নথি: মানে কাঙ্ক্ষিত সংশোধন আগে থেকেই থাকতে হবে।

<a id="yaml-fails-although-another-parser-accepts-it"></a>

## অন্য পার্সার নিলেও YAML ব্যর্থ

সময়চিহ্ন উদ্ধৃতিতে রাখুন, অ্যালিয়াস/অ্যাঙ্কর/নিজস্ব ট্যাগ ও পুনরাবৃত্ত কী সরান, সসীম সংখ্যা দিন। টাইপের ভুল ধরতে অজানা ক্ষেত্র ত্রুটি। দুই বিন্যাসেই সীমা প্রযোজ্য। দ্ব্যর্থক YAML স্কেলার সমস্যা করলে বিনিময়ে JSON ব্যবহার করুন।

<a id="ha-import-fails-on-timestamps"></a>

## সময়চিহ্নে HA আমদানি ব্যর্থ

`timestamp_attribute` প্রকৃত পরিমাপসময়ের অ্যাট্রিবিউটে দিন। `last_reported` শুধু HA-তে গ্রহণ প্রমাণ করে। উৎসসময় ছাড়া সরঞ্জাম তাজা থাকা নির্ধারণ করতে পারে না; নমুনা অনুপলব্ধ রাখুন। পরীক্ষা করার টোকেন বা সংযোগ নেই: আমদানি অফলাইন।

<a id="safe-issue-report"></a>

## নিরাপদ সমস্যা প্রতিবেদন

প্যাকেজ/Python সংস্করণ, স্থায়ী কোড, ন্যূনতম কৃত্রিম কনট্র্যাক্ট, বাছা `--at`, প্রত্যাশিত ও বাস্তব ফল দিন। পূর্ণ HA এক্সপোর্ট, টোকেন, প্রকৃত ঠিকানা, পরিবারের সময়সূচি বা ব্যক্তিগত যন্ত্র ID দেবেন না। পুনরুৎপাদনে 0 W এবং অনুপলব্ধ নমুনা আলাদা থাকতে হবে।
