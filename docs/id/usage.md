<a id="usage"></a>

# Penggunaan

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
<a href="usage.md" lang="id" dir="ltr">Bahasa Indonesia</a> ·
<a href="../it/usage.md" lang="it" dir="ltr">Italiano</a> ·
<a href="../ja/usage.md" lang="ja" dir="ltr">日本語</a> ·
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

## Audit

```sh
ha-meter-contracts check contract.json --json --lang en
ha-meter-contracts check examples/minimal.yaml --at 2026-01-01T12:00:05Z --lang es
```

`--at` menerima stempel waktu ISO 8601 dengan zona waktu. Bawaannya UTC saat ini. Dengan masukan, waktu, dan bahasa yang sama, JSON bersifat deterministik. Sampel tetap segar sampai batas `freshness_seconds` inklusif; baru menjadi usang sesudahnya. Sampel masa depan tidak valid, tanpa toleransi selisih jam implisit.

Kode keluar: 0 = tanpa kesalahan/peringatan; 1 = masalah semantik atau kualitas sampel; 2 = kesalahan masukan/CLI. Temuan informatif seperti alias tidak terpakai tidak menyebabkan kegagalan. `--json` menulis laporan dan objek kesalahan masukan ke stdout. Tanpanya, teks audit menuju stdout dan kesalahan masukan menuju stderr. Pipa keluaran terputus mengembalikan 2.

Jangan gunakan `|| true` dalam CI untuk menyembunyikan temuan. Contoh yang sengaja tidak valid harus secara eksplisit memeriksa kode keluar 1. Bantuan dan versi mengembalikan 0. `import-ha` selalu menulis kontrak JSON; `--json` tidak mengubah skemanya.

<a id="python-library"></a>

## Pustaka Python

```python
from datetime import datetime, timezone
from ha_meter_contracts import audit, load_document, parse_contract

contract = parse_contract(load_document("examples/valid-three-meters.json"))
report = audit(contract, at=datetime(2026, 1, 1, 12, 0, 5, tzinfo=timezone.utc))
assert report["sums"][0]["value"] == 720
```

`parse_contract` membuat dataclass yang tidak dapat diubah; `InputError` menyediakan `code`, `path`, `params`. Gunakan parser pada setiap batas masukan tak tepercaya. `audit` mengharapkan `Contract` tervalidasi dan tidak menerjemahkan temuan. CLI menambahkan nilai `message` terlokalisasi. Dalam pustaka, pemanggil memilih waktu evaluasi secara eksplisit. Tidak ada API yang mengubah masukan atau menulis berkas.

<a id="offline-home-assistant-adapter"></a>

## Adaptor Home Assistant luring

```sh
ha-meter-contracts import-ha examples/ha-contract.json --ha-states examples/ha-states.synthetic.json > /tmp/meter-contract.json
ha-meter-contracts check /tmp/meter-contract.json --at 2026-01-01T12:00:05Z --json
```

Petakan `entity_id` dan `timestamp_attribute` pada setiap meter yang diinginkan. Ekspor merupakan array status HA dengan `entity_id`, `state`, dan `attributes`. Atribut yang dipetakan harus memuat waktu pengukuran ISO asli dengan zona waktu. `attributes.unit_of_measurement` harus memiliki dimensi yang sama; W/kW dan Wh/kWh dikonversi ke satuan kontrak.

Hanya nilai terpetakan dan waktu sumber yang disalin. Atribut lain, termasuk nama ramah pengguna, diabaikan. Sampel yang benar-benar lebih baru memindahkan sampel yang ada ke `previous`. Mengulang nilai sama dengan waktu sumber sama bersifat idempoten; sampel lebih tua atau nilai bertentangan pada waktu sama ditolak sebagai `ha_sample_order`. Entitas hilang dan status `unknown`/`unavailable` menghapus sampel; tidak menjadi nol. Waktu hilang, satuan tidak cocok, nilai cacat, atau ID entitas duplikat menggagalkan impor dengan 2. Meter yang tidak dipetakan tidak berubah. Kontrak privat bisa berisi ID entitas; contoh publik memakai pengenal sintetis.

Ekspor HA biasa sering tidak memiliki stempel waktu asli. Dalam keadaan itu, adaptor sengaja menolak mengarangnya. Dapatkan data perangkat bertanda waktu atau biarkan meter tidak tersedia. Waktu penerimaan/pembaruan HA tidak membuktikan akuisisi perangkat. Adaptor tidak pernah terhubung ke `/api/states` atau membaca token. Ia tidak menyalin penanda reset energi dari HA; tambahkan bukti terverifikasi secara terpisah sebelum menjumlahkan energi.

<a id="suggested-workflow"></a>

## Alur kerja yang disarankan

1. Deklarasikan pohon cakupan fisik dan asal-usul sumber berdasarkan dokumentasi pengawatan.
2. Mulai dengan satu meter dan contoh sintetis tetap.
3. Ekspor hanya pengamatan yang diperlukan ke berkas privat.
4. Jalankan audit dan tinjau setiap temuan sebelum mengubah otomatisasi hilir.
5. Pertahankan waktu asli dan bukti kalibrasi saat migrasi.

Paket ini tidak memperbaiki, mengganti nama entitas, mereset perangkat, atau menerapkan otomatisasi.
