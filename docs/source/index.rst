PySWMM documentation
=====================

**Date**: |today| **Version**: |version|

|appveyor status| |travisci status|
|docs| |license| |pypi version| |downloads| |cite|

-------------------

More information about pyswmm can be found at the `official pyswmm website`_.

.. panels::
    :container: container pb-4
    :card: + intro-card text-center
    :column: col-lg-6 col-md-6 col-sm-6 col-xs-12 p-2

    ---
    :img-top: _static/map.svg

    Overview
    ^^^^^^^^^^^^

    Learn about pyswmm's ambition!

    +++

    .. link-button:: overview
            :type: ref
            :text: Overview!
            :classes: btn-block btn-secondary stretched-link

    ---
    :img-top: _static/power.svg

    Tutorials
    ^^^^^^^^^^

    The tutorials provide sample code snippets for various use cases of pyswmm.
    This is the perfect place to jump-start your own project with pswmm.

    +++

    .. link-button:: tutorial
            :type: ref
            :text: Tutorials!
            :classes: btn-block btn-secondary stretched-link

    ---
    :img-top: _static/book.svg

    API reference
    ^^^^^^^^^^^^^

    The API reference provides a catalogue of all docstrings written in pswmm.
    It lays out the modules, functions, and classes provided in pswmm like and encyclopedia.

    +++

    .. link-button:: reference/index
            :type: ref
            :text: API Reference!
            :classes: btn-block btn-secondary stretched-link

    ---
    :img-top: _static/coffee.svg

    Examples
    ^^^^^^^^^^^^^

    Stand-alone example projects can be found here so you can
    try out pyswmm without needing your own model and data.

    +++

    .. link-button:: https://www.pyswmm.org/examples
            :text: Examples!
            :classes: btn-block btn-secondary stretched-link



.. toctree::
   :maxdepth: 2
   :hidden:

   overview
   install
   tutorial
   reference/index
   Examples <https://www.pyswmm.org/examples>
   authors
   cite

.. only:: html

.. |appveyor status| image:: https://ci.appveyor.com/api/projects/status/gm3ci07gmkoyaeol/branch/master?svg=true
   :target: https://ci.appveyor.com/project/bemcdonnell/pyswmm
   :alt: Appveyor build status
.. |travisci status| image:: https://travis-ci.org/OpenWaterAnalytics/pyswmm.svg?branch=master
   :target: https://travis-ci.org/OpenWaterAnalytics/pyswmm
   :alt: Travis-CI build status
.. |downloads| image:: https://img.shields.io/badge/dynamic/json.svg?label=Downloads&url=https%3A%2F%2Fpypistats.org%2Fapi%2Fpackages%2Fpyswmm%2Frecent&query=%24.data.last_month&colorB=green&suffix=%20last%20month
   :target: https://pypi.python.org/pypi/pyswmm/
   :alt: PyPI Monthly Downloads
.. |license| image:: https://img.shields.io/pypi/l/pyswmm.svg
   :target: LICENSE.txt
   :alt: License
.. |pypi version| image:: https://img.shields.io/pypi/v/pyswmm.svg
   :target: https://pypi.python.org/pypi/pyswmm/
   :alt: Latest PyPI version
.. |docs| image:: https://readthedocs.org/projects/pyswmm/badge/?version=latest
   :target: http://pyswmm.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status
.. |cite| image:: https://joss.theoj.org/papers/10.21105/joss.02292/status.svg
   :target: https://doi.org/10.21105/joss.02292
   :alt: Cite our Paper
.. _official pyswmm website: https://www.pyswmm.org