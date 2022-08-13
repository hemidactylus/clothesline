[![Documentation Status](https://readthedocs.org/projects/clothesline/badge/?version=latest)](https://clothesline.readthedocs.io/en/latest/?badge=latest)

# clothesline

```
pip install clothesline
```

A library to handle sets, made of intervals over a continuous 
infinite axis (a "domain") such as the real numbers or date/times.

```python
import clothesline
bld = clothesline.RealIntervalSet.builder()
set1 = bld[-10](10) - bld(0)[1]
set1                       # [-10, 0] U (1, 10)
set1.extension()           # 19
set2 = set1 + bld[100](...)
set2.complement()          # (-inf, -10) U (0, 1] U [10, 100)
set2 + set2.complement()   # (-inf, +inf)
```

<img src="https://raw.githubusercontent.com/hemidactylus/clothesline/main/docs/_static/logo.png" width="400px" />

## Quickstart

_Note_: for the full documentation, visit [`clothesline.readthedocs.io`](https://clothesline.readthedocs.io).

### Work with sets

The library provides ready-to-use
`RealIntervalSet` to deal with sets over a number line
and `DatetimeIntervalSet` for date intervals.

Start by importing the library and getting a `builder`
for interval sets on the real line:

```python
import clothesline
bld = clothesline.RealIntervalSet.builder()
```

Create a couple of intervals:

```python
set1 = bld(0)(10)
set2 = bld[0][1] + bld(2)(3) + bld[20](...)
print(set2)
```

Here, round brackets mean that the boundary is excluded; square brackets mean the point is included.
Three dots stand for the point at infinity.

You can also get an `utils` object, to create standard sets such as open or closed intervals, point-like sets and so on:

```python
uti = clothesline.RealIntervalSet.utils()
set3 = uti.open(0, 5)
set4 = uti.high_slice(10, included=True)
```

Most set operations are supported: from complement to difference,
from inclusion tests to XOR. Interval Sets should be treated as immutable objects.
Moreover, since the internal representation of a set is always
normalized to a canonical form, equality tests work as you would
expect:

```python
set5 = set4.union(set2)
set4 - set2
set3 + bld[3](10) == set1   # True
```

For more ways to create and manipulate sets, have a look at the
**User Guide** in the full documentation.

### Store and retrieve

You can convert any interval set into a string (e.g. to store it into
a database) and re-hydrate it later:

```python
import json
serialized = json.dumps(set3.to_dict())
# ...
new_set3 = uti.from_dict(json.loads(serialized))
new_set3 == set3    # True
```

### Datetimes

Support for datetimes is ready out-of-the-box:

```python
from datetime import datetime
dbld = clothesline.DatetimeIntervalSet.builder()
timespan1 = dbld[datetime(2010, 10, 10)](datetime(2011, 2, 20))
print(timespan1.complement())
print(timespan1.extension())
```

That's it! For more, check the [full documentation](https://clothesline.readthedocs.io).

## Contributing

> Coming soon.
