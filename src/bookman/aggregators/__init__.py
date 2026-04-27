"""Aggregators and combinators for reducing collections of events."""

from bookman.bookman_types import Temporality
from bookman.aggregators.aggregator import Aggregator
from bookman.aggregators.runners import fold, group_by, stream, stream_group_by
from bookman.aggregators.combinators import map_insert, map_extract, filter_events, zip_agg, zip_all
from bookman.aggregators.results import as_scalar, as_series
from bookman.aggregators.zoo import series, running_sum, distinct, count_distinct, count, mean

__all__ = [
    "Temporality",
    "Aggregator",
    "fold",
    "group_by",
    "stream",
    "stream_group_by",
    "map_insert",
    "map_extract",
    "filter_events",
    "zip_agg",
    "zip_all",
    "as_scalar",
    "as_series",
    "series",
    "running_sum",
    "distinct",
    "count_distinct",
    "count",
    "mean",
]
