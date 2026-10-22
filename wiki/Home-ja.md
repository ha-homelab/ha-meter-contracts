<a id="ha-meter-contracts-wiki"></a>

# HA Meter Contracts Wiki

<!-- language-navigation:start -->
<p dir="ltr">
<a href="Home.md" lang="en" dir="ltr">English</a> ·
<a href="Home-ar.md" lang="ar" dir="rtl">العربية</a> ·
<a href="Home-bn.md" lang="bn" dir="ltr">বাংলা</a> ·
<a href="Home-cs.md" lang="cs" dir="ltr">Čeština</a> ·
<a href="Home-de.md" lang="de" dir="ltr">Deutsch</a> ·
<a href="Home-es.md" lang="es" dir="ltr">Español</a> ·
<a href="Home-fa.md" lang="fa" dir="rtl">فارسی</a> ·
<a href="Home-fr.md" lang="fr" dir="ltr">Français</a> ·
<a href="Home-he.md" lang="he" dir="rtl">עברית</a> ·
<a href="Home-hi.md" lang="hi" dir="ltr">हिन्दी</a> ·
<a href="Home-id.md" lang="id" dir="ltr">Bahasa Indonesia</a> ·
<a href="Home-it.md" lang="it" dir="ltr">Italiano</a> ·
<a href="Home-ja.md" lang="ja" dir="ltr">日本語</a> ·
<a href="Home-ko.md" lang="ko" dir="ltr">한국어</a> ·
<a href="Home-nl.md" lang="nl" dir="ltr">Nederlands</a> ·
<a href="Home-pl.md" lang="pl" dir="ltr">Polski</a> ·
<a href="Home-pt.md" lang="pt" dir="ltr">Português</a> ·
<a href="Home-ru.md" lang="ru" dir="ltr">Русский</a> ·
<a href="Home-th.md" lang="th" dir="ltr">ไทย</a> ·
<a href="Home-tr.md" lang="tr" dir="ltr">Türkçe</a> ·
<a href="Home-uk.md" lang="uk" dir="ltr">Українська</a> ·
<a href="Home-vi.md" lang="vi" dir="ltr">Tiếng Việt</a> ·
<a href="Home-zh-Hans.md" lang="zh-Hans" dir="ltr">简体中文</a> ·
<a href="Home-zh-Hant.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->
メーターの物理的意味、加算トポロジー、サンプル品質をオフラインで検証します。デバイス接続や命令送信はありません。

- [クイックスタート](https://github.com/ha-homelab/ha-meter-contracts/wiki/Usage-ja)
- [契約とレポート](https://github.com/ha-homelab/ha-meter-contracts/wiki/Contract-ja)
- [トラブルシューティング](https://github.com/ha-homelab/ha-meter-contracts/wiki/Troubleshooting-ja)

タップ全体のメーターは1つの集約値です。MQTTのコピーは2台目の独立メーターではありません。利用不能はゼロではありません。これらの区別が最初のリリースの中核です。

Wikiソースは主リポジトリで版管理します。同じリリースの `docs/` 以下に24のドキュメント言語で完全なガイドがあり、Wikiページはそれらの正本へリンクします。CLIは対応する4つのメッセージ言語を維持します。
