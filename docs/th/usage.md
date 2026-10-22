<a id="usage"></a>

# การใช้งาน

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
<a href="usage.md" lang="th" dir="ltr">ไทย</a> ·
<a href="../tr/usage.md" lang="tr" dir="ltr">Türkçe</a> ·
<a href="../uk/usage.md" lang="uk" dir="ltr">Українська</a> ·
<a href="../vi/usage.md" lang="vi" dir="ltr">Tiếng Việt</a> ·
<a href="../zh-Hans/usage.md" lang="zh-Hans" dir="ltr">简体中文</a> ·
<a href="../zh-Hant/usage.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->
<a id="audit"></a>

## ตรวจสอบ

```sh
ha-meter-contracts check contract.json --json --lang en
ha-meter-contracts check examples/minimal.yaml --at 2026-01-01T12:00:05Z --lang es
```

`--at` รับเวลา ISO 8601 พร้อมเขตเวลา ค่าเริ่มต้นคือ UTC ปัจจุบัน เมื่ออินพุต เวลา และภาษาเหมือนกัน JSON จะให้ผลแน่นอน ตัวอย่างยังสดใหม่จนถึงและรวมขอบเขต `freshness_seconds` หลังจากนั้นจึงล้าสมัย ตัวอย่างในอนาคตไม่ถูกต้อง ไม่มีค่าเผื่อความคลาดเคลื่อนนาฬิกาโดยปริยาย

รหัสออก: 0 = ไม่มีข้อผิดพลาด/คำเตือน; 1 = ปัญหาความหมายหรือคุณภาพตัวอย่าง; 2 = ข้อผิดพลาดอินพุต/CLI ข้อค้นพบเชิงข้อมูล เช่น ชื่อแทนที่ไม่ได้ใช้ ไม่ทำให้ล้มเหลว `--json` เขียนรายงานและออบเจ็กต์ข้อผิดพลาดอินพุตไป stdout หากไม่มีตัวเลือกนี้ ข้อความตรวจสอบไป stdout และข้อผิดพลาดอินพุตไป stderr ไปป์เอาต์พุตที่ขาดคืน 2

อย่าใช้ `|| true` ใน CI เพื่อซ่อนข้อค้นพบ ตัวอย่างที่จงใจไม่ถูกต้องควรตรวจรหัสออก 1 อย่างชัดเจน คำสั่งช่วยเหลือและรุ่นคืน 0 `import-ha` เขียนสัญญา JSON เสมอ `--json` ไม่เปลี่ยนสคีมานั้น

<a id="python-library"></a>

## ไลบรารี Python

```python
from datetime import datetime, timezone
from ha_meter_contracts import audit, load_document, parse_contract

contract = parse_contract(load_document("examples/valid-three-meters.json"))
report = audit(contract, at=datetime(2026, 1, 1, 12, 0, 5, tzinfo=timezone.utc))
assert report["sums"][0]["value"] == 720
```

`parse_contract` สร้าง dataclass ที่แก้ไขไม่ได้ `InputError` เปิดให้เข้าถึง `code`, `path`, `params` ใช้ตัวแยกวิเคราะห์ทุกขอบเขตอินพุตที่ไม่เชื่อถือ `audit` ต้องการ `Contract` ที่ตรวจสอบแล้วและไม่แปลข้อค้นพบ CLI เพิ่มค่า `message` ที่แปลแล้ว ในไลบรารีผู้เรียกเลือกเวลาประเมินอย่างชัดเจน ไม่มี API ใดแก้อินพุตหรือเขียนไฟล์

<a id="offline-home-assistant-adapter"></a>

## อะแดปเตอร์ Home Assistant แบบออฟไลน์

```sh
ha-meter-contracts import-ha examples/ha-contract.json --ha-states examples/ha-states.synthetic.json > /tmp/meter-contract.json
ha-meter-contracts check /tmp/meter-contract.json --at 2026-01-01T12:00:05Z --json
```

แมป `entity_id` และ `timestamp_attribute` ในมิเตอร์แต่ละตัวที่ต้องการ ข้อมูลส่งออกเป็นอาร์เรย์สถานะ HA ที่มี `entity_id`, `state`, `attributes` แอตทริบิวต์ที่แมปต้องมีเวลา ISO ต้นฉบับของการวัดพร้อมเขตเวลา `attributes.unit_of_measurement` ต้องมีมิติเดียวกัน W/kW และ Wh/kWh ถูกแปลงเป็นหน่วยของสัญญา

คัดลอกเฉพาะค่าที่แมปและเวลาต้นทาง แอตทริบิวต์อื่นรวมทั้งชื่อที่อ่านง่ายถูกละเลย ตัวอย่างที่ใหม่กว่าจริงย้ายตัวอย่างเดิมไป `previous` การทำซ้ำค่าเดิมกับเวลาต้นทางเดิมให้ผลเหมือนเดิม ตัวอย่างเก่ากว่าหรือค่าขัดแย้งในเวลาเดียวกันถูกปฏิเสธเป็น `ha_sample_order` เอนทิตีที่หายไปและสถานะ `unknown`/`unavailable` ล้างตัวอย่าง ไม่เปลี่ยนเป็นศูนย์ เวลาที่ขาด หน่วยไม่เข้ากัน ค่าผิดรูปแบบ หรือ ID เอนทิตีซ้ำ ทำให้การนำเข้าล้มเหลวด้วย 2 มิเตอร์ที่ไม่แมปคงเดิม สัญญาส่วนตัวอาจมี ID เอนทิตี ตัวอย่างสาธารณะใช้ตัวระบุสังเคราะห์

ข้อมูลส่งออก HA ปกติมักไม่มีเวลาต้นฉบับ ในกรณีนี้อะแดปเตอร์จงใจปฏิเสธการแต่งเวลาเอง หาข้อมูลอุปกรณ์ที่มีเวลา หรือปล่อยมิเตอร์ไม่พร้อมใช้ เวลารับ/อัปเดตของ HA ไม่พิสูจน์เวลาวัดของอุปกรณ์ อะแดปเตอร์ไม่เชื่อมต่อ `/api/states` หรืออ่านโทเค็น และไม่คัดลอกเครื่องหมายรีเซ็ตพลังงานจาก HA ให้เพิ่มหลักฐานที่ตรวจสอบแล้วแยกต่างหากก่อนรวมพลังงาน

<a id="suggested-workflow"></a>

## ขั้นตอนที่แนะนำ

1. ประกาศต้นไม้ขอบเขตกายภาพและแหล่งกำเนิดจากเอกสารการเดินสาย
2. เริ่มด้วยมิเตอร์หนึ่งตัวและตัวอย่างสังเคราะห์คงที่
3. ส่งออกเฉพาะข้อมูลสังเกตที่จำเป็นลงไฟล์ส่วนตัว
4. รันการตรวจสอบและทบทวนทุกข้อค้นพบก่อนแก้ระบบอัตโนมัติที่รับข้อมูลต่อ
5. เก็บเวลาต้นฉบับและหลักฐานการสอบเทียบไว้ระหว่างย้ายระบบ

แพ็กเกจไม่แก้ปัญหาอัตโนมัติ ไม่เปลี่ยนชื่อเอนทิตี ไม่รีเซ็ตอุปกรณ์ และไม่ติดตั้งระบบอัตโนมัติ
