from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication

STYLE = """
QWidget { background: #182330; color: #e8eef4; font-size: 14px; }
QWidget#sidebar { background: #101923; border-right: 1px solid #314253; }
QLabel#brand { font-size: 25px; font-weight: 700; color: #91c9ef; }
QLabel#pageTitle { font-size: 30px; font-weight: 600; }
QLabel#muted { color: #a6b8c9; }
QLabel { background: transparent; }
QPushButton { background: #243548; border: 1px solid #3b536b;
    padding: 11px 18px; border-radius: 6px; text-align: left; }
QPushButton:hover { background: #314b63; }
QPushButton:checked, QPushButton#primary { background: #315e83; border-color: #78b8e0; }
QPushButton:focus, QLineEdit:focus, QComboBox:focus { border: 2px solid #a4d5f5; }
QLineEdit, QComboBox { background: #101923; border: 1px solid #486078;
    border-radius: 4px; padding: 10px; }
QComboBox QAbstractItemView { background: #182330; selection-background-color: #315e83; }
QStatusBar { color: #a6b8c9; }
"""


def apply_theme(app: QApplication) -> None:
    app.setStyle("Fusion")
    app.setFont(QFont("Segoe UI", 10))
    app.setStyleSheet(STYLE)
