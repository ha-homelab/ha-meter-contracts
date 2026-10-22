<a id="limits-and-trust-boundary"></a>

# Batasan dan batas kepercayaan

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
<a href="limits.md" lang="id" dir="ltr">Bahasa Indonesia</a> ·
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
<a href="../zh-Hans/limits.md" lang="zh-Hans" dir="ltr">简体中文</a> ·
<a href="../zh-Hant/limits.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->
Ini adalah validator deklarasi luring, bukan pengendali proteksi, alat uji teknisi listrik, layanan penemuan pengawatan, atau integrasi Home Assistant yang melakukan tindakan.

- Satu pembacaan total tidak dapat memulihkan daya simultan yang tepat dari tiga beban tak diketahui. Dugaan statistik merupakan perkiraan, bukan pengukuran yang sesuai untuk proteksi.
- Cakupan, asal-usul, arah tanda, dan klaim kalibrasi diberikan operator. Deklarasi palsu dapat membuat sistem fisik yang tidak valid tampak valid secara struktural.
- `complete` berarti lengkap terhadap daun yang dideklarasikan, bukan pengawatan yang diverifikasi secara independen. Penanda reset sumber adalah bukti yang dipercaya, bukan atestasi perangkat.
- W, kW, Wh, kWh, V, dan A didukung. Kami tidak memodelkan daya reaktif/semu, aljabar tiga fase, saturasi CT, trafo tegangan, putaran balik pencacah, atau tarif.
- Anggota penjumlahan adalah meter langsung, bukan penjumlahan lain. Jumlah daya memerlukan stempel waktu selaras. Jumlah energi memerlukan asal pencacah bersama yang eksplisit dan sampel yang selaras.
- Nilai berupa bilangan titik mengambang berhingga. Ini bukan pembukuan desimal untuk penagihan. Faktor kalibrasi dicatat, bukan diterapkan.
- Hanya satu sampel saat ini dan sampel sebelumnya yang opsional diperiksa. Ini bukan basis data historis, pendeteksi anomali atau penyimpangan, maupun audit integritas pencacah secara menyeluruh.
- Stempel waktu sumber HA harus tersedia dan benar-benar menandakan akuisisi pengukuran. Waktu penerimaan tembolok tidak diam-diam diterima sebagai pengganti.
- Pemuatan JSON/YAML dibatasi; API pustaka `audit` mengharapkan `Contract` yang dihasilkan parser. Jangan membangun dataclass sembarang yang cacat dari objek yang tidak tepercaya.
- Masukan berkas hanya menerima berkas biasa. Tautan simbolik pada komponen jalur terakhir, FIFO, perangkat, dan direktori ditolak; berkas dibuka tanpa pemblokiran dan deskriptor yang terbuka diperiksa sebelum pembacaan. Platform tanpa `O_NOFOLLOW` dan `O_NONBLOCK` menolak masukan berkas; gunakan `ha_meter_contracts.reader.loads_document` dengan string yang sudah dibatasi di sana. Tautan simbolik pada direktori induk bukan batas sandbox. Batas byte tetap berlaku jika berkas membesar saat dibaca.
- Hasil lulus tidak membuktikan operasi fisik relai, katup, motor, aliran pompa, atau keselamatan listrik. Tidak ada perbaikan atau percobaan ulang otomatis.

Masukan dan keluaran dapat memuat ID entitas dan waktu dari operator. Simpan kontrak/ekspor nyata secara privat. Repositori hanya berisi contoh sintetis. Program tidak mengunggah data, tetapi meneruskan laporan ke layanan eksternal merupakan pilihan operator.
