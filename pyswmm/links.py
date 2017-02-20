# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014 Bryant E. McDonnell
#
# Licensed under the terms of the BSD2 License
# See LICENSE.txt for details
# -----------------------------------------------------------------------------
"""Links module for the pythonic interface to SWMM5."""

from toolkitapi import *
from swmm5 import SWMMException, PYSWMMException

class Links(object):
    """
    Link Iterator Methods

    :param object model: Open Model Instance 

    Examples:
        
    >>> from pyswmm import Simulation
    >>>
    >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
    ...     for link in Links(sim):
    ...         print link
    ...         print link.linkid
    ...
    >>> <swmm5.Link object at 0x031B0350>
    >>> C1
    >>> <swmm5.Link object at 0x030693D0>
    >>> C2
    >>> <swmm5.Link object at 0x031B0350>
    >>> C3
    >>> <swmm5.Link object at 0x030693D0>
    >>> C0

    Iterating or Links Object
    
    >>> links = Links(sim)
    >>> for link in links:
    ...     print link.linkid
    >>> C1:C2
    >>> C2
    >>> C3

    Testing Existence
    
    >>> links = Links(sim)
    >>> "C1:C2" in links
    >>> True

    Initializing a link Object

    >>> links = Links(sim)
    >>> c1c2 = links['C1:C2']
    >>> c1c2.qlimit = 12
    >>> c1c2.qlimit
    >>> 12

    
    """
    def __init__(self, model):
        if not model._model.fileLoaded:
            raise PYSWMMException("SWMM Model Not Open")
        self._model = model._model
        self._cuindex = 0
        self._nLinks = self._model.getProjectSize(ObjectType.LINK)
        
    def __len__(self):
        """Return number of links. Use the expression 'len(Links)'.

        :return: Number of Links
        :rtype: int
        
        """
        return self._model.getProjectSize(ObjectType.LINK)

    def __contains__(self, linkid):
        """Checks if Link ID exists

        :return: ID Exists
        :rtype: bool        
        """
        return self._model.ObjectIDexist(ObjectType.LINK, linkid)

    def __getitem__(self, linkid):
        if self.__contains__(linkid):
            return Link(self._model, linkid)
        else:
            raise PYSWMMException("Link ID Does not Exist")
        
    def __iter__(self):
        return self
    
    def next(self):
        if self._cuindex < self._nLinks:
            linkobject = Link(self._model, self._linkid)
            self._cuindex+=1 #Next Iteration
            return linkobject
        else:
            raise StopIteration()
        
    @property
    def _linkid(self):
        """Link ID"""
        return self._model.getObjectId(ObjectType.LINK, self._cuindex)
    
class Link(object):
    """
    Link Methods
    
    :param object model: Open Model Instance 
    :param str linkid: Link ID

    Examples:

    >>> from pyswmm import Simulation
    >>>
    >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
    ...     c1c2 = Links(sim)["C1:C2"]
    ...     print c1c2.flow
    ...     for step in simulation:
    ...         print c1c2.flow
    ... 0.0
    
    """
    def __init__(self, model, linkid):
        if not model.fileLoaded:
            raise PYSWMMException("SWMM Model Not Open")
        if linkid not in model.getObjectIDList(ObjectType.LINK):
            raise PYSWMMException("ID Not valid")
        self._model = model
        self._linkid = linkid
    #Get Parameters
        
    @property
    def linkid(self):
        """
        Get Link ID

        :return: Paramater Value
        :rtype: float

        Examples:

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     c1c2 = Links(sim)["C1:C2"]
        ...     print c1c2.linkid
        >>> "C1"
        """
        return self._linkid
    
    def is_conduit(self):
        """ Check if link is a Conduit Type

        :return: is conduit
        :rtype: bool
        
        Examples:

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     c1c2 = Links(sim)["C1:C2"]
        ...     print c1c2.is_conduit()
        >>> True
        """
        return self._model.getLinkType(self._linkid) is LinkType.conduit

    def is_pump(self):
        """ Check if link is a Pump Type

        :return: is pump
        :rtype: bool
        
        Examples:

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     c1c2 = Links(sim)["C1:C2"]
        ...     print c1c2.is_pump()
        >>> False
        """
        return self._model.getLinkType(self._linkid) is LinkType.pump
        
    def is_orifice(self):
        """ Check if link is a Orifice Type

        :return: is orifie
        :rtype: bool
        
        Examples:

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     c1c2 = Links(sim)["C1:C2"]
        ...     print c1c2.is_orifice()
        >>> False
        """
        return self._model.getLinkType(self._linkid) is LinkType.orifice
        
    def is_weir(self):
        """ Check if link is a Weir Type

        :return: is weir
        :rtype: bool
        
        Examples:

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     c1c2 = Links(sim)["C1:C2"]
        ...     print c1c2.is_weir()
        >>> False
        """
        return self._model.getLinkType(self._linkid) is LinkType.weir
        
    def is_outlet(self):
        """ Check if link is a Outlet Type

        :return: is outlet
        :rtype: bool
        
        Examples:

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     c1c2 = Links(sim)["C1:C2"]
        ...     print c1c2.is_outlet()
        >>> False
        """
        return self._model.getLinkType(self._linkid) is LinkType.outlet
        
    @property
    def connections(self):
        """ Get link upstream and downstream node IDs

        :return: ("UpstreamNodeID","DownstreamNodeID")
        :rtype: tuple

        Examples:

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     c1c2 = Links(sim)["C1:C2"]
        ...     print c1c2.connections
        >>> ("C1","C2")
        """
        return self._model.getLinkConnections(self._linkid)

    @property
    def inlet_node(self):
        """ Get link inlet node ID

        :return: Inlet node ID
        :rtype: str

        Examples:

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     c1c2 = Links(sim)["C1:C2"]
        ...     print c1c2.inlet_node
        >>> C1
        """
        return self._model.getLinkConnections(self._linkid)[0]

    @property
    def outlet_node(self):
        """ Get link outlet node ID

        :return: Outlet node ID
        :rtype: str

        Examples:

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     c1c2 = Links(sim)["C1:C2"]
        ...     print c1c2.outlet_node
        >>> C2
        """
        return self._model.getLinkConnections(self._linkid)[1]
    
    @property
    def inlet_offset(self):
        """
        Get/set Upstream Offset Depth

        :return: Paramater Value
        :rtype: float

        Examples:

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     c1c2 = Links(sim)["C1:C2"]
        ...     print c1c2.inlet_offset
        >>> 0.1

        Setting the value

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     c1c2 = Links(sim)["C1:C2"]
        ...     print c1c2.inlet_offset
        ...     c1c2.inlet_offset = 0.2
        ...     print c1c2.inlet_offset
        >>> 0.1
        >>> 0.2        
        """
        return self._model.getLinkParam(self._linkid,LinkParams.offset1)

    @inlet_offset.setter
    def inlet_offset(self, param):
        """Set Link Upstream Link Offset"""  
        self._model.setLinkParam(self._linkid,LinkParams.offset1, param)
        
    @property
    def outlet_offset(self):
        """
        Get/set Downstream Offset Depth

        :return: Paramater Value
        :rtype: float

        Examples:

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     c1c2 = Links(sim)["C1:C2"]
        ...     print c1c2.outlet_offset
        >>> 0.1

        Setting the value
        
        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     c1c2 = Links(sim)["C1:C2"]
        ...     print c1c2.outlet_offset
        ...     c1c2.outlet_offset = 0.2
        ...     print c1c2.outlet_offset
        >>> 0.1
        >>> 0.2        
        """
        return self._model.getLinkParam(self._linkid,LinkParams.offset1)

    @outlet_offset.setter
    def outlet_offset(self, param):
        """Set Link Downstream Link Offset"""  
        self._model.setLinkParam(self._linkid,LinkParams.offset2, param)
    
    @property
    def initial_flow(self):
        """
        Get/set Link Initial Flow

        :return: Paramater Value
        :rtype: float

        Examples:

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     c1c2 = Links(sim)["C1:C2"]
        ...     print c1c2.initial_flow
        >>> 0

        Setting the Value

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     c1c2 = Links(sim)["C1:C2"]
        ...     print c1c2.initial_flow
        ...     c1c2.initial_flow = 0.2
        ...     print c1c2.initial_flow
        >>> 0.1
        >>> 0.2        
        """
        return self._model.getLinkParam(self._linkid,LinkParams.q0)

    @initial_flow.setter    
    def initial_flow(self, param):
        """Set Link Initial Flow Rate"""  
        self._model.setLinkParam(self._linkid,LinkParams.q0, param)
    
    @property
    def flow_limit(self):
        """
        Get/set link flow limit

        :return: Paramater Value
        :rtype: float

        Examples:

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     c1c2 = Links(sim)["C1:C2"]
        ...     print c1c2.flow_limit
        >>> 0

        Setting the Value

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     c1c2 = Links(sim)["C1:C2"]
        ...     print c1c2.flow_limit
        ...     c1c2.flow_limit = 0.2
        ...     print c1c2.flow_limit
        >>> 0
        >>> 0.2        
        """
        return self._model.getLinkParam(self._linkid,LinkParams.qLimit)

    @flow_limit.setter
    def flow_limit(self, param):
        """Set Link Flow Limit"""  
        self._model.setLinkParam(self._linkid,LinkParams.qLimit, param)
    
    @property
    def inlet_head_loss(self):
        """
        Get/set Inlet Head Loss

        :return: Paramater Value
        :rtype: float

        Examples:

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     c1c2 = Links(sim)["C1:C2"]
        ...     print c1c2.inlet_head_loss
        >>> 0

        Setting the Value

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     c1c2 = Links(sim)["C1:C2"]
        ...     print c1c2.inlet_head_loss
        ...     c1c2.inlet_head_loss = 0.2
        ...     print c1c2.inlet_head_loss
        >>> 0
        >>> 0.2          
        """
        return self._model.getLinkParam(self._linkid,LinkParams.cLossInlet)

    @inlet_head_loss.setter
    def inlet_head_loss(self, param):
        """Set Link Inlet Head Loss"""  
        self._model.setLinkParam(self._linkid,LinkParams.cLossInlet, param)
    
    @property
    def outlet_head_loss(self):
        """
        Get/set Outlet Head Loss

        :return: Paramater Value
        :rtype: float

        Examples:

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     c1c2 = Links(sim)["C1:C2"]
        ...     print c1c2.outlet_head_loss
        >>> 0

        Setting the Value

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     c1c2 = Links(sim)["C1:C2"]
        ...     print c1c2.outlet_head_loss
        ...     c1c2.outlet_head_loss = 0.2
        ...     print c1c2.outlet_head_loss
        >>> 0
        >>> 0.2            
        """
        return self._model.getLinkParam(self._linkid,LinkParams.cLossOutlet)
    
    @outlet_head_loss.setter
    def outlet_head_loss(self, param):
        """Set Link Outlet Head Loss"""  
        self._model.setLinkParam(self._linkid,LinkParams.cLossOutlet, param)
    
    @property
    def average_head_loss(self):
        """
        Get/set Average Conduit Loss

        :return: Paramater Value
        :rtype: float

        Examples:

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     c1c2 = Links(sim)["C1:C2"]
        ...     print c1c2.average_head_loss
        >>> 0

        Setting the value

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     c1c2 = Links(sim)["C1:C2"]
        ...     print c1c2.average_head_loss
        ...     c1c2.average_head_loss = 0.2
        ...     print c1c2.average_head_loss
        >>> 0
        >>> 0.2           
        """
        return self._model.getLinkParam(self._linkid,LinkParams.cLossAvg)

    @average_head_loss.setter
    def average_head_loss(self, param):
        """Set Link Average Head Loss"""  
        self._model.setLinkParam(self._linkid,LinkParams.cLossAvg, param)
    
    @property
    def seepagerate(self):
        """
        Get/set Conduit Seepage Loss

        :return: Paramater Value
        :rtype: float

        Examples:

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     c1c2 = Links(sim)["C1:C2"]
        ...     print c1c2.seepagerate
        >>> 0

        Setting the Value

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     c1c2 = Links(sim)["C1:C2"]
        ...     print c1c2.seepagerate
        ...     c1c2.seepagerate = 0.2
        ...     print c1c2.seepagerate
        >>> 0
        >>> 0.2          
        """
        return self._model.getLinkParam(self._linkid,LinkParams.seepRate)

    @seepagerate.setter
    def seepagerate(self, param):
        """Set Link Average Seepage Loss"""  
        self._model.setLinkParam(self._linkid,LinkParams.seepRate, param)
        
    @property
    def flow(self):
        """
        Get Link Results for Flow. If Simulation is not running
        this method will raise a warning and return 0. 

        :return: Paramater Value
        :rtype: float
        
        Examples:

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     c1c2 = Links(sim)["C1:C2"]
        ...     for step in sim:
        ...         print c1c2.flow
        >>> 0
        >>> 1.2
        >>> 1.5
        >>> 1.9
        >>> 1.2
        """  
        return self._model.getLinkResult(self._linkid,LinkResults.newFlow)
    
    @property
    def depth(self):
        """
        Get Link Results for Depth. If Simulation is not running
        this method will raise a warning and return 0. 

        :return: Paramater Value
        :rtype: float
        
        Examples:

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     c1c2 = Links(sim)["C1:C2"]
        ...     for step in sim:
        ...         print c1c2.depth
        >>> 0
        >>> 1.2
        >>> 1.5
        >>> 1.9
        >>> 1.2
        """  
        return self._model.getLinkResult(self._linkid,LinkResults.newDepth)
    
    @property
    def volume(self):
        """
        Get Link Results for Volume. If Simulation is not running
        this method will raise a warning and return 0. 

        :return: Paramater Value
        :rtype: float
        
        Examples:

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     c1c2 = Links(sim)["C1:C2"]
        ...     for step in sim:
        ...         print c1c2.volume
        >>> 0
        >>> 1.2
        >>> 1.5
        >>> 1.9
        >>> 1.2
        """  
        return self._model.getLinkResult(self._linkid,LinkResults.newVolume)

    @property
    def froude(self):
        """
        Get Link Results for Froude. If Simulation is not running
        this method will raise a warning and return 0. 

        :return: Paramater Value
        :rtype: float
        
        Examples:

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     c1c2 = Links(sim)["C1:C2"]
        ...     for step in sim:
        ...         print c1c2.froude
        >>> 0
        >>> 1.2
        >>> 1.5
        >>> 1.9
        >>> 1.2
        """  
        return self._model.getLinkResult(self._linkid,LinkResults.froude)
    
    @property
    def ups_xsection_area(self):
        """
        Get Link Results for Upstream X-section Flow Area. If Simulation is not running
        this method will raise a warning and return 0. 

        :return: Paramater Value
        :rtype: float
        
        Examples:

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     c1c2 = Links(sim)["C1:C2"]
        ...     for step in sim:
        ...         print c1c2.ups_xsection_area
        >>> 0
        >>> 1.2
        >>> 1.5
        >>> 1.9
        >>> 1.2
        """  
        return self._model.getLinkResult(self._linkid,LinkResults.surfArea1)
    
    @property
    def ds_xsection_area(self):
        """
        Get Link Results for Downstream X-section Flow Area. If Simulation is not running
        this method will raise a warning and return 0. 

        :return: Paramater Value
        :rtype: float
        
        Examples:

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     c1c2 = Links(sim)["C1:C2"]
        ...     for step in sim:
        ...         print c1c2.ds_xsection_area
        >>> 0
        >>> 1.2
        >>> 1.5
        >>> 1.9
        >>> 1.2
        """  
        return self._model.getLinkResult(self._linkid,LinkResults.surfArea2)
    
    @property
    def current_setting(self):
        """
        Get Link current setting. If Simulation is not running
        this method will raise a warning and return 0. 

        :return: Paramater Value
        :rtype: float
        
        Examples:

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     c1c2 = Links(sim)["C1:C2"]
        ...     for step in sim:
        ...         print c1c2.current_setting
        >>> 0
        >>> 1
        >>> 0
        >>> 0.5
        >>> 1
        """  
        return self._model.getLinkResult(self._linkid,LinkResults.setting)
    
    @property
    def target_setting(self):
        """
        Get/set Link Target Setting. If Simulation is not running
        this method will raise a warning and return 0. 

        :return: Paramater Value
        :rtype: float
        
        Examples:

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     c1c2 = Links(sim)["C1:C2"]
        ...     for step in sim:
        ...         print c1c2.target_setting
        >>> 0
        >>> 0
        >>> 1
        >>> 0.5
        >>> 1

        Setting the Value

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     c1c2 = Links(sim)["C1:C2"]
        ...     for step in sim:
        ...         print c1c2.target_setting
        ...         if c1c2.flow > 3:
        ...             c1c2.target_setting = 0.1
        >>> 0
        >>> 0
        >>> 0.1
        >>> 0.1
        >>> 0.1        
        """  
        return self._model.getLinkResult(self._linkid,LinkResults.targetSetting)

    @target_setting.setter
    def target_setting(self, setting):
        """
        Set Link Target Setting. If Simulation is not running
        this method will raise a warning and return 0.
        """  
        return self._model.setLinkSetting(self._linkid, setting)
    

