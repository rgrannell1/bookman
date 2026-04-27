"""The Aggregator type: a composable quadruple for reducing collections of Events."""

from collections.abc import Callable
from dataclasses import dataclass

from bookman.bookman_types import Temporality
from bookman.events import Event


@dataclass(frozen=True)
class Aggregator[M, R]:
    """A composable aggregation defined by insert, combine, empty, and extract."""

    # Maps an Event into the accumulator type
    insert: Callable[[Event], M]
    # Merges two accumulators
    combine: Callable[[M, M], M]
    # Returns a fresh identity accumulator
    empty: Callable[[], M]
    # Finalises the accumulator into the result type
    extract: Callable[[M], R]
    # Whether the result represents a change (delta) or a running total (cumulative)
    temporality: Temporality
