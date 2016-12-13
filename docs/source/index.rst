.. pyswmm documentation master file, created by
   sphinx-quickstart on Mon Nov 07 21:15:57 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

PYSWMM - Python Wrapper for Stormwater Management Model (SWMM)

Abstract:

In support of the OpenWaterAnalytics open souce inititive, project encompasses the ongoing development of the USEPA Stormwater Management Model (SWMM5) application programming interface (API) and the parallel development of ''PySWMM'' - the Python interfacing wrapper to SWMM5. PySWMM has been developed to extend the SWMM5 data model into Python to facilitate rapid prototyping (such as network analysis and control frameworks), observe simulated values and gives the user the ability to change controllable features such as weir and pump settings during simulation time.  The over-arching goal is to provide the community with a complete collection of low-level interfacing functions for which the user can access the entire data model as well as make modifications (getters and setters).  With the development of PySWMM, complex control algorithms can now be developed exclusively in Python which has been a limitation in the current SWMM5 controls.  Up until the SWMM API was extend, complex controls required special non-connected hydraulic units known generally as ''widgets'' had to be incorporated to track state systems (e.g. WWF, DWF, Ramping up, Ramping Down).  With PySWMM, complex control algorithims can be quickly developed to support basin-wide coordinated control frameworks employing agent-based modeling or market-based optimization, and can incorporate machine learning techniques such as a support vector machine (SVM) to be used as forecasting tools.

Goals:

As the project evolves, the goal is to not only extend the SWMM data model into Python, but to expose and input API enabling a user to deliver a model to the engine outside to formal scope of an input file.  

See more in the PySWMM Wiki: https://github.com/OpenWaterAnalytics/pyswmm/wiki
   
   
Welcome to pyswmm's documentation!
==================================

Contents:

.. toctree::
   :maxdepth: 2



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

