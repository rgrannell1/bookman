"""Aggregators for counting unique values across an event stream."""

from collections.abc import Callable
from functools import partial

from bookman.aggregators.aggregator import Aggregator
from bookman.aggregators.combinators import map_extract
from bookman.events import Event


def _distinct_insert(key_fn: Callable, ev: Event) -> frozenset:
    return frozenset({key_fn(ev)})


def _distinct_combine(acc1: frozenset, acc2: frozenset) -> frozenset:
    return acc1 | acc2


def _distinct_empty() -> frozenset:
    return frozenset()


def _distinct_extract(acc: frozenset) -> frozenset:
    return acc


def distinct(key_fn: Callable[[Event], str]) -> Aggregator:
    """Collect the unique values of key_fn across all events.
    """

    return Aggregator(
        insert=partial(_distinct_insert, key_fn),
        combine=_distinct_combine,
        empty=_distinct_empty,
        extract=_distinct_extract,
        temporality="delta",
    )


def count_distinct(key_fn: Callable[[Event], str]) -> Aggregator:
    """Count the unique values of key_fn across all events."""

    return map_extract(len, distinct(key_fn))
