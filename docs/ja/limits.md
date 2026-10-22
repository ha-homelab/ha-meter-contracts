<a id="limits-and-trust-boundary"></a>

# 制限と信頼境界

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
<a href="limits.md" lang="ja" dir="ltr">日本語</a> ·
<a href="../ko/limits.md" lang="ko" dir="ltr">한국어</a> ·
<a href="../nl/limits.md" lang="nl" dir="ltr">Nederlands</a> ·
<a href="../pl/limits.md" lang="pl" dir="ltr">Polski</a> ·
<a href="../pt/limits.md" lang="pt" dir="ltr">Português</a> ·
<a href="../ru/limits.md" lang="ru" dir="ltr">Русский</a> ·
<a href="../th/limits.md" lang="th" dir="ltr">ไทย</a> ·
<a href="../tr/limits.md" lang="tr" dir="ltr">Türkçe</a> ·
<a href="../uk/limits.md" lang="uk" dir="ltr">Українська</a> ·
<a href="../vi/limits.md" lang="vi" dir="ltr">Tiếng Việt</a> ·
<a href="../zh-Hans/limits.md" lang="zh-Hans" dir="ltr">简体中文</a> ·
<a href="../zh-Hant/limits.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->
これはオフラインの宣言検証器であり、保護制御装置、電気工事用試験器、配線検出サービス、操作を実行するHome Assistant連携ではありません。

- 1つの合計測定値から、未知の3つの負荷それぞれの同時電力を正確に復元することはできません。統計的な推測は推定値であって、保護に使える等級の測定ではありません。
- 範囲、来歴、符号の方向、校正の申告は運用者が与えます。虚偽の宣言により、物理的に不正なシステムが構造的には有効に見える場合があります。
- `complete` は宣言した葉に対して完全という意味で、配線を独立に確認したという意味ではありません。ソースのリセット印は信頼する証拠であり、デバイスの証明ではありません。
- W、kW、Wh、kWh、V、Aに対応します。無効/皮相電力、三相の代数、CT飽和、計器用変圧器、カウンターの周回、料金はモデル化しません。
- 合計のメンバーは直接のメーターであり、別の合計ではありません。電力合計には時刻の整合が、電力量合計には共通の明示的なカウンター起点と整合したサンプルが必要です。
- 値は有限の浮動小数点数です。課金等級の十進会計システムではありません。校正係数は記録するだけで適用しません。
- 現在のサンプルと任意の直前サンプルだけを確認します。履歴データベース、異常検知器、ドリフト検知器、完全なカウンター整合性監査ではありません。
- HAソース時刻は存在し、実際に取得時刻を表す必要があります。キャッシュ受信時刻を黙って代用しません。
- JSON/YAMLの読み込みには上限があります。ライブラリの `audit` APIはパーサーが生成した `Contract` を想定します。信頼できないオブジェクトから任意の不正なdataclassを作らないでください。
- ファイル入力は通常ファイルのみです。最終パス要素のシンボリックリンク、FIFO、デバイス、ディレクトリを拒否し、非ブロッキングで開いて、読む前に開いた記述子を確認します。`O_NOFOLLOW` と `O_NONBLOCK` がないプラットフォームではファイル入力を拒否します。その環境では既にサイズ制限した文字列に `ha_meter_contracts.reader.loads_document` を使ってください。親ディレクトリのシンボリックリンクはサンドボックス境界ではありません。読み込み中にファイルが増大してもバイト上限を強制します。
- 合格結果は、実際のリレー、バルブ、モーター、ポンプ流量、電気的安全性を証明しません。自動修復や再試行は行いません。

入出力には運用者が提供したエンティティIDや時刻が含まれる場合があります。実際の契約/エクスポートは非公開にしてください。リポジトリには合成例だけがあります。プログラムはアップロードしませんが、レポートを外部サービスへ転送するかは運用者の判断です。
