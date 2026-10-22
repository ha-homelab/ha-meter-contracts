<a id="limits-and-trust-boundary"></a>

# Giới hạn và ranh giới tin cậy

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
<a href="../tr/limits.md" lang="tr" dir="ltr">Türkçe</a> ·
<a href="../uk/limits.md" lang="uk" dir="ltr">Українська</a> ·
<a href="limits.md" lang="vi" dir="ltr">Tiếng Việt</a> ·
<a href="../zh-Hans/limits.md" lang="zh-Hans" dir="ltr">简体中文</a> ·
<a href="../zh-Hant/limits.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->
Đây là bộ kiểm tra khai báo ngoại tuyến, không phải bộ điều khiển bảo vệ, thiết bị thử của thợ điện, dịch vụ khám phá dây dẫn hay tích hợp Home Assistant thực hiện hành động.

- Một số đo tổng không thể suy ra công suất đồng thời chính xác của ba tải chưa biết. Phỏng đoán thống kê chỉ là ước lượng, không phải số đo phù hợp cho bảo vệ.
- Phạm vi, nguồn gốc, chiều dấu và khai báo hiệu chuẩn do người vận hành cung cấp. Khai báo sai có thể khiến hệ thống vật lý không hợp lệ trông hợp lệ về cấu trúc.
- `complete` nghĩa là đầy đủ so với các nút lá đã khai báo, không phải dây dẫn đã được kiểm chứng độc lập. Dấu đặt lại từ nguồn là bằng chứng được tin cậy, không phải chứng thực thiết bị.
- Hỗ trợ W, kW, Wh, kWh, V và A. Không mô hình hóa công suất phản kháng/biểu kiến, đại số ba pha, bão hòa CT, biến áp điện áp, vòng quay bộ đếm hay biểu giá.
- Thành viên của tổng là đồng hồ trực tiếp, không phải tổng khác. Tổng công suất đòi hỏi mốc thời gian đồng bộ. Tổng năng lượng đòi hỏi điểm gốc bộ đếm chung tường minh và các mẫu đồng bộ.
- Giá trị là số dấu phẩy động hữu hạn. Đây không phải sổ sách thập phân đủ chuẩn thanh toán. Hệ số hiệu chuẩn được ghi lại, không được áp dụng.
- Chỉ kiểm tra một mẫu hiện tại và tùy chọn một mẫu trước đó. Đây không phải cơ sở dữ liệu lịch sử, bộ phát hiện bất thường hoặc trôi, hay kiểm toán toàn vẹn bộ đếm đầy đủ.
- Mốc thời gian nguồn HA phải tồn tại và thực sự biểu thị lúc lấy số đo. Thời gian bộ nhớ đệm nhận dữ liệu không được âm thầm chấp nhận thay thế.
- Việc nạp JSON/YAML có giới hạn; API thư viện `audit` yêu cầu `Contract` do bộ phân tích tạo ra. Không tạo các lớp dữ liệu tùy ý sai cấu trúc từ đối tượng không đáng tin cậy.
- Đầu vào tệp chỉ chấp nhận tệp thông thường. Nó từ chối liên kết tượng trưng ở thành phần đường dẫn cuối, FIFO, thiết bị và thư mục, mở không chặn rồi kiểm tra bộ mô tả đã mở trước khi đọc. Nền tảng không có `O_NOFOLLOW` và `O_NONBLOCK` từ chối đầu vào tệp; tại đó hãy dùng `ha_meter_contracts.reader.loads_document` với chuỗi đã được giới hạn. Liên kết trong thư mục cha không phải ranh giới sandbox. Giới hạn byte vẫn áp dụng nếu tệp lớn lên khi đang đọc.
- Kết quả đạt không chứng minh hoạt động vật lý của rơ-le, van, động cơ, lưu lượng bơm hay an toàn điện. Không thực hiện sửa chữa hay thử lại tự động.

Đầu vào và đầu ra có thể chứa ID thực thể cùng thời gian do người vận hành cung cấp. Giữ hợp đồng/bản xuất thực tế ở chế độ riêng tư. Kho mã chỉ chứa ví dụ tổng hợp. Chương trình không tải dữ liệu lên, nhưng chuyển báo cáo đến dịch vụ ngoài là lựa chọn của người vận hành.
