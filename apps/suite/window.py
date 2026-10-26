import logging

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QButtonGroup, QComboBox, QFormLayout, QHBoxLayout, QLabel,
    QLineEdit, QMainWindow, QMessageBox, QPushButton, QScrollArea,
    QStackedWidget, QVBoxLayout, QWidget,
)

from core.config import ConfigStore
from core.registry import ToolRegistry
from modules import create_registry


class SuiteWindow(QMainWindow):
    def __init__(self, config: ConfigStore | None = None, registry: ToolRegistry | None = None) -> None:
        super().__init__()
        self.config = config if config is not None else ConfigStore()
        self.registry = registry if registry is not None else create_registry()
        self.setWindowTitle("NhanTools")
        self.resize(1080, 720)
        self.setMinimumSize(800, 560)
        root = QWidget()
        layout = QHBoxLayout(root)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setCentralWidget(root)

        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(220)
        navigation = QVBoxLayout(sidebar)
        navigation.setContentsMargins(20, 28, 20, 24)
        navigation.setSpacing(12)
        brand = QLabel("NhanTools")
        brand.setObjectName("brand")
        navigation.addWidget(brand)
        subtitle = QLabel("Không gian tiện ích")
        subtitle.setObjectName("muted")
        navigation.addWidget(subtitle)
        navigation.addSpacing(30)
        self.nav_group = QButtonGroup(self)
        self.nav_buttons: dict[str, QPushButton] = {}
        for name in ("Dashboard", "All Tools", "Settings"):
            button = QPushButton(name)
            button.setCheckable(True)
            button.clicked.connect(lambda checked=False, page=name: self.navigate(page))
            self.nav_group.addButton(button)
            self.nav_buttons[name] = button
            navigation.addWidget(button)
        navigation.addStretch()
        footer = QLabel("Phiên bản 0.1.0\nDữ liệu lưu trên máy")
        footer.setObjectName("muted")
        navigation.addWidget(footer)
        layout.addWidget(sidebar)

        self.stack = QStackedWidget()
        layout.addWidget(self.stack, 1)
        self.pages: dict[str, QWidget] = {}
        self.tool_pages: dict[str, QWidget] = {}
        self._build_dashboard()
        self._build_tools()
        self._build_settings()
        self.navigate(self.config.values["start_page"])
        if self.config.load_error:
            self.statusBar().showMessage("Không đọc được cấu hình. Đang dùng mặc định; xem log và sửa file cấu hình.")

    def _page(self, name: str, title: str, description: str) -> QVBoxLayout:
        page = QWidget()
        outer = QVBoxLayout(page)
        outer.setContentsMargins(32, 30, 32, 30)
        outer.setSpacing(20)
        heading = QLabel(title)
        heading.setObjectName("pageTitle")
        outer.addWidget(heading)
        detail = QLabel(description)
        detail.setObjectName("muted")
        detail.setWordWrap(True)
        outer.addWidget(detail)
        self.pages[name] = page
        self.stack.addWidget(page)
        return outer

    def _build_dashboard(self) -> None:
        layout = self._page("Dashboard", "Mọi tiện ích, một nơi.", "Mở công cụ bạn cần và bắt đầu ngay trong NhanTools.")
        self.welcome = QLabel()
        self.welcome.setTextFormat(Qt.TextFormat.PlainText)
        self.welcome.setWordWrap(True)
        self._update_welcome()
        layout.addWidget(self.welcome)
        layout.addWidget(QLabel(f"{len(self.registry.list_tools())} công cụ sẵn sàng"))
        browse = QPushButton("Khám phá công cụ")
        browse.setObjectName("primary")
        browse.clicked.connect(lambda: self.navigate("All Tools"))
        layout.addWidget(browse)
        layout.addStretch()

    def _build_tools(self) -> None:
        layout = self._page("All Tools", "All Tools", "Chọn một công cụ để mở trong không gian làm việc.")
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        contents = QWidget()
        tools_layout = QVBoxLayout(contents)
        tools_layout.setContentsMargins(0, 0, 0, 0)
        self.tool_buttons: dict[str, QPushButton] = {}
        for tool in self.registry.list_tools():
            button = QPushButton(f"{tool.name}\n{tool.description}")
            button.clicked.connect(lambda checked=False, tool_id=tool.id: self.open_tool(tool_id))
            self.tool_buttons[tool.id] = button
            tools_layout.addWidget(button)
        if not self.registry.list_tools():
            tools_layout.addWidget(QLabel("Chưa có công cụ được đăng ký."))
        tools_layout.addStretch()
        scroll.setWidget(contents)
        layout.addWidget(scroll)

    def _build_settings(self) -> None:
        layout = self._page("Settings", "Settings", "Tùy chỉnh thông tin và trang mở khi khởi động.")
        form = QFormLayout()
        form.setSpacing(16)
        self.display_name = QLineEdit(self.config.values["display_name"])
        self.start_page = QComboBox()
        self.start_page.addItems(list(self.nav_buttons))
        self.start_page.setCurrentText(self.config.values["start_page"])
        form.addRow("Tên hiển thị", self.display_name)
        form.addRow("Trang khởi động", self.start_page)
        layout.addLayout(form)
        self.save_button = QPushButton("Lưu cài đặt")
        self.save_button.setObjectName("primary")
        self.save_button.clicked.connect(self.save_settings)
        layout.addWidget(self.save_button)
        location = QLabel(f"File cấu hình:\n{self.config.path}")
        location.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        location.setWordWrap(True)
        location.setObjectName("muted")
        layout.addWidget(location)
        layout.addStretch()

    def _update_welcome(self) -> None:
        self.welcome.setText(f"Xin chào, {self.config.values['display_name']}.")

    def navigate(self, page: str) -> None:
        self.stack.setCurrentWidget(self.pages[page])
        self.nav_buttons[page].setChecked(True)

    def open_tool(self, tool_id: str) -> None:
        try:
            if tool_id not in self.tool_pages:
                widget = self.registry.get(tool_id).create_widget()
                self.stack.addWidget(widget)
                self.tool_pages[tool_id] = widget
            self.stack.setCurrentWidget(self.tool_pages[tool_id])
            self.nav_buttons["All Tools"].setChecked(True)
        except Exception as error:
            logging.getLogger("nhantools").exception("Cannot open tool %s", tool_id)
            QMessageBox.critical(self, "Không mở được công cụ", str(error))

    def save_settings(self) -> None:
        try:
            self.config.save(display_name=self.display_name.text(), start_page=self.start_page.currentText())
        except (OSError, ValueError) as error:
            logging.getLogger("nhantools").exception("Cannot save settings")
            QMessageBox.warning(self, "Không lưu được cấu hình", str(error))
            return
        self._update_welcome()
        self.statusBar().showMessage("Đã lưu cài đặt.", 5000)
