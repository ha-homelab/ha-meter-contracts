<a id="troubleshooting"></a>

# トラブルシューティング

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
<a href="troubleshooting.md" lang="ja" dir="ltr">日本語</a> ·
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

## 3口タップから3つの電力測定値は得られない

`scope_outside` は個別結果の要求に、より広い範囲の測定を使っていることを示します。タップ全体のエンティティを1つ維持してください。個別電力が必要なら正しいスコープの独立測定を追加します。リレーがオンでも負荷の消費電力は証明できず、ポンプが電力を消費しても水流は証明できません。

<a id="a-migrated-sensor-doubles-the-total"></a>

## 移行したセンサーで合計が2倍になる

`alias_stream` だけなら情報です。`duplicate_stream` は両方のコピーが合計に入っていることを示します。同じCTのコピーには同じ来歴を設定し、合計には1つだけ残します。検査を黙らせるためだけに来歴を変えないでください。

![1つのソースと2つの表現](../images/duplicate-stream.svg)

<a id="no-numeric-sum-despite-individually-plausible-numbers"></a>

## 個別値が妥当に見えても数値合計がない

`sample_stale`、`sample_future`、`sample_skew`、`sample_missing`、`incomplete_coverage`、`unit_dimension`、`scope_overlap` を確認します。元のソースを更新し、その取得時刻を保持します。鮮度予算を延ばすのはポリシー変更であって、測定の修復ではありません。完全合計は宣言した葉スコープと比較するので、宣言も確認します。

![合成サンプル品質の時系列](../images/sample-quality.svg)

<a id="energy-decreased-at-midnight"></a>

## 深夜に電力量が減った

減少は実際のリセット、交換、修正かもしれません。ポリシーを宣言し、実際のソース証拠から `reset_at` を追加してください。HAが値を再生した時刻はリセット印ではありません。`total_increasing` は符号付き差引電力量に不適切です。起点が異なる2つのカウンターは合計しません。

<a id="voltage-looks-calibrated-but-watts-still-differ"></a>

## 電圧は校正済みに見えるがワットが異なる

校正は量ごとです。電圧補正は電流、位相関係、電力、積算電力量を検証しません。係数フィールドは記録専用で、値はすでに意図する補正を含む必要があります。

<a id="yaml-fails-although-another-parser-accepts-it"></a>

## 他のパーサーは受け入れるYAMLが失敗する

時刻を引用符で囲み、エイリアス/アンカー/独自タグと重複キーを除き、有限数を使用します。未知フィールドは誤字を検出するためエラーです。上限は両形式に適用します。曖昧なYAMLスカラーが不便なら交換にはJSONを使用します。

<a id="ha-import-fails-on-timestamps"></a>

## HAインポートが時刻で失敗する

`timestamp_attribute` を実際の測定時刻属性に設定します。`last_reported` が証明するのはHAによる受信だけです。ソース時刻がなければ鮮度を確定できないので、サンプルを利用不能のままにします。インポートはオフラインなので、トークンやネットワーク接続を調査する必要はありません。

<a id="safe-issue-report"></a>

## 安全な不具合報告

パッケージ/Pythonの版、安定した指摘コード、最小の合成契約、指定した `--at`、期待結果、実際の結果を含めます。完全なHAエクスポート、トークン、実住所、家庭の予定、非公開デバイス識別子は添付しないでください。再現例では0 Wと利用不能サンプルを区別できる必要があります。
