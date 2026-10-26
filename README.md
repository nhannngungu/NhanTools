# NhanTools

Khung ứng dụng tiện ích Windows, Python 3.11+ và PySide6. Suite quản lý nhiều
module; từng công cụ có entry point Standalone và dùng chung logic, widget.
Hiện có Dashboard, All Tools, Settings và Hybrid Demo; chưa có công cụ thực tế.

## Cài đặt (PowerShell)

Chạy từ thư mục dự án:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Không cần kích hoạt virtualenv. Interpreter được chọn phải là Python 3.11 trở lên.

## Chạy

```powershell
# Suite
.\.venv\Scripts\python.exe -m apps.suite

# Standalone
.\.venv\Scripts\python.exe -m apps.standalone.demo

# Kiểm thử (không cần mở cửa sổ trên màn hình)
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Trong Suite, chọn All Tools → Hybrid Demo → nhập tên → Chạy demo.
Settings cho phép lưu tên hiển thị và trang khởi động. Mở lại để kiểm tra dữ liệu.

Có thể cài package bằng `python -m pip install -e .` trong virtualenv để dùng
lệnh `nhantools` và `nhantools-demo` từ bất kỳ thư mục nào.

## Cấu trúc

```text
apps/suite/        Shell, sidebar, các trang và entry point Suite
apps/standalone/   Entry point từng công cụ
core/             Registry, cấu hình local và logging; không phụ thuộc Qt
modules/demo/     Metadata, business logic và widget demo
shared_ui/        Theme và lifecycle Qt dùng chung
tests/            unittest cho core, UI và khởi động cả hai entry point
docs/             Kiến trúc và hướng dẫn mở rộng
```

## Dữ liệu local

- Cấu hình: `%LOCALAPPDATA%\NhanTools\config.json`.
- Log: `%LOCALAPPDATA%\NhanTools\logs\nhantools.log` (xoay 1 MB, giữ 3 bản cũ).
- Đặt `NHANTOOLS_DATA_DIR` để đổi thư mục dữ liệu, ví dụ khi kiểm thử.
- Chưa có file cấu hình thì dùng mặc định, file được tạo khi bấm Lưu cài đặt.
- File JSON hỏng được giữ nguyên, dùng mặc định và thông báo trên thanh trạng thái.
  Sao lưu/sửa file rồi mở lại trước khi lưu. Lưu cấu hình dùng thay thế file nguyên tử.
- Lỗi mở module/lưu cấu hình có hộp thoại; lỗi chưa xử lý được ghi log và báo lỗi.
- Không có telemetry, không yêu cầu kết nối mạng khi chạy.

Tests dùng thư mục tạm, không ghi cấu hình cá nhân. Nếu thiếu PySide6, tests core
vẫn chạy và tests UI được đánh dấu skip. Phải cài PySide6 để kiểm chứng đầy đủ.

Xem [docs/architecture.md](docs/architecture.md) để thêm module. Chưa đóng gói `.exe`.
