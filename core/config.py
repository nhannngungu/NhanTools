"""Atomic local JSON settings; invalid files are preserved."""

import json
import logging
import os
from pathlib import Path
import tempfile

logger = logging.getLogger(__name__)
DEFAULTS = {"display_name": "Bạn", "start_page": "Dashboard"}


def data_directory() -> Path:
    override = os.environ.get("NHANTOOLS_DATA_DIR")
    if override:
        return Path(override).expanduser()
    return Path(os.environ.get("LOCALAPPDATA", str(Path.home() / ".local" / "share"))) / "NhanTools"


class ConfigStore:
    def __init__(self, path: Path | None = None) -> None:
        self.path = path if path is not None else data_directory() / "config.json"
        self.values = DEFAULTS.copy()
        self.load_error: str | None = None
        self.load()

    def load(self) -> None:
        self.values = DEFAULTS.copy()
        self.load_error = None
        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
            if not isinstance(raw, dict):
                raise ValueError("Settings must be a JSON object")
            self.values.update(raw)
            if not isinstance(self.values["display_name"], str):
                raise ValueError("display_name must be a string")
            if self.values["start_page"] not in ("Dashboard", "All Tools", "Settings"):
                raise ValueError("Unknown start_page")
        except FileNotFoundError:
            pass
        except (OSError, ValueError) as error:
            self.values = DEFAULTS.copy()
            self.load_error = str(error)
            logger.warning("Cannot load settings %s: %s", self.path, error)

    def save(self, *, display_name: str, start_page: str) -> None:
        if start_page not in ("Dashboard", "All Tools", "Settings"):
            raise ValueError("Unknown start_page")
        if self.load_error:
            raise ValueError(f"Cannot overwrite unreadable settings: {self.path}. Back up or repair this file first.")
        values = {**self.values, "display_name": display_name.strip() or "Bạn", "start_page": start_page}
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=self.path.parent, delete=False) as stream:
                temporary = Path(stream.name)
                json.dump(values, stream, ensure_ascii=False, indent=2)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary, self.path)
            self.values = values
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)
