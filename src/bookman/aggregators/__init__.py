"""Aggregators and combinators for reducing collections of events."""

from bookman.aggregators.aggregator import Aggregator
from bookman.aggregators.combinators import filter_events, map_extract, map_insert, zip_agg, zip_all
from bookman.aggregators.results import as_scalar, as_series
from bookman.aggregators.runners import fold, group_by, stream, stream_group_by
from bookman.aggregators.zoo import count, count_distinct, distinct, mean, running_sum, series
from bookman.bookman_types import Temporality

__all__ = [
    "Aggregator",
    "Temporality",
    "as_scalar",
    "as_series",
    "count",
    "count_distinct",
    "distinct",
    "filter_events",
    "fold",
    "group_by",
    "map_extract",
    "map_insert",
    "mean",
    "running_sum",
    "series",
    "stream",
    "stream_group_by",
    "zip_agg",
    "zip_all",
]
