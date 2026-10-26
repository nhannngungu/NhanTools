"""Application startup and a common uncaught-error boundary."""

import logging
import sys
from typing import Callable

from PySide6.QtWidgets import QApplication, QMessageBox, QWidget

from core.config import data_directory
from core.logging_setup import configure_logging
from shared_ui.theme import apply_theme


def run_application(factory: Callable[[], QWidget], argv: list[str] | None = None) -> int:
    app = QApplication(sys.argv if argv is None else argv)
    app.setApplicationName("NhanTools")
    app.setOrganizationName("NhanTools")
    apply_theme(app)
    try:
        configure_logging(data_directory() / "logs")
    except OSError as error:
        logging.basicConfig(level=logging.INFO)
        logging.getLogger("nhantools").warning("File logging unavailable: %s", error)
    logger = logging.getLogger("nhantools")
    previous_hook = sys.excepthook

    def report_error(kind, value, traceback):
        if issubclass(kind, KeyboardInterrupt):
            app.quit()
            return
        logger.error("Unhandled application error", exc_info=(kind, value, traceback))
        QMessageBox.critical(None, "NhanTools", f"Có lỗi xảy ra: {value}\nXem log để biết chi tiết.")

    sys.excepthook = report_error
    try:
        window = factory()
        window.show()
        logger.info("Application started: %s", window.windowTitle())
        return app.exec()
    except Exception:
        report_error(*sys.exc_info())
        return 1
    finally:
        sys.excepthook = previous_hook
