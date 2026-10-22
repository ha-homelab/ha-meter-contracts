<a id="usage"></a>

# Kullanım

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
<a href="../ja/usage.md" lang="ja" dir="ltr">日本語</a> ·
<a href="../ko/usage.md" lang="ko" dir="ltr">한국어</a> ·
<a href="../nl/usage.md" lang="nl" dir="ltr">Nederlands</a> ·
<a href="../pl/usage.md" lang="pl" dir="ltr">Polski</a> ·
<a href="../pt/usage.md" lang="pt" dir="ltr">Português</a> ·
<a href="../ru/usage.md" lang="ru" dir="ltr">Русский</a> ·
<a href="../th/usage.md" lang="th" dir="ltr">ไทย</a> ·
<a href="usage.md" lang="tr" dir="ltr">Türkçe</a> ·
<a href="../uk/usage.md" lang="uk" dir="ltr">Українська</a> ·
<a href="../vi/usage.md" lang="vi" dir="ltr">Tiếng Việt</a> ·
<a href="../zh-Hans/usage.md" lang="zh-Hans" dir="ltr">简体中文</a> ·
<a href="../zh-Hant/usage.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->
<a id="audit"></a>

## Denetim

```sh
ha-meter-contracts check contract.json --json --lang en
ha-meter-contracts check examples/minimal.yaml --at 2026-01-01T12:00:05Z --lang es
```

`--at`, saat dilimli ISO 8601 zaman damgası kabul eder. Varsayılan güncel UTC'dir. Aynı girdi, zaman ve dil için JSON deterministiktir. Örnek `freshness_seconds` sınırı dahil güncel kalır; ancak sonrasında eskir. Gelecekteki örnek, gizli saat sapması toleransı olmadan geçersizdir.

Çıkış kodları: 0 = hata/uyarı yok; 1 = anlamsal veya örnek kalitesi sorunu; 2 = girdi/CLI hatası. Kullanılmayan takma ad gibi bilgilendirici bulgular başarısızlığa yol açmaz. `--json` raporları ve girdi hata nesnelerini stdout'a yazar. Bu seçenek olmadan denetim metni stdout'a, girdi hataları stderr'e gider. Kopuk çıktı borusu 2 döndürür.

Bulguları gizlemek için CI'da `|| true` kullanmayın. Kasten geçersiz örnekler açıkça çıkış 1'i doğrulamalıdır. Yardım ve sürüm 0 döndürür. `import-ha` daima JSON sözleşmesi yazar; `--json` bu şemayı değiştirmez.

<a id="python-library"></a>

## Python kitaplığı

```python
from datetime import datetime, timezone
from ha_meter_contracts import audit, load_document, parse_contract

contract = parse_contract(load_document("examples/valid-three-meters.json"))
report = audit(contract, at=datetime(2026, 1, 1, 12, 0, 5, tzinfo=timezone.utc))
assert report["sums"][0]["value"] == 720
```

`parse_contract` değişmez veri sınıfları oluşturur; `InputError`, `code`, `path`, `params` sağlar. Ayrıştırıcıyı her güvenilmeyen girdi sınırında kullanın. `audit`, doğrulanmış bir `Contract` bekler ve bulguları çevirmez. CLI yerelleştirilmiş `message` değerleri ekler. Kitaplıkta çağıran taraf değerlendirme zamanını açıkça seçer. Hiçbir API girdiyi değiştirmez veya dosya yazmaz.

<a id="offline-home-assistant-adapter"></a>

## Çevrimdışı Home Assistant bağdaştırıcısı

```sh
ha-meter-contracts import-ha examples/ha-contract.json --ha-states examples/ha-states.synthetic.json > /tmp/meter-contract.json
ha-meter-contracts check /tmp/meter-contract.json --at 2026-01-01T12:00:05Z --json
```

İstenen her ölçerde `entity_id` ve `timestamp_attribute` alanlarını eşleyin. Dışa aktarım, `entity_id`, `state` ve `attributes` içeren HA durumları dizisidir. Eşlenen öznitelik, saat dilimiyle özgün ISO ölçüm zamanını içermelidir. `attributes.unit_of_measurement` aynı boyutta olmalıdır; W/kW ve Wh/kWh sözleşme birimine çevrilir.

Yalnızca eşlenen değerler ve kaynak zamanları kopyalanır. Görünen adlar dahil diğer öznitelikler yok sayılır. Kesin olarak daha yeni bir örnek mevcut olanı `previous` alanına taşır. Aynı kaynak zamanıyla aynı değerin tekrarı idempotenttir; eski örnek veya aynı zamandaki çelişen değer `ha_sample_order` olarak reddedilir. Eksik varlıklar ve `unknown`/`unavailable` durumları örneği temizler; sıfıra dönüşmez. Eksik zaman, uyumsuz birim, bozuk değer veya yinelenen varlık kimliği içe aktarımı 2 ile başarısız yapar. Eşlenmeyen ölçerler değişmez. Özel sözleşmeler varlık kimlikleri içerebilir; açık örnekler sentetik tanımlayıcılar kullanır.

Normal HA dışa aktarımı çoğunlukla özgün zaman damgasını içermez. Bağdaştırıcı bu durumda onu uydurmayı bilerek reddeder. Zaman damgalı cihaz verisi alın veya ölçeri kullanılamaz bırakın. HA alma/güncelleme zamanları cihaz ölçümünü kanıtlamaz. Bağdaştırıcı asla `/api/states` adresine bağlanmaz veya token okumaz. HA'dan enerji sıfırlama işaretleri kopyalamaz; enerjiyi toplamadan önce doğrulanmış kanıtı ayrı ekleyin.

<a id="suggested-workflow"></a>

## Önerilen iş akışı

1. Fiziksel kapsam ağacını ve kaynak kimliklerini kablolama belgelerinden beyan edin.
2. Bir ölçer ve sabit sentetik örnekle başlayın.
3. Yalnız gerekli gözlemleri özel bir dosyaya aktarın.
4. Denetimi çalıştırın ve veriyi kullanan otomasyonu değiştirmeden önce her bulguyu inceleyin.
5. Geçişlerde özgün zamanları ve kalibrasyon kanıtlarını koruyun.

Paket düzeltme yapmaz, varlıkları yeniden adlandırmaz, cihazları sıfırlamaz veya otomasyon dağıtmaz.
