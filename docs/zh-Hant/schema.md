<a id="contract-schema-v1"></a>

# 契約模式 v1

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
<a href="schema.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->
機器可讀的 [schema.json](../../schema.json) 描述結構。邊界以 Python 解析器為準；`audit` 增加 JSON Schema 無法證明的物理和時間語義。用 `python3 scripts/generate_schema.py` 生成結構檔案。

<a id="root-and-limits"></a>

## 根物件與限制

必需：整數 `schema_version: 1`、`scopes`、`meters`。可選：`sums`，預設為空。在契約每一層都拒絕未知欄位。最多 512 個範圍、512 個儀表、128 個求和；範圍和儀表不能為空。每個求和含 1–512 個成員。輸入為 UTF-8，最多 1,048,576 位元組，巢狀深度 16，20,000 個值節點。拒絕 JSON 重複鍵、NaN/Infinity，以及 YAML 別名/錨點/顯式標籤。YAML 時間戳應加引號以保留為字串。

識別符號為 1–96 個 ASCII 字元，以字母/數字開頭，之後允許字母、數字、`.`、`_`、`-`。ID 在各集合內部唯一，範圍和儀表的名稱空間分開。所有時間都含 `T` 和時區。數字必須有限、不是布林值，且在 ±10^15 內，除非另有更窄限制。

<a id="physical-scopes"></a>

## 物理範圍

每個範圍包含 `id`、`kind`（`site`、`circuit`、`strip`、`outlet`、`load`）及可選 `parent`。父節點必須存在並形成無環森林。父節點上的儀表覆蓋其全部後代。範圍型別只是描述，不推斷電壓、相數、額定值、佈線或允許的父節點。真實拓撲由你宣告。

<a id="meters"></a>

## 儀表

必需欄位：

- `id`、`scope`：唯一測量識別符號和已宣告物理範圍。
- `quantity`：`power`、`energy`、`voltage`、`current`。
- `unit`：分別為 W/kW、Wh/kWh、V、A。解析器接受詞彙，審計器檢查量綱。
- `kind`：`measured` 或 `estimated`。這是宣告，不是實驗室驗證。
- `provenance`：物理測量流的穩定身份，**不是**其 HA/MQTT 表示。別名讀數共享它。同一來源身份卻具有不同符號/物理量/範圍即為衝突；無論輸入順序如何，該衝突流的所有別名都不能用於求和。真正獨立的物理流通道應使用獨立來源身份。
- `sign`：僅消耗/僅輸入/僅輸出的幅值用 `nonnegative`；宣告的雙向流用 `signed`。此版本不推斷哪個物理方向為正。
- `state_class`：`measurement`、`total`、`total_increasing`。
- `freshness_seconds`：正的允許樣本年齡，0.001–604800 秒。

可選 `reset`：`never`、`periodic`、`device_restart`、`unknown`、`not_applicable`（預設）。電能需要顯式、非 `not_applicable` 的策略及累計型狀態類。有符號電能不能使用 `total_increasing`。其他物理量需要 `measurement` 和 `not_applicable`。

可選 `sample`、`previous`：null 或物件，物件包含 `value`（數值或 null）、`measured_at` 及可選 `reset_at`。前一樣本必須更早。非負計數器下降要求兩樣本之間有重置標記；`never` 會拒絕下降。`reset_at` 不能晚於其樣本，且僅適用於電能。未知的計數器重置語義會產生警告。有符號淨計數器可以合理下降；生產方仍需負責正確起點。

可選 `calibration`：`quantity`、正 `factor`（10^-12–10^12）、合成/私有 `reference` 識別符號、`verified_at`。它只記錄該物理量的證據。樣本值**已經校準**，驗證器絕不再次應用因子。未來校準或把電壓校準用於功率儀表均無效。缺少校準既不證明精度，也不會自動成為錯誤。

可選 `entity_id`、`timestamp_attribute`：離線 HA 對映，見[用法](usage.md#offline-home-assistant-adapter)。

<a id="sums"></a>

## 求和

必需：`id`、目標 `scope`、`meters` 中的儀表 ID 列表、`quantity`（`power` 或 `energy`）、`coverage`（`partial` 或 `complete`）。可選 `max_skew_seconds`：0–604800，預設 2。

成員必須位於目標範圍內，量綱及符號語義匹配，使用不同物理流，且不能以父子關係或相同範圍互相重疊。完整求和必須覆蓋目標下每一個**已宣告葉範圍**。無法檢測未宣告佈線。部分求和會明確報告覆蓋不完整。不支援巢狀求和，成員始終引用儀表。

每個成員必須有有效且新鮮的資料，採集時間須在允許偏差內。電能另外要求相同的顯式 `reset_at` 起點。這檢查宣告的對齊，不檢查歷史累計精度。求和轉換為 W 或 Wh。特意不支援電流、電壓求和，因為其意義取決於電路拓撲。

任何必需證據或語義檢查失敗，數值求和就不可用。估計會以 `kind: estimated` 傳遞。兩個別名可以共存於清單，但不能同時參與求和。不會為未測量的單獨插座推斷總量。

<a id="report-v1"></a>

## 報告 v1

根物件包含 `schema_version`、規範化為 UTC 的評估時間 `at`、按嚴重度計數的 `summary`、已排序的 `findings` 和 `sums`。每項發現含 `code`、`severity`、JSON 風格 `path`、結構化 `params`；CLI 新增 `message`。每項求和含 `id`、`scope`、`quantity`、基本 `unit`、`value`、`status`、`kind`、`coverage`。未知值用 JSON null，絕不用 NaN。
