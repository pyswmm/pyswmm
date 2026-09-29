..  -*- coding: utf-8 -*-

.. currentmodule:: pyswmm.output

Output Module
==============

   .. autosummary::
      :nosignatures:
      :toctree: api/

      Output
      SubcatchSeries
      NodeSeries
      LinkSeries
      SystemSeries

Multiple pollutants
-------------------

The ``subcatch_attributes``, ``node_attributes``, and ``link_attributes``
mappings include selectors for every pollutant in an output file. Their
``POLLUT_CONC_0``, ``POLLUT_CONC_1``, ... indices correspond to the values in
``Output.pollutants``. For example, to read each pollutant's concentration
at a link throughout a simulation:

.. code-block:: python

   from pyswmm import Output

   with Output("model.out") as out:
       concentrations = {
           name: out.link_series(
               "C1", out.link_attributes["POLLUT_CONC_{}".format(index)]
           )
           for name, index in out.pollutants.items()
       }

The same selectors work with ``link_attribute`` to retrieve a pollutant's
concentration at all links for one report time. Use the corresponding mappings
for subcatchment and node results. The ``subcatch_result``, ``node_result``, and
``link_result`` methods include every pollutant in their returned dictionaries.

The series helpers also expose the available pollutants. For a model with at
least two pollutants, ``LinkSeries(out)["C1"].pollut_conc_1`` returns the second
pollutant's time series; ``SubcatchSeries`` and ``NodeSeries`` work the same way.

Each output file has its own attribute mapping, so opening files with different
pollutants does not alter the attributes available in another file. Existing
``swmm.toolkit.shared_enum`` selectors remain valid and retain their identities.
Files without pollutants have no ``POLLUT_CONC_*`` entries, and accessing a
missing pollutant through a series helper raises ``AttributeError``.
