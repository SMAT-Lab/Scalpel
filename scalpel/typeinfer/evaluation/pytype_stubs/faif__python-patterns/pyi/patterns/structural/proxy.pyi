# (generated with --quick)

from typing import Union

doctest: module

class Proxy(Subject):
    _real_subject: RealSubject
    def __init__(self) -> None: ...
    def do_the_job(self, user: str) -> None: ...

class RealSubject(Subject):
    __doc__: str
    def do_the_job(self, user: str) -> None: ...

class Subject:
    __doc__: str
    def do_the_job(self, user: str) -> None: ...

def client(job_doer: Union[Proxy, RealSubject], user: str) -> None: ...
def main() -> None: ...
