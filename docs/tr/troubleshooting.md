<a id="troubleshooting"></a>

# Sorun giderme

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
<a href="../ja/troubleshooting.md" lang="ja" dir="ltr">日本語</a> ·
<a href="../ko/troubleshooting.md" lang="ko" dir="ltr">한국어</a> ·
<a href="../nl/troubleshooting.md" lang="nl" dir="ltr">Nederlands</a> ·
<a href="../pl/troubleshooting.md" lang="pl" dir="ltr">Polski</a> ·
<a href="../pt/troubleshooting.md" lang="pt" dir="ltr">Português</a> ·
<a href="../ru/troubleshooting.md" lang="ru" dir="ltr">Русский</a> ·
<a href="../th/troubleshooting.md" lang="th" dir="ltr">ไทย</a> ·
<a href="troubleshooting.md" lang="tr" dir="ltr">Türkçe</a> ·
<a href="../uk/troubleshooting.md" lang="uk" dir="ltr">Українська</a> ·
<a href="../vi/troubleshooting.md" lang="vi" dir="ltr">Tiếng Việt</a> ·
<a href="../zh-Hans/troubleshooting.md" lang="zh-Hans" dir="ltr">简体中文</a> ·
<a href="../zh-Hant/troubleshooting.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->
<a id="a-three-outlet-strip-cannot-produce-three-power-readings"></a>

## Üç çıkışlı priz grubu üç güç okuması üretmez

`scope_outside`, istenen bireysel sonucun daha geniş bir ölçümü kullandığı anlamına gelir. Tüm priz grubu için bir varlık tutun. Bireysel güç için doğru kapsamda bağımsız ölçümler gerekir. Açık röle yükün tükettiğini kanıtlamaz; elektrik tüketen pompa su akışını kanıtlamaz.

<a id="a-migrated-sensor-doubles-the-total"></a>

## Taşınmış bir sensör toplamı ikiye katlıyor

Tek başına `alias_stream` bilgilendiricidir. `duplicate_stream`, iki kopyanın da toplamda olduğunu belirtir. Aynı CT'nin kopyalarına aynı kaynak kimliğini verin ve toplamda yalnızca birini tutun. Sırf kontrolü susturmak için kaynak kimliğini değiştirmeyin.

![Bir kaynak ve iki gösterim](../images/duplicate-stream.svg)

<a id="no-numeric-sum-despite-individually-plausible-numbers"></a>

## Makul değerlere rağmen sayısal toplam yok

`sample_stale`, `sample_future`, `sample_skew`, `sample_missing`, `incomplete_coverage`, `unit_dimension`, `scope_overlap` denetleyin. Gerçek kaynağı yenileyin ve ölçüm zamanını koruyun. İzin verilen yaşı artırmak politikayı değiştirir, ölçümü onarmaz. Tam toplam beyan edilen yapraklara göre değerlendirilir: beyanı da denetleyin.

![Sentetik örnek kalitesi zaman çizelgesi](../images/sample-quality.svg)

<a id="energy-decreased-at-midnight"></a>

## Enerji gece yarısında azaldı

Düşüş gerçek sıfırlama, değişim veya düzeltme olabilir. Politikayı beyan edin ve gerçek kaynak kanıtından `reset_at` ekleyin. HA yeniden oynatma zamanı sıfırlama işareti değildir. `total_increasing`, işaretli net enerjiye uygun değildir. Farklı başlangıçlı sayaçlar toplanmaz.

<a id="voltage-looks-calibrated-but-watts-still-differ"></a>

## Gerilim kalibre görünüyor ama watt değerleri farklı

Kalibrasyon büyüklüğe özeldir. Gerilim düzeltmesi akımı, faz ilişkisini, gücü veya birikmiş enerjiyi doğrulamaz. Katsayı alanı yalnız belgelemedir: değerler amaçlanan düzeltmeyi zaten içermelidir.

<a id="yaml-fails-although-another-parser-accepts-it"></a>

## Başka ayrıştırıcı kabul ettiği halde YAML başarısız

Zaman damgalarını tırnak içine alın, takma adları/çapaları/özel etiketleri ve yinelenen anahtarları kaldırın, sonlu sayılar kullanın. Yazım hatalarını yakalamak için bilinmeyen alanlar hatadır. Sınırlar iki biçim için de geçerlidir. Belirsiz YAML skalerleri sorun çıkarıyorsa veri alışverişinde JSON kullanın.

<a id="ha-import-fails-on-timestamps"></a>

## HA içe aktarımı zaman damgalarında başarısız

`timestamp_attribute` alanını gerçek ölçüm zamanı özniteliğine ayarlayın. `last_reported` yalnızca HA'nın aldığını kanıtlar. Kaynak zamanı olmadan araç güncelliği belirleyemez; örneği kullanılamaz bırakın. Teşhis edilecek token veya bağlantı yoktur: içe aktarım çevrimdışıdır.

<a id="safe-issue-report"></a>

## Güvenli sorun bildirimi

Paket/Python sürümlerini, kalıcı kodları, en küçük sentetik sözleşmeyi, seçilen `--at`, beklenen ve gerçek sonucu ekleyin. Tam HA dışa aktarımı, tokenlar, gerçek adres, ev programları veya özel cihaz kimlikleri eklemeyin. Tekrar üretimde 0 W ile kullanılamayan örnek ayrı kalmalıdır.
