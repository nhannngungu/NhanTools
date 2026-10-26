def create_window():
    from PySide6.QtWidgets import QMainWindow
    from modules.demo import TOOL

    window = QMainWindow()
    window.setWindowTitle("NhanTools • Hybrid Demo")
    window.resize(720, 460)
    window.setMinimumSize(560, 360)
    window.setCentralWidget(TOOL.create_widget())
    return window


def main() -> int:
    from shared_ui.application import run_application
    return run_application(create_window)


if __name__ == "__main__":
    raise SystemExit(main())
