PYSWMM
======

*Python Wrapper for Stormwater Management Model (SWMM5)*

Documentation
	http://pyswmm.readthedocs.io/en/latest/
Development
	https://github.com/OpenWaterAnalytics/pyswmm/
PySWMM Wiki
	https://github.com/OpenWaterAnalytics/pyswmm/wiki/
Cite our Paper
	McDonnell, Bryant E., Ratliff, Katherine M., Tryby, Michael E., Wu, Jennifer Jia Xin, & Mullapudi, Abhiram. (2020). PySWMM: The Python Interface to Stormwater Management Model (SWMM). *Journal of Open Source Software, 5*\ (52), 2292, https://doi.org/10.21105/joss.02292

Build status
------------
|appveyor status| |travisci status|

Project information
-------------------
|docs| |license| |pypi version| |downloads| |cite|

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


YouTube Examples
----------------
Stream Results and Adjust Weir Setting
	.. image:: http://img.youtube.com/vi/U5Z0NXTEjHE/0.jpg
	  :target: http://www.youtube.com/watch?v=U5Z0NXTEjHE

Overview
--------

PySWMM is a Python language software package for the creation,
manipulation, and study of the structure, dynamics, and function of complex networks.

With PySWMM you can load and manipulate USEPA Stormwater Management Models.
With the development of PySWMM, control algorithms can now be developed exclusively
in Python which allows the use of functions and objects as well as storing and
tracking hydraulic trends for control actions.

As of version v1.1.0, PySWMM includes new features to proccess metadata and timeseries
stored in SWMM binary output file.

Who uses PySWMM?
----------------

PySWMM is used by engineers, modelers, and researchers who want to streamline
stormwater modeling optimization, controls, and post-processing results.

Goals
-----
PySWMM is intended to provide

-  tools for the study of the structure and
   dynamics within USEPA SWMM5,

-  a standard programming interface and graph implementation that is suitable
   for many applications,

-  a rapid development environment for collaborative, multidisciplinary
   projects,

-  an interface to USEPA SWMM5,

-  development and implementation of control logic outside of native EPA-SWMM Controls,

-  methods for users to establish their own node inflows,

-  a coding interface to binary output files,

-  new modeling possibilities for the SWMM5 Community.

Download
--------

Get the latest version of PySWMM from
https://pypi.python.org/pypi/pyswmm/

::

	$ pip install pyswmm

To get the git version do

::

	$ git clone https://github.com/OpenWaterAnalytics/pyswmm.git


Usage
-----

A quick example that steps through a simulation:

Examples:

Intialize using with statement.  This automatically cleans up
after a simulation

>>> from pyswmm import Simulation
>>>
>>> with Simulation('model.inp') as sim:
...     for ind in sim:
...         pass


Initialize the simulation and execute.  This style does not allow
the user to interact with the simulation.  However, this approach
tends to be the fastest.

>>> from pyswmm import Simulation
>>>
>>> sim = Simulation('model.inp')
>>> sim.execute()


Intialize a simulation and iterate through a simulation. This
approach requires some clean up.

>>> from pyswmm import Simulation
>>>
>>> sim = Simulation('model.inp')
>>> for ind in sim:
...     pass
>>>
>>> sim.close()

Opening a SWMM binary output file and accessing model metadata and
timeseries.

>>> from swmm.toolkit.shared_enum import SubcatchAttribute, NodeAttribute, LinkAttribute
>>> from pyswmm import Output
>>>
>>> with Output('model.out') as out:
...     print(len(out.subcatchments))
...     print(len(out.nodes))
...     print(len(out.links))
...     print(out.version)
...     sub_ts = out.subcatch_series('S1', SubcatchAttribute.RUNOFF_RATE)
...     node_ts = out.node_series('J1', NodeAttribute.INVERT_DEPTH)
...     link_ts = out.link_series('C2', LinkAttribute.FLOW_RATE)

Bugs
----

Our issue tracker is at https://github.com/OpenWaterAnalytics/pyswmm/issues.
Please report any bugs that you find.  Or, even better, fork the repository on
GitHub and create a pull request.  All changes are welcome, big or small, and we
will help you make the pull request if you are new to git
(just ask on the issue).

Contributing
------------
Please check out our Wiki https://github.com/OpenWaterAnalytics/pyswmm/wiki
for more information on contributing, including an Author Contribution Checklist.

License
-------

Distributed with a BSD2 license; see LICENSE.txt::

   Copyright (C) 2014-2022 PySWMM Developers
   Community-Owned See AUTHORS and CITATION.cff

Acknowledgements
----------------

- Tim Cera
- Assela Pathirana
