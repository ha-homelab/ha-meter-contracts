<a id="usage"></a>

# 使い方

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
<a href="usage.md" lang="ja" dir="ltr">日本語</a> ·
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
<a href="../zh-Hant/usage.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->
<a id="audit"></a>

## 監査

```sh
ha-meter-contracts check contract.json --json --lang en
ha-meter-contracts check examples/minimal.yaml --at 2026-01-01T12:00:05Z --lang es
```

`--at` はタイムゾーン付きISO 8601時刻を受け付け、既定は現在のUTCです。入力、時刻、言語が同じならJSON出力は決定的です。サンプルは `freshness_seconds` の境界を含めて新鮮で、境界を越えて初めて古くなります。未来サンプルは無効で、暗黙のクロックずれ許容はありません。

終了コードは0がエラー/警告なし、1が意味またはサンプル品質の指摘あり、2が入力/CLIエラーです。未使用別名などの情報は検査を失敗させません。`--json` は監査レポートと入力エラーオブジェクトの両方をstdoutに出します。指定しない場合は監査テキストをstdout、入力エラーをstderrに出します。出力パイプ破損は2を返します。

CIで指摘を隠すために `|| true` を使わないでください。意図的に無効な例は終了1を明示的に検証します。ヘルプとバージョンは0です。`import-ha` は常にJSON契約を出力し、`--json` でスキーマは変わりません。

<a id="python-library"></a>

## Pythonライブラリ

```python
from datetime import datetime, timezone
from ha_meter_contracts import audit, load_document, parse_contract

contract = parse_contract(load_document("examples/valid-three-meters.json"))
report = audit(contract, at=datetime(2026, 1, 1, 12, 0, 5, tzinfo=timezone.utc))
assert report["sums"][0]["value"] == 720
```

`parse_contract` は凍結dataclassを作り、`InputError` は `code`、`path`、`params` を公開します。信頼できない入力の全境界でこのパーサーを使用してください。`audit` は検証済み `Contract` を想定し、指摘を翻訳しません。CLIが翻訳済み `message` 値を追加します。ライブラリでは呼び出し側が評価時刻を明示的に選びます。どちらのAPIも入力を変更せず、ファイルを書きません。

<a id="offline-home-assistant-adapter"></a>

## オフラインHome Assistantアダプター

```sh
ha-meter-contracts import-ha examples/ha-contract.json --ha-states examples/ha-states.synthetic.json > /tmp/meter-contract.json
ha-meter-contracts check /tmp/meter-contract.json --at 2026-01-01T12:00:05Z --json
```

対象メーターごとに `entity_id` と `timestamp_attribute` を対応付けます。エクスポートは `entity_id`、`state`、`attributes` を持つHA状態オブジェクトの配列です。対応付けた属性には元のタイムゾーン付きISO測定時刻が必要です。`attributes.unit_of_measurement` は同じ次元である必要があり、W/kWとWh/kWhは契約の単位へ変換します。

対応付けた値とソース時刻だけをコピーします。親しみやすい名前を含め、他の属性は無視します。厳密に新しいサンプルは既存サンプルを `previous` へ移します。同じ値とソース時刻の再生は冪等です。古いサンプル、または同時刻の矛盾する値は `ha_sample_order` で拒否します。欠落エンティティと `unknown`/`unavailable` 状態はサンプルを消去し、ゼロにはしません。ソース時刻欠落、単位不一致、不正値、エンティティID重複は終了2でインポートを失敗させます。未対応付けメーターは不変です。非公開契約にエンティティIDが含まれることはありますが、公開例は合成識別子を使います。

一般的なHAエクスポートには元のソース時刻がない場合がよくあります。その場合、アダプターは時刻を捏造することを意図的に拒否します。時刻付きデバイスデータを取得するか、メーターを利用不能のままにしてください。HA受信/更新時刻はデバイス取得時刻の証明ではありません。アダプターは `/api/states` へ接続せず、トークンも読みません。HAから電力量リセット印をコピーしないため、電力量を足す前に確認済みリセット証拠を別途追加してください。

<a id="suggested-workflow"></a>

## 推奨手順

1. 配線資料に基づき物理スコープの木とソース来歴を宣言します。
2. 1台のメーターと固定の合成例から始めます。
3. 必要な観測値だけを非公開ファイルへ出力します。
4. 下流のオートメーションを変更する前に監査し、各指摘を確認します。
5. 移行時に元のソース時刻と校正証拠を保持します。

本パッケージは修復、エンティティ改名、デバイスリセット、オートメーション配置を行いません。
