PYSWMM 
======

*Python Wrapper for Stormwater Management Model (SWMM5)*

Documentation
	http://pyswmm.readthedocs.io/en/latest/
Development
	https://github.com/OpenWaterAnalytics/pyswmm/
PySWMM Wiki 
	https://github.com/OpenWaterAnalytics/pyswmm/wiki/

Build status
------------
|appveyor status| |circleci status| |travisci status| |scrutinizer|

Project information
-------------------
|docs| |license| |pypi version|

.. |appveyor status| image:: https://ci.appveyor.com/api/projects/status/jjxpum62nf8ajcar/branch/master?svg=true
   :target: https://ci.appveyor.com/project/OpenWaterAnalytics/pyswmm
   :alt: Appveyor build status
.. |circleci status| image:: https://circleci.com/gh/OpenWaterAnalytics/pyswmm/tree/master.svg?style=shield
   :target: https://circleci.com/gh/OpenWaterAnalytics/pyswmm/tree/master
   :alt: Circle-CI build status
.. |travisci status| image:: https://travis-ci.org/OpenWaterAnalytics/pyswmm.svg?branch=master
   :target: https://travis-ci.org/OpenWaterAnalytics/pyswmm
   :alt: Travis-CI build status
.. |scrutinizer| image:: https://scrutinizer-ci.com/g/OpenWaterAnalytics/pyswmm/badges/quality-score.png?b=master
   :target: https://scrutinizer-ci.com/g/OpenWaterAnalytics/pyswmm/?branch=master
   :alt: Scrutinizer Code Quality
.. |license| image:: https://img.shields.io/pypi/l/pyswmm.svg
   :target: LICENSE.txt
   :alt: License
.. |pypi version| image:: https://img.shields.io/pypi/v/pyswmm.svg
   :target: https://pypi.python.org/pypi/pyswmm/
   :alt: Latest PyPI version
.. |docs| image:: https://readthedocs.org/projects/pyswmm/badge/?version=latest
   :target: http://pyswmm.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status	
   
	  
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
...     sim.report()


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
>>> sim.report()
>>> sim.close()	
	
Bugs
----

Our issue tracker is at https://github.com/OpenWaterAnalytics/pyswmm/issues.
Please report any bugs that you find.  Or, even better, fork the repository on
GitHub and create a pull request.  All changes are welcome, big or small, and we
will help you make the pull request if you are new to git
(just ask on the issue).

License
-------

Distributed with a BSD2 license; see LICENSE.txt::

   Copyright (C) 2014 PySWMM Developers
   Bryant E. McDonnell <bemcdonnell@gmail.com>

Powered By
----------

EmNet LLC:
	.. image:: http://emnet.net/templates/emnet/images/footer_logo.png
	  :target: http://emnet.net/
Open Storm:
    .. image:: https://avatars2.githubusercontent.com/u/28744644?v=3&s=200
      :target: http://open-storm.org/

Acknowledgements
----------------

- Tim Cera
- Assela Pathirana


