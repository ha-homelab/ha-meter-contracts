<a id="contract-schema-v1"></a>

# Skema kontrak v1

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
<a href="schema.md" lang="id" dir="ltr">Bahasa Indonesia</a> ·
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
<a href="../zh-Hans/schema.md" lang="zh-Hans" dir="ltr">简体中文</a> ·
<a href="../zh-Hant/schema.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->
[schema.json](../../schema.json) yang dapat dibaca mesin menjelaskan strukturnya. Parser Python menjadi otoritas untuk batasan; `audit` menambahkan semantik fisik dan waktu yang tidak dapat dibuktikan JSON Schema. Hasilkan berkas struktur dengan `python3 scripts/generate_schema.py`.

<a id="root-and-limits"></a>

## Akar dan batasan

Wajib: bilangan bulat `schema_version: 1`, `scopes`, `meters`. Opsional: `sums` (kosong secara bawaan). Kolom yang tidak dikenal ditolak pada setiap tingkat. Maksimal 512 cakupan, 512 meter, dan 128 penjumlahan; cakupan dan meter tidak boleh kosong. Setiap penjumlahan memiliki 1–512 anggota. Masukan UTF-8, maksimal 1.048.576 byte, kedalaman 16, dan 20.000 simpul nilai. Kunci JSON duplikat, NaN/Infinity, dan alias/jangkar/tag eksplisit YAML ditolak. Apit stempel waktu YAML dengan tanda kutip agar tetap menjadi string.

Pengenal memiliki 1–96 karakter ASCII: huruf/angka pertama, lalu huruf, angka, `.`, `_`, `-`. ID unik dalam setiap koleksi; cakupan dan meter memiliki ruang nama terpisah. Semua waktu menyertakan `T` dan zona waktu. Bilangan harus berhingga, bukan boolean, dalam ±10^15 kecuali dibatasi lebih ketat.

<a id="physical-scopes"></a>

## Cakupan fisik

Setiap cakupan memiliki `id`, `kind` (`site`, `circuit`, `strip`, `outlet`, `load`), dan `parent` opsional. Induk harus ada dan membentuk hutan tanpa siklus. Meter pada induk mencakup semua turunannya. Jenis cakupan bersifat deskriptif: tidak menyimpulkan tegangan, fase, rating, pengawatan, atau induk yang diperbolehkan. Topologi sebenarnya dideklarasikan pengguna.

<a id="meters"></a>

## Meter

Kolom wajib:

- `id`, `scope`: pengenal pembacaan unik dan cakupan fisik yang dideklarasikan.
- `quantity`: `power`, `energy`, `voltage`, `current`.
- `unit`: masing-masing W/kW, Wh/kWh, V, A. Parser menerima kosakata; auditor memeriksa dimensi.
- `kind`: `measured` atau `estimated`. Ini deklarasi, bukan verifikasi laboratorium.
- `provenance`: identitas stabil aliran pengukuran fisik, **bukan** representasi HA/MQTT-nya. Pembacaan alias berbagi identitas ini. Tanda/besaran/cakupan yang berbeda dengan satu asal-usul menimbulkan konflik; semua alias aliran menjadi tidak tersedia untuk penjumlahan tanpa bergantung urutan masukan. Pilih asal-usul berbeda untuk kanal fisik yang benar-benar berbeda.
- `sign`: `nonnegative` untuk magnitudo hanya konsumsi/impor/ekspor; `signed` untuk aliran dua arah yang dideklarasikan. Versi ini tidak menyimpulkan arah fisik mana yang positif.
- `state_class`: `measurement`, `total`, `total_increasing`.
- `freshness_seconds`: usia maksimum positif, 0.001–604800 detik.

`reset` opsional: `never`, `periodic`, `device_restart`, `unknown`, `not_applicable` (bawaan). Energi memerlukan kebijakan eksplisit selain `not_applicable` dan kelas status bertipe total. Energi bertanda tidak boleh memakai `total_increasing`. Besaran lain memerlukan `measurement` dan `not_applicable`.

`sample`, `previous` opsional: null atau objek dengan `value` (angka atau null), `measured_at`, dan `reset_at` opsional. Sampel sebelumnya harus lebih tua. Penurunan pencacah nonnegatif memerlukan penanda reset di antara sampel; `never` menolaknya. `reset_at` tidak boleh sesudah sampelnya dan hanya berlaku untuk energi. Semantik reset yang tidak diketahui menghasilkan peringatan. Pencacah bersih bertanda boleh menurun secara sah; basis yang benar tetap tanggung jawab produsen.

`calibration` opsional: `quantity`, `factor` positif (10^-12–10^12), pengenal sintetis/privat `reference`, `verified_at`. Ini mencatat bukti untuk besaran tepat tersebut. Nilai **sudah dikalibrasi**: validator tidak pernah menerapkan faktor ulang. Kalibrasi masa depan atau kalibrasi tegangan pada meter daya tidak valid. Ketiadaan kalibrasi tidak membuktikan akurasi dan tidak otomatis menjadi kesalahan.

`entity_id`, `timestamp_attribute` opsional: pemetaan HA luring; lihat [penggunaan](usage.md#offline-home-assistant-adapter).

<a id="sums"></a>

## Penjumlahan

Wajib: `id`, `scope` tujuan, daftar ID meter dalam `meters`, `quantity` (`power` atau `energy`), `coverage` (`partial` atau `complete`). `max_skew_seconds` opsional: 0–604800, bawaan 2.

Anggota harus berada dalam cakupan tujuan, memiliki dimensi dan semantik tanda yang cocok, memakai aliran fisik berbeda, dan tidak tumpang tindih sebagai induk/anak atau cakupan identik. Penjumlahan lengkap mencakup setiap **cakupan daun yang dideklarasikan** di bawah tujuan. Pengawatan yang tidak dideklarasikan tidak dapat ditemukan. Penjumlahan parsial secara eksplisit menyatakan cakupan parsial. Penjumlahan bersarang tidak didukung; anggota selalu merujuk pada meter.

Setiap anggota harus memiliki data valid dan segar; waktu akuisisi harus berada dalam selisih yang diizinkan. Energi juga memerlukan asal `reset_at` eksplisit yang identik. Ini memeriksa keselarasan yang dideklarasikan, bukan akurasi akumulasi historis. Penjumlahan dikonversi ke W atau Wh. Penjumlahan arus dan tegangan sengaja tidak didukung karena bergantung pada topologi rangkaian.

Jumlah numerik tidak tersedia bila bukti yang diperlukan hilang atau pemeriksaan semantik gagal. Perkiraan merambat sebagai `kind: estimated`. Dua alias boleh hidup bersama dalam inventaris, tetapi tidak boleh keduanya berkontribusi pada satu penjumlahan. Tidak ada total yang disimpulkan untuk stopkontak individual yang tidak diukur.

<a id="report-v1"></a>

## Laporan v1

Akar: `schema_version`, waktu evaluasi `at` yang dinormalisasi ke UTC, hitungan tingkat keparahan dalam `summary`, `findings` terurut, dan `sums`. Setiap temuan memuat `code`, `severity`, `path` bergaya JSON, `params` terstruktur; CLI menambahkan `message`. Setiap jumlah memuat `id`, `scope`, `quantity`, `unit` dasar, `value`, `status`, `kind`, `coverage`. Nilai tak diketahui berupa JSON null, tidak pernah NaN.
