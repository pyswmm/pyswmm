PYSWMM 
======

*Python Wrapper for Stormwater Management Model (SWMM5)*

Documentation
	http://pyswmm.readthedocs.io/en/latest/?badge=latest#
Development
	https://github.com/OpenWaterAnalytics/pyswmm/
PySWMM Wiki 
	https://github.com/OpenWaterAnalytics/pyswmm/wiki/
	
   .. image:: https://readthedocs.org/projects/pyswmm/badge/?version=latest
      :target: http://pyswmm.readthedocs.io/en/latest/?badge=latest
      :alt: Documentation Status	

   .. image:: https://www.quantifiedcode.com/api/v1/project/8f76319eee384957bd1b83325774e52c/badge.svg
      :target: https://www.quantifiedcode.com/app/project/8f76319eee384957bd1b83325774e52c
      :alt: Code issues
	  
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
tracking hydraulic trends for control actions.  Enabling complex controls rules 
opens the door to faster prototyping for basin-wide coordinated control frameworks 
such as agent-based modeling or market-based optimization. PySWMM more easily 
facilitates the implementation of machine learning techniques such as a support 
vector machine to be used as forecasting tools. 

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

Get the latest version of PySWMM from (COMING SOON!!!!!)
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

Sponsors
--------

EmNet LLC: 
	.. image:: http://emnet.net/templates/emnet/images/footer_logo.png
	  :target: http://emnet.net/
	  
Acknowledgements
----------------

- Tim Cera
- Assela Pathirana



