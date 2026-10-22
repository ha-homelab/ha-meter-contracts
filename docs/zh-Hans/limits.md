<a id="limits-and-trust-boundary"></a>

# 限制与信任边界

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
<a href="limits.md" lang="zh-Hans" dir="ltr">简体中文</a> ·
<a href="../zh-Hant/limits.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->
这是离线声明验证器，不是保护控制器、电工测试仪、布线发现服务，也不是执行动作的 Home Assistant 集成。

- 一个总测量值无法还原三个未知负载同时发生的精确功率。统计猜测只能是估计，不能作为保护级测量。
- 范围、来源身份、符号方向及校准声明来自操作员。虚假声明可能使物理上无效的系统在结构上显得有效。
- `complete` 表示相对于已声明叶节点完整，不表示布线经过独立验证。来源重置标记是受信任的证据，不是设备认证。
- 支持 W、kW、Wh、kWh、V 和 A。不建模无功/视在功率、三相代数、CT 饱和、电压互感器、计数器回卷或电价。
- 求和成员是直接仪表，不能是其他求和。功率求和需要时间戳对齐；电能求和需要共同的显式计数起点和对齐样本。
- 数值是有限浮点数。这不是计费级十进制记账系统。校准因子只记录，不应用。
- 只检查当前样本和可选的前一样本。这不是历史数据库、异常检测器、漂移检测器，也不是完整计数器完整性审计。
- HA 来源时间戳必须存在且真正表示采集时间，不会悄悄接受缓存接收时间作为替代。
- JSON/YAML 加载有限制；库的 `audit` API 期望解析器生成的 `Contract`。不要从不可信对象任意构造格式错误的 dataclass。
- 文件输入仅接受常规文件。拒绝末级路径符号链接、FIFO、设备及目录，以非阻塞方式打开，并在读取前检查已打开的描述符。缺少 `O_NOFOLLOW` 和 `O_NONBLOCK` 的平台拒绝文件输入；在这些平台，应对已限制大小的字符串使用 `ha_meter_contracts.reader.loads_document`。父目录符号链接不是沙箱边界。即使读取期间文件增大，仍执行字节上限。
- 检查通过不能证明物理继电器、阀门、电机、泵流量或电气安全。不会自动修复或重试。

输入和输出可能包含操作员提供的实体 ID 和时间。真实契约/导出应保持私有。仓库仅包含合成示例。程序不上传数据，但将报告重定向到外部服务是操作员自己的选择。
