<a id="contract-schema-v1"></a>

# Lược đồ hợp đồng v1

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
<a href="../id/schema.md" lang="id" dir="ltr">Bahasa Indonesia</a> ·
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
<a href="schema.md" lang="vi" dir="ltr">Tiếng Việt</a> ·
<a href="../zh-Hans/schema.md" lang="zh-Hans" dir="ltr">简体中文</a> ·
<a href="../zh-Hant/schema.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->
[schema.json](../../schema.json) mà máy đọc được mô tả cấu trúc. Bộ phân tích Python là thẩm quyền về giới hạn; `audit` bổ sung ngữ nghĩa vật lý và thời gian mà JSON Schema không thể chứng minh. Tạo tệp cấu trúc bằng `python3 scripts/generate_schema.py`.

<a id="root-and-limits"></a>

## Gốc và giới hạn

Bắt buộc: số nguyên `schema_version: 1`, `scopes`, `meters`. Tùy chọn: `sums` (mặc định rỗng). Trường không biết bị từ chối ở mọi cấp. Tối đa 512 phạm vi, 512 đồng hồ và 128 tổng; phạm vi và đồng hồ không được rỗng. Mỗi tổng có 1–512 thành viên. Đầu vào UTF-8, tối đa 1.048.576 byte, độ sâu 16 và 20.000 nút giá trị. Khóa JSON trùng lặp, NaN/Infinity và bí danh/neo/thẻ tường minh YAML bị từ chối. Đặt mốc thời gian YAML trong dấu ngoặc kép để chúng vẫn là chuỗi.

Định danh gồm 1–96 ký tự ASCII: đầu tiên là chữ/số, sau đó là chữ, số, `.`, `_`, `-`. ID duy nhất trong từng tập hợp; phạm vi và đồng hồ có không gian tên riêng. Mọi thời gian đều chứa `T` và múi giờ. Số phải hữu hạn, không phải boolean, trong ±10^15 trừ khi có giới hạn chặt hơn.

<a id="physical-scopes"></a>

## Phạm vi vật lý

Mỗi phạm vi có `id`, `kind` (`site`, `circuit`, `strip`, `outlet`, `load`) và `parent` tùy chọn. Cha phải tồn tại và tạo thành rừng không chu trình. Đồng hồ ở cha bao phủ mọi hậu duệ. Loại phạm vi mang tính mô tả: không suy ra điện áp, pha, định mức, dây dẫn hay cha được phép. Người dùng khai báo tô-pô thực tế.

<a id="meters"></a>

## Đồng hồ

Các trường bắt buộc:

- `id`, `scope`: định danh số đo duy nhất và phạm vi vật lý được khai báo.
- `quantity`: `power`, `energy`, `voltage`, `current`.
- `unit`: lần lượt W/kW, Wh/kWh, V, A. Bộ phân tích chấp nhận từ vựng; bộ kiểm tra xác minh thứ nguyên.
- `kind`: `measured` hoặc `estimated`. Đây là khai báo, không phải kiểm chứng phòng thí nghiệm.
- `provenance`: danh tính ổn định của luồng đo vật lý, **không phải** biểu diễn HA/MQTT của nó. Các số đo bí danh dùng chung danh tính. Dấu/đại lượng/phạm vi khác nhau với cùng nguồn gốc tạo xung đột; mọi bí danh của luồng trở nên không khả dụng cho tổng, bất kể thứ tự đầu vào. Chọn nguồn gốc khác nhau cho các kênh vật lý thực sự khác nhau.
- `sign`: `nonnegative` cho độ lớn chỉ tiêu thụ/nhập/xuất; `signed` cho luồng hai chiều được khai báo. Phiên bản này không suy ra chiều vật lý nào là dương.
- `state_class`: `measurement`, `total`, `total_increasing`.
- `freshness_seconds`: tuổi tối đa dương, 0.001–604800 giây.

`reset` tùy chọn: `never`, `periodic`, `device_restart`, `unknown`, `not_applicable` (mặc định). Năng lượng đòi hỏi chính sách tường minh khác `not_applicable` và lớp trạng thái kiểu total. Năng lượng có dấu không được dùng `total_increasing`. Các đại lượng khác đòi hỏi `measurement` và `not_applicable`.

`sample`, `previous` tùy chọn: null hoặc đối tượng có `value` (số hoặc null), `measured_at`, `reset_at` tùy chọn. Mẫu trước phải cũ hơn. Bộ đếm không âm giảm đòi hỏi dấu đặt lại giữa các mẫu; `never` từ chối dấu đó. `reset_at` không được muộn hơn mẫu của nó và chỉ áp dụng cho năng lượng. Ngữ nghĩa đặt lại không biết tạo cảnh báo. Bộ đếm ròng có dấu có thể giảm hợp lệ; điểm gốc đúng vẫn là trách nhiệm của bên tạo dữ liệu.

`calibration` tùy chọn: `quantity`, `factor` dương (10^-12–10^12), định danh tổng hợp/riêng tư `reference`, `verified_at`. Nó ghi bằng chứng cho đúng đại lượng đó. Giá trị **đã được hiệu chuẩn**: bộ kiểm tra không bao giờ áp dụng hệ số lần nữa. Hiệu chuẩn trong tương lai hoặc hiệu chuẩn điện áp trên đồng hồ công suất là không hợp lệ. Không có hiệu chuẩn không chứng minh độ chính xác và không tự động là lỗi.

`entity_id`, `timestamp_attribute` tùy chọn: ánh xạ HA ngoại tuyến; xem [cách dùng](usage.md#offline-home-assistant-adapter).

<a id="sums"></a>

## Tổng

Bắt buộc: `id`, `scope` đích, danh sách ID đồng hồ trong `meters`, `quantity` (`power` hoặc `energy`), `coverage` (`partial` hoặc `complete`). `max_skew_seconds` tùy chọn: 0–604800, mặc định 2.

Thành viên phải thuộc phạm vi đích, có thứ nguyên và ngữ nghĩa dấu tương thích, dùng luồng vật lý khác nhau và không chồng lấp theo cha/con hoặc phạm vi giống hệt. Tổng đầy đủ bao phủ mọi **phạm vi lá được khai báo** dưới đích. Không thể phát hiện dây dẫn chưa khai báo. Tổng một phần khai báo rõ độ bao phủ một phần. Không hỗ trợ tổng lồng nhau; thành viên luôn tham chiếu đồng hồ.

Mọi thành viên phải có dữ liệu hợp lệ và mới; thời gian lấy mẫu phải nằm trong độ lệch cho phép. Năng lượng còn đòi hỏi điểm gốc `reset_at` tường minh giống hệt. Điều này kiểm tra sự đồng bộ đã khai báo, không kiểm tra độ chính xác tích lũy lịch sử. Tổng được chuyển về W hoặc Wh. Cố ý không hỗ trợ tổng dòng điện và điện áp vì chúng phụ thuộc tô-pô mạch.

Tổng dạng số không khả dụng khi thiếu bằng chứng bắt buộc hoặc kiểm tra ngữ nghĩa thất bại. Ước lượng lan truyền thành `kind: estimated`. Hai bí danh có thể cùng tồn tại trong danh mục, nhưng không được cùng đóng góp vào một tổng. Không suy ra tổng nào cho từng ổ cắm không được đo.

<a id="report-v1"></a>

## Báo cáo v1

Gốc: `schema_version`, thời gian đánh giá `at` chuẩn hóa về UTC, số lượng theo mức độ trong `summary`, `findings` được sắp xếp và `sums`. Mỗi phát hiện chứa `code`, `severity`, `path` kiểu JSON, `params` có cấu trúc; CLI thêm `message`. Mỗi tổng chứa `id`, `scope`, `quantity`, `unit` cơ sở, `value`, `status`, `kind`, `coverage`. Giá trị không biết là JSON null, không bao giờ NaN.
