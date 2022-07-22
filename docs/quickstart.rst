.. _quickstart:

Quickstart
==========

Work with sets
--------------

The library provides ready-to-use
:code:`RealIntervalSet` to deal with sets over a number line
and :code:`DatetimeIntervalSet` for date intervals.

Start by importing the library and getting a :code:`builder`
for interval sets on the real line:

.. code-block:: python

  import clothesline
  bld = clothesline.RealIntervalSet.builder()

Create a couple of intervals:

.. code-block:: python

  set1 = bld(0)(10)
  set2 = bld[0][1] + bld(2)(3) + bld[20](...)
  print(set2)

Here, round brackets mean that the boundary is excluded; square brackets mean the point is included.
Three dots stand for the point at infinity.

You can also get an :code:`utils` object, to create standard sets such as open or closed intervals, point-like sets and so on:

.. code-block:: python

  uti = clothesline.RealIntervalSet.utils()
  set3 = uti.open(0, 5)
  set4 = uti.high_slice(10, included=True)

Most set operations are supported: from complement to difference,
from inclusion tests to XOR. Interval Sets should be treated as immutable objects.
Moreover, since the internal representation of a set is always
normalized to a canonical form, equality tests work as you would
expect:

.. code-block:: python

  set5 = set4.union(set2)
  set4 - set2
  set3 + bld[3](10) == set1   # True

For more ways to create and manipulate sets, have a look at the :ref:`user_guide`.

Store and retrieve
------------------

You can convert any interval set into a string (e.g. to store it into
a database) and re-hydrate it later:

.. code-block:: python

  import json
  serialized = json.dumps(set3.to_dict())
  # ...
  new_set3 = uti.from_dict(json.loads(serialized))
  new_set3 == set3    # True


Datetimes
---------

Support for datetimes is ready out-of-the-box:

.. code-block:: python

  from datetime import datetime
  dbld = clothesline.DatetimeIntervalSet.builder()
  timespan1 = dbld[datetime(2010, 10, 10)](datetime(2011, 2, 20))
  print(timespan1.complement())
  print(timespan1.extension())

That's it! For more, check the rest of this documentation.