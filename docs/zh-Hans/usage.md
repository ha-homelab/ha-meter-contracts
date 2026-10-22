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
<a href="usage.md" lang="zh-Hans" dir="ltr">简体中文</a> ·
<a href="../zh-Hant/usage.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->
<a id="audit"></a>

## 审计

```sh
ha-meter-contracts check contract.json --json --lang en
ha-meter-contracts check examples/minimal.yaml --at 2026-01-01T12:00:05Z --lang es
```

`--at` 接受含时区的 ISO 8601 时间戳，默认当前 UTC。相同输入、时间和语言产生确定性的 JSON 输出。样本在包含边界的 `freshness_seconds` 范围内仍新鲜，只在超过边界后过期。未来样本无效，没有隐含时钟偏差宽容值。

退出代码：0 表示无错误/警告；1 表示存在语义或样本质量发现；2 表示输入/CLI 错误。未使用别名等信息项不会使检查失败。`--json` 将审计报告及输入错误对象都写到 stdout。未指定时，审计文本到 stdout，输入错误到 stderr。输出管道断开返回 2。

不要在 CI 中用 `|| true` 隐藏发现。故意无效的示例应显式断言退出 1。帮助和版本退出 0。`import-ha` 始终输出 JSON 契约；`--json` 不改变其模式。

<a id="python-library"></a>

## Python 库

```python
from datetime import datetime, timezone
from ha_meter_contracts import audit, load_document, parse_contract

contract = parse_contract(load_document("examples/valid-three-meters.json"))
report = audit(contract, at=datetime(2026, 1, 1, 12, 0, 5, tzinfo=timezone.utc))
assert report["sums"][0]["value"] == 720
```

`parse_contract` 创建冻结 dataclass；`InputError` 暴露 `code`、`path`、`params`。在每个不可信输入边界都使用此解析器。`audit` 期望已验证的 `Contract`，不翻译发现。CLI 添加本地化 `message` 值。库调用者显式选择评估时间。这两个 API 都不修改输入，也不写文件。

<a id="offline-home-assistant-adapter"></a>

## 离线 Home Assistant 适配器

```sh
ha-meter-contracts import-ha examples/ha-contract.json --ha-states examples/ha-states.synthetic.json > /tmp/meter-contract.json
ha-meter-contracts check /tmp/meter-contract.json --at 2026-01-01T12:00:05Z --json
```

为每个所需仪表映射 `entity_id` 和 `timestamp_attribute`。导出是 HA 状态对象数组，含 `entity_id`、`state`、`attributes`。映射属性必须包含带时区的原始 ISO 测量时间。`attributes.unit_of_measurement` 必须量纲相同；W/kW 和 Wh/kWh 会转换为契约单位。

只复制已映射数值和来源时间，其他属性均忽略，包括友好名称。严格更新的样本会把原样本移入 `previous`。重放相同来源时间戳和数值是幂等的；更早样本或同一时间戳下的冲突值会以 `ha_sample_order` 拒绝。缺失实体和 `unknown`/`unavailable` 状态会清空样本，而不是变成零。缺失来源时间戳、单位不兼容、格式错误的值或重复实体 ID 都使导入以 2 失败。未映射仪表保持不变。私有契约可含实体 ID；公开示例使用合成标识符。

普通 HA 导出经常缺少原始来源时间戳，此时适配器有意拒绝编造。应获取带时间戳的设备数据，或让仪表保持不可用。HA 接收/更新时间不能证明设备采集时间。适配器绝不连接 `/api/states` 或读取令牌。它不从 HA 复制电能重置标记；求和电能前须单独添加已验证的重置证据。

<a id="suggested-workflow"></a>

## 建议流程

1. 根据布线文档声明物理范围树和来源身份。
2. 从一个仪表及固定合成示例开始。
3. 只把必需观察值导出到私有文件。
4. 更改下游自动化前，审计并逐项审查发现。
5. 迁移期间保留原始来源时间及校准证据。

此包不执行修复、实体改名、设备重置或自动化部署。
