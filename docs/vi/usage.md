<a id="usage"></a>

# Cách dùng

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
<a href="../tr/usage.md" lang="tr" dir="ltr">Türkçe</a> ·
<a href="../uk/usage.md" lang="uk" dir="ltr">Українська</a> ·
<a href="usage.md" lang="vi" dir="ltr">Tiếng Việt</a> ·
<a href="../zh-Hans/usage.md" lang="zh-Hans" dir="ltr">简体中文</a> ·
<a href="../zh-Hant/usage.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->
<a id="audit"></a>

## Kiểm tra

```sh
ha-meter-contracts check contract.json --json --lang en
ha-meter-contracts check examples/minimal.yaml --at 2026-01-01T12:00:05Z --lang es
```

`--at` chấp nhận mốc thời gian ISO 8601 có múi giờ. Mặc định là UTC hiện tại. Với cùng đầu vào, thời gian và ngôn ngữ, JSON có tính xác định. Mẫu vẫn mới đến hết giới hạn `freshness_seconds`; chỉ cũ sau đó. Mẫu trong tương lai không hợp lệ, không có dung sai lệch đồng hồ ngầm định.

Mã thoát: 0 = không lỗi/cảnh báo; 1 = vấn đề ngữ nghĩa hoặc chất lượng mẫu; 2 = lỗi đầu vào/CLI. Phát hiện thông tin như bí danh không dùng không gây thất bại. `--json` ghi báo cáo và đối tượng lỗi đầu vào ra stdout. Không có tùy chọn này, văn bản kiểm tra đến stdout còn lỗi đầu vào đến stderr. Ống đầu ra bị ngắt trả về 2.

Không dùng `|| true` trong CI để che phát hiện. Ví dụ cố ý không hợp lệ phải kiểm tra rõ mã thoát 1. Trợ giúp và phiên bản trả về 0. `import-ha` luôn ghi hợp đồng JSON; `--json` không đổi lược đồ đó.

<a id="python-library"></a>

## Thư viện Python

```python
from datetime import datetime, timezone
from ha_meter_contracts import audit, load_document, parse_contract

contract = parse_contract(load_document("examples/valid-three-meters.json"))
report = audit(contract, at=datetime(2026, 1, 1, 12, 0, 5, tzinfo=timezone.utc))
assert report["sums"][0]["value"] == 720
```

`parse_contract` tạo các lớp dữ liệu bất biến; `InputError` cung cấp `code`, `path`, `params`. Dùng bộ phân tích tại mọi ranh giới đầu vào không đáng tin. `audit` yêu cầu `Contract` đã xác thực và không dịch phát hiện. CLI thêm giá trị `message` bản địa hóa. Trong thư viện, bên gọi chọn rõ thời gian đánh giá. Không API nào sửa đầu vào hay ghi tệp.

<a id="offline-home-assistant-adapter"></a>

## Bộ điều hợp Home Assistant ngoại tuyến

```sh
ha-meter-contracts import-ha examples/ha-contract.json --ha-states examples/ha-states.synthetic.json > /tmp/meter-contract.json
ha-meter-contracts check /tmp/meter-contract.json --at 2026-01-01T12:00:05Z --json
```

Ánh xạ `entity_id` và `timestamp_attribute` trên mỗi đồng hồ mong muốn. Bản xuất là mảng trạng thái HA với `entity_id`, `state` và `attributes`. Thuộc tính được ánh xạ phải chứa thời gian đo ISO gốc có múi giờ. `attributes.unit_of_measurement` phải cùng thứ nguyên; W/kW và Wh/kWh được chuyển thành đơn vị hợp đồng.

Chỉ sao chép giá trị được ánh xạ và thời gian nguồn. Thuộc tính khác, kể cả tên dễ đọc, bị bỏ qua. Mẫu mới hơn nghiêm ngặt chuyển mẫu hiện có sang `previous`. Lặp lại cùng giá trị với cùng thời gian nguồn là lũy đẳng; mẫu cũ hơn hoặc giá trị mâu thuẫn tại cùng thời gian bị từ chối dưới dạng `ha_sample_order`. Thực thể thiếu và trạng thái `unknown`/`unavailable` xóa mẫu; chúng không trở thành số không. Thiếu thời gian, đơn vị không tương thích, giá trị sai dạng hoặc ID thực thể trùng khiến nhập thất bại với 2. Đồng hồ không được ánh xạ giữ nguyên. Hợp đồng riêng tư có thể chứa ID thực thể; ví dụ công khai dùng định danh tổng hợp.

Bản xuất HA thông thường thường không chứa mốc thời gian gốc. Khi đó bộ điều hợp cố ý từ chối bịa ra nó. Lấy dữ liệu thiết bị có thời gian hoặc để đồng hồ không khả dụng. Thời gian nhận/cập nhật HA không chứng minh việc thiết bị lấy số đo. Bộ điều hợp không bao giờ kết nối `/api/states` hay đọc token. Nó không sao chép dấu đặt lại năng lượng từ HA; hãy thêm riêng bằng chứng đã kiểm chứng trước khi cộng năng lượng.

<a id="suggested-workflow"></a>

## Quy trình đề xuất

1. Khai báo cây phạm vi vật lý và nguồn gốc từ tài liệu dây dẫn.
2. Bắt đầu với một đồng hồ và ví dụ tổng hợp cố định.
3. Chỉ xuất những quan sát cần thiết vào tệp riêng tư.
4. Chạy kiểm tra và xem từng phát hiện trước khi đổi tự động hóa phụ thuộc.
5. Giữ thời gian gốc và bằng chứng hiệu chuẩn khi di chuyển.

Gói không khắc phục, đổi tên thực thể, đặt lại thiết bị hay triển khai tự động hóa.
