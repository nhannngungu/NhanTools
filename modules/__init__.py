"""Tools and explicit built-in registration."""

from core.registry import ToolRegistry
from modules.demo import TOOL


def create_registry() -> ToolRegistry:
    registry = ToolRegistry()
    registry.register(TOOL)
    return registry
