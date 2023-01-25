..  -*- coding: utf-8 -*-

Introduction
~~~~~~~~~~~~
.. currentmodule:: pyswmm

.. only:: html




PySWMM Basics
-------------

After starting Python, import the pyswmm module with

>>> from pyswmm import Simulation

To save repetition, in the documentation we assume that 
PySWMM has been imported this way.

If importing pyswmm fails, it means that Python cannot find the installed
module. Check your installation and your PYTHONPATH.

The following simulation classes are available:

:class:`Simulation`
   This class initializes a simulation object from a SWMM input file (\*.inp).

Initialize a SWMM Model with

>>> sim = Simulation(r"./example.inp")

Once a model is initialized, there are several options available to 
run a simulation as well as edit the simulation. 
