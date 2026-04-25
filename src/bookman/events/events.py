"""The Event type: the single unit of emitted telemetry data in bookman."""

from typing import NamedTuple
from bookman.events.primitives import Dims, Duration, EventKind, Primitive, Timestamp, TimeUnit
from bookman.events.constants import _TIME_UNIT_FACTORS


class Event(NamedTuple):
    # When the event started
    at: Timestamp
    # When the event ended
    until: Timestamp
    # Dimensions we can group and filter along
    dims: Dims
    # Whether the event is a point observation or a completed span with a duration
    kind: EventKind
    # The value we carry, optionally; sometimes the event is the value itself
    value: Primitive | None = None

    def dim(self, key: str, default: str = "") -> str:
        """Return the first value for a dimension key, or default if absent or empty."""

        values = self.dims.get(key)
        return values[0] if values else default # TODO this is suspect

    def duration(self, unit: TimeUnit = "s") -> Duration:
        """Elapsed time in the given unit. Zero for point events."""

        if self.kind == "point":
            return 0.0

        if unit not in _TIME_UNIT_FACTORS:
            raise ValueError(f"Invalid time unit: {unit}")

        return (self.until - self.at) * _TIME_UNIT_FACTORS[unit]
