<a id="contract-schema-v1"></a>

# 契約スキーマv1

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
<a href="schema.md" lang="ja" dir="ltr">日本語</a> ·
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
<a href="../zh-Hant/schema.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->
機械可読の [schema.json](../../schema.json) は構造を記述します。上限についてはPythonパーサーが正本です。`audit` はJSON Schemaでは証明できない物理的・時間的意味を追加します。構造ファイルは `python3 scripts/generate_schema.py` で生成します。

<a id="root-and-limits"></a>

## ルートと上限

必須は整数 `schema_version: 1`、`scopes`、`meters` です。任意の `sums` は既定で空です。契約の全階層で未知フィールドを拒否します。最大512スコープ、512メーター、128合計で、スコープとメーターは空にできません。各合計のメンバーは1–512です。入力はUTF-8、最大1,048,576バイト、入れ子深さ16、値ノード20,000です。JSONの重複キー、NaN/Infinity、YAMLのエイリアス/アンカー/明示タグは拒否します。YAMLでは時刻を引用符で囲み、文字列のままにします。

識別子は1–96文字のASCIIで、英字/数字から始まり、続きに英字、数字、`.`、`_`、`-` を使えます。IDは各集合内で一意で、スコープとメーターの名前空間は別です。すべての時刻は `T` とタイムゾーンを含みます。数値は有限で真偽値ではなく、より狭い上限がない限り±10^15以内です。

<a id="physical-scopes"></a>

## 物理スコープ

各スコープは `id`、`kind`（`site`、`circuit`、`strip`、`outlet`、`load`）と任意の `parent` を持ちます。親は存在し、閉路のない森を構成する必要があります。親のメーターはその全子孫を覆います。スコープ種別は説明であり、電圧、相、定格、配線、許可される親を推論しません。実際のトポロジーは自分で宣言します。

<a id="meters"></a>

## メーター

必須フィールド：

- `id`、`scope`：一意の測定識別子と宣言された物理スコープ。
- `quantity`：`power`、`energy`、`voltage`、`current`。
- `unit`：それぞれW/kW、Wh/kWh、V、A。パーサーが語彙を受け入れ、監査器が次元を検査します。
- `kind`：`measured` または `estimated`。宣言であって実験室での検証ではありません。
- `provenance`：物理測定ストリームの安定した同一性であり、そのHA/MQTT表現**ではありません**。別名の読み値はこれを共有します。同じ来歴で符号/量/スコープが異なると競合となり、入力順に関係なく、そのストリームの全別名は合計に使用不能になります。本当に異なる物理ストリームには別の来歴を指定してください。
- `sign`：消費のみ/輸入のみ/輸出のみの大きさは `nonnegative`、宣言された双方向の流れは `signed`。この版は物理的な正方向を推論しません。
- `state_class`：`measurement`、`total`、`total_increasing`。
- `freshness_seconds`：正の許容経過時間、0.001–604800秒。

任意の `reset` は `never`、`periodic`、`device_restart`、`unknown`、`not_applicable`（既定）です。電力量には `not_applicable` 以外の明示ポリシーと累計型状態クラスが必要です。符号付き電力量に `total_increasing` は使えません。その他の量には `measurement` と `not_applicable` が必要です。

任意の `sample`、`previous` はnull、または `value`（数値かnull）、`measured_at`、任意の `reset_at` を持つオブジェクトです。直前サンプルは古い必要があります。非負カウンターの減少にはサンプル間のリセット印が必要で、`never` は減少を拒否します。`reset_at` はサンプル時刻より後にできず、電力量のみに適用します。未知のリセット意味論は警告になります。符号付きの差引カウンターは正当に減少し得ますが、正しい起点は生成側の責任です。

任意の `calibration` は `quantity`、正の `factor`（10^-12–10^12）、合成/非公開の `reference` 識別子、`verified_at` です。その量に対する証拠だけを記録します。サンプル値は**校正済み**で、検証器は係数を再適用しません。未来の校正や電力メーターへの電圧校正は無効です。校正がないことは精度の証明ではなく、自動的なエラーでもありません。

任意の `entity_id`、`timestamp_attribute` はオフラインHA対応付けです。[使い方](usage.md#offline-home-assistant-adapter)を参照してください。

<a id="sums"></a>

## 合計

必須は `id`、対象の `scope`、`meters` 内のメーターID一覧、`quantity`（`power` または `energy`）、`coverage`（`partial` または `complete`）です。任意の `max_skew_seconds` は0–604800、既定2です。

メンバーは対象スコープ内にあり、次元と符号の意味が一致し、異なる物理ストリームを使い、親子または同一スコープとして重複してはいけません。完全な合計は対象配下の**宣言された葉スコープ**をすべて覆う必要があります。未宣言の配線は検出できません。部分合計は部分的な被覆であると明示します。入れ子の合計は非対応で、メンバーは常にメーターを参照します。

全メンバーに有効で新鮮なデータが必要で、取得時刻は許容ずれ以内でなければなりません。電力量はさらに同一の明示的 `reset_at` 起点を必要とします。確認するのは宣言された整合であり、過去の積算精度ではありません。合計はWまたはWhへ変換します。電流と電圧の合計は回路トポロジー次第で意味が変わるため、意図的に非対応です。

必要な証拠か意味検査が1つでも失敗すると数値合計は利用不能です。推定は `kind: estimated` として伝播します。2つの別名はインベントリに共存できますが、両方が合計へ寄与することはできません。未測定の個別コンセントに合計値を推論しません。

<a id="report-v1"></a>

## レポートv1

ルートには `schema_version`、UTCへ正規化した評価時刻 `at`、重大度別件数の `summary`、ソート済み `findings`、`sums` があります。各指摘は `code`、`severity`、JSON形式の `path`、構造化 `params` を持ち、CLIが `message` を追加します。各合計は `id`、`scope`、`quantity`、基準 `unit`、`value`、`status`、`kind`、`coverage` を含みます。未知の値はJSON nullで、NaNにはしません。
