"""Named aggregators: the pre-built shelf of aggregation functions users compose from."""

from operator import itemgetter

from bookman.aggregators.aggregator import Aggregator
from bookman.bookman_types import Counter, Delta, Cumulative, Timestamp


# series


def _series_insert(ev) -> list:
    return [(ev.at, ev.value)]


def _series_combine(acc1: list, acc2: list) -> list:
    return acc1 + acc2


def _series_empty() -> list:
    return []


def _series_extract(acc: list) -> list:
    return sorted(acc, key=itemgetter(0))


def series() -> Aggregator:
    """Collect (timestamp, value) pairs into a time-ordered Series."""

    return Aggregator(
        insert=_series_insert,
        combine=_series_combine,
        empty=_series_empty,
        extract=_series_extract,
        temporality="delta",
    )


# running_sum


def _apply_counter(total: int, counter: Counter) -> int:
    """Add a Delta increment or replace with a Cumulative snapshot."""

    match counter:
        case Delta(value=delta):
            return total + delta
        case Cumulative(value=cumulative):
            return cumulative


def running_sum(pairs: list[tuple[Timestamp, Counter]]) -> list[tuple[Timestamp, int]]:
    """Compute cumulative integer total from a sorted series of Counter values.

    Each Delta increments the running total; each Cumulative resets it.
    Returns a list of (timestamp, cumulative_total) pairs in input order.
    """

    total = 0
    result = []
    for at, counter in pairs:
        total = _apply_counter(total, counter)
        result.append((at, total))
    return result
