"""Tool metadata stays importable without Qt."""

from dataclasses import dataclass
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from PySide6.QtWidgets import QWidget


@dataclass(frozen=True)
class Tool:
    id: str
    name: str
    description: str
    create_widget: "Callable[[], QWidget]"


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        if not tool.id.strip():
            raise ValueError("Tool ID must not be empty")
        if tool.id in self._tools:
            raise ValueError(f"Tool already registered: {tool.id}")
        self._tools[tool.id] = tool

    def get(self, tool_id: str) -> Tool:
        return self._tools[tool_id]

    def list_tools(self) -> tuple[Tool, ...]:
        return tuple(self._tools.values())
