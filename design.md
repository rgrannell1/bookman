## Primitives

```
Timestamp    = Float
Duration     = Float               -- until - at
Counter      = Delta Int           -- increment by N
             | Cumulative Int      -- current total is N
Gauge        = Float
Message      = Str
Boolean      = True | False
Categorical  = Str
```

## Events

All emitted data is a flat `Event`. Wrappers are constructors into this type, not distinct types.

```
Label        = Str
Primitive    = Counter | Gauge | Message | Boolean | Categorical

Event = {
  at    : Timestamp
  until : Timestamp            -- = at for point events, > at for spans
  value : Primitive
  dims  : Map Label [Str]      -- multimap; id, parent, tag, unit, and user-defined dimensions
}
```

`dims` entries are conventions:

```
dims["id"]     -- own identity, a slash-delimited string e.g. "zahir/job/123"
dims["parent"] -- links this event to an ancestor by its id
dims["tag"]    -- one or more categorical labels e.g. ["error", "slow"]
dims["unit"]   -- unit of measurement e.g. ["ms"]
```

## Layers

The design has two distinct layers.

The **emission layer** consists of `Event` values flowing through `EEmit`. No aggregation logic lives here.

The **aggregation layer** consists of functions over collections of emitted events. Distributions, rates,
and summaries are computed here, downstream of emission.

## Aggregation

Internally, aggregators are `(prepare, monoid, present)` triples. The triple stays closed under
composition — users never interact with this structure directly; they see a human-friendly interface
instead.

```
Aggregator M R = (insert : Event → M,  combine : M → M → M,  empty : M,  extract : M → R)

fold agg xs = agg.extract (fold agg.combine agg.empty (map agg.insert xs))
```

Non-commutative monoids are permitted — ordered aggregations (last-seen value, message sequences,
categorical transitions) are valid. This library targets sub-gigabyte in-process aggregations where
commutativity is not required.

`groupBy` plus fold is sufficient for all keyed breakdowns (per job, per tag, per identifier):

```
groupBy : (Event → K) → Aggregator M R → [Event] → Map K R
```

Common projections for `groupBy`:

```
groupBy (head . .dims["id"])
groupBy (head . .dims["tag"])
groupBy (head . .dims["parent"])
```

The triple is closed under these operations:

```
map_insert f agg      -- pre-process inputs before insert
map_extract g agg     -- post-process output after extract, changes R
zip agg1 agg2         -- run two aggregators in parallel over the same input, produce (R, S)
filter p agg          -- skip non-matching inputs via the monoid identity
sample k agg          -- augment with a reservoir sample of k inputs, produce (R, [Event])
```

`sample` is a combinator, not a primitive — it works on any aggregator. A reservoir of size `k`
is itself a monoid (merge by combining and re-sampling to `k`), so `(M × Reservoir k)` is a monoid
when `M` is. This gives provenance — a representative sample of the inputs that produced a result —
on any aggregation, composably.

```
sample k agg = Aggregator {
  insert  = ev -> (agg.insert ev, reservoir [ev])
  combine = (m1, r1) (m2, r2) -> (agg.combine m1 m2, merge_reservoir k r1 r2)
  empty   = (agg.empty, reservoir [])
  extract = (m, r) -> (agg.extract m, r.events)
}
```

Common aggregation patterns:

```
-- point events only
filter (ev -> ev.until == ev.at)

-- spans only
filter (ev -> ev.until > ev.at)

-- events with a specific tag
filter (ev -> "error" ∈ ev.dims["tag"])

-- span duration
insert = ev -> ev.until - ev.at

-- time series
insert = ev -> (ev.at, ev.value)

-- rate from delta counters
filter (ev -> ev.value is Delta) |> sum |> per_second
```

## Results

`extract` maps each aggregator's internal monoid to a `Result`:

```
Result =
  | Scalar    Float
  | Dist      [Float]
  | Series    [(Timestamp, Float)]
  | Matrix    Map (Key × Key) Float
  | Messages  [Str]
  | Tags      [Tag]
```
