<a id="usage"></a>

# उपयोग

<!-- language-navigation:start -->
<p dir="ltr">
<a href="../usage.md" lang="en" dir="ltr">English</a> ·
<a href="../ar/usage.md" lang="ar" dir="rtl">العربية</a> ·
<a href="../bn/usage.md" lang="bn" dir="ltr">বাংলা</a> ·
<a href="../cs/usage.md" lang="cs" dir="ltr">Čeština</a> ·
<a href="../de/usage.md" lang="de" dir="ltr">Deutsch</a> ·
<a href="../es/usage.md" lang="es" dir="ltr">Español</a> ·
<a href="../fa/usage.md" lang="fa" dir="rtl">فارسی</a> ·
<a href="../fr/usage.md" lang="fr" dir="ltr">Français</a> ·
<a href="../he/usage.md" lang="he" dir="rtl">עברית</a> ·
<a href="usage.md" lang="hi" dir="ltr">हिन्दी</a> ·
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

## ऑडिट

```sh
ha-meter-contracts check contract.json --json --lang en
ha-meter-contracts check examples/minimal.yaml --at 2026-01-01T12:00:05Z --lang es
```

`--at` समय-क्षेत्र सहित ISO 8601 समयचिह्न स्वीकार करता है। डिफ़ॉल्ट वर्तमान UTC है। समान इनपुट, समय और भाषा पर JSON नियतात्मक है। नमूना `freshness_seconds` सीमा तक, उसे शामिल करके, ताज़ा रहता है; उसके बाद ही पुराना होता है। भविष्य का नमूना अमान्य है, घड़ी के अंतर के लिए कोई छिपी छूट नहीं।

निकास कोड: 0 = कोई त्रुटि/चेतावनी नहीं; 1 = अर्थगत या नमूना-गुणवत्ता समस्या; 2 = इनपुट/CLI त्रुटि। अप्रयुक्त उपनाम जैसी जानकारी विफलता नहीं बनती। `--json` रिपोर्ट और इनपुट त्रुटि ऑब्जेक्ट stdout पर लिखता है। इसके बिना ऑडिट पाठ stdout और इनपुट त्रुटियाँ stderr पर जाती हैं। टूटी आउटपुट पाइप 2 लौटाती है।

निष्कर्ष छिपाने के लिए CI में `|| true` न उपयोग करें। जानबूझकर अमान्य उदाहरणों को निकास 1 स्पष्ट रूप से जाँचना चाहिए। सहायता और संस्करण 0 लौटाते हैं। `import-ha` हमेशा JSON कॉन्ट्रैक्ट लिखता है; `--json` उसकी स्कीमा नहीं बदलता।

<a id="python-library"></a>

## Python लाइब्रेरी

```python
from datetime import datetime, timezone
from ha_meter_contracts import audit, load_document, parse_contract

contract = parse_contract(load_document("examples/valid-three-meters.json"))
report = audit(contract, at=datetime(2026, 1, 1, 12, 0, 5, tzinfo=timezone.utc))
assert report["sums"][0]["value"] == 720
```

`parse_contract` अपरिवर्तनीय डेटाक्लास बनाता है; `InputError`, `code`, `path`, `params` उपलब्ध कराता है। हर अविश्वसनीय इनपुट सीमा पर पार्सर उपयोग करें। `audit` सत्यापित `Contract` की अपेक्षा करता है और निष्कर्षों का अनुवाद नहीं करता। CLI स्थानीयकृत `message` मान जोड़ता है। लाइब्रेरी में कॉलर मूल्यांकन समय स्पष्ट रूप से चुनता है। कोई API इनपुट नहीं बदलता या फ़ाइल नहीं लिखता।

<a id="offline-home-assistant-adapter"></a>

## ऑफ़लाइन Home Assistant अडैप्टर

```sh
ha-meter-contracts import-ha examples/ha-contract.json --ha-states examples/ha-states.synthetic.json > /tmp/meter-contract.json
ha-meter-contracts check /tmp/meter-contract.json --at 2026-01-01T12:00:05Z --json
```

हर वांछित मीटर पर `entity_id` और `timestamp_attribute` मैप करें। एक्सपोर्ट HA स्थितियों की ऐरे है जिसमें `entity_id`, `state` और `attributes` हैं। मैप किए गए एट्रिब्यूट में समय-क्षेत्र सहित मूल ISO मापन समय होना चाहिए। `attributes.unit_of_measurement` की विमा समान हो; W/kW और Wh/kWh कॉन्ट्रैक्ट इकाई में बदलते हैं।

केवल मैप किए मान और स्रोत समय कॉपी होते हैं। पठनीय नाम समेत अन्य एट्रिब्यूट अनदेखे होते हैं। निश्चित रूप से नया नमूना मौजूदा नमूने को `previous` में भेजता है। समान स्रोत समय पर समान मान दोहराना इडेम्पोटेंट है; पुराना नमूना या उसी समय विरोधी मान `ha_sample_order` के रूप में अस्वीकार होता है। गायब इकाइयाँ और `unknown`/`unavailable` स्थितियाँ नमूना हटा देती हैं; शून्य नहीं बनतीं। गायब समय, असंगत इकाई, विकृत मान या दोहराया इकाई ID आयात को 2 से विफल करते हैं। गैर-मैप किए मीटर अपरिवर्तित रहते हैं। निजी कॉन्ट्रैक्ट में इकाई ID हो सकते हैं; सार्वजनिक उदाहरण कृत्रिम पहचानकर्ता उपयोग करते हैं।

सामान्य HA एक्सपोर्ट में अक्सर मूल समयचिह्न नहीं होता। उस स्थिति में अडैप्टर जानबूझकर उसे गढ़ने से मना करता है। समय सहित उपकरण डेटा लें या मीटर अनुपलब्ध रहने दें। HA प्राप्ति/अपडेट समय उपकरण के मापन का प्रमाण नहीं। अडैप्टर कभी `/api/states` से नहीं जुड़ता और टोकन नहीं पढ़ता। वह HA से ऊर्जा रीसेट चिह्न कॉपी नहीं करता; ऊर्जा जोड़ने से पहले सत्यापित साक्ष्य अलग से जोड़ें।

<a id="suggested-workflow"></a>

## सुझाया कार्यप्रवाह

1. वायरिंग दस्तावेज़ से भौतिक दायरा-वृक्ष और स्रोत की पहचान घोषित करें।
2. एक मीटर और स्थिर कृत्रिम उदाहरण से शुरू करें।
3. केवल आवश्यक अवलोकन निजी फ़ाइल में एक्सपोर्ट करें।
4. ऑडिट चलाएँ और आगे की स्वचालन व्यवस्था बदलने से पहले हर निष्कर्ष जाँचें।
5. माइग्रेशन के दौरान मूल समय और अंशांकन साक्ष्य सुरक्षित रखें।

पैकेज सुधार नहीं करता, इकाइयों का नाम नहीं बदलता, उपकरण रीसेट नहीं करता या स्वचालन तैनात नहीं करता।
