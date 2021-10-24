# (generated with --quick)

from typing import Any, Optional

json: module
last_info: Optional[VideoExtractor]

class VideoExtractor:
    name: Any
    streams: dict
    title: Any
    url: Any

def download_urls(urls = ..., title = ..., ext = ..., total_size = ..., refer = ...) -> None: ...
def output(video_extractor, pretty_print = ...) -> None: ...
def print_info(site_info = ..., title = ..., type = ..., size = ...) -> None: ...
