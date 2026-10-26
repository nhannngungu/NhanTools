"""Shared business logic; no dependency on Qt or application shell."""


def greeting(name: str) -> str:
    return f"Xin chào, {name.strip() or 'bạn'}! Module Hybrid đang hoạt động."
