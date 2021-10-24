# (generated with --quick)

import PIL.Image
from typing import Any, Union

Image: module

class LoadedImage:
    height: int
    imageData: Any
    loadedImage: Union[PIL.Image.Image, bool]
    path: Any
    width: int
    def __init__(self, path) -> None: ...
    def getCopyOfLoadedPILImage(self) -> Any: ...
    def loadImage(self) -> None: ...
    def loadImageData(self) -> None: ...
