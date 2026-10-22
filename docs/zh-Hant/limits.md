<a id="limits-and-trust-boundary"></a>

# 限制與信任邊界

<!-- language-navigation:start -->
<p dir="ltr">
<a href="../limits.md" lang="en" dir="ltr">English</a> ·
<a href="../ar/limits.md" lang="ar" dir="rtl">العربية</a> ·
<a href="../bn/limits.md" lang="bn" dir="ltr">বাংলা</a> ·
<a href="../cs/limits.md" lang="cs" dir="ltr">Čeština</a> ·
<a href="../de/limits.md" lang="de" dir="ltr">Deutsch</a> ·
<a href="../es/limits.md" lang="es" dir="ltr">Español</a> ·
<a href="../fa/limits.md" lang="fa" dir="rtl">فارسی</a> ·
<a href="../fr/limits.md" lang="fr" dir="ltr">Français</a> ·
<a href="../he/limits.md" lang="he" dir="rtl">עברית</a> ·
<a href="../hi/limits.md" lang="hi" dir="ltr">हिन्दी</a> ·
<a href="../id/limits.md" lang="id" dir="ltr">Bahasa Indonesia</a> ·
<a href="../it/limits.md" lang="it" dir="ltr">Italiano</a> ·
<a href="../ja/limits.md" lang="ja" dir="ltr">日本語</a> ·
<a href="../ko/limits.md" lang="ko" dir="ltr">한국어</a> ·
<a href="../nl/limits.md" lang="nl" dir="ltr">Nederlands</a> ·
<a href="../pl/limits.md" lang="pl" dir="ltr">Polski</a> ·
<a href="../pt/limits.md" lang="pt" dir="ltr">Português</a> ·
<a href="../ru/limits.md" lang="ru" dir="ltr">Русский</a> ·
<a href="../th/limits.md" lang="th" dir="ltr">ไทย</a> ·
<a href="../tr/limits.md" lang="tr" dir="ltr">Türkçe</a> ·
<a href="../uk/limits.md" lang="uk" dir="ltr">Українська</a> ·
<a href="../vi/limits.md" lang="vi" dir="ltr">Tiếng Việt</a> ·
<a href="../zh-Hans/limits.md" lang="zh-Hans" dir="ltr">简体中文</a> ·
<a href="limits.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->
這是離線宣告驗證器，不是保護控制器、電工測試儀、佈線發現服務，也不是執行動作的 Home Assistant 整合。

- 一個總測量值無法還原三個未知負載同時發生的精確功率。統計猜測只能是估計，不能作為保護級測量。
- 範圍、來源身份、符號方向及校準宣告來自操作員。虛假宣告可能使物理上無效的系統在結構上顯得有效。
- `complete` 表示相對於已宣告葉節點完整，不表示佈線經過獨立驗證。來源重置標記是受信任的證據，不是裝置認證。
- 支援 W、kW、Wh、kWh、V 和 A。不建模無功/視在功率、三相代數、CT 飽和、電壓互感器、計數器回捲或電價。
- 求和成員是直接儀表，不能是其他求和。功率求和需要時間戳對齊；電能求和需要共同的顯式計數起點和對齊樣本。
- 數值是有限浮點數。這不是計費級十進位制記賬系統。校準因子只記錄，不應用。
- 只檢查當前樣本和可選的前一樣本。這不是歷史資料庫、異常檢測器、漂移檢測器，也不是完整計數器完整性審計。
- HA 來源時間戳必須存在且真正表示採集時間，不會悄悄接受快取接收時間作為替代。
- JSON/YAML 載入有限制；庫的 `audit` API 期望解析器生成的 `Contract`。不要從不可信物件任意構造格式錯誤的 dataclass。
- 檔案輸入僅接受常規檔案。拒絕末級路徑符號連結、FIFO、裝置及目錄，以非阻塞方式開啟，並在讀取前檢查已開啟的描述符。缺少 `O_NOFOLLOW` 和 `O_NONBLOCK` 的平臺拒絕檔案輸入；在這些平臺，應對已限制大小的字串使用 `ha_meter_contracts.reader.loads_document`。父目錄符號連結不是沙箱邊界。即使讀取期間檔案增大，仍執行位元組上限。
- 檢查透過不能證明物理繼電器、閥門、電機、泵流量或電氣安全。不會自動修復或重試。

輸入和輸出可能包含操作員提供的實體 ID 和時間。真實契約/匯出應保持私有。倉庫僅包含合成示例。程式不上傳資料，但將報告重定向到外部服務是操作員自己的選擇。
