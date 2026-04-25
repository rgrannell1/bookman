"""Runners that execute an Aggregator over a collection of Events."""

from collections import defaultdict
from collections.abc import Callable, Iterable
from functools import reduce

from bookman.events import Event
from bookman.aggregators.aggregator import Aggregator


def fold[M, R](agg: Aggregator[M, R], events: Iterable[Event]) -> R:
    """We take an aggregator and a sequence of events. And:
    - Lift each event into the accumulator type using the aggregator's insert function.
    - Combine the accumulators using the aggregator's combine function.

    It's a monoidal reduction, we pull back out the result using extract. So,
    like stock reduce with pre and post processing.
    """

    acc = reduce(agg.combine, (agg.insert(ev) for ev in events), agg.empty())
    return agg.extract(acc)


def group_by[M, R, K](
    key_fn: Callable[[Event], K],
    agg: Aggregator[M, R],
    events: Iterable[Event],
) -> dict[K, R]:
    """Given a key function and an aggregator, we group events by key and fold each group independently.
    """

    groups: dict[K, list[Event]] = defaultdict(list)
    for ev in events:
        groups[key_fn(ev)].append(ev)
