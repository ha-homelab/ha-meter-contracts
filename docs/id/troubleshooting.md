<a id="troubleshooting"></a>

# Pemecahan masalah

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
<a href="troubleshooting.md" lang="id" dir="ltr">Bahasa Indonesia</a> ·
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
<a href="../zh-Hans/troubleshooting.md" lang="zh-Hans" dir="ltr">简体中文</a> ·
<a href="../zh-Hant/troubleshooting.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->
<a id="a-three-outlet-strip-cannot-produce-three-power-readings"></a>

## Terminal tiga stopkontak tidak menghasilkan tiga pembacaan daya

`scope_outside` berarti hasil individual yang diminta menggunakan pengukuran lebih luas. Pertahankan satu entitas untuk seluruh terminal. Daya individual memerlukan pengukuran independen dengan cakupan yang benar. Relai menyala tidak membuktikan beban mengonsumsi; pompa mengonsumsi listrik tidak membuktikan air mengalir.

<a id="a-migrated-sensor-doubles-the-total"></a>

## Sensor yang dimigrasikan menggandakan total

`alias_stream` saja bersifat informatif. `duplicate_stream` berarti kedua salinan masuk penjumlahan. Berikan asal-usul sama kepada salinan CT yang sama dan pertahankan hanya satu dalam penjumlahan. Jangan ubah asal-usul hanya untuk membungkam pemeriksaan.

![Satu sumber dan dua representasi](../images/duplicate-stream.svg)

<a id="no-numeric-sum-despite-individually-plausible-numbers"></a>

## Tidak ada jumlah numerik meskipun nilainya masuk akal

Periksa `sample_stale`, `sample_future`, `sample_skew`, `sample_missing`, `incomplete_coverage`, `unit_dimension`, `scope_overlap`. Segarkan sumber sebenarnya dan pertahankan waktu akuisisinya. Menaikkan usia yang diizinkan mengubah kebijakan, bukan memperbaiki pengukuran. Penjumlahan lengkap dinilai terhadap daun yang dideklarasikan: periksa deklarasinya juga.

![Linimasa sintetis kualitas sampel](../images/sample-quality.svg)

<a id="energy-decreased-at-midnight"></a>

## Energi menurun tengah malam

Penurunan bisa berupa reset nyata, penggantian, atau koreksi. Deklarasikan kebijakan dan tambahkan `reset_at` dari bukti sumber nyata. Waktu pemutaran ulang HA bukan penanda reset. `total_increasing` tidak cocok untuk energi bersih bertanda. Pencacah dengan asal berbeda tidak dijumlahkan.

<a id="voltage-looks-calibrated-but-watts-still-differ"></a>

## Tegangan tampak terkalibrasi tetapi watt berbeda

Kalibrasi khusus untuk besaran tertentu. Koreksi tegangan tidak memvalidasi arus, hubungan fase, daya, atau energi terakumulasi. Kolom faktor hanya dokumentasi: nilai sudah harus memuat koreksi yang dimaksud.

<a id="yaml-fails-although-another-parser-accepts-it"></a>

## YAML gagal walaupun parser lain menerimanya

Apit waktu dengan tanda kutip, hapus alias/jangkar/tag khusus dan kunci duplikat, gunakan bilangan berhingga. Kolom tidak dikenal dianggap kesalahan untuk menangkap salah ketik. Batasan berlaku untuk kedua format. Gunakan JSON untuk pertukaran jika skalar YAML ambigu menimbulkan masalah.

<a id="ha-import-fails-on-timestamps"></a>

## Impor HA gagal pada stempel waktu

Atur `timestamp_attribute` ke atribut waktu pengukuran yang nyata. `last_reported` hanya membuktikan penerimaan oleh HA. Tanpa waktu sumber, alat tidak dapat menentukan kesegaran; biarkan sampel tidak tersedia. Tidak ada token atau koneksi yang perlu didiagnosis: impor bersifat luring.

<a id="safe-issue-report"></a>

## Laporan masalah yang aman

Sertakan versi paket/Python, kode stabil, kontrak sintetis minimal, `--at` terpilih, hasil yang diharapkan dan aktual. Jangan lampirkan ekspor HA lengkap, token, alamat sebenarnya, jadwal rumah tangga, atau ID perangkat privat. Dalam reproduksi, 0 W dan sampel tidak tersedia harus tetap berbeda.
