"""Aggregators that reduce an event stream to a single scalar value."""

from collections.abc import Callable
from functools import partial

from bookman.aggregators.aggregator import Aggregator
from bookman.events import Event


def _count_insert(ev: Event) -> int:
    return 1


def _count_combine(acc1: int, acc2: int) -> int:
    return acc1 + acc2


def _count_empty() -> int:
    return 0


def _count_extract(acc: int) -> int:
    return acc


def count() -> Aggregator:
    """Count the number of events in the stream."""

    return Aggregator(
        insert=_count_insert,
        combine=_count_combine,
        empty=_count_empty,
        extract=_count_extract,
        temporality="delta",
    )


def _mean_insert(value_fn: Callable, ev: Event) -> tuple[float, int]:
    return (value_fn(ev), 1)


def _mean_combine(acc1: tuple[float, int], acc2: tuple[float, int]) -> tuple[float, int]:
    return (acc1[0] + acc2[0], acc1[1] + acc2[1])


def _mean_empty() -> tuple[float, int]:
    return (0.0, 0)


def _mean_extract(acc: tuple[float, int]) -> float:
    total, n = acc
    return total / n if n > 0 else 0.0


def mean(value_fn: Callable[[Event], float]) -> Aggregator:
    """Compute the arithmetic mean of value_fn(event) across all events."""

    return Aggregator(
        insert=partial(_mean_insert, value_fn),
        combine=_mean_combine,
        empty=_mean_empty,
        extract=_mean_extract,
        temporality="delta",
    )
