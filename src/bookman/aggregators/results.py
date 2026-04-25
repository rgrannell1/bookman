"""Combinators that lift aggregator outputs into Result types for export."""

from bookman.aggregators.aggregator import Aggregator
from bookman.aggregators.combinators import map_extract
from bookman.bookman_types import Scalar, Series, Timestamp


def _to_scalar(value) -> Scalar:
    return Scalar(float(value))


def _to_series(pairs: list[tuple[Timestamp, float]]) -> Series:
    return Series([(ts, float(val)) for ts, val in pairs])


def as_scalar[M, R](agg: Aggregator[M, R]) -> Aggregator[M, Scalar]:
    """Lift an aggregator's numeric result into a Scalar for export."""

    return map_extract(_to_scalar, agg)


def as_series[M, R](agg: Aggregator[M, R]) -> Aggregator[M, Series]:
    """Lift an aggregator's (timestamp, value) list result into a Series for export."""

    return map_extract(_to_series, agg)
