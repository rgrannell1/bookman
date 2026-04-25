from typing import Literal, NamedTuple, NewType

type Timestamp = float
"""Seconds since epoch."""

type Duration = float
"""Elapsed time in seconds, computed as until - at."""

type TimeUnit = Literal["s", "ms", "us", "ns"]
"""Time unit for duration calculations."""

type Label = str
"""A dimension key, e.g. 'id', 'tag', 'unit'. Dimensions are used to group and filter events."""

type Dims = dict[Label, list[str]]
"""A multimap of named dimensions attached to an event. Dimensions are used to group and filter events"""


class Delta(NamedTuple):
    """A counter increment: add this value to the running total. Summed directly by aggregators."""
    value: int


class Cumulative(NamedTuple):
    """A counter snapshot: the current total, not a change."""
    value: int

Gauge = NewType("Gauge", float)
"""Point measurements like memory usage"""

Message = NewType("Message", str)
"""A log, probably."""

Boolean = NewType("Boolean", bool)

Categorical = NewType("Categorical", str)
"""A discrete string value from an open set of labels."""

type Counter = Delta | Cumulative
type Primitive = Counter | Gauge | Message | Boolean | Categorical
type EventKind = Literal["span", "point"]
