# (generated with --quick)

from typing import Any, List, Tuple

Box2D: Any
ENGINE_POWER: float
FRICTION_LIMIT: float
HULL_POLY1: List[Tuple[int, int]]
HULL_POLY2: List[Tuple[int, int]]
HULL_POLY3: List[Tuple[int, int]]
HULL_POLY4: List[Tuple[int, int]]
MUD_COLOR: Tuple[float, float, float]
SIZE: float
WHEELPOS: List[Tuple[int, int]]
WHEEL_COLOR: Tuple[float, float, float]
WHEEL_MOMENT_OF_INERTIA: float
WHEEL_R: int
WHEEL_W: int
WHEEL_WHITE: Tuple[float, float, float]
circleShape: Any
contactListener: Any
edgeShape: Any
fixtureDef: Any
math: module
np: module
polygonShape: Any
revoluteJointDef: Any
shape: Any

class Car:
    drawlist: list
    fuel_spent: Any
    hull: Any
    particles: list
    wheels: list
    world: Any
    def __init__(self, world, init_angle, init_x, init_y) -> None: ...
    def _create_particle(self, point1, point2, grass) -> Any: ...
    def brake(self, b) -> None: ...
    def destroy(self) -> None: ...
    def draw(self, viewer, draw_particles = ...) -> None: ...
    def gas(self, gas) -> None: ...
    def steer(self, s) -> None: ...
    def step(self, dt) -> None: ...
