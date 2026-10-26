# Kiến trúc Hybrid

```text
Suite shell ───────┐
                  ├── modules/<tool>/widget.py ── service.py
Standalone shell ─┘

modules.create_registry() ── core.registry.ToolRegistry
Hai shell ── shared_ui.application/theme ── core.config/logging_setup
```

`core` không import Qt. Metadata module dùng lazy factory nên liệt kê registry
không khởi tạo giao diện. `service.py` độc lập với Qt, có thể kiểm thử trực tiếp.
Suite chỉ điều hướng và chứa widget; Standalone tạo QMainWindow chứa cùng widget.
Mỗi phiên Suite tái sử dụng widget đã mở để giữ trạng thái khi chuyển trang.

## Thêm module

1. Tạo `modules/<tool>/service.py` chứa business logic không phụ thuộc shell.
2. Tạo `widget.py` cung cấp QWidget gọi service.
3. Khai báo `Tool(id, name, description, create_widget)` trong `__init__.py`;
   import Qt/widget bên trong factory để giữ metadata độc lập UI.
4. Đăng ký metadata tại `modules.create_registry()`. ID phải duy nhất.
5. Thêm `apps/standalone/<tool>.py` dùng factory của module và
   `shared_ui.application.run_application`, tham khảo demo.
6. Thêm test service và kiểm tra widget trong cả hai shell.

Không sao chép business logic vào entry point. Registry hiện đăng ký tường minh;
chưa tự quét plugin bên ngoài. Chưa triển khai tác vụ nền, công cụ thực tế hoặc
đóng gói PyInstaller.

## Kiểm chứng

`python -m unittest discover -s tests -v` kiểm tra round-trip cấu hình, JSON hỏng,
registry trùng ID, logic demo, logging, điều hướng, lưu Settings, widget dùng chung
và event loop của cả hai entry point bằng Qt offscreen.

Kiểm tra thủ công trên Windows: chạy Suite, chuyển ba trang, mở Hybrid Demo,
chạy demo, lưu Settings, mở lại Suite; sau đó chạy Standalone và so sánh kết quả.
