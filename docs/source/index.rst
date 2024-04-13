.. use raw html to hide the doc title show it is shows up in browser tab but not on page
.. https://github.com/sphinx-doc/sphinx/issues/8356#issuecomment-1201029122
.. raw:: html

   <div style="visibility: hidden;height:0px">

PySWMM documentation
=====================

.. raw:: html

   </div>

.. image:: _static/banner.jpg
  :alt: pyswmm banner

**Date**: |today| **Version**: |version|

|gh actions| |docs| |license| |pypi version| |downloads| |cite|

-------------------

More information about pyswmm can be found at the `official pyswmm website`_.

.. grid:: 1 2 2 2
    :gutter: 2

    .. grid-item-card::
      :img-top: _static/map.svg
      :class-img-top: sphinx-panel-img
      :class-header: text-center
      :link: overview
      :link-type: doc

      Overview
      ^^^^^^^^^^^^

      Learn about pyswmm's ambition!

    .. grid-item-card::
      :img-top: _static/power.svg
      :class-img-top: sphinx-panel-img
      :class-header: text-center
      :link: quickstart
      :link-type: doc

      Quick Start
      ^^^^^^^^^^

      The quick start section provides sample code snippets for various use cases of pyswmm.
      This is the perfect place to jump-start your own project with pyswmm.

    .. grid-item-card::
      :img-top: _static/book.svg
      :class-img-top: sphinx-panel-img
      :class-header: text-center
      :link: reference/index
      :link-type: doc

      API reference
      ^^^^^^^^^^^^^

      The API reference provides a catalogue of all docstrings written in pyswmm.
      It lays out the modules, functions, and classes provided in pyswmm like and encyclopedia.


    .. grid-item-card::
      :img-top: _static/coffee.svg
      :class-img-top: sphinx-panel-img
      :class-header: text-center
      :link: https://www.pyswmm.org/tutorial

      Video Tutorials
      ^^^^^^^^^^^^^^^^

      The pyswmm development team is putting together a video
      tutorial series the covers the various use cases of pyswmm.

.. toctree::
   :maxdepth: 2
   :hidden:

   overview
   install
   quickstart
   reference/index
   Examples <https://www.pyswmm.org/examples>
   authors
   cite

.. only:: html

.. |gh actions| image:: https://github.com/pyswmm/pyswmm/actions/workflows/python-package.yml/badge.svg?branch=master
   :target: https://github.com/pyswmm/pyswmm/actions/workflows/python-package.yml
   :alt: GitHub Actions Build Status
.. |downloads| image:: https://img.shields.io/badge/dynamic/json.svg?label=Downloads&url=https%3A%2F%2Fpypistats.org%2Fapi%2Fpackages%2Fpyswmm%2Frecent&query=%24.data.last_month&colorB=green&suffix=%20last%20month
   :target: https://pypi.python.org/pypi/pyswmm/
   :alt: PyPI Monthly Downloads
.. |license| image:: https://img.shields.io/pypi/l/pyswmm.svg
   :target: LICENSE.txt
   :alt: License
.. |pypi version| image:: https://img.shields.io/pypi/v/pyswmm.svg
   :target: https://pypi.python.org/pypi/pyswmm/
   :alt: Latest PyPI version
.. |docs| image:: https://github.com/pyswmm/pyswmm/actions/workflows/documentation.yml/badge.svg?branch=master
   :target: http://docs.pyswmm.org/
   :alt: Documentation Status
.. |cite| image:: https://joss.theoj.org/papers/10.21105/joss.02292/status.svg
   :target: https://doi.org/10.21105/joss.02292
   :alt: Cite our Paper
.. _official pyswmm website: https://www.pyswmm.org
