<a id="contract-schema-v1"></a>

# কনট্র্যাক্ট স্কিমা v1

<!-- language-navigation:start -->
<p dir="ltr">
<a href="../schema.md" lang="en" dir="ltr">English</a> ·
<a href="../ar/schema.md" lang="ar" dir="rtl">العربية</a> ·
<a href="schema.md" lang="bn" dir="ltr">বাংলা</a> ·
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
যন্ত্রপাঠ্য [schema.json](../../schema.json) কাঠামো বর্ণনা করে। সীমার ক্ষেত্রে Python পার্সারই প্রামাণ্য; `audit` ভৌত ও সময়গত অর্থ যোগ করে যা JSON Schema প্রমাণ করতে পারে না। `python3 scripts/generate_schema.py` দিয়ে কাঠামোর ফাইল তৈরি করুন।

<a id="root-and-limits"></a>

## মূল ও সীমা

আবশ্যক: পূর্ণসংখ্যা `schema_version: 1`, `scopes`, `meters`। ঐচ্ছিক: `sums` (ডিফল্ট খালি)। অজানা ক্ষেত্র সব স্তরে প্রত্যাখ্যাত। সর্বোচ্চ 512 পরিসর, 512 মিটার ও 128 যোগফল; পরিসর ও মিটার খালি হতে পারবে না। প্রতিটি যোগফলে 1–512 সদস্য। UTF-8 ইনপুট, সর্বোচ্চ 1,048,576 বাইট, গভীরতা 16 এবং 20,000 মান-নোড। পুনরাবৃত্ত JSON কী, NaN/Infinity এবং YAML অ্যালিয়াস/অ্যাঙ্কর/স্পষ্ট ট্যাগ প্রত্যাখ্যাত। YAML সময়চিহ্ন উদ্ধৃতিতে রাখুন যাতে স্ট্রিং থাকে।

পরিচয় 1–96 ASCII অক্ষর: প্রথমে বর্ণ/অঙ্ক, তারপর বর্ণ, অঙ্ক, `.`, `_`, `-`। প্রতিটি সংগ্রহে ID অনন্য; পরিসর ও মিটারের পৃথক নামস্থান। সব সময়ে `T` ও সময় অঞ্চল থাকে। সংখ্যা সসীম, বুলিয়ান নয়, এবং আরও কঠোর সীমা না থাকলে ±10^15-এর মধ্যে।

<a id="physical-scopes"></a>

## ভৌত পরিসর

প্রতিটি পরিসরে `id`, `kind` (`site`, `circuit`, `strip`, `outlet`, `load`) ও ঐচ্ছিক `parent` আছে। অভিভাবক থাকতে হবে এবং চক্রহীন বন গঠন করতে হবে। অভিভাবকের মিটার সব বংশধরকে অন্তর্ভুক্ত করে। পরিসরের ধরন বর্ণনামূলক: এগুলো ভোল্টেজ, ফেজ, রেটিং, তারের সংযোগ বা অনুমোদিত অভিভাবক নির্ণয় করে না। প্রকৃত টপোলজি ব্যবহারকারী ঘোষণা করেন।

<a id="meters"></a>

## মিটার

আবশ্যক ক্ষেত্র:

- `id`, `scope`: অনন্য পাঠের পরিচয় এবং ঘোষিত ভৌত পরিসর।
- `quantity`: `power`, `energy`, `voltage`, `current`।
- `unit`: যথাক্রমে W/kW, Wh/kWh, V, A। পার্সার শব্দতালিকা গ্রহণ করে; নিরীক্ষক মাত্রা যাচাই করে।
- `kind`: `measured` বা `estimated`। এটি ঘোষণা, পরীক্ষাগারের যাচাই নয়।
- `provenance`: ভৌত পরিমাপপ্রবাহের স্থায়ী পরিচয়, তার HA/MQTT উপস্থাপনার **নয়**। অ্যালিয়াস পাঠ একই পরিচয় ব্যবহার করে। এক উৎসপরিচয়ে ভিন্ন চিহ্ন/রাশি/পরিসর সংঘাত সৃষ্টি করে; ইনপুটের ক্রম নির্বিশেষে প্রবাহের সব অ্যালিয়াস যোগফলের জন্য অনুপলব্ধ হয়। সত্যিকার ভিন্ন ভৌত চ্যানেলে ভিন্ন উৎসপরিচয় বেছে নিন।
- `sign`: শুধু ব্যবহার/আমদানি/রপ্তানির মানের জন্য `nonnegative`; ঘোষিত দ্বিমুখী প্রবাহে `signed`। এই সংস্করণ কোন ভৌত দিক ধনাত্মক তা নির্ণয় করে না।
- `state_class`: `measurement`, `total`, `total_increasing`।
- `freshness_seconds`: ধনাত্মক সর্বোচ্চ বয়স, 0.001–604800 সেকেন্ড।

ঐচ্ছিক `reset`: `never`, `periodic`, `device_restart`, `unknown`, `not_applicable` (ডিফল্ট)। শক্তির জন্য `not_applicable`-এর বাইরে স্পষ্ট নীতি এবং total ধরনের স্টেট ক্লাস চাই। চিহ্নযুক্ত শক্তি `total_increasing` ব্যবহার করতে পারে না। অন্যান্য রাশিতে `measurement` ও `not_applicable` চাই।

ঐচ্ছিক `sample`, `previous`: null বা `value` (সংখ্যা বা null), `measured_at`, ঐচ্ছিক `reset_at`-সহ অবজেক্ট। আগের নমুনা পুরোনো হতে হবে। অঋণাত্মক কাউন্টার কমলে নমুনার মাঝখানে রিসেট চিহ্ন চাই; `never` তা প্রত্যাখ্যান করে। `reset_at` নিজের নমুনার পরের হতে পারে না এবং শুধু শক্তিতে প্রযোজ্য। অজানা রিসেট অর্থ সতর্কতা দেয়। চিহ্নযুক্ত নিট কাউন্টার বৈধভাবে কমতে পারে; সঠিক ভিত্তি উৎপাদকের দায়িত্বেই থাকে।

ঐচ্ছিক `calibration`: `quantity`, ধনাত্মক `factor` (10^-12–10^12), কৃত্রিম/ব্যক্তিগত পরিচয় `reference`, `verified_at`। ঠিক ওই রাশির প্রমাণ নথিভুক্ত করে। মান **আগেই ক্যালিব্রেটেড**: যাচাইকারী কখনো গুণক আবার প্রয়োগ করে না। ভবিষ্যতের ক্যালিব্রেশন বা ক্ষমতার মিটারে ভোল্টেজ ক্যালিব্রেশন অবৈধ। ক্যালিব্রেশন না থাকা নির্ভুলতা প্রমাণ করে না এবং নিজে থেকেই ত্রুটি নয়।

ঐচ্ছিক `entity_id`, `timestamp_attribute`: অফলাইন HA ম্যাপিং; [ব্যবহার](usage.md#offline-home-assistant-adapter) দেখুন।

<a id="sums"></a>

## যোগফল

আবশ্যক: `id`, লক্ষ্য `scope`, `meters`-এ মিটার ID-র তালিকা, `quantity` (`power` বা `energy`), `coverage` (`partial` বা `complete`)। ঐচ্ছিক `max_skew_seconds`: 0–604800, ডিফল্ট 2।

সদস্য লক্ষ্য পরিসরের মধ্যে থাকতে হবে, সামঞ্জস্যপূর্ণ মাত্রা ও চিহ্নের অর্থ রাখতে হবে, ভিন্ন ভৌত প্রবাহ ব্যবহার করতে হবে এবং অভিভাবক/সন্তান বা অভিন্ন পরিসর হিসেবে ওভারল্যাপ করা চলবে না। পূর্ণ যোগফল লক্ষ্যের নিচের প্রতিটি **ঘোষিত পাতা-পরিসর** অন্তর্ভুক্ত করে। অঘোষিত তারের সংযোগ আবিষ্কার করা যায় না। আংশিক যোগফল স্পষ্টভাবে আংশিক অন্তর্ভুক্তি ঘোষণা করে। নেস্টেড যোগফল সমর্থিত নয়; সদস্য সবসময় মিটারকে নির্দেশ করে।

প্রতিটি সদস্যে বৈধ ও তাজা ডেটা চাই; পরিমাপ গ্রহণের সময় অনুমোদিত ব্যবধানের মধ্যে হতে হবে। শক্তিতে অভিন্ন স্পষ্ট `reset_at` সূচনাও চাই। এটি ঘোষিত সামঞ্জস্য পরীক্ষা করে, ঐতিহাসিক সঞ্চয়ের নির্ভুলতা নয়। যোগফল W বা Wh-এ রূপান্তরিত হয়। তড়িৎপ্রবাহ ও ভোল্টেজের যোগফল ইচ্ছাকৃতভাবে সমর্থিত নয়, কারণ তা সার্কিটের টপোলজির ওপর নির্ভর করে।

প্রয়োজনীয় প্রমাণ না থাকলে বা অর্থগত পরীক্ষা ব্যর্থ হলে সাংখ্যিক যোগফল অনুপলব্ধ। অনুমান `kind: estimated` হিসেবে ছড়ায়। তালিকায় দুই অ্যালিয়াস একসঙ্গে থাকতে পারে, কিন্তু দুটোই এক যোগফলে অবদান দিতে পারে না। আলাদা অপরিমাপকৃত সকেটের মোট অনুমান করা হয় না।

<a id="report-v1"></a>

## রিপোর্ট v1

মূল: `schema_version`, UTC-তে স্বাভাবিকীকৃত মূল্যায়নের সময় `at`, `summary`-তে গুরুত্বভিত্তিক গণনা, সাজানো `findings` ও `sums`। প্রতিটি ফলাফলে `code`, `severity`, JSON-ধাঁচের `path`, কাঠামোবদ্ধ `params`; CLI যোগ করে `message`। প্রতিটি যোগফলে `id`, `scope`, `quantity`, মূল `unit`, `value`, `status`, `kind`, `coverage`। অজানা মান JSON null, কখনো NaN নয়।
