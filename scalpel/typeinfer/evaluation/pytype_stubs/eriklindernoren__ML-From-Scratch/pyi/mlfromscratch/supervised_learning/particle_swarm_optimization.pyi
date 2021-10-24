# (generated with --quick)

import __future__
from typing import Any

copy: module
division: __future__._Feature
np: module
print_function: __future__._Feature

class ParticleSwarmOptimizedNN:
    X: Any
    __doc__: str
    best_individual: Any
    cognitive_w: Any
    inertia_w: Any
    max_v: Any
    min_v: Any
    population: list
    population_size: Any
    social_w: Any
    y: Any
    def __init__(self, population_size, model_builder, inertia_weight = ..., cognitive_weight = ..., social_weight = ..., max_velocity = ...) -> None: ...
    def _build_model(self, id) -> Any: ...
    def _calculate_fitness(self, individual) -> None: ...
    def _initialize_population(self) -> None: ...
    def _update_weights(self, individual) -> None: ...
    def evolve(self, X, y, n_generations) -> Any: ...
    def model_builder(self) -> Any: ...
