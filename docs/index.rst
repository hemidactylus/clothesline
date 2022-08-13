.. clothesline documentation master file, created by
   sphinx-quickstart on Wed Jul 13 16:25:55 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

clothesline
===========

A library to handle sets, made of intervals over a continuous 
infinite axis (a "domain") such as the real numbers or date/times.

.. code-block:: python

   import clothesline
   bld = clothesline.RealIntervalSet.builder()
   set1 = bld[-10](10) - bld(0)[1]
   set1                       # [-10, 0] U (1, 10)
   set1.extension()           # 19
   set2 = set1 + bld[100](...)
   set2.complement()          # (-inf, -10) U (0, 1] U [10, 100)
   set2 + set2.complement()   # (-inf, +inf)

For a primer, jump to :ref:`quickstart`.
Then you may be interested in the :ref:`user_guide`.
To build your own extension (covering a custom domain), see :ref:`extension`
(which does not require knowledge of the :ref:`structure`).

.. image:: _static/logo.png
  :width: 400
  :alt: Alternative text

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   quickstart
   user_guide
   structure
   extension
   modules

.. Indices and tables
.. ==================

.. * :ref:`genindex`
.. * :ref:`modindex`
.. * :ref:`search`
