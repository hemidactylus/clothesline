.. _user_guide:

User guide
==========

Terminology
-----------

By `domain` we mean a set of values forming a continuum,
spanning all the way from "minus infinity" to "plus infinity".
Obvious examples are the real numbers, the timeline, but any
other totally-ordered, unbound, continuous set would do.

Interval Sets are a collection of zero, one or more Intervals.
Each :code:`Interval` is the set made of all points in the domain comprised between its two
ends (each an :code:`IntervalPeg`). The values themselves at the pegs can be included or
not in the interval, as specified by the mathematical notation:

.. code-block::

  [a, b] = { x / a <= x <= b }
  (a, b) = { x / a <  x <  b }

An :code:`Interval` can span all the way to the infinities.

An :code:`IntervalSet` is the union of an arbitrary (finite) number of Intervals.
In the internal representation of Interval Sets in :code:`clothesline`,
interval sets are always reduced to a canonical form, which enables, among other advantages, a meaningful implementation of the equality operator.

.. note::
  In other words, an Interval is an uninterrupted segment within the domain, whil an Interval Set is any set of points, possibly with "holes".

The :code:`clothesline` library lets you create Interval Set in several
ways, operate on them, combine them, store/retrieve them in serialized form. You should be able to do everything you need without the need to
reach the lower-level objects such as :code:`Interval` and :code:`IntervalPeg`.

Interval Sets are meant for use as immutable objects.

:code:`clothesline` offers ready-made classes to handle Interval Sets
over two domains: real numbers (:code:`clothesline.RealIntervalSet`) and :code:`datetime.datetime` objects (:code:`clothesline.DatetimeIntervalSet`). In the follow we mostly stick to the former, but analogous usage patterns hold (with the input values adapted appropriately).

.. warning::    
    It is unwise, and not supported, to mix Interval Sets built on different domains.
    That said, regardless of the domain, the symbols representing the infinities are the same.

Set creation
------------

There are various ways to create Interval Sets.

Builder
~~~~~~~

One can get a `builder` from the class and use it to generate single-interval Interval Sets, with a syntax reminiscent
of the above mathematical notation:

.. code-block:: python

  import clothesline
  bld = clothesline.RealIntervalSet.builder()

  bset1 = bld[0][1]     # [0, 1]
  bset2 = bld(7)(9)     # (7, 9)
  bset3 = bld[0](10)    # [0, 10)
  bset4 = bld(...)(6)   # (-inf, 6)
  bset5 = bld[-8][...]  # [-8, +inf)

The ellipsis, depending on the position, would get translated
to the correct infinity. If the end point is lesser than the start point,
a :code:`clothesline.exceptions.InvalidValueError` is raised.

Usage of the builder, as for the utils case below, results in
single-interval Interval Sets: to build more generic sets, one can make
use of the set operations to combine them as desired.

Utils
~~~~~

It is possible to get an `utils` object from the Interval Set class
and use it to generate standard interval sets:

.. code-block:: python

  import clothesline
  uti = clothesline.RealIntervalSet.utils()

  uset0 = uti.empty()                       # {}
  uset1 = uti.open(2, 3)                    # (2, 3)
  uset2 = uti.closed(4, 5)                  # [4, 5]
  uset3 = uti.point(6)                      # [6, 6]
  uset4 = uti.low_slice(7)                  # (-inf, 7)
  uset5 = uti.high_slice(8, included=True)  # [8, +inf)
  uset6 = uti.all()                         # (-inf, +inf)
  uset7 = uti.interval(9, False, 10, True)  # (9, 10]

The last and most general method (:code:`interval()`) requires
specifying, for the begin and end value, whether the
point itself is included.

Constructor
~~~~~~~~~~~

Interval Sets can be created with the class constructor:
:code:`newIntervalSet = RealIntervalSet([interval1, interval2, ...])`,
which may be more amenable to programmatic approaches.
The provided Intervals, in turn, can be built in three
ways:

- with a `builder` obtained from an Interval class;
- with an `utils` obtained from an Interval class;
- through the explicit constructor of the Interval class itself

Note that the `builder` and the `utils` obtained from Intervals, while having essentially the same behaviour as those from Interval Sets, will
always return instances of the appropriate Interval class.
(Note: the Interval :code:`utils` lacks the :code:`empty()` method.)

When creating an Interval through its constructor, one must provide
two instances of the :code:`IntervalPeg` class (which represents
a domain value and a boolean to express whether included
in the interval or excluded). In case infinities are involved, these
are to be explicitly imported and used as symbols as seen above.

The following code snippet exemplifies the techniques described above:

.. code-block:: python

  from clothesline import RealIntervalSet
  from clothesline.real_interval import RealInterval
  from clothesline.interval_peg import IntervalPeg
  #
  rbld = RealInterval.builder()
  ruti = RealInterval.utils()

  int1 = rbld[3](5)
  #
  int2 = ruti.open(10, 20)
  #
  peg1 = IntervalPeg(4, False)
  peg2 = IntervalPeg(10, True)
  int3 = RealInterval(peg1, peg2)
  ##
  intervalset = RealIntervalSet([int1, int2, int3])   # [3, 20)

.. note::
  While there are separate Interval and Interval Set
  classes for each domain (e.g. real numbers vs. datetimes),
  the :code:`IntervalPeg` class is universal. As a consequence,
  one does not have to subclass it when building an extension
  to a different domain.

Infinities
~~~~~~~~~~

Infinities can be specified as explicit values:

.. code-block:: python

  import clothesline
  from clothesline.algebra.symbols import PlusInf, MinusInf
  from clothesline.interval_peg import IntervalPeg
  uti = clothesline.RealIntervalSet.utils()
  #
  my_peg = IntervalPeg(MinusInf, False)
  uset8 = uti.interval(9, False, PlusInf, False) # (9, +inf)
  er = uti.interval(MinusInf, True, 10, False)   # InvalidValueError!

Infinities are handled automatically in all operations
and are always
`references to` (and not "instances of") two special
classes: :code:`clothesline.algebra.symbols.MinusInf`
and :code:`clothesline.algebra.symbols.PlusInf`.

One should rarely, if at all, concern themselves with
the actual nature of infinities in clothesline.

Set operations
--------------

Most standard set operations, both unary and binary,
are supported between Interval Sets.
Union (:code:`union` method, aliased as :code:`+`) and difference (:code:`difference` method, equivalently :code:`-`)
are useful to build more complex Interval Sets
starting from the one-interval elements seen so far.

.. code-block:: python

  import clothesline
  bld = clothesline.RealIntervalSet.builder()
  uti = clothesline.RealIntervalSet.utils()

  set1 = bld[-1][1]
  set2 = bld(0)[2]
  set3 = set1 + set2
  set3 == set1.union(set2)            # True
  set4 = set3.difference(uti.point(0))
  set4 == set3 - uti.point(0)         # True
  print(set1.xor(set4))
  set5 = bld[-5](5)
  print(set5.complement())
  set5.superset_of(set2)              # True
  set5.superset_of(uti.high_slice(0)) # False

Inspection
----------

The method :code:`intervals()` of an Interval Set returns a (sorted) iterator
over all component Intervals (instances of the appropriate Interval class).
Each of these, in turn, exposes an iterator over its two pegs
(start and end, in that order), whose properties :code:`value`
and :code:`included` can be accessed for any further use.

If needed, moreover, package :py:mod:`clothesline.algebra.symbols`
offers tools to work with a domain in a way that is friendly with
the :code:`MinusInf` and :code:`PlusInf` objects.

.. code-block:: python

  import clothesline
  bld = clothesline.RealIntervalSet.builder()
  set1 = bld[...](-5) + bld[0][10] - bld[2](4)

  for int in set1.intervals():
      begin, end = list(int.pegs())
      print('From %s (%s) ' % (begin.value, begin.included), end='')
      print('to %s (%s)' % (end.value, end.included))

  from clothesline.algebra.symbols import is_symbol
  all_pegs = (peg for int in set1.intervals() for peg in int.pegs())
  if any(is_symbol(peg.value) for peg in all_pegs):
      print('Infinities involved!')

Hashability
-----------

Methods :code:`__eq__()` and :code:`__hash__()` are implemented,
which enables usage of Interval Sets (as well as Intervals)
as elements of standard Python sets or keys of dicts, for instance.
Moreover, since the internal representation of Interval Sets is always
normalized to a canonical form, sets that are "mathematically equal" will always
evaluate to the same Python hash (and yield :code:`True` under the
:code:`==` comparison).

Metric
------

Most domains, such as real numbers, are 
equipped with a metric, i.e. a way to determine
the "extent" of an interval.

.. code-block:: python

  import clothesline
  bld = clothesline.RealIntervalSet.builder()

  bld[0](10).extension()      # 10
  bld(...)[0].extension()
      # <class 'clothesline.algebra.symbols.PlusInf'>
  (bld[1][2] + bld[6][8]).extension() # 3

Serializability
---------------

The :code:`clothesline` package does not directly provide
serialization/deserialization facilities, thus leaving
maximum flexibility to the user: what it does,
instead, is to provide a JSON-friendly dict
representation for its
objects, that can then be dumped, stored and loaded
wherever it is seen fit using e.g. the JSON format.

.. code-block:: python

  import clothesline
  bld = clothesline.RealIntervalSet.builder()
  uti = clothesline.RealIntervalSet.utils()

  set1 = bld[0](3) + bld(5)(8)
  set2 = bld[...](-1) - bld[-3][-2]

  dset1 = set1.to_dict()
  dset2 = set2.to_dict()

  import json

  jset1 = json.dumps(dset1)   # this is a String
  jset2 = json.dumps(dset2)   # this is a String

  set1 == uti.from_dict(json.loads(jset1))    # True
  set2 == uti.from_dict(json.loads(jset2))    # True


Datetime
--------

Support for datetime-based interval sets is ready to use:
class `DatetimeIntervalSet` supports everything
that has been shown so far.

.. code-block:: python

  import clothesline
  from datetime import datetime
  bld = clothesline.DatetimeIntervalSet.builder()
  uti = clothesline.DatetimeIntervalSet.utils()

  tset1 = bld[datetime(1999, 12, 31)][...]
  tset2 = bld[datetime(2001, 1, 1)](...)

  tset3 = bld[datetime(2022, 1, 1)](datetime(2023, 1, 1))
  print(tset3.extension())  # 365 days, 0:00:00

  import json
  jtset1 = json.dumps(tset1.to_dict())
  tset1 == uti.from_dict(json.loads(jtset1))  # True

.. warning::    
    It is unwise, and not supported, to mix Interval Sets built on different domains.
