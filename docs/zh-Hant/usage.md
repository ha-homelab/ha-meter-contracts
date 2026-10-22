<a id="usage"></a>

# 用法

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
<a href="usage.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->
<a id="audit"></a>

## 審計

```sh
ha-meter-contracts check contract.json --json --lang en
ha-meter-contracts check examples/minimal.yaml --at 2026-01-01T12:00:05Z --lang es
```

`--at` 接受含時區的 ISO 8601 時間戳，預設當前 UTC。相同輸入、時間和語言產生確定性的 JSON 輸出。樣本在包含邊界的 `freshness_seconds` 範圍內仍新鮮，只在超過邊界後過期。未來樣本無效，沒有隱含時鐘偏差寬容值。

退出程式碼：0 表示無錯誤/警告；1 表示存在語義或樣本質量發現；2 表示輸入/CLI 錯誤。未使用別名等資訊項不會使檢查失敗。`--json` 將審計報告及輸入錯誤物件都寫到 stdout。未指定時，審計文字到 stdout，輸入錯誤到 stderr。輸出管道斷開返回 2。

不要在 CI 中用 `|| true` 隱藏發現。故意無效的示例應顯式斷言退出 1。幫助和版本退出 0。`import-ha` 始終輸出 JSON 契約；`--json` 不改變其模式。

<a id="python-library"></a>

## Python 庫

```python
from datetime import datetime, timezone
from ha_meter_contracts import audit, load_document, parse_contract

contract = parse_contract(load_document("examples/valid-three-meters.json"))
report = audit(contract, at=datetime(2026, 1, 1, 12, 0, 5, tzinfo=timezone.utc))
assert report["sums"][0]["value"] == 720
```

`parse_contract` 建立凍結 dataclass；`InputError` 暴露 `code`、`path`、`params`。在每個不可信輸入邊界都使用此解析器。`audit` 期望已驗證的 `Contract`，不翻譯發現。CLI 新增本地化 `message` 值。庫呼叫者顯式選擇評估時間。這兩個 API 都不修改輸入，也不寫檔案。

<a id="offline-home-assistant-adapter"></a>

## 離線 Home Assistant 介面卡

```sh
ha-meter-contracts import-ha examples/ha-contract.json --ha-states examples/ha-states.synthetic.json > /tmp/meter-contract.json
ha-meter-contracts check /tmp/meter-contract.json --at 2026-01-01T12:00:05Z --json
```

為每個所需儀表對映 `entity_id` 和 `timestamp_attribute`。匯出是 HA 狀態物件陣列，含 `entity_id`、`state`、`attributes`。對映屬性必須包含帶時區的原始 ISO 測量時間。`attributes.unit_of_measurement` 必須量綱相同；W/kW 和 Wh/kWh 會轉換為契約單位。

只複製已對映數值和來源時間，其他屬性均忽略，包括友好名稱。嚴格更新的樣本會把原樣本移入 `previous`。重放相同來源時間戳和數值是冪等的；更早樣本或同一時間戳下的衝突值會以 `ha_sample_order` 拒絕。缺失實體和 `unknown`/`unavailable` 狀態會清空樣本，而不是變成零。缺失來源時間戳、單位不相容、格式錯誤的值或重複實體 ID 都使匯入以 2 失敗。未對映儀表保持不變。私有契約可含實體 ID；公開示例使用合成識別符號。

普通 HA 匯出經常缺少原始來源時間戳，此時介面卡有意拒絕編造。應獲取帶時間戳的裝置資料，或讓儀表保持不可用。HA 接收/更新時間不能證明裝置採集時間。介面卡絕不連線 `/api/states` 或讀取令牌。它不從 HA 複製電能重置標記；求和電能前須單獨新增已驗證的重置證據。

<a id="suggested-workflow"></a>

## 建議流程

1. 根據佈線文件宣告物理範圍樹和來源身份。
2. 從一個儀表及固定合成示例開始。
3. 只把必需觀察值匯出到私有檔案。
4. 更改下游自動化前，審計並逐項審查發現。
5. 遷移期間保留原始來源時間及校準證據。

此包不執行修復、實體改名、裝置重置或自動化部署。
