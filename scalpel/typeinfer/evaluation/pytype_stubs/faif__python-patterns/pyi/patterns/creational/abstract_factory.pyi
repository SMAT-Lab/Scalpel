# (generated with --quick)

from typing import Type

doctest: module
random: module

class Cat(Pet):
    name: str
    def __str__(self) -> str: ...
    def speak(self) -> None: ...

class Dog(Pet):
    name: str
    def __str__(self) -> str: ...
    def speak(self) -> None: ...

class Pet:
    name: str
    def __init__(self, name: str) -> None: ...
    def __str__(self) -> str: ...
    def speak(self) -> None: ...

class PetShop:
    __doc__: str
    pet_factory: Type[Pet]
    def __init__(self, animal_factory: Type[Pet]) -> None: ...
    def buy_pet(self, name: str) -> Pet: ...

def main() -> None: ...
def random_animal(name: str) -> Pet: ...
