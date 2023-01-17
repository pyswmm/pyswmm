..  -*- coding: utf-8 -*-

============
Quick Start
============

Start here to begin working with pyswmm.

The pyswmm package allows seamless interaction with the USEPA-SWMM5
data model.  Parameter getters/setters and results getters have been
exposed, allowing the user to see results while a simulation is
running as well as update link settings.

Loading a Model
---------------

There are three options to load a model. If there is no desire to
interact with the simulation then the simplest way to run the
model is the following:

.. code-block:: python

	>>> from pyswmm import Simulation
	>>>
	>>> sim = Simulation('./testmodel.inp')
	>>> sim.execute()


The following method allows the user to read in a model and
manually step through the simulation and get/set parameters and
results.  This scenario is the cleanest solution using a
with statement. It automatically cleans up after the
simulation is complete.

.. code-block:: python

	>>> from pyswmm import Simulation
	>>>
	>>> with Simulation('./testmodel.inp') as sim:
	... 	for step in sim:
	... 		pass

One feature that pyswmm adds to the modeling world is the simulation
stride function ``step_advance``.  Assuming a user has developed all
of their control rules in in a Python script, to reduce simulation
time a user can specify how often Python controls should be evaluated.

For example, let's assume ``testmodel.inp`` has a 30 second routing step
(using the dynamic wave solver, this step could vary significantly).  If
complex control scenarios are developed, evaluating rules could add
significant time to the simulation.

.. code-block:: python

	>>> from pyswmm import Simulation
	>>>
	>>> with Simulation('testmodel.inp') as sim:
	... 	sim.step_advance(300)
	... 	for step in sim:
	... 		print(sim.current_time)
	... 		# or here! sim.step_advance(newvalue)

	2015-11-01 14:05:00
	2015-11-01 14:10:00
	2015-11-01 14:15:00
	2015-11-01 14:20:00

Nodes
-----

For interacting with nodes a :py:class:`pyswmm.nodes.Nodes` object must be initialized.
See the following example. Once the ``Nodes`` object is initialized,
you can then initialize a :py:class:`pyswmm.nodes.Node`

.. code-block:: python

	>>> from pyswmm import Simulation, Nodes
	>>>
	>>> with Simulation('./testmodel.inp') as sim:
	... 	node_object = Nodes(sim)
	...
	... 	#J1 node instantiation
	... 	J1 = node_object["J1"]
	... 	print(J1.invert_elevation)
	... 	print(J1.is_junction())
	...
	... 	#Step through a simulation
	... 	for step in sim:
	... 		print(J1.total_inflow)
	...


Links
-----

For interacting with links a :py:class:`pyswmm.links.Links` object must be initialized.
See the following example. Once the ``Links`` object is initialized,
you can then initialize a :py:class:`pyswmm.links.Link`

.. code-block:: python


	>>> from pyswmm import Simulation, Links
	>>>
	>>> with Simulation('./testmodel.inp') as sim:
	... 	link_object = Links(sim)
	...
	... 	#C1:C2 link instantiation
	... 	c1c2 = link_object["C1:C2"]
	... 	print(c1c2.flow_limit)
	... 	print(c1c2.is_conduit())
	...
	... 	#Step through a simulation
	... 	for step in sim:
	... 		print(c1c2.flow)
	... 		if c1c2.flow > 10.0:
	... 			c1c2.target_setting = 0.5
	...


Subcatchments
-------------

For interacting with subcatchments a :py:class:`pyswmm.subcatchments.Subcatchments`
object must be initialized. See the following example. Once the ``Subcatchments`` object is initialized,
you can then initialize a :py:class:`pyswmm.subcatchments.Subcatchment`

.. code-block:: python


	>>> from pyswmm import Simulation, Subcatchments
	>>>
	>>> with Simulation('./testmodel.inp') as sim:
	... 	subcatch_object = Subcatchments(sim)
	...
	... 	#SC1 subcatchment instantiation
	... 	SC1 = subcatch_object["S1"]
	... 	print(SC1.area)
	...
	... 	#Step through a simulation
	... 	for step in sim:
	... 		print(SC1.runoff)
	...


In the example above we introduce the option to change a link's settings.

PySWMM Controls
---------------

The pyswmm package exposes new possibility in interfacing with models.  All control
rules can now be removed from USEPA SWMM5 and brought into Python.  Now that this
functionality exists, open-source Python packages can now be used in conjunction
with pyswmm to bring even more complex control routines.

The following example illustrates the use of functions for
comparing two depths.

.. code-block:: python

	>>> from pyswmm import Simulation, Links, Nodes
	>>>
	>>> def TestDepth(node, node2):
	>>> 	if node > node2:
	>>> 		return True
	>>> 	else:
	>>> 		return False
	>>>
	>>> with Simulation('./testmodel.inp') as sim:
	... 	link_object = Links(sim)
	...
	... 	#C1:C2 link instantiation
	... 	c1c2 = link_object["C1:C2"]
	...
	... 	node_object = Nodes(sim)
	... 	#J1 node instantiation
	... 	J1 = node_object["J1"]
	... 	#J2 node instantiation
	... 	J2 = node_object["J2"]
	...
	... 	#Step through a simulation
	... 	for step in sim:
	... 		if TestDepth(J1.depth, J2.depth):
	... 			c1c2.target_setting = 0.5
	...

If an EPA-SWMM5 Model has existing control actions within, any control
rules developed using pyswmm will have the highest priority.  All pyswmm
control actions are evaluated at the end of each simulation step, after
EPA-SWMM native controls have been evaluated.  If control actions are reported,
any control action updated by pyswmm will be output to the \*.rpt file.


Generate Node Inflows
---------------------

Among the newest features pyswmm brings to SWMM5 modeling is the ability to
set a node's inflow.  This can enable the user to model different behavior such as
runoff or seasonality.

.. code-block:: python

	>>> from pyswmm import Simulation, Nodes
	>>>
	>>> with Simulation('/testmodel.inp') as sim:
	... 	j1 = Nodes(sim)["J1"]
	... 	for step in sim:
	... 		j1.generated_inflow(9)
    
    
Access SWMM Output Binary File
-------------------------------
As of pyswmm version v1.1.0, the Output module provides the ability to process 
timeseries and metadata in the SWMM output binary file. This feature enables the user to 
access data in the binary file without re-running the simulation.

To access a SWMM outfile, you need to initialize a :py:class:`pyswmm.output.Output` object.
Once the ``Output`` object is initialized, you can use pre-defined methods to access data in the binary file.

The following example opens a SWMM output binary file and identifies the number of subcatchments, nodes,
and links and the SWMM engine used to generate the binary file. 

.. code-block:: python

    >>> from pyswmm import Output
    >>>
    >>> with Output('tests/data/model_full_features.out') as out:
    ...     print(len(out.subcatchments))
    ...     print(len(out.nodes))
    ...     print(len(out.links))
    ...     print(out.version)

The next example opens a SWMM output binary file and gets the entire depth timeseries for node `J1` stored in the 
binary file using :py:class:`pyswmm.output.Output.node_series` method.

.. code-block:: python

        >>> from swmm.toolkit.shared_enum import NodeAttribute
        >>> from pyswmm import Output
        >>>
        >>> with Output('tests/data/model_full_features.out') as out:
        ...     ts = out.node_series('J1', NodeAttribute.INVERT_DEPTH, datetime(2015, 11, 1, 15), datetime(2015, 11, 1, 16))
        ...     for index in ts:
        ...         print(index, ts[index])
        >>> 2015-11-01 15:00:00 15.0
        >>> 2015-11-01 15:01:00 15.0
        >>> 2015-11-01 15:02:00 15.0
        >>> 2015-11-01 15:03:00 15.0

The :py:class:`pyswmm.output.Output.node_series` method allows the user to access all timeseries types for node objects such as INVERT_DEPTH, HYDRAULIC_HEAD, 
PONDED_VOLUME, LATERAL_INFLOW, TOTAL_INFLOW, and FLOODING_LOSSES. If pollutants are defined in the simulation, the concentration 
timeseries can be accessed using POLLUT_CONC_0.

Lid Controls
---------------------
For interacting with lid controls a :py:class:`pyswmm.lidcontrols.LidControls`
object must be initialized. See the following example. Once the ``LidControls`` object is initialized,
you can then initialize a :py:class:`pyswmm.lidcontrols.LidControl`. Once the ``LidControl`` object is initialized, 
you can then interact with the parameters defined in each layers within an Lid Control: ``Surface``, ``Soil``, 
``Storage``, ``Pavement``, ``Drain``, ``DrainMat``. 

The layers parameters that can be accessed using PySWMM are listed in the table below.

.. code-block:: python

	>>> from pyswmm import Simulation, LidControls
	>>>
	>>> with Simulation('/testmodel.inp') as sim:
	... 	rain_barrel = LidControls(sim)["rain_barrel"]
	... 	print(rain_barrel.drain.coefficient)
	... 	rain_barrel.drain.coefficient = 0.60
	... 	print(rain_barrel.drain.coefficient)    
    
All LidControl parameters can be accessed before and during model simulations. 
All LidControl parameters can be set before model simulation. Only some LidControl parameters can be set 
during model simulation.


Lid Groups
---------------------
For interacting with group of lids defined on a subcatchment :py:class:`pyswmm.lidgroups.LidGroups`
object must be initialized. See the following example. Once the ``LidGroups`` object is initialized,
you can then initialize a :py:class:`pyswmm.lidgroups.LidGroup`. Once the ``LidGroup`` object is initialized, 
you can then interact with the lid units defined on the subcatchment. You can iterate through the list of lid units 
using the LidGroup object. 

.. code-block:: python

	>>> from pyswmm import Simulation, LidGroups
	>>>
	>>> with Simulation('/testmodel.inp') as sim:
	... 	lid_on_sub = LidGroups(sim)["subcatch_id"]
	... 	for lid in lid_on_sub:
	... 		print(lid)
	... 	print(lid_on_sub[0])
	... 	for step in sim:
	... 		print(lid_on_sub.old_drain_flow)
    

Lid Units
---------------------
For interacting with group of lids defined on a subcatchment :py:class:`pyswmm.lidgroups.LidGroups`
object must be initialized. See the example above. Once the ``LidGroups`` object is initialized,
you can then initialize a :py:class:`pyswmm.lidgroups.LidGroup`. Once the ``LidGroup`` object is initialized, 
you can then interact with the lid units defined on the subcatchment. You can iterate through the list of lid units 
using the LidGroup object. 

.. code-block:: python

	>>> from pyswmm import Simulation, LidGroups
	>>>
	>>> with Simulation('/testmodel.inp') as sim:
	... 	lid_on_sub = LidGroups(sim)["subcatch_id"]
	... 	for lid in lid_on_sub:
	... 		print(lid)
	... 	print(lid_on_sub[0])
	... 	for step in sim:
	... 		print(lid_on_sub.water_balance.inflow)
	... 		print(lid_on_sub.water_balance.evaporation)
    
All LidUnits parameters can be accessed before and during model simulations. 
All LidUnits parameters can be set before model simulation. Only some LidUnits parameters can be set 
during model simulation.
