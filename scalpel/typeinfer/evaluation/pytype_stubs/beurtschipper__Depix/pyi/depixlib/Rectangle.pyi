# (generated with --quick)

from typing import Any

class ColorRectange(Rectangle):
    color: Any
    endCoordinates: Any
    height: Any
    startCoordinates: Any
    width: Any
    x: Any
    y: Any
    def __init__(self, color, startCoordinates, endCoordinates) -> None: ...

class Rectangle:
    endCoordinates: Any
    height: Any
    startCoordinates: Any
    width: Any
    x: Any
    y: Any
    def __init__(self, startCoordinates, endCoordinates) -> None: ...

class RectangleMatch:
    data: Any
    x: Any
    y: Any
    def __init__(self, x, y, data) -> None: ...
