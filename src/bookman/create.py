"""Constructors for creating Event values."""

import time

from bookman.events import Event
from bookman.primitives import Dims, Primitive, Timestamp


def point(value: Primitive, dims: Dims, at: Timestamp | None = None) -> Event:
    """Construct a point event, defaulting to the current time."""

    resolved = Timestamp(time.time()) if at is None else at
    return Event(at=resolved, until=resolved, value=value, dims=dims)


def span(value: Primitive, dims: Dims, at: Timestamp, until: Timestamp) -> Event:
    """Construct a span event over an explicit time range."""

    return Event(at=at, until=until, value=value, dims=dims)
