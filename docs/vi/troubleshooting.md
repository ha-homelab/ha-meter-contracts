<a id="troubleshooting"></a>

# Khắc phục sự cố

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
<a href="../tr/troubleshooting.md" lang="tr" dir="ltr">Türkçe</a> ·
<a href="../uk/troubleshooting.md" lang="uk" dir="ltr">Українська</a> ·
<a href="troubleshooting.md" lang="vi" dir="ltr">Tiếng Việt</a> ·
<a href="../zh-Hans/troubleshooting.md" lang="zh-Hans" dir="ltr">简体中文</a> ·
<a href="../zh-Hant/troubleshooting.md" lang="zh-Hant" dir="ltr">繁體中文</a>
</p>
<!-- language-navigation:end -->
<a id="a-three-outlet-strip-cannot-produce-three-power-readings"></a>

## Ổ điện ba cổng không tạo ra ba số đo công suất

`scope_outside` nghĩa là kết quả riêng được yêu cầu dùng số đo rộng hơn. Giữ một thực thể cho toàn bộ ổ điện. Muốn công suất riêng cần số đo độc lập đúng phạm vi. Rơ-le bật không chứng minh tải tiêu thụ; bơm tiêu thụ điện không chứng minh nước chảy.

<a id="a-migrated-sensor-doubles-the-total"></a>

## Cảm biến sau di chuyển làm tổng tăng gấp đôi

Riêng `alias_stream` mang tính thông tin. `duplicate_stream` nghĩa là cả hai bản sao nằm trong tổng. Gán cùng nguồn gốc cho các bản sao cùng CT và chỉ giữ một trong tổng. Đừng đổi nguồn gốc chỉ để tắt kiểm tra.

![Một nguồn và hai biểu diễn](../images/duplicate-stream.svg)

<a id="no-numeric-sum-despite-individually-plausible-numbers"></a>

## Không có tổng dạng số dù giá trị hợp lý

Kiểm tra `sample_stale`, `sample_future`, `sample_skew`, `sample_missing`, `incomplete_coverage`, `unit_dimension`, `scope_overlap`. Làm mới nguồn thực tế và giữ thời gian lấy mẫu. Tăng tuổi cho phép thay đổi chính sách, không sửa số đo. Tổng đầy đủ được đánh giá theo các lá đã khai báo: hãy kiểm tra cả khai báo.

![Dòng thời gian tổng hợp về chất lượng mẫu](../images/sample-quality.svg)

<a id="energy-decreased-at-midnight"></a>

## Năng lượng giảm lúc nửa đêm

Giảm có thể do đặt lại thực, thay thế hoặc hiệu chỉnh. Khai báo chính sách và thêm `reset_at` từ bằng chứng nguồn thực tế. Thời gian phát lại HA không phải dấu đặt lại. `total_increasing` không phù hợp với năng lượng ròng có dấu. Các bộ đếm khác điểm gốc không được cộng.

<a id="voltage-looks-calibrated-but-watts-still-differ"></a>

## Điện áp có vẻ đã hiệu chuẩn nhưng watt khác nhau

Hiệu chuẩn dành riêng cho đại lượng. Hiệu chỉnh điện áp không xác nhận dòng điện, quan hệ pha, công suất hay năng lượng tích lũy. Trường hệ số chỉ để ghi tài liệu: giá trị phải chứa sẵn hiệu chỉnh mong muốn.

<a id="yaml-fails-although-another-parser-accepts-it"></a>

## YAML thất bại dù bộ phân tích khác chấp nhận

Đặt thời gian trong dấu ngoặc kép, bỏ bí danh/neo/thẻ tùy chỉnh và khóa trùng, dùng số hữu hạn. Trường không biết là lỗi để bắt lỗi gõ. Giới hạn áp dụng cho cả hai định dạng. Dùng JSON để trao đổi nếu vô hướng YAML mơ hồ gây vấn đề.

<a id="ha-import-fails-on-timestamps"></a>

## Nhập HA thất bại ở mốc thời gian

Đặt `timestamp_attribute` thành thuộc tính thời gian đo thực sự. `last_reported` chỉ chứng minh HA nhận dữ liệu. Không có thời gian nguồn, công cụ không thể xác định độ mới; để mẫu không khả dụng. Không có token hay kết nối để chẩn đoán: việc nhập là ngoại tuyến.

<a id="safe-issue-report"></a>

## Báo cáo sự cố an toàn

Kèm phiên bản gói/Python, mã ổn định, hợp đồng tổng hợp tối thiểu, `--at` đã chọn, kết quả mong đợi và thực tế. Không đính kèm toàn bộ bản xuất HA, token, địa chỉ thật, lịch sinh hoạt gia đình hay ID thiết bị riêng tư. Trong bản tái hiện, 0 W và mẫu không khả dụng phải luôn được phân biệt.
