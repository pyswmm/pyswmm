PYSWMM 
======

*Python Wrapper for Stormwater Management Model (SWMM5)*

Documentation
	http://pyswmm.readthedocs.io/
Development
	https://github.com/OpenWaterAnalytics/pyswmm/
PySWMM Wiki 
	https://github.com/OpenWaterAnalytics/pyswmm/wiki/
	
   .. image:: https://readthedocs.org/projects/pyswmm/badge/?version=inputapienhancements
      :target: http://pyswmm.readthedocs.io/en/inputapienhancements/?badge=inputapienhancements
      :alt: Documentation Status	


YouTube Examples
----------------
Stream Results and Adjust Weir Setting
	.. image:: http://img.youtube.com/vi/U5Z0NXTEjHE/0.jpg
	  :target: http://www.youtube.com/watch?v=U5Z0NXTEjHE

Abstract
--------

In support of the OpenWaterAnalytics open source initiative, the PySWMM project encompasses the development of a Python interfacing wrapper to SWMM5 with parallel ongoing development of the USEPA Stormwater Management Model (SWMM5) application programming interface (API). PySWMM (along with the co-development of the SWMM5-API) is being developed to enable Python to access the SWMM5 data model to facilitate rapid prototyping enabling users to observe simulated values during simulation time, change controllable features, such as weir and pump settings, as well as load externally generated inflows to a node during simulation time.  The over-arching goal is to provide the community with a complete collection of low-level interfacing functions through which the user can access the entire data model as well as make modifications (getters and setters).  Until the recent work on the extended SWMM5-API, complex control configurations required special non-connected hydraulic units known generally as *widgets* that had to be incorporated to track state systems (e.g. WWF, DWF, ramping up, ramping down).  With the development of PySWMM, control algorithms can now be developed exclusively in Python which allows the use of functions and objects as well as storing and tracking hydraulic trends (running averages).  Enabling complex controls rules opens the door to faster prototyping for basin-wide coordinated control frameworks such as agent-based modeling or market-based optimization and more easily facilitates the implementation of machine learning techniques such as a support vector machine to be used as forecasting tools. Some of these tools are demonstrated within. Allowing users to programmatically assign inflow rate values to nodes provides a framework for making model run faster.  Models can run faster by replacing a tributary pipe network with a trained neural network.  As the project evolves, the SWMM-API will provide a complete interfacing framework that gives full access to the SWMM data model, active simulation results and stability, and simulated output values.  

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

A quick example that steps through a simulation::

	>>> from swmm5 import pyswmm
    >>> swmm_model = pyswmm(r'\\.inp',r'\\.rpt',r'\\.out')
    >>> swmm_model.swmm_open()
    >>> swmm_model.swmm_start()
    >>> while(True):
    ...     time = swmm_model.swmm_step() # or swmm_stride()
    ...     if (time <= 0.0): break
    >>>
    >>> swmm_model.swmm_end()
    >>> swmm_model.swmm_report()
    >>> swmm_model.swmm_close()  	

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

   Copyright (C) 2004-2017 PySWMM Developers
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



