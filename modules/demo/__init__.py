"""Lazy UI factory allows headless registry use."""

from core.registry import Tool


def create_widget():
    from modules.demo.widget import DemoWidget
    return DemoWidget()


TOOL = Tool("demo", "Hybrid Demo", "Thử cùng một module trong Suite hoặc cửa sổ riêng.", create_widget)
