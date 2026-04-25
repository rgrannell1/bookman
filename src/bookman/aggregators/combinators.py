"""Combinators for transforming Aggregator instances into new Aggregator instances."""

from collections.abc import Callable
from functools import partial

from bookman.events import Event
from bookman.aggregators.aggregator import Aggregator
from bookman.bookman_types import Temporality


def _map_insert_apply(original_insert: Callable, fn: Callable, ev: Event):
    return original_insert(fn(ev))


def map_insert[M, R](fn: Callable[[Event], Event], agg: Aggregator[M, R]) -> Aggregator[M, R]:
    """Pre-process each Event before it reaches insert."""

    return Aggregator(
        insert=partial(_map_insert_apply, agg.insert, fn),
        combine=agg.combine,
        empty=agg.empty,
        extract=agg.extract,
        temporality=agg.temporality,
    )


def _map_extract_apply(original_extract: Callable, fn: Callable, acc):
    return fn(original_extract(acc))


def map_extract[M, R, S](fn: Callable[[R], S], agg: Aggregator[M, R]) -> Aggregator[M, S]:
    """Post-process the result of extract."""

    return Aggregator(
        insert=agg.insert,
        combine=agg.combine,
        empty=agg.empty,
        extract=partial(_map_extract_apply, agg.extract, fn),
        temporality=agg.temporality,
    )


def _filter_insert(pred: Callable, agg: Aggregator, ev: Event):
    return agg.insert(ev) if pred(ev) else agg.empty()


def filter_events[M, R](pred: Callable[[Event], bool], agg: Aggregator[M, R]) -> Aggregator[M, R]:
    """Skip non-matching events by substituting the identity accumulator."""

    return Aggregator(
        insert=partial(_filter_insert, pred, agg),
        combine=agg.combine,
        empty=agg.empty,
        extract=agg.extract,
        temporality=agg.temporality,
    )


def _zip_insert(agg1: Aggregator, agg2: Aggregator, ev: Event) -> tuple:
    return (agg1.insert(ev), agg2.insert(ev))


def _zip_combine(agg1: Aggregator, agg2: Aggregator, pair_a: tuple, pair_b: tuple) -> tuple:
    return (agg1.combine(pair_a[0], pair_b[0]), agg2.combine(pair_a[1], pair_b[1]))


def _zip_empty(agg1: Aggregator, agg2: Aggregator) -> tuple:
    return (agg1.empty(), agg2.empty())


def _zip_extract(agg1: Aggregator, agg2: Aggregator, pair: tuple) -> tuple:
    return (agg1.extract(pair[0]), agg2.extract(pair[1]))


def _zip_temporality(agg1: Aggregator, agg2: Aggregator) -> Temporality:
    if agg1.temporality != agg2.temporality:
        raise ValueError(
            f"Cannot zip aggregators with different temporalities: {agg1.temporality!r} and {agg2.temporality!r}"
        )
    return agg1.temporality


def zip_agg[M, N, R, S](
    agg1: Aggregator[M, R], agg2: Aggregator[N, S]
) -> Aggregator[tuple[M, N], tuple[R, S]]:
    """Run two aggregators in parallel over the same events, producing a pair of results."""

    return Aggregator(
        insert=partial(_zip_insert, agg1, agg2),
        combine=partial(_zip_combine, agg1, agg2),
        empty=partial(_zip_empty, agg1, agg2),
        extract=partial(_zip_extract, agg1, agg2),
        temporality=_zip_temporality(agg1, agg2),
    )
