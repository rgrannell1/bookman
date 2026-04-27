"""Named aggregators: the pre-built shelf of aggregation functions."""

from bookman.aggregators.zoo.distinct import count_distinct, distinct
from bookman.aggregators.zoo.scalar import count, mean
from bookman.aggregators.zoo.series import running_sum, series

__all__ = [
    "count",
    "count_distinct",
    "distinct",
    "mean",
    "running_sum",
    "series",
]
