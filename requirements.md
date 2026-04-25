This project is a telemetry layer built on top of the EEmit interface from zahir2. It supports multiple telemetry primitives — tags, time ranges, and spans — and is designed to be convertible to OpenTelemetry without being tied to it. The library is simple by design and follows the functional programming style of its sibling libraries orbis, tertius, and zahir. It handles the emission of raw telemetry data and provides general-purpose utilities for aggregating that data.

The aggregation layer is internally structured as composable (insert, combine, empty, extract) quadruples. `insert` maps an Event into the accumulator type, `combine` merges two accumulators, `empty` is the identity accumulator, and `extract` finalises the accumulator into the result type. The combinators `map_insert`, `map_extract`, `zip`, `filter`, and `sample` are used internally to build aggregators from this structure; `fold` and `group_by` are the runners that execute them.

Users never interact with the quadruple structure or the combinators directly. Instead they see a rich library of named, pre-built aggregators — things like `count`, `sum`, `mean`, `last`, `rate`, `percentile`, `messages` — and the two runners. The goal is that a user can pick aggregators off a shelf, compose them with `zip` and `group_by`, and run them against a list of events without knowing anything about accumulators.

Each named aggregator carries a `temporality` field alongside the quadruple — either `DELTA` or `CUMULATIVE` — so that an OTel export layer can serialise correctly without guessing. This field is metadata on the aggregator definition, not part of the accumulator type.

The second milestone covers the aggregation layer. It has two parts.

The first part is the internal machinery: the `Aggregator` type (a dataclass holding the quadruple plus `temporality`), the combinators (`map_insert`, `map_extract`, `zip`, `filter`, `sample`), and the two runners (`fold`, `group_by`). Rolling windows are not a combinator — they are handled by passing a time-bucketing key function to `group_by`, keeping the aggregator structure time-unaware.

The second part is the named aggregator zoo, grouped by result type:

- Scalar reductions: `count`, `sum`, `min`, `max`, `mean`, `first`, `last`
- Distribution: `dist`, `percentile(k)`, `quantiles(ks)`
- Sequence: `head(k)`, `tail(k)`, `messages`
- Frequency: `mode`, `frequencies`
- Span-specific: `duration_mean`, `duration_dist`, `duration_percentile(k)` — these are `map_insert(lambda ev: ev.duration())` wrappers over the scalar and distribution aggregators
- Time series: `series` — collects `(at, value)` pairs into a `Series`

The project is a UV-based Python package named `bookman`, using the `rs` build system. The first implementation milestone covers the primitive types (`src/bookman/primitives.py`) and the flat event type (`src/bookman/events.py`). Primitives are `Counter` (with `Delta` and `Cumulative` variants), `Gauge`, `Message`, `Boolean`, and `Categorical`. An `Event` is a flat record with `at` and `until` timestamps, a `value` of any primitive type, and a `dims` multimap of string keys to lists of strings. These two modules are the foundation all aggregation logic will build on.
