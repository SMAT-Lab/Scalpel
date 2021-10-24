# (generated with --quick)

import __future__
from typing import Any, List, Tuple

division: __future__._Feature
np: module
print_function: __future__._Feature
string: module

class GeneticAlgorithm:
    __doc__: str
    letters: List[str]
    mutation_rate: Any
    population: List[str]
    population_size: Any
    target: Any
    def __init__(self, target_string, population_size, mutation_rate) -> None: ...
    def _calculate_fitness(self) -> List[float]: ...
    def _crossover(self, parent1, parent2) -> Tuple[Any, Any]: ...
    def _initialize(self) -> None: ...
    def _mutate(self, individual) -> str: ...
    def run(self, iterations) -> None: ...
