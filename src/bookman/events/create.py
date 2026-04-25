"""Constructors for creating Event values. How users create events."""

import time

from bookman.events.events import Event
from bookman.events.primitives import Dims, Primitive, Timestamp


def point(
    dims: Dims, at: Timestamp | None = None, value: Primitive | None = None
) -> Event:
    """Construct a point event, defaulting to the current time."""

    resolved = time.time() if at is None else at
    return Event(at=resolved, until=resolved, dims=dims, kind="point", value=value)


def span(
    dims: Dims, at: Timestamp, until: Timestamp, value: Primitive | None = None
) -> Event:
    """Construct a span event over an explicit time range."""

    return Event(at=at, until=until, dims=dims, kind="span", value=value)
