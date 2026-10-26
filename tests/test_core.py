import json
import logging
from pathlib import Path
import tempfile
import unittest

from core.config import ConfigStore, DEFAULTS
from core.logging_setup import configure_logging
from core.registry import Tool, ToolRegistry
from modules import create_registry
from modules.demo.service import greeting


class ConfigTests(unittest.TestCase):
    def test_save_reload_unicode(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "nested" / "config.json"
            store = ConfigStore(path)
            self.assertEqual(store.values, DEFAULTS)
            store.save(display_name="  Nhân  ", start_page="All Tools")
            self.assertEqual(ConfigStore(path).values, {"display_name": "Nhân", "start_page": "All Tools"})
            self.assertEqual(list(path.parent.iterdir()), [path])

    def test_invalid_config_preserved(self):
        for content in ("broken", "[]", '{"display_name": 12}', '{"start_page": []}'):
            with self.subTest(content=content), tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "config.json"
                path.write_text(content, encoding="utf-8")
                store = ConfigStore(path)
                self.assertEqual(store.values, DEFAULTS)
                self.assertIsNotNone(store.load_error)
                with self.assertRaises(ValueError):
                    store.save(display_name="Test", start_page="Dashboard")
                self.assertEqual(path.read_text(encoding="utf-8"), content)

    def test_unknown_settings_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config.json"
            path.write_text(json.dumps({"future_setting": True}), encoding="utf-8")
            store = ConfigStore(path)
            store.save(display_name="", start_page="Settings")
            self.assertTrue(ConfigStore(path).values["future_setting"])
            self.assertEqual(store.values["display_name"], "Bạn")


class RegistryTests(unittest.TestCase):
    def test_builtins_and_duplicate(self):
        registry = create_registry()
        self.assertEqual([tool.id for tool in registry.list_tools()], ["demo"])
        with self.assertRaises(ValueError):
            registry.register(registry.get("demo"))
        with self.assertRaises(KeyError):
            registry.get("missing")

    def test_empty_id_rejected(self):
        with self.assertRaises(ValueError):
            ToolRegistry().register(Tool(" ", "Empty", "", lambda: None))

    def test_demo_logic(self):
        self.assertIn("Nhân", greeting(" Nhân "))
        self.assertIn("bạn", greeting(" "))


class LoggingTests(unittest.TestCase):
    def test_log_written(self):
        with tempfile.TemporaryDirectory() as directory:
            logger = logging.getLogger("nhantools")
            old_handlers = logger.handlers[:]
            old_level, old_propagate = logger.level, logger.propagate
            logger.handlers.clear()
            try:
                configure_logging(Path(directory))
                configure_logging(Path(directory))
                self.assertEqual(len(logger.handlers), 1)
                logger.info("test log entry")
                logger.handlers[0].flush()
                self.assertIn("test log entry", (Path(directory) / "nhantools.log").read_text(encoding="utf-8"))
            finally:
                for handler in logger.handlers[:]:
                    logging.getLogger("core").removeHandler(handler)
                    logger.removeHandler(handler)
                    handler.close()
                logger.handlers[:] = old_handlers
                logger.setLevel(old_level)
                logger.propagate = old_propagate
