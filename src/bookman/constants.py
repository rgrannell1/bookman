"""Constants used across the bookman package."""

from bookman.primitives import TimeUnit

# Multiplication factors to convert seconds into each supported time unit
_TIME_UNIT_FACTORS: dict[TimeUnit, float] = {
    "s": 1.0,
    "ms": 1_000.0,
    "us": 1_000_000.0,
    "ns": 1_000_000_000.0,
}
