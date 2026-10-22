<a id="troubleshooting"></a>

# 故障排查

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
<a href="troubleshooting.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->
<a id="a-three-outlet-strip-cannot-produce-three-power-readings"></a>

## 三個插座的插排無法產生三個功率讀數

`scope_outside` 表示請求的單獨結果使用了更大範圍的測量。應保留一個整體插排實體。若需要單獨功率，應增加獨立且範圍正確的測量。繼電器開啟不證明負載在耗電，泵耗電也不證明水在流動。

<a id="a-migrated-sensor-doubles-the-total"></a>

## 遷移後的感測器使總量翻倍

單獨的 `alias_stream` 是資訊項。`duplicate_stream` 表示兩個副本同時進入求和。給同一 CT 的副本相同來源身份，求和只保留一個。不要僅為消除檢查而改變來源身份。

![一個來源與兩種表示](../images/duplicate-stream.svg)

<a id="no-numeric-sum-despite-individually-plausible-numbers"></a>

## 單個數值看似合理卻沒有數值求和

檢查 `sample_stale`、`sample_future`、`sample_skew`、`sample_missing`、`incomplete_coverage`、`unit_dimension`、`scope_overlap`。重新整理原始來源並保留採集時間。延長新鮮度預算是策略更改，不是修復測量。完整求和依據已宣告葉範圍判斷，因此也應審查宣告。

![合成樣本質量時間線](../images/sample-quality.svg)

<a id="energy-decreased-at-midnight"></a>

## 電能在午夜下降

下降可能是真正重置、更換或修正。宣告策略，並根據真實來源證據新增 `reset_at`。HA 重放該值的時間戳不是重置標記。`total_increasing` 不適用於有符號淨電能。起點不同的兩個計數器不會求和。

<a id="voltage-looks-calibrated-but-watts-still-differ"></a>

## 電壓看起來已校準，但瓦數仍不同

校準針對每種物理量。修正電壓不驗證電流、相位關係、功率或累計電能。因子欄位只作記錄，數值必須已經包含預期修正。

<a id="yaml-fails-although-another-parser-accepts-it"></a>

## 其他解析器接受的 YAML 在這裡失敗

給時間戳加引號，移除別名/錨點/自定義標籤及重複鍵，並使用有限數值。未知欄位作為錯誤以發現拼寫問題。兩種格式都適用限制。若 YAML 標量歧義造成不便，交換時使用 JSON。

<a id="ha-import-fails-on-timestamps"></a>

## HA 匯入因時間戳失敗

把 `timestamp_attribute` 設為真正的測量時間屬性。`last_reported` 只能證明 HA 接收。沒有來源時間，工具無法確定新鮮度，應保持樣本不可用。匯入是離線的，因此沒有令牌或網路連通性問題需要排查。

<a id="safe-issue-report"></a>

## 安全報告問題

包含包/Python 版本、穩定發現程式碼、最小合成契約、選擇的 `--at`、期望和實際結果。不要附完整 HA 匯出、令牌、真實地址、家庭作息或私有裝置標識。復現示例必須區分 0 W 和不可用樣本。
