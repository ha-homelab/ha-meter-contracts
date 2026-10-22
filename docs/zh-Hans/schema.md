<a id="contract-schema-v1"></a>

# 契约模式 v1

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
<a href="schema.md" lang="zh-Hans" dir="ltr">简体中文</a> ·
<a href="../zh-Hant/schema.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->
机器可读的 [schema.json](../../schema.json) 描述结构。边界以 Python 解析器为准；`audit` 增加 JSON Schema 无法证明的物理和时间语义。用 `python3 scripts/generate_schema.py` 生成结构文件。

<a id="root-and-limits"></a>

## 根对象与限制

必需：整数 `schema_version: 1`、`scopes`、`meters`。可选：`sums`，默认为空。在契约每一层都拒绝未知字段。最多 512 个范围、512 个仪表、128 个求和；范围和仪表不能为空。每个求和含 1–512 个成员。输入为 UTF-8，最多 1,048,576 字节，嵌套深度 16，20,000 个值节点。拒绝 JSON 重复键、NaN/Infinity，以及 YAML 别名/锚点/显式标签。YAML 时间戳应加引号以保留为字符串。

标识符为 1–96 个 ASCII 字符，以字母/数字开头，之后允许字母、数字、`.`、`_`、`-`。ID 在各集合内部唯一，范围和仪表的命名空间分开。所有时间都含 `T` 和时区。数字必须有限、不是布尔值，且在 ±10^15 内，除非另有更窄限制。

<a id="physical-scopes"></a>

## 物理范围

每个范围包含 `id`、`kind`（`site`、`circuit`、`strip`、`outlet`、`load`）及可选 `parent`。父节点必须存在并形成无环森林。父节点上的仪表覆盖其全部后代。范围类型只是描述，不推断电压、相数、额定值、布线或允许的父节点。真实拓扑由你声明。

<a id="meters"></a>

## 仪表

必需字段：

- `id`、`scope`：唯一测量标识符和已声明物理范围。
- `quantity`：`power`、`energy`、`voltage`、`current`。
- `unit`：分别为 W/kW、Wh/kWh、V、A。解析器接受词汇，审计器检查量纲。
- `kind`：`measured` 或 `estimated`。这是声明，不是实验室验证。
- `provenance`：物理测量流的稳定身份，**不是**其 HA/MQTT 表示。别名读数共享它。同一来源身份却具有不同符号/物理量/范围即为冲突；无论输入顺序如何，该冲突流的所有别名都不能用于求和。真正独立的物理流通道应使用独立来源身份。
- `sign`：仅消耗/仅输入/仅输出的幅值用 `nonnegative`；声明的双向流用 `signed`。此版本不推断哪个物理方向为正。
- `state_class`：`measurement`、`total`、`total_increasing`。
- `freshness_seconds`：正的允许样本年龄，0.001–604800 秒。

可选 `reset`：`never`、`periodic`、`device_restart`、`unknown`、`not_applicable`（默认）。电能需要显式、非 `not_applicable` 的策略及累计型状态类。有符号电能不能使用 `total_increasing`。其他物理量需要 `measurement` 和 `not_applicable`。

可选 `sample`、`previous`：null 或对象，对象包含 `value`（数值或 null）、`measured_at` 及可选 `reset_at`。前一样本必须更早。非负计数器下降要求两样本之间有重置标记；`never` 会拒绝下降。`reset_at` 不能晚于其样本，且仅适用于电能。未知的计数器重置语义会产生警告。有符号净计数器可以合理下降；生产方仍需负责正确起点。

可选 `calibration`：`quantity`、正 `factor`（10^-12–10^12）、合成/私有 `reference` 标识符、`verified_at`。它只记录该物理量的证据。样本值**已经校准**，验证器绝不再次应用因子。未来校准或把电压校准用于功率仪表均无效。缺少校准既不证明精度，也不会自动成为错误。

可选 `entity_id`、`timestamp_attribute`：离线 HA 映射，见[用法](usage.md#offline-home-assistant-adapter)。

<a id="sums"></a>

## 求和

必需：`id`、目标 `scope`、`meters` 中的仪表 ID 列表、`quantity`（`power` 或 `energy`）、`coverage`（`partial` 或 `complete`）。可选 `max_skew_seconds`：0–604800，默认 2。

成员必须位于目标范围内，量纲及符号语义匹配，使用不同物理流，且不能以父子关系或相同范围互相重叠。完整求和必须覆盖目标下每一个**已声明叶范围**。无法检测未声明布线。部分求和会明确报告覆盖不完整。不支持嵌套求和，成员始终引用仪表。

每个成员必须有有效且新鲜的数据，采集时间须在允许偏差内。电能另外要求相同的显式 `reset_at` 起点。这检查声明的对齐，不检查历史累计精度。求和转换为 W 或 Wh。特意不支持电流、电压求和，因为其意义取决于电路拓扑。

任何必需证据或语义检查失败，数值求和就不可用。估计会以 `kind: estimated` 传递。两个别名可以共存于清单，但不能同时参与求和。不会为未测量的单独插座推断总量。

<a id="report-v1"></a>

## 报告 v1

根对象包含 `schema_version`、规范化为 UTC 的评估时间 `at`、按严重度计数的 `summary`、已排序的 `findings` 和 `sums`。每项发现含 `code`、`severity`、JSON 风格 `path`、结构化 `params`；CLI 添加 `message`。每项求和含 `id`、`scope`、`quantity`、基本 `unit`、`value`、`status`、`kind`、`coverage`。未知值用 JSON null，绝不用 NaN。
