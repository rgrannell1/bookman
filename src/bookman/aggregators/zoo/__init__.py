"""Named aggregators: the pre-built shelf of aggregation functions."""

from bookman.aggregators.zoo.series import series, running_sum
from bookman.aggregators.zoo.distinct import distinct, count_distinct

__all__ = [
    "series",
    "running_sum",
    "distinct",
    "count_distinct",
]
