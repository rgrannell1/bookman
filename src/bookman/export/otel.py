"""OTel export for bookman Result types. Only Scalar and Series are supported for now."""

import time

from bookman.bookman_types import Scalar, Series, Timestamp

type OtelDataPoint = dict
type OtelMetric = dict


def _data_point(time_unix_nano: int, value: float) -> OtelDataPoint:
    return {"time_unix_nano": time_unix_nano, "as_double": value, "attributes": {}}


def _scalar_to_gauge(name: str, result: Scalar, at: Timestamp) -> OtelMetric:
    point = _data_point(int(at * 1_000_000_000), result.value)
    return {"name": name, "type": "gauge", "data_points": [point]}


def _series_to_gauge(name: str, result: Series) -> OtelMetric:
    points = [_data_point(int(ts * 1_000_000_000), value) for ts, value in result.points]
    return {"name": name, "type": "gauge", "data_points": points}


def to_otel(name: str, result: Scalar | Series, at: Timestamp | None = None) -> OtelMetric:
    """Convert a Scalar or Series result to an OTel gauge metric dict.

    For Scalar, at is the measurement timestamp; defaults to now if not provided.
    For Series, timestamps come from the points themselves.
    """

    match result:
        case Scalar():
            resolved_at = at if at is not None else time.time()
            return _scalar_to_gauge(name, result, resolved_at)
        case Series():
            return _series_to_gauge(name, result)
        case _:
            raise TypeError(f"no OTel mapping for result type {type(result).__name__!r}")
