from typing import NamedTuple, NewType

type Timestamp = float
"""Seconds since epoch."""

type Duration = float
"""Elapsed time in seconds, computed as until - at."""

type Label = str
"""A dimension key, e.g. 'id', 'tag', 'unit'."""

type Dims = dict[Label, list[str]]
"""A multimap of named dimensions attached to an event.

Keys are labels; values are lists of strings so a single event can carry
multiple values for the same dimension — e.g. dims['tag'] = ['error', 'slow']."""


class Delta(NamedTuple):
    """A counter increment: add this value to the running total.

    Use when an event represents a change — e.g. "3 requests completed".
    Aggregators sum deltas directly to compute totals or rates."""

    value: int


class Cumulative(NamedTuple):
    """A counter snapshot: the current total, not a change.

    Use when the source tracks a running total — e.g. a process reporting lifetime
    request count. Rate computation must account for resets (process restarts cause
    the cumulative value to drop)."""

    value: int


type Counter = Delta | Cumulative
"""A counted quantity, either as an increment or a running total.

Delta and Cumulative have different aggregation semantics: deltas are summed
directly; cumulatives require last-seen tracking and reset detection."""

Gauge = NewType("Gauge", float)
"""An instantaneous reading of a continuous quantity that can rise or fall.

Use for measurements sampled at a point in time — memory usage, queue depth,
temperature. Aggregators compute min, max, mean, or distributions over gauges."""

Message = NewType("Message", str)
"""A free-form string event for logs, annotations, or human-readable observations.

Not aggregated numerically; aggregators collect or search them."""

Boolean = NewType("Boolean", bool)
"""A true/false state at a point in time.

Use for flags, health checks, or binary conditions — e.g. circuit breaker open.
Aggregators count truths, compute ratios, or detect transitions."""

Categorical = NewType("Categorical", str)
"""A discrete string value from an open set of labels.

Use for classification or state — HTTP status class, job outcome, error kind.
Aggregators compute frequency distributions or detect transitions."""

type Primitive = Counter | Gauge | Message | Boolean | Categorical
"""The set of all emittable value types. Every Event carries exactly one Primitive."""
