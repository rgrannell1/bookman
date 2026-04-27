"""Runners that execute an Aggregator over a stream of Events.

The streaming runners are primary — they yield an updated result after each event.
The batch runners (fold, group_by) are convenience wrappers that return the final value.
"""

from collections.abc import Callable, Generator, Iterable

from bookman.aggregators.aggregator import Aggregator
from bookman.events import Event


def stream[M, R](agg: Aggregator[M, R], events: Iterable[Event]) -> Generator[R]:
    """Yield an updated result after each event, maintaining a running accumulator.

    This is the primary runner. fold is derived from it.
    """

    acc = agg.empty()
    for ev in events:
        acc = agg.combine(acc, agg.insert(ev))
        yield agg.extract(acc)


def fold[M, R](agg: Aggregator[M, R], events: Iterable[Event]) -> R:
    """Return the final aggregated result after all events have been processed.

    Equivalent to last(stream(agg, events)). Returns the identity result for an empty stream.
    """

    acc = agg.empty()
    for ev in events:
        acc = agg.combine(acc, agg.insert(ev))
    return agg.extract(acc)


def stream_group_by[M, R, K](
    key_fn: Callable[[Event], K],
    agg: Aggregator[M, R],
    events: Iterable[Event],
) -> Generator[dict[K, R]]:
    """Yield an updated per-key result dict after each event, maintaining a running accumulator per key.

    This is the primary grouped runner. group_by is derived from it.
    """

    groups: dict[K, M] = {}
    for ev in events:
        key = key_fn(ev)
        if key not in groups:
            groups[key] = agg.empty()
        groups[key] = agg.combine(groups[key], agg.insert(ev))
        yield {k: agg.extract(acc) for k, acc in groups.items()}


def group_by[M, R, K](
    key_fn: Callable[[Event], K],
    agg: Aggregator[M, R],
    events: Iterable[Event],
) -> dict[K, R]:
    """Return the final per-key result dict after all events have been processed.

    Equivalent to last(stream_group_by(key_fn, agg, events)). Returns an empty dict for an empty stream.
    """

    groups: dict[K, M] = {}
    for ev in events:
        key = key_fn(ev)
        if key not in groups:
            groups[key] = agg.empty()
        groups[key] = agg.combine(groups[key], agg.insert(ev))
    return {k: agg.extract(acc) for k, acc in groups.items()}
