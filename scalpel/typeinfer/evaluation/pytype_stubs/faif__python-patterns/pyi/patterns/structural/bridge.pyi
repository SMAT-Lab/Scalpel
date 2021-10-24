# (generated with --quick)

from typing import Any

doctest: module

class CircleShape:
    _drawing_api: Any
    _radius: Any
    _x: Any
    _y: Any
    def __init__(self, x, y, radius, drawing_api) -> None: ...
    def draw(self) -> None: ...
    def scale(self, pct) -> None: ...

class DrawingAPI1:
    def draw_circle(self, x, y, radius) -> None: ...

class DrawingAPI2:
    def draw_circle(self, x, y, radius) -> None: ...

def main() -> None: ...
