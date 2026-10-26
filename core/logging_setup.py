"""Bounded logs shared by both entry points."""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def configure_logging(directory: Path) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    root = logging.getLogger("nhantools")
    root.setLevel(logging.INFO)
    root.propagate = False
    if root.handlers:
        return
    handler = RotatingFileHandler(directory / "nhantools.log", maxBytes=1_000_000, backupCount=3, encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
    root.addHandler(handler)
    # Infrastructure warnings use the same handler without altering root logging.
    logging.getLogger("core").addHandler(handler)
