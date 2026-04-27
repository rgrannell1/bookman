"""Aggregators that reduce an event stream to a single scalar value."""

from collections.abc import Callable

from bookman.aggregators.aggregator import Aggregator
from bookman.events import Event


def count() -> Aggregator:
    """Count the number of events in the stream."""

    return Aggregator(
        insert=lambda ev: 1,
        combine=lambda acc1, acc2: acc1 + acc2,
        empty=lambda: 0,
        extract=lambda acc: acc,
        temporality="delta",
    )


def mean(value_fn: Callable[[Event], float]) -> Aggregator:
    """Compute the arithmetic mean of value_fn(event) across all events."""

    return Aggregator(
        insert=lambda ev: (value_fn(ev), 1),
        combine=lambda acc1, acc2: (acc1[0] + acc2[0], acc1[1] + acc2[1]),
        empty=lambda: (0.0, 0),
        extract=lambda acc: acc[0] / acc[1] if acc[1] > 0 else 0.0,
        temporality="delta",
    )
