import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
HAS_QT = importlib.util.find_spec("PySide6") is not None


@unittest.skipUnless(HAS_QT, "PySide6 chưa được cài")
class UiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from PySide6.QtWidgets import QApplication
        from shared_ui.theme import apply_theme
        cls.app = QApplication.instance() or QApplication([])
        apply_theme(cls.app)

    def test_navigation_demo_and_settings(self):
        from apps.suite.window import SuiteWindow
        from core.config import ConfigStore
        from modules.demo.service import greeting

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config.json"
            window = SuiteWindow(config=ConfigStore(path))
            try:
                window.show()
                for name, button in window.nav_buttons.items():
                    button.click()
                    self.app.processEvents()
                    self.assertIs(window.stack.currentWidget(), window.pages[name])
                window.tool_buttons["demo"].click()
                demo = window.tool_pages["demo"]
                demo.name_input.setText("Nhân")
                demo.run_button.click()
                self.assertEqual(demo.result.text(), greeting("Nhân"))
                window.navigate("All Tools")
                window.open_tool("demo")
                self.assertIs(window.stack.currentWidget(), demo)
                window.display_name.setText("Nhân")
                window.start_page.setCurrentText("Settings")
                window.save_button.click()
                restored = SuiteWindow(config=ConfigStore(path))
                try:
                    self.assertIs(restored.stack.currentWidget(), restored.pages["Settings"])
                    self.assertEqual(restored.display_name.text(), "Nhân")
                finally:
                    restored.close()
            finally:
                window.close()

    def test_standalone_shared_widget(self):
        from apps.standalone.demo import create_window
        from modules.demo.widget import DemoWidget
        window = create_window()
        try:
            window.show()
            self.app.processEvents()
            self.assertIsInstance(window.centralWidget(), DemoWidget)
            window.centralWidget().run_button.click()
            self.assertIn("bạn", window.centralWidget().result.text())
        finally:
            window.close()

    def test_entry_points_event_loop(self):
        # Exercise actual main() startup, hook installation and Qt event loop.
        for entry in ("apps.suite.__main__", "apps.standalone.demo"):
            with self.subTest(entry=entry), tempfile.TemporaryDirectory() as directory:
                env = {**os.environ, "NHANTOOLS_DATA_DIR": directory, "QT_QPA_PLATFORM": "offscreen"}
                code = (
                    "from PySide6.QtCore import QTimer; "
                    "from PySide6.QtWidgets import QApplication; "
                    f"from {entry} import main; "
                    "original = QApplication.exec; "
                    "QApplication.exec = staticmethod(lambda: (QTimer.singleShot(150, QApplication.instance().quit), original())[1]); "
                    "raise SystemExit(main())"
                )
                result = subprocess.run([sys.executable, "-c", code], env=env, capture_output=True, text=True, timeout=20)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn("Application started", (Path(directory) / "logs" / "nhantools.log").read_text(encoding="utf-8"))
