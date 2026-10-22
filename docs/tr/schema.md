<a id="contract-schema-v1"></a>

# Sözleşme şeması v1

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
<a href="schema.md" lang="tr" dir="ltr">Türkçe</a> ·
<a href="../uk/schema.md" lang="uk" dir="ltr">Українська</a> ·
<a href="../vi/schema.md" lang="vi" dir="ltr">Tiếng Việt</a> ·
<a href="../zh-Hans/schema.md" lang="zh-Hans" dir="ltr">简体中文</a> ·
<a href="../zh-Hant/schema.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->
Makine tarafından okunabilir [schema.json](../../schema.json) yapıyı tanımlar. Sınırlar için Python ayrıştırıcısı yetkilidir; `audit`, JSON Schema'nın kanıtlayamadığı fiziksel ve zamansal anlamları ekler. Yapı dosyasını `python3 scripts/generate_schema.py` ile üretin.

<a id="root-and-limits"></a>

## Kök ve sınırlar

Zorunlu: tamsayı `schema_version: 1`, `scopes`, `meters`. İsteğe bağlı: `sums` (varsayılan boş). Bilinmeyen alanlar her seviyede reddedilir. En fazla 512 kapsam, 512 ölçer ve 128 toplam; kapsamlar ve ölçerler boş olmamalıdır. Her toplamda 1–512 üye vardır. Girdi UTF-8, en fazla 1.048.576 bayt, derinlik 16 ve 20.000 değer düğümüdür. Yinelenen JSON anahtarları, NaN/Infinity ve YAML takma adları/çapaları/açık etiketleri reddedilir. Dizge kalmaları için YAML zaman damgalarını tırnak içine alın.

Tanımlayıcılar 1–96 ASCII karakteridir: önce harf/rakam, sonra harfler, rakamlar, `.`, `_`, `-`. Kimlikler her koleksiyonda benzersizdir; kapsamlar ve ölçerlerin ad alanları ayrıdır. Bütün zamanlar `T` ve saat dilimi içerir. Sayılar sonludur, boolean değildir ve daha sıkı sınır yoksa ±10^15 aralığındadır.

<a id="physical-scopes"></a>

## Fiziksel kapsamlar

Her kapsamda `id`, `kind` (`site`, `circuit`, `strip`, `outlet`, `load`) ve isteğe bağlı `parent` bulunur. Üstler mevcut olmalı ve döngüsüz bir orman oluşturmalıdır. Üst kapsamdaki ölçer bütün altlarını kapsar. Kapsam türleri açıklayıcıdır: gerilim, fazlar, anma değerleri, kablolama veya izin verilen üstleri çıkarsamaz. Gerçek topolojiyi kullanıcı beyan eder.

<a id="meters"></a>

## Ölçerler

Zorunlu alanlar:

- `id`, `scope`: benzersiz okuma tanımlayıcısı ve beyan edilen fiziksel kapsam.
- `quantity`: `power`, `energy`, `voltage`, `current`.
- `unit`: sırasıyla W/kW, Wh/kWh, V, A. Ayrıştırıcı sözlüğü kabul eder; denetleyici boyutu kontrol eder.
- `kind`: `measured` veya `estimated`. Bu bir beyan, laboratuvar doğrulaması değildir.
- `provenance`: HA/MQTT gösteriminin **değil**, fiziksel ölçüm akışının kalıcı kimliği. Takma ad okumaları bunu paylaşır. Tek kaynak kimliğinde farklı işaret/büyüklük/kapsam çelişki oluşturur; akışın bütün takma adları, girdi sırasından bağımsız olarak toplamlar için kullanılamaz olur. Gerçekten farklı fiziksel kanallar için farklı kaynak kimlikleri seçin.
- `sign`: yalnız tüketim/ithalat/ihracat büyüklükleri için `nonnegative`; beyan edilen çift yönlü akış için `signed`. Bu sürüm hangi fiziksel yönün pozitif olduğunu çıkarsamaz.
- `state_class`: `measurement`, `total`, `total_increasing`.
- `freshness_seconds`: pozitif azami yaş, 0.001–604800 saniye.

İsteğe bağlı `reset`: `never`, `periodic`, `device_restart`, `unknown`, `not_applicable` (varsayılan). Enerji, `not_applicable` dışında açık bir politika ve total türünde durum sınıfı gerektirir. İşaretli enerji `total_increasing` kullanamaz. Diğer büyüklükler `measurement` ve `not_applicable` gerektirir.

İsteğe bağlı `sample`, `previous`: null veya `value` (sayı ya da null), `measured_at`, isteğe bağlı `reset_at` içeren nesne. Önceki örnek daha eski olmalıdır. Negatif olmayan sayaçtaki düşüş, örnekler arasında sıfırlama işareti gerektirir; `never` bunu reddeder. `reset_at` kendi örneğinden sonra olamaz ve yalnız enerjiye uygulanır. Bilinmeyen sıfırlama anlamı uyarı üretir. İşaretli net sayaç geçerli olarak azalabilir; doğru başlangıç hâlâ üreticinin sorumluluğudur.

İsteğe bağlı `calibration`: `quantity`, pozitif `factor` (10^-12–10^12), sentetik/özel tanımlayıcı `reference`, `verified_at`. Tam olarak o büyüklük için kanıt kaydeder. Değerler **zaten kalibre edilmiştir**: doğrulayıcı katsayıyı asla yeniden uygulamaz. Gelecekteki kalibrasyon veya güç ölçerine gerilim kalibrasyonu geçersizdir. Kalibrasyonun bulunmaması doğruluk kanıtı değildir ve otomatik olarak hata sayılmaz.

İsteğe bağlı `entity_id`, `timestamp_attribute`: çevrimdışı HA eşlemesi; [kullanıma](usage.md#offline-home-assistant-adapter) bakın.

<a id="sums"></a>

## Toplamlar

Zorunlu: `id`, hedef `scope`, `meters` içinde ölçer kimlikleri listesi, `quantity` (`power` veya `energy`), `coverage` (`partial` veya `complete`). İsteğe bağlı `max_skew_seconds`: 0–604800, varsayılan 2.

Üyeler hedef kapsamda olmalı, uyumlu boyutlara ve işaret anlamlarına sahip olmalı, farklı fiziksel akışlar kullanmalı ve üst/alt ya da aynı kapsam olarak örtüşmemelidir. Tam toplam, hedef altındaki her **beyan edilmiş yaprak kapsamını** kapsar. Beyan edilmemiş kablolama bulunamaz. Kısmi toplam açıkça kısmi kapsama beyan eder. İç içe toplamlar desteklenmez; üyeler daima ölçerlere başvurur.

Her üyenin geçerli ve güncel verisi olmalıdır; ölçüm zamanları izin verilen sapma içinde kalmalıdır. Enerji ayrıca aynı açık `reset_at` başlangıçlarını gerektirir. Bu, geçmiş birikimin doğruluğunu değil, beyan edilen hizalamayı denetler. Toplamlar W veya Wh birimine çevrilir. Akım ve gerilim toplamları devre topolojisine bağlı olduklarından bilerek desteklenmez.

Gerekli kanıt eksikse veya anlamsal denetim başarısızsa sayısal toplam kullanılamaz. Tahminler `kind: estimated` olarak yayılır. İki takma ad envanterde birlikte bulunabilir, fakat ikisi bir toplama birlikte katkı veremez. Tek tek ölçülmeyen prizler için herhangi bir toplam çıkarılmaz.

<a id="report-v1"></a>

## Rapor v1

Kök: `schema_version`, UTC'ye normalleştirilmiş değerlendirme zamanı `at`, `summary` içinde önem düzeyi sayıları, sıralı `findings` ve `sums`. Her bulgu `code`, `severity`, JSON tarzı `path`, yapısal `params` içerir; CLI `message` ekler. Her toplam `id`, `scope`, `quantity`, temel `unit`, `value`, `status`, `kind`, `coverage` içerir. Bilinmeyen değerler JSON null olur, asla NaN olmaz.
