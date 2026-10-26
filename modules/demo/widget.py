from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget

from modules.demo.service import greeting


class DemoWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(16)
        title = QLabel("Hybrid Demo")
        title.setObjectName("pageTitle")
        layout.addWidget(title)
        description = QLabel("Nhập tên để kiểm tra module dùng chung giữa Suite và Standalone.")
        description.setWordWrap(True)
        layout.addWidget(description)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Tên của bạn")
        self.name_input.setAccessibleName("Tên của bạn")
        layout.addWidget(self.name_input)
        self.run_button = QPushButton("Chạy demo")
        self.run_button.setObjectName("primary")
        layout.addWidget(self.run_button)
        self.result = QLabel("")
        self.result.setWordWrap(True)
        self.result.setTextFormat(Qt.TextFormat.PlainText)
        layout.addWidget(self.result)
        layout.addStretch()
        self.run_button.clicked.connect(self.run_demo)
        self.name_input.returnPressed.connect(self.run_demo)

    def run_demo(self) -> None:
        self.result.setText(greeting(self.name_input.text()))
