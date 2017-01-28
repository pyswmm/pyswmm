.. pyswmm documentation master file, created by
   sphinx-quickstart on Mon Nov 07 21:15:57 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

PYSWMM - Python Wrapper for Stormwater Management Model (SWMM)
==============================================================

Abstract:

In support of the OpenWaterAnalytics open source initiative, the PySWMM project encompasses the development of a Python interfacing wrapper to SWMM5 with parallel ongoing development of the USEPA Stormwater Management Model (SWMM5) application programming interface (API). PySWMM (along with the co-development of the SWMM5-API) is being developed to enable Python to access the SWMM5 data model to facilitate rapid prototyping enabling users to observe simulated values during simulation time, change controllable features, such as weir and pump settings, as well as load externally generated inflows to a node during simulation time.  The over-arching goal is to provide the community with a complete collection of low-level interfacing functions through which the user can access the entire data model as well as make modifications (getters and setters).  Until the recent work on the extended SWMM5-API, complex control configurations required special non-connected hydraulic units known generally as ''widgets'' that had to be incorporated to track state systems (e.g. WWF, DWF, ramping up, ramping down).  With the development of PySWMM, control algorithms can now be developed exclusively in Python which allows the use of functions and objects as well as storing and tracking hydraulic trends (running averages).  Enabling complex controls rules opens the door to faster prototyping for basin-wide coordinated control frameworks such as agent-based modeling or market-based optimization and more easily facilitates the implementation of machine learning techniques such as a support vector machine to be used as forecasting tools. Some of these tools are demonstrated within. Allowing users to programmatically assign inflow rate values to nodes provides a framework for making model run faster.  Models can run faster by replacing a tributary pipe network with a trained neural network.  As the project evolves, the SWMM-API will provide a complete interfacing framework that gives full access to the SWMM data model, active simulation results and stability, and simulated output values.  

Goals:

As the project evolves, the goal is to not only extend the SWMM data model into Python, but to expose and input API enabling a user to deliver a model to the engine outside to formal scope of an input file.  

See more in the PySWMM Wiki: https://github.com/OpenWaterAnalytics/pyswmm/wiki
   
Contents:

.. toctree::
   :maxdepth: 2



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

