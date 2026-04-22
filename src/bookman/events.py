"""The Event type: the single unit of emitted telemetry data in bookman."""

from typing import Literal, NamedTuple

from bookman.primitives import Dims, Duration, Primitive, Timestamp, Unit

type EventKind = Literal["span", "point"]
"""Whether an event is a point observation or a completed span with a duration."""

# seconds per unit — multiply (until - at) by the factor for the requested unit
_UNIT_FACTORS: dict[Unit, float] = {
    "s": 1.0,
    "ms": 1_000.0,
    "us": 1_000_000.0,
    "ns": 1_000_000_000.0,
}


class Event(NamedTuple):
    """A flat, immutable record representing one emitted telemetry observation.

    at    — when the observation was made
    until — when it ended; equal to at for point events, greater for spans
    dims  — named dimensions for grouping and filtering (id, parent, tag, unit, etc.)
    kind  — set by constructors in create.py; 'point' or 'span'
    value — the measured primitive; absent for structural/lifecycle events"""

    at: Timestamp
    until: Timestamp
    dims: Dims
    kind: EventKind
    value: Primitive | None = None

    def dim(self, key: str, default: str = "") -> str:
        """Return the first value for a dimension key, or default if absent or empty."""
        values = self.dims.get(key)
        return values[0] if values else default

    def duration(self, unit: Unit = "s") -> Duration:
        """Elapsed time in the given unit. Zero for point events."""
        return (self.until - self.at) * _UNIT_FACTORS[unit]
