<a id="contract-schema-v1"></a>

# कॉन्ट्रैक्ट स्कीमा v1

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
<a href="../he/schema.md" lang="he" dir="rtl">עברית</a> ·
<a href="schema.md" lang="hi" dir="ltr">हिन्दी</a> ·
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
मशीन-पठनीय [schema.json](../../schema.json) संरचना बताता है। सीमाओं के लिए Python पार्सर प्रामाणिक है; `audit` भौतिक और समयगत अर्थ जोड़ता है जिन्हें JSON Schema सिद्ध नहीं कर सकता। संरचनात्मक फ़ाइल `python3 scripts/generate_schema.py` से बनाएँ।

<a id="root-and-limits"></a>

## मूल और सीमाएँ

आवश्यक: पूर्णांक `schema_version: 1`, `scopes`, `meters`। वैकल्पिक: `sums` (डिफ़ॉल्ट खाली)। अज्ञात फ़ील्ड हर स्तर पर अस्वीकार होते हैं। अधिकतम 512 दायरे, 512 मीटर और 128 योग; दायरे और मीटर खाली नहीं हो सकते। हर योग में 1–512 सदस्य होते हैं। UTF-8 इनपुट, अधिकतम 1,048,576 बाइट, गहराई 16 और 20,000 मान-नोड। दोहराई गई JSON कुंजियाँ, NaN/Infinity और YAML उपनाम/एंकर/स्पष्ट टैग अस्वीकार होते हैं। YAML समयचिह्न उद्धरणों में रखें ताकि वे स्ट्रिंग रहें।

पहचानकर्ता 1–96 ASCII वर्ण के हैं: पहले अक्षर/अंक, फिर अक्षर, अंक, `.`, `_`, `-`। ID हर संग्रह में अद्वितीय हैं; दायरों और मीटरों के अलग नामस्थान हैं। सभी समय में `T` और समय-क्षेत्र शामिल है। संख्याएँ परिमित हैं, बूलियन नहीं, और कठोर सीमा न होने पर ±10^15 के भीतर हैं।

<a id="physical-scopes"></a>

## भौतिक दायरे

हर दायरे में `id`, `kind` (`site`, `circuit`, `strip`, `outlet`, `load`) और वैकल्पिक `parent` होता है। अभिभावक मौजूद हों और अचक्रीय वन बनाएँ। अभिभावक पर मीटर सभी वंशजों को समेटता है। दायरों के प्रकार वर्णनात्मक हैं: वे वोल्टेज, फेज़, रेटिंग, वायरिंग या अनुमत अभिभावक नहीं निकालते। वास्तविक टोपोलॉजी उपयोगकर्ता घोषित करता है।

<a id="meters"></a>

## मीटर

आवश्यक फ़ील्ड:

- `id`, `scope`: अद्वितीय रीडिंग पहचानकर्ता और घोषित भौतिक दायरा।
- `quantity`: `power`, `energy`, `voltage`, `current`।
- `unit`: क्रमशः W/kW, Wh/kWh, V, A। पार्सर शब्दावली स्वीकार करता है; ऑडिटर विमा जाँचता है।
- `kind`: `measured` या `estimated`। यह घोषणा है, प्रयोगशाला सत्यापन नहीं।
- `provenance`: भौतिक मापन प्रवाह की स्थिर पहचान, उसके HA/MQTT निरूपण की **नहीं**। उपनाम रीडिंग इसे साझा करती हैं। एक स्रोत-पहचान के साथ भिन्न चिह्न/राशि/दायरा विरोध उत्पन्न करते हैं; इनपुट क्रम से स्वतंत्र उस प्रवाह के सभी उपनाम योग के लिए अनुपलब्ध हो जाते हैं। सचमुच भिन्न भौतिक चैनलों के लिए अलग स्रोत-पहचान चुनें।
- `sign`: केवल खपत/आयात/निर्यात के परिमाणों के लिए `nonnegative`; घोषित द्विदिश प्रवाह के लिए `signed`। यह संस्करण यह नहीं निकालता कि कौन-सी भौतिक दिशा धनात्मक है।
- `state_class`: `measurement`, `total`, `total_increasing`।
- `freshness_seconds`: धनात्मक अधिकतम आयु, 0.001–604800 सेकंड।

वैकल्पिक `reset`: `never`, `periodic`, `device_restart`, `unknown`, `not_applicable` (डिफ़ॉल्ट)। ऊर्जा के लिए `not_applicable` से अलग स्पष्ट नीति और total-प्रकार की स्थिति कक्षा आवश्यक है। चिह्नित ऊर्जा `total_increasing` नहीं उपयोग कर सकती। अन्य राशियों के लिए `measurement` और `not_applicable` आवश्यक हैं।

वैकल्पिक `sample`, `previous`: null या `value` (संख्या या null), `measured_at`, वैकल्पिक `reset_at` वाला ऑब्जेक्ट। पिछला नमूना पुराना होना चाहिए। गैर-ऋणात्मक काउंटर में गिरावट के लिए नमूनों के बीच रीसेट चिह्न चाहिए; `never` उसे अस्वीकार करता है। `reset_at` अपने नमूने से बाद का नहीं हो सकता और केवल ऊर्जा पर लागू है। अज्ञात रीसेट अर्थ चेतावनी देता है। चिह्नित नेट काउंटर वैध रूप से घट सकता है; सही आधार निर्माता की जिम्मेदारी है।

वैकल्पिक `calibration`: `quantity`, धनात्मक `factor` (10^-12–10^12), कृत्रिम/निजी पहचानकर्ता `reference`, `verified_at`। यह ठीक उसी राशि के लिए साक्ष्य दर्ज करता है। मान **पहले से अंशांकित** हैं: सत्यापक गुणांक दोबारा कभी नहीं लगाता। भविष्य का अंशांकन या शक्ति मीटर पर वोल्टेज अंशांकन अमान्य है। अंशांकन की अनुपस्थिति शुद्धता सिद्ध नहीं करती और अपने आप त्रुटि नहीं है।

वैकल्पिक `entity_id`, `timestamp_attribute`: ऑफ़लाइन HA मैपिंग; [उपयोग](usage.md#offline-home-assistant-adapter) देखें।

<a id="sums"></a>

## योग

आवश्यक: `id`, लक्ष्य `scope`, `meters` में मीटर ID की सूची, `quantity` (`power` या `energy`), `coverage` (`partial` या `complete`)। वैकल्पिक `max_skew_seconds`: 0–604800, डिफ़ॉल्ट 2।

सदस्य लक्ष्य दायरे के भीतर हों, संगत विमा और चिह्न-अर्थ रखें, भिन्न भौतिक प्रवाह उपयोग करें तथा अभिभावक/वंशज या समान दायरों के रूप में न ओवरलैप हों। पूर्ण योग लक्ष्य के नीचे हर **घोषित पत्ती-दायरे** को समेटता है। अघोषित वायरिंग खोजी नहीं जा सकती। आंशिक योग स्पष्ट रूप से आंशिक कवरेज घोषित करता है। नेस्टेड योग समर्थित नहीं; सदस्य हमेशा मीटरों को संदर्भित करते हैं।

हर सदस्य का डेटा वैध और ताज़ा हो; मापन प्राप्ति के समय अनुमत अंतर में हों। ऊर्जा के लिए समान स्पष्ट `reset_at` आरंभ भी आवश्यक हैं। यह घोषित संरेखण जाँचता है, ऐतिहासिक संचय की शुद्धता नहीं। योग W या Wh में बदलते हैं। करंट और वोल्टेज योग जानबूझकर समर्थित नहीं क्योंकि वे परिपथ टोपोलॉजी पर निर्भर हैं।

आवश्यक साक्ष्य न होने या अर्थगत जाँच विफल होने पर संख्यात्मक योग अनुपलब्ध है। अनुमान `kind: estimated` के रूप में आगे बढ़ते हैं। दो उपनाम सूची में साथ हो सकते हैं, लेकिन दोनों एक योग में योगदान नहीं कर सकते। अलग-अलग बिना मापे सॉकेट के लिए कोई कुल नहीं निकाला जाता।

<a id="report-v1"></a>

## रिपोर्ट v1

मूल: `schema_version`, UTC में सामान्यीकृत मूल्यांकन समय `at`, `summary` में गंभीरता की गिनतियाँ, क्रमबद्ध `findings` और `sums`। हर निष्कर्ष में `code`, `severity`, JSON-जैसा `path`, संरचित `params`; CLI `message` जोड़ता है। हर योग में `id`, `scope`, `quantity`, मूल `unit`, `value`, `status`, `kind`, `coverage` होते हैं। अज्ञात मान JSON null हैं, कभी NaN नहीं।
