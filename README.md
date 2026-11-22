# Labtainer: Browser Hijacking Defense & Incident Response

Bài lab thực hành điều tra sự cố chiếm quyền điều khiển trình duyệt (Browser Hijacking) và thiết lập chính sách phòng thủ doanh nghiệp bằng **Mozilla AutoConfig** trên nền tảng **Labtainers**.

---

## 📌 Tổng quan kịch bản
- **Nạn nhân / Máy trạm (`workstation`)**: Máy trạm của nhân viên NovaCorp có triệu chứng dính browser hijacker: khi mở Firefox, trang chủ tự động chuyển sang trang quảng cáo lạ (`http://ads.local:8080/`) và công cụ tìm kiếm mặc định bị đổi thành `AdsSearch`.
- **Hồ sơ sự cố (`~/incident/`)**: Chứa 3 extension nghi vấn đã được cô lập (`ext-a`, `ext-b`, `ext-c`), mỗi extension chỉ gồm file khai báo tĩnh `manifest.json` (không chứa JavaScript độc hại thực thi):
  - `ext-a`: Tiện ích mở rộng thông thường, chỉ yêu cầu quyền `storage`.
  - `ext-b`: Tiện ích mở rộng độc hại, chứa `chrome_settings_overrides` chuyển hướng `homepage` về `http://ads.local:8080/` và `search_provider` về `AdsSearch` -> **Thủ phạm**.
  - `ext-c`: Tiện ích mở rộng có quyền rộng (`tabs`, `history`) nhưng không can thiệp cài đặt trình duyệt (nhiễu điều tra).
- **Dịch vụ mạng nội bộ**: Web server mô phỏng chạy cổng 8080 phục vụ trang quảng cáo `http://ads.local:8080/` và cổng thông tin nội bộ an toàn `http://novacorp.local:8080/`.

---

## 🎯 6 Nhiệm vụ của sinh viên (Tasks)
1. **Task 1: Xác nhận triệu chứng**
   - Kiểm tra `~/.mozilla/firefox/default/user.js`, ghi nhận URL trang chủ và search engine bị thay đổi vào `~/incident/trieu_chung.txt`.
2. **Task 2: Trích xuất quyền của 3 extension**
   - Đọc các trường `permissions`, `host_permissions` và `chrome_settings_overrides` từ `manifest.json` của cả 3 extension, lưu vào `~/incident/quyen_extension.txt`.
3. **Task 3: Phân tích và kết luận thủ phạm**
   - Xác định `ext-b` là thủ phạm dựa trên trường `chrome_settings_overrides`, ghi phân tích vào `~/incident/ketluan.txt`.
4. **Task 4: Gỡ bỏ và khôi phục cấu hình**
   - Xóa thư mục extension độc hại `ext-b`, xóa 2 dòng `user_pref` bị nhiễm trong `user.js`, ghi log vào `~/incident/go_bo.log`.
5. **Task 5: Triển khai chính sách doanh nghiệp bằng Mozilla AutoConfig**
   - Tạo `/usr/lib/firefox/defaults/pref/local-settings.js` nạp file cấu hình `mozilla.cfg`.
   - Tạo `/usr/lib/firefox/mozilla.cfg` (bắt đầu bằng dòng `//`) khóa Homepage về `http://novacorp.local:8080/`, khóa Search engine về `NovaSearch`, và chặn hoàn toàn việc cài extension mới (`lockPref("xpinstall.enabled", false);`).
6. **Task 6: Kiểm chứng chính sách bảo mật**
   - Khởi động Firefox xác nhận các khóa ở trạng thái **locked** trong `about:config`.
   - Chạy script kiểm tra tự động `./check_policy.py` và xác nhận đạt kết quả `PASS`.

---

## 🚀 Cài đặt và Khởi chạy qua Labtainers

### 1. Cài đặt tự động bằng lệnh `imodule`
Trên bất kỳ máy cài đặt Labtainers, thực thi lệnh sau để nạp bài lab trực tiếp từ GitHub:
```bash
imodule https://github.com/Huan-0808/browser-hijack-defense-lab/raw/master/imodule_browser-hijack-defense.tar
```

Hoặc tải thủ công file `imodule_browser-hijack-defense.tar` và nạp:
```bash
imodule file:///path/to/imodule_browser-hijack-defense.tar
```

### 2. Bắt đầu bài thực hành
```bash
labtainer browser-hijack-defense
```

### 3. Dừng và Chấm điểm bài thực hành
```bash
stoplab browser-hijack-defense
gradelab browser-hijack-defense
```

---

## 📁 Cấu trúc thư mục Lab

- `imodule_browser-hijack-defense.tar`: Gói phân phối sẵn cho hệ thống Labtainers.
- `config/`: Cấu hình container, tài khoản và tham số (`start.config`, `parameter.config`).
- `dockerfiles/`: Dockerfile cấu hình môi trường máy trạm `workstation` trên nền `labtainer.firefox`.
- `docs/`: Tài liệu hướng dẫn thực hành (`read_first.txt`, `browser-hijack-defense.tex`, `BAO_CAO.md`).
- `instr_config/`: Cấu hình đánh giá và chấm điểm tự động (`results.config`, `goals.config`).
- `workstation/`: Cấu hình hệ thống, mock web server, file profile và công cụ kiểm thử.
