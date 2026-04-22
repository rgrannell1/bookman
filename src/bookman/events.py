"""The Event type: the single unit of emitted telemetry data in bookman."""

from typing import NamedTuple
from bookman.primitives import Dims, Primitive, Timestamp


class Event(NamedTuple):
    """A flat, immutable record representing one emitted telemetry observation.

    at    — when the observation was made
    until — when it ended; equal to at for point events, greater for spans
    value — the measured primitive
    dims  — named dimensions for grouping and filtering (id, parent, tag, unit, etc.)"""

    at: Timestamp
    until: Timestamp
    value: Primitive
    dims: Dims
