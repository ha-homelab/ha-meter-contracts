<a id="limits-and-trust-boundary"></a>

# Sınırlar ve güven sınırı

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
<a href="../ja/limits.md" lang="ja" dir="ltr">日本語</a> ·
<a href="../ko/limits.md" lang="ko" dir="ltr">한국어</a> ·
<a href="../nl/limits.md" lang="nl" dir="ltr">Nederlands</a> ·
<a href="../pl/limits.md" lang="pl" dir="ltr">Polski</a> ·
<a href="../pt/limits.md" lang="pt" dir="ltr">Português</a> ·
<a href="../ru/limits.md" lang="ru" dir="ltr">Русский</a> ·
<a href="../th/limits.md" lang="th" dir="ltr">ไทย</a> ·
<a href="limits.md" lang="tr" dir="ltr">Türkçe</a> ·
<a href="../uk/limits.md" lang="uk" dir="ltr">Українська</a> ·
<a href="../vi/limits.md" lang="vi" dir="ltr">Tiếng Việt</a> ·
<a href="../zh-Hans/limits.md" lang="zh-Hans" dir="ltr">简体中文</a> ·
<a href="../zh-Hant/limits.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->
Bu, çevrimdışı bir beyan doğrulayıcısıdır; koruma denetleyicisi, elektrikçi test cihazı, kablolama keşif hizmeti veya eylem yürüten Home Assistant entegrasyonu değildir.

- Tek bir toplam okuma, bilinmeyen üç yükün aynı andaki kesin gücünü çıkaramaz. İstatistiksel tahminler, korumaya uygun ölçümler değil tahminler olurdu.
- Kapsam, kaynak kimliği, işaret yönü ve kalibrasyon beyanları işletmeciden gelir. Yanlış beyanlar, fiziksel olarak geçersiz bir sistemi yapısal olarak geçerli gösterebilir.
- `complete`, bağımsız olarak doğrulanmış kablolamaya değil, beyan edilmiş yapraklara göre tam anlamına gelir. Kaynaktaki sıfırlama işareti, güvenilen bir kanıttır; cihaz tasdiki değildir.
- W, kW, Wh, kWh, V ve A desteklenir. Reaktif/görünür güç, üç fazlı cebir, CT doygunluğu, gerilim trafoları, sayaç taşması veya tarifeler modellenmez.
- Toplam üyeleri başka toplamlar değil doğrudan ölçerlerdir. Güç toplamları hizalı zaman damgaları gerektirir. Enerji toplamları açık ortak sayaç başlangıcı ve hizalı örnekler gerektirir.
- Değerler sonlu kayan noktalı sayılardır. Bu, faturalandırmaya uygun ondalık muhasebe değildir. Kalibrasyon katsayıları kaydedilir, uygulanmaz.
- Yalnızca güncel örnek ve isteğe bağlı bir önceki örnek denetlenir. Bu bir tarihçe veritabanı, anomali ya da kayma algılayıcısı veya tam sayaç bütünlüğü denetimi değildir.
- HA kaynak zaman damgaları var olmalı ve gerçekten ölçümün alınma anını göstermelidir. Önbelleğe ulaşma zamanları sessizce yerlerine kabul edilmez.
- JSON/YAML yüklemesi sınırlıdır; `audit` kitaplık API'si ayrıştırıcının ürettiği bir `Contract` bekler. Güvenilmeyen nesnelerden rastgele bozuk veri sınıfları oluşturmayın.
- Dosya girdisi yalnızca normal dosyaları kabul eder. Son yol bileşenindeki sembolik bağları, FIFO'ları, aygıtları ve dizinleri reddeder; engellemesiz açar ve okumadan önce açılan tanımlayıcıyı denetler. `O_NOFOLLOW` ve `O_NONBLOCK` bulunmayan platformlar dosyaları reddeder; oralarda zaten sınırlandırılmış bir dizgeyle `ha_meter_contracts.reader.loads_document` kullanın. Üst dizinlerdeki sembolik bağlar bir sandbox sınırı değildir. Dosya okunurken büyüse de bayt sınırı geçerlidir.
- Başarılı sonuç, rölelerin, vanaların, motorların fiziksel çalışmasını, pompa debisini veya elektrik güvenliğini kanıtlamaz. Otomatik onarım veya yeniden deneme yapılmaz.

Girdi ve çıktı, işletmecinin sağladığı varlık kimliklerini ve zamanları içerebilir. Gerçek sözleşmeleri/dışa aktarımları özel tutun. Depo yalnızca sentetik örnekler içerir. Program veri yüklemez; ancak raporu dış bir hizmete yönlendirmek işletmecinin seçimidir.
