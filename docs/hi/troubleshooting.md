<a id="troubleshooting"></a>

# समस्या समाधान

<!-- language-navigation:start -->
<p dir="ltr">
<a href="../troubleshooting.md" lang="en" dir="ltr">English</a> ·
<a href="../ar/troubleshooting.md" lang="ar" dir="rtl">العربية</a> ·
<a href="../bn/troubleshooting.md" lang="bn" dir="ltr">বাংলা</a> ·
<a href="../cs/troubleshooting.md" lang="cs" dir="ltr">Čeština</a> ·
<a href="../de/troubleshooting.md" lang="de" dir="ltr">Deutsch</a> ·
<a href="../es/troubleshooting.md" lang="es" dir="ltr">Español</a> ·
<a href="../fa/troubleshooting.md" lang="fa" dir="rtl">فارسی</a> ·
<a href="../fr/troubleshooting.md" lang="fr" dir="ltr">Français</a> ·
<a href="../he/troubleshooting.md" lang="he" dir="rtl">עברית</a> ·
<a href="troubleshooting.md" lang="hi" dir="ltr">हिन्दी</a> ·
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

## तीन सॉकेट की पट्टी तीन शक्ति रीडिंग नहीं देती

`scope_outside` का अर्थ है कि माँगा गया अलग परिणाम व्यापक माप उपयोग करता है। पूरी पट्टी के लिए एक इकाई रखें। अलग शक्ति के लिए सही दायरे वाले स्वतंत्र माप चाहिए। चालू रिले भार की खपत सिद्ध नहीं करता; बिजली लेता पंप पानी का प्रवाह सिद्ध नहीं करता।

<a id="a-migrated-sensor-doubles-the-total"></a>

## माइग्रेट किया सेंसर कुल को दोगुना करता है

केवल `alias_stream` जानकारी है। `duplicate_stream` का अर्थ है कि दोनों प्रतियाँ योग में हैं। एक ही CT की प्रतियों को समान स्रोत-पहचान दें और योग में केवल एक रखें। केवल जाँच शांत करने के लिए स्रोत-पहचान न बदलें।

![एक स्रोत और दो निरूपण](../images/duplicate-stream.svg)

<a id="no-numeric-sum-despite-individually-plausible-numbers"></a>

## उचित मानों के बावजूद संख्यात्मक योग नहीं

`sample_stale`, `sample_future`, `sample_skew`, `sample_missing`, `incomplete_coverage`, `unit_dimension`, `scope_overlap` जाँचें। वास्तविक स्रोत ताज़ा करें और मापन समय सुरक्षित रखें। अनुमत आयु बढ़ाने से नीति बदलती है, माप ठीक नहीं होता। पूर्ण योग घोषित पत्तियों के सापेक्ष आँका जाता है: घोषणा भी जाँचें।

![नमूना गुणवत्ता की कृत्रिम समयरेखा](../images/sample-quality.svg)

<a id="energy-decreased-at-midnight"></a>

## आधी रात ऊर्जा घट गई

गिरावट वास्तविक रीसेट, बदलाव या सुधार हो सकती है। नीति घोषित करें और वास्तविक स्रोत साक्ष्य से `reset_at` जोड़ें। HA रीप्ले का समय रीसेट चिह्न नहीं। `total_increasing` चिह्नित नेट ऊर्जा के योग्य नहीं। अलग आरंभ वाले काउंटर नहीं जोड़े जाते।

<a id="voltage-looks-calibrated-but-watts-still-differ"></a>

## वोल्टेज अंशांकित लगता है, लेकिन वाट अलग हैं

अंशांकन राशि-विशिष्ट है। वोल्टेज सुधार करंट, फेज़ संबंध, शक्ति या संचित ऊर्जा की पुष्टि नहीं करता। गुणांक फ़ील्ड केवल दस्तावेज़ है: मानों में इच्छित सुधार पहले से होना चाहिए।

<a id="yaml-fails-although-another-parser-accepts-it"></a>

## दूसरा पार्सर स्वीकार करता है, फिर भी YAML विफल है

समयचिह्न उद्धरणों में रखें, उपनाम/एंकर/कस्टम टैग और दोहराई कुंजियाँ हटाएँ, परिमित संख्याएँ उपयोग करें। टाइपिंग गलतियाँ पकड़ने के लिए अज्ञात फ़ील्ड त्रुटि हैं। सीमाएँ दोनों प्रारूपों पर लागू हैं। संदिग्ध YAML स्केलर समस्या करें तो आदान-प्रदान में JSON उपयोग करें।

<a id="ha-import-fails-on-timestamps"></a>

## HA आयात समयचिह्न पर विफल है

`timestamp_attribute` वास्तविक मापन समय के एट्रिब्यूट पर सेट करें। `last_reported` केवल HA द्वारा प्राप्ति का प्रमाण है। स्रोत समय के बिना उपकरण ताज़गी तय नहीं कर सकता; नमूना अनुपलब्ध छोड़ें। जाँचने के लिए टोकन या कनेक्शन नहीं हैं: आयात ऑफ़लाइन है।

<a id="safe-issue-report"></a>

## सुरक्षित समस्या रिपोर्ट

पैकेज/Python संस्करण, स्थिर कोड, न्यूनतम कृत्रिम कॉन्ट्रैक्ट, चुना `--at`, अपेक्षित और वास्तविक परिणाम शामिल करें। पूर्ण HA एक्सपोर्ट, टोकन, वास्तविक पता, घरेलू समय-सारणी या निजी उपकरण ID न जोड़ें। पुनरुत्पादन में 0 W और अनुपलब्ध नमूना अलग रहने चाहिए।
