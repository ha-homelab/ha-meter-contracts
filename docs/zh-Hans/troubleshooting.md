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
<a href="troubleshooting.md" lang="zh-Hans" dir="ltr">简体中文</a> ·
<a href="../zh-Hant/troubleshooting.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->
<a id="a-three-outlet-strip-cannot-produce-three-power-readings"></a>

## 三个插座的插排无法产生三个功率读数

`scope_outside` 表示请求的单独结果使用了更大范围的测量。应保留一个整体插排实体。若需要单独功率，应增加独立且范围正确的测量。继电器开启不证明负载在耗电，泵耗电也不证明水在流动。

<a id="a-migrated-sensor-doubles-the-total"></a>

## 迁移后的传感器使总量翻倍

单独的 `alias_stream` 是信息项。`duplicate_stream` 表示两个副本同时进入求和。给同一 CT 的副本相同来源身份，求和只保留一个。不要仅为消除检查而改变来源身份。

![一个来源与两种表示](../images/duplicate-stream.svg)

<a id="no-numeric-sum-despite-individually-plausible-numbers"></a>

## 单个数值看似合理却没有数值求和

检查 `sample_stale`、`sample_future`、`sample_skew`、`sample_missing`、`incomplete_coverage`、`unit_dimension`、`scope_overlap`。刷新原始来源并保留采集时间。延长新鲜度预算是策略更改，不是修复测量。完整求和依据已声明叶范围判断，因此也应审查声明。

![合成样本质量时间线](../images/sample-quality.svg)

<a id="energy-decreased-at-midnight"></a>

## 电能在午夜下降

下降可能是真正重置、更换或修正。声明策略，并根据真实来源证据添加 `reset_at`。HA 重放该值的时间戳不是重置标记。`total_increasing` 不适用于有符号净电能。起点不同的两个计数器不会求和。

<a id="voltage-looks-calibrated-but-watts-still-differ"></a>

## 电压看起来已校准，但瓦数仍不同

校准针对每种物理量。修正电压不验证电流、相位关系、功率或累计电能。因子字段只作记录，数值必须已经包含预期修正。

<a id="yaml-fails-although-another-parser-accepts-it"></a>

## 其他解析器接受的 YAML 在这里失败

给时间戳加引号，移除别名/锚点/自定义标签及重复键，并使用有限数值。未知字段作为错误以发现拼写问题。两种格式都适用限制。若 YAML 标量歧义造成不便，交换时使用 JSON。

<a id="ha-import-fails-on-timestamps"></a>

## HA 导入因时间戳失败

把 `timestamp_attribute` 设为真正的测量时间属性。`last_reported` 只能证明 HA 接收。没有来源时间，工具无法确定新鲜度，应保持样本不可用。导入是离线的，因此没有令牌或网络连通性问题需要排查。

<a id="safe-issue-report"></a>

## 安全报告问题

包含包/Python 版本、稳定发现代码、最小合成契约、选择的 `--at`、期望和实际结果。不要附完整 HA 导出、令牌、真实地址、家庭作息或私有设备标识。复现示例必须区分 0 W 和不可用样本。
