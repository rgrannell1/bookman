"""Prometheus text exposition format export for bookman Result types."""

import time

from bookman.bookman_types import Scalar, Series, Timestamp


def _format_labels(labels: dict[str, str]) -> str:
    if not labels:
        return ""
    pairs = ", ".join(f'{key}="{val}"' for key, val in labels.items())
    return f"{{{pairs}}}"


def _format_line(name: str, labels_str: str, value: float, timestamp_ms: int) -> str:
    return f"{name}{labels_str} {value} {timestamp_ms}"


def _scalar_lines(name: str, result: Scalar, labels_str: str, at: Timestamp) -> list[str]:
    line = _format_line(name, labels_str, result.value, int(at * 1000))
    return [f"# TYPE {name} gauge", line]


def _series_lines(name: str, result: Series, labels_str: str) -> list[str]:
    data_lines = [
        _format_line(name, labels_str, value, int(ts * 1000))
        for ts, value in result.points
    ]
    return [f"# TYPE {name} gauge"] + data_lines


def to_prometheus(
    name: str,
    result: Scalar | Series,
    labels: dict[str, str] | None = None,
    at: Timestamp | None = None,
) -> str:
    """Convert a Scalar or Series result to Prometheus text exposition format.

    For Scalar, at is the measurement timestamp in seconds; defaults to now.
    For Series, timestamps come from the points themselves.
    Labels are rendered as Prometheus label selectors on every line.
    """

    labels_str = _format_labels(labels or {})

    match result:
        case Scalar():
            resolved_at = at if at is not None else time.time()
            lines = _scalar_lines(name, result, labels_str, resolved_at)
        case Series():
            lines = _series_lines(name, result, labels_str)
        case _:
            raise TypeError(f"no Prometheus mapping for result type {type(result).__name__!r}")

    return "\n".join(lines)
