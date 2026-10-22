<a id="usage"></a>

# ব্যবহার

<!-- language-navigation:start -->
<p dir="ltr">
<a href="../usage.md" lang="en" dir="ltr">English</a> ·
<a href="../ar/usage.md" lang="ar" dir="rtl">العربية</a> ·
<a href="usage.md" lang="bn" dir="ltr">বাংলা</a> ·
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
<a id="audit"></a>

## নিরীক্ষা

```sh
ha-meter-contracts check contract.json --json --lang en
ha-meter-contracts check examples/minimal.yaml --at 2026-01-01T12:00:05Z --lang es
```

`--at` সময় অঞ্চলসহ ISO 8601 সময়চিহ্ন গ্রহণ করে। ডিফল্ট বর্তমান UTC। একই ইনপুট, সময় ও ভাষায় JSON নির্ধারিত। নমুনা `freshness_seconds` সীমাসহ তাজা থাকে; তার পরেই পুরোনো হয়। ভবিষ্যতের নমুনা অবৈধ, ঘড়ির পার্থক্যের জন্য কোনো গোপন ছাড় নেই।

প্রস্থান কোড: 0 = ত্রুটি/সতর্কতা নেই; 1 = অর্থগত বা নমুনার মানগত সমস্যা; 2 = ইনপুট/CLI ত্রুটি। অব্যবহৃত অ্যালিয়াসের মতো তথ্যমূলক ফল ব্যর্থতা ঘটায় না। `--json` রিপোর্ট ও ইনপুট ত্রুটির অবজেক্ট stdout-এ লেখে। এটি ছাড়া নিরীক্ষার লেখা stdout-এ এবং ইনপুট ত্রুটি stderr-এ যায়। ভাঙা আউটপুট পাইপ 2 ফেরায়।

ফল লুকাতে CI-তে `|| true` ব্যবহার করবেন না। ইচ্ছাকৃত অবৈধ উদাহরণে স্পষ্টভাবে প্রস্থান 1 যাচাই করা উচিত। সহায়তা ও সংস্করণ 0 ফেরায়। `import-ha` সবসময় JSON কনট্র্যাক্ট লেখে; `--json` তার স্কিমা বদলায় না।

<a id="python-library"></a>

## Python লাইব্রেরি

```python
from datetime import datetime, timezone
from ha_meter_contracts import audit, load_document, parse_contract

contract = parse_contract(load_document("examples/valid-three-meters.json"))
report = audit(contract, at=datetime(2026, 1, 1, 12, 0, 5, tzinfo=timezone.utc))
assert report["sums"][0]["value"] == 720
```

`parse_contract` অপরিবর্তনীয় ডেটাক্লাস তৈরি করে; `InputError` দেয় `code`, `path`, `params`। প্রতিটি অবিশ্বস্ত ইনপুট সীমানায় পার্সার ব্যবহার করুন। `audit` যাচাইকৃত `Contract` আশা করে এবং ফল অনুবাদ করে না। CLI স্থানীয়কৃত `message` মান যোগ করে। লাইব্রেরিতে কলকারী স্পষ্টভাবে মূল্যায়নের সময় বেছে নেন। কোনো API ইনপুট বদলায় না বা ফাইল লেখে না।

<a id="offline-home-assistant-adapter"></a>

## অফলাইন Home Assistant অ্যাডাপ্টার

```sh
ha-meter-contracts import-ha examples/ha-contract.json --ha-states examples/ha-states.synthetic.json > /tmp/meter-contract.json
ha-meter-contracts check /tmp/meter-contract.json --at 2026-01-01T12:00:05Z --json
```

প্রতিটি কাঙ্ক্ষিত মিটারে `entity_id` ও `timestamp_attribute` ম্যাপ করুন। এক্সপোর্ট হলো `entity_id`, `state`, `attributes`-সহ HA অবস্থার অ্যারে। ম্যাপ করা অ্যাট্রিবিউটে সময় অঞ্চলসহ মূল ISO পরিমাপের সময় থাকতে হবে। `attributes.unit_of_measurement`-এর মাত্রা একই হতে হবে; W/kW ও Wh/kWh কনট্র্যাক্টের এককে রূপান্তরিত হয়।

শুধু ম্যাপ করা মান ও উৎসের সময় কপি হয়। ব্যবহারবান্ধব নামসহ অন্য অ্যাট্রিবিউট উপেক্ষিত। কঠোরভাবে নতুন নমুনা বিদ্যমানটিকে `previous`-এ সরায়। একই উৎসসময়ে একই মান আবার দিলে ফল অপরিবর্তিত; পুরোনো নমুনা বা একই সময়ে বিরোধী মান `ha_sample_order` হিসেবে প্রত্যাখ্যাত। অনুপস্থিত এনটিটি ও `unknown`/`unavailable` অবস্থা নমুনা মুছে দেয়; শূন্যে বদলায় না। সময় অনুপস্থিত, অসামঞ্জস্যপূর্ণ একক, বিকৃত মান বা পুনরাবৃত্ত এনটিটি ID আমদানিকে 2 দিয়ে ব্যর্থ করে। ম্যাপ না করা মিটার অপরিবর্তিত। ব্যক্তিগত কনট্র্যাক্টে এনটিটি ID থাকতে পারে; প্রকাশ্য উদাহরণে কৃত্রিম পরিচয় থাকে।

সাধারণ HA এক্সপোর্টে প্রায়ই মূল সময়চিহ্ন থাকে না। সেক্ষেত্রে অ্যাডাপ্টার ইচ্ছাকৃতভাবে তা বানাতে অস্বীকার করে। সময়চিহ্নযুক্ত যন্ত্রের ডেটা নিন বা মিটার অনুপলব্ধ রাখুন। HA গ্রহণ/আপডেটের সময় যন্ত্রের পরিমাপ গ্রহণ প্রমাণ করে না। অ্যাডাপ্টার কখনো `/api/states`-এ সংযোগ করে না বা টোকেন পড়ে না। HA থেকে শক্তির রিসেট চিহ্ন কপি করে না; শক্তি যোগের আগে আলাদাভাবে যাচাইকৃত প্রমাণ যোগ করুন।

<a id="suggested-workflow"></a>

## প্রস্তাবিত কর্মপ্রবাহ

1. তারের সংযোগের নথি থেকে ভৌত পরিসরের গাছ ও উৎসপরিচয় ঘোষণা করুন।
2. একটি মিটার ও স্থির কৃত্রিম উদাহরণ দিয়ে শুরু করুন।
3. শুধু প্রয়োজনীয় পর্যবেক্ষণ ব্যক্তিগত ফাইলে এক্সপোর্ট করুন।
4. নিরীক্ষা চালিয়ে নির্ভরশীল অটোমেশন বদলানোর আগে প্রতিটি ফল পর্যালোচনা করুন।
5. স্থানান্তরের সময় মূল সময় ও ক্যালিব্রেশন প্রমাণ সংরক্ষণ করুন।

প্যাকেজ মেরামত করে না, এনটিটির নাম বদলায় না, যন্ত্র রিসেট করে না বা অটোমেশন স্থাপন করে না।
