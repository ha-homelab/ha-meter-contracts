<a id="troubleshooting"></a>

# การแก้ปัญหา

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
<a href="troubleshooting.md" lang="th" dir="ltr">ไทย</a> ·
<a href="../tr/troubleshooting.md" lang="tr" dir="ltr">Türkçe</a> ·
<a href="../uk/troubleshooting.md" lang="uk" dir="ltr">Українська</a> ·
<a href="../vi/troubleshooting.md" lang="vi" dir="ltr">Tiếng Việt</a> ·
<a href="../zh-Hans/troubleshooting.md" lang="zh-Hans" dir="ltr">简体中文</a> ·
<a href="../zh-Hant/troubleshooting.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->
<a id="a-three-outlet-strip-cannot-produce-three-power-readings"></a>

## ปลั๊กพ่วงสามช่องไม่ได้ให้ค่ากำลังสามค่า

`scope_outside` หมายถึงผลรายตัวที่ขอใช้การวัดขอบเขตกว้างกว่า เก็บเอนทิตีเดียวสำหรับปลั๊กพ่วงทั้งชุด กำลังรายตัวต้องมีการวัดอิสระในขอบเขตที่ถูกต้อง รีเลย์เปิดไม่พิสูจน์ว่าโหลดใช้ไฟ ปั๊มใช้ไฟไม่พิสูจน์ว่ามีน้ำไหล

<a id="a-migrated-sensor-doubles-the-total"></a>

## เซนเซอร์ที่ย้ายระบบทำให้ยอดรวมเป็นสองเท่า

`alias_stream` เพียงอย่างเดียวเป็นข้อมูล `duplicate_stream` หมายถึงสำเนาทั้งสองอยู่ในผลรวม ให้สำเนาของ CT เดียวกันใช้แหล่งกำเนิดเดียวกันและเก็บเพียงหนึ่งในผลรวม อย่าเปลี่ยนแหล่งกำเนิดเพียงเพื่อให้การตรวจหยุดเตือน

![หนึ่งแหล่งข้อมูลและสองรูปแทน](../images/duplicate-stream.svg)

<a id="no-numeric-sum-despite-individually-plausible-numbers"></a>

## ไม่มีผลรวมตัวเลขแม้ค่าดูน่าเชื่อถือ

ตรวจ `sample_stale`, `sample_future`, `sample_skew`, `sample_missing`, `incomplete_coverage`, `unit_dimension`, `scope_overlap` อัปเดตแหล่งข้อมูลจริงและคงเวลาวัดไว้ การเพิ่มอายุที่อนุญาตคือเปลี่ยนนโยบาย ไม่ได้ซ่อมการวัด ผลรวมครบถ้วนประเมินเทียบกับใบที่ประกาศ จึงต้องตรวจคำประกาศด้วย

![เส้นเวลาสังเคราะห์ของคุณภาพตัวอย่าง](../images/sample-quality.svg)

<a id="energy-decreased-at-midnight"></a>

## พลังงานลดลงตอนเที่ยงคืน

การลดอาจเป็นรีเซ็ตจริง การเปลี่ยนอุปกรณ์ หรือการแก้ค่า ประกาศนโยบายและเพิ่ม `reset_at` จากหลักฐานต้นทางจริง เวลาเล่นข้อมูล HA ซ้ำไม่ใช่เครื่องหมายรีเซ็ต `total_increasing` ไม่เหมาะกับพลังงานสุทธิที่มีเครื่องหมาย ตัวนับที่มีจุดเริ่มต้นต่างกันจะไม่ถูกรวม

<a id="voltage-looks-calibrated-but-watts-still-differ"></a>

## แรงดันดูสอบเทียบแล้วแต่วัตต์ต่างกัน

การสอบเทียบจำเพาะต่อปริมาณ การแก้แรงดันไม่ยืนยันกระแส ความสัมพันธ์เฟส กำลัง หรือพลังงานสะสม ฟิลด์ตัวคูณเป็นเพียงบันทึก ค่าต้องมีการแก้ที่ต้องการอยู่แล้ว

<a id="yaml-fails-although-another-parser-accepts-it"></a>

## YAML ล้มเหลวทั้งที่ตัวแยกวิเคราะห์อื่นยอมรับ

ใส่เวลาในเครื่องหมายคำพูด ลบ alias/anchor/tag กำหนดเองและคีย์ซ้ำ ใช้จำนวนที่มีค่าจำกัด ฟิลด์ไม่รู้จักถือเป็นข้อผิดพลาดเพื่อจับการพิมพ์ผิด ขีดจำกัดใช้ทั้งสองรูปแบบ ใช้ JSON แลกเปลี่ยนหากสเกลาร์ YAML ที่กำกวมก่อปัญหา

<a id="ha-import-fails-on-timestamps"></a>

## การนำเข้า HA ล้มเหลวที่เวลา

ตั้ง `timestamp_attribute` ให้เป็นแอตทริบิวต์เวลาวัดจริง `last_reported` พิสูจน์เพียง HA รับข้อมูล หากไม่มีเวลาต้นทาง เครื่องมือระบุความสดใหม่ไม่ได้ ให้ตัวอย่างไม่พร้อมใช้ ไม่มีโทเค็นหรือการเชื่อมต่อให้วินิจฉัย การนำเข้าเป็นแบบออฟไลน์

<a id="safe-issue-report"></a>

## การรายงานปัญหาอย่างปลอดภัย

ระบุรุ่นแพ็กเกจ/Python รหัสคงที่ สัญญาสังเคราะห์ขนาดเล็กที่สุด `--at` ที่เลือก ผลที่คาดและผลจริง อย่าแนบข้อมูลส่งออก HA ทั้งชุด โทเค็น ที่อยู่จริง ตารางกิจวัตรบ้าน หรือ ID อุปกรณ์ส่วนตัว ในตัวอย่างทำซ้ำปัญหาต้องแยก 0 W ออกจากตัวอย่างไม่พร้อมใช้
