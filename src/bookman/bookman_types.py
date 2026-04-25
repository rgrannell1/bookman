"""Package-wide type definitions for bookman."""

from typing import Literal, NamedTuple, NewType

# Time and measurement units
type Timestamp = float
"""Seconds since epoch."""

type Duration = float
"""Elapsed time in seconds, computed as until - at."""

type TimeUnit = Literal["s", "ms", "us", "ns"]
"""Time unit for duration calculations."""

# Event dimension types
type Label = str
"""A dimension key, e.g. 'id', 'tag', 'unit'. Dimensions are used to group and filter events."""

type Dims = dict[Label, list[str]]
"""A multimap of named dimensions attached to an event."""

# Counter primitives
class Delta(NamedTuple):
    """A counter increment: add this value to the running total. Summed directly by aggregators."""
    value: int


class Cumulative(NamedTuple):
    """A counter snapshot: the current total, not a change."""
    value: int

# Scalar primitives
Gauge = NewType("Gauge", float)
"""Point measurements like memory usage."""

Message = NewType("Message", str)
"""A log, probably."""

Boolean = NewType("Boolean", bool)

Categorical = NewType("Categorical", str)
"""A discrete string value from an open set of labels."""

# Compound primitive types
type Counter = Delta | Cumulative
type Primitive = Counter | Gauge | Message | Boolean | Categorical
type EventKind = Literal["span", "point"]

# Aggregator metadata
type Temporality = Literal["delta", "cumulative"]
"""Whether an aggregated result represents a change since last export (delta) or a running total (cumulative)."""

# Aggregation result types — stable dispatch targets for exporters
class Scalar(NamedTuple):
    """A single numeric measurement, e.g. a count or gauge reading."""
    value: float


class Series(NamedTuple):
    """A time-ordered sequence of (timestamp, value) pairs."""
    points: list[tuple[Timestamp, float]]
