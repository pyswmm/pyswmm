from toolkitapi import *
from swmm5 import SWMMException, PYSWMMException

__author__ = 'Bryant E. McDonnell (EmNet LLC) - bemcdonnell@gmail.com'
__copyright__ = 'Copyright (c) 2016 Bryant E. McDonnell'
__licence__ = 'BSD2'
__version__ = '0.2.1'

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
        return self._nLinks

    def __contains__(self, linkid):
        """Checks if Link ID exists

        :return: ID Exists
        :rtype: bool        
        """
        return self._model.ObjectIDexist(ObjectType.LINK, linkid)

    def __getitem__(self, linkid):
        if self.__contains__(linkid):
            return Link(self._model, linkid)
        
    def __iter__(self):
        return self
    
    def next(self):
        if self._cuindex < self._nLinks:
            linkobject = Link(self._model, self.linkid)
            self._cuindex+=1 #Next Iteration
            return linkobject
        else:
            raise StopIteration()        
    @property
    def linkid(self):
        "Link ID"
        return self._model.getObjectId(ObjectType.LINK,self._cuindex)
    
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
        ...     link = Links(sim)["C1:C2"]
        ...     print link.linkid
        >>> "C1"
        """
        return self._linkid
    
    @property
    def offset1(self):
        """
        Get Upstream Offset Depth

        :return: Paramater Value
        :rtype: float

        Examples:

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     link = Links(sim)["C1:C2"]
        ...     print link.offset1
        >>> 0.1
        """
        return self._model.getLinkParam(self._linkid,LinkParams.offset1)

    @offset1.setter
    def offset1(self, param):
        """
        Set Link Upstream Link Offset

        :param float param: New Parameter value
  
        Examples:

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     link = Links(sim)["C1:C2"]
        ...     print link.offset1
        ...     link.offset1 = 0.2
        ...     print link.offset1
        >>> 0.1
        >>> 0.2
        """  
        self._model.setLinkParam(self._linkid,LinkParams.offset1, param)
        
    @property
    def offset2(self):
        """
        Get Downstream Offset Depth

        :return: Paramater Value
        :rtype: float

        Examples:

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     link = Links(sim)["C1:C2"]
        ...     print link.offset2
        >>> 0.1
        """
        return self._model.getLinkParam(self._linkid,LinkParams.offset1)

    @offset2.setter
    def offset2(self, param):
        """
        Set Link Downstream Link Offset

        :param float param: New Parameter value
  
        Examples:

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     link = Links(sim)["C1:C2"]
        ...     print link.offset2
        ...     link.offset2 = 0.2
        ...     print link.offset2
        >>> 0.1
        >>> 0.2
        """  
        self._model.setLinkParam(self._linkid,LinkParams.offset2, param)
    
    @property
    def q0(self):
        """
        Get Link Initial Flow

        :return: Paramater Value
        :rtype: float

        Examples:

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     link = Links(sim)["C1:C2"]
        ...     print link.q0
        >>> 0
        """
        return self._model.getLinkParam(self._linkid,LinkParams.q0)

    @q0.setter    
    def q0(self, param):
        """
        Set Link Initial Flow Rate

        :param float param: New Parameter value
  
        Examples:

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     link = Links(sim)["C1:C2"]
        ...     print link.q0
        ...     link.offset1 = 0.2
        ...     print link.offset1
        >>> 0.1
        >>> 0.2
        """  
        self._model.setLinkParam(self._linkid,LinkParams.q0, param)
    
    @property
    def qlimit(self):
        """
        Get Downstream Offset Depth

        :return: Paramater Value
        :rtype: float

        Examples:

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     link = Links(sim)["C1:C2"]
        ...     print link.qlimit
        >>> 0
        """
        return self._model.getLinkParam(self._linkid,LinkParams.qLimit)

    @qlimit.setter
    def qlimit(self, param):
        """
        Set Link Flow Limit

        :param float param: New Parameter value
  
        Examples:
        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     link = Links(sim)["C1:C2"]
        ...     print link.qlimi
        ...     link.qlimi = 0.2
        ...     print link.qlimi
        >>> 0
        >>> 0.2
        
        """  
        self._model.setLinkParam(self._linkid,LinkParams.qLimit, param)
    
    @property
    def clossinlet(self):
        """
        Get Inlet Head Loss

        :return: Paramater Value
        :rtype: float

        Examples:

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     link = Links(sim)["C1:C2"]
        ...     print link.q0
        >>> 0
        """
        return self._model.getLinkParam(self._linkid,LinkParams.cLossInlet)

    @clossinlet.setter
    def clossinlet(self, param):
        """
        Set Link Inlet Head Loss

        :param float param: New Parameter value
  
        Examples:

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     link = Links(sim)["C1:C2"]
        ...     print link.cLossInlet
        ...     link.cLossInlet = 0.2
        ...     print link.cLossInlet
        >>> 0
        >>> 0.2        
        """  
        self._model.setLinkParam(self._linkid,LinkParams.cLossInlet, param)
    
    @property
    def clossoutlet(self):
        """
        Get Outlet Head Loss

        :return: Paramater Value
        :rtype: float

        Examples:

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     link = Links(sim)["C1:C2"]
        ...     print link.clossoutlet
        >>> 0
        """
        return self._model.getLinkParam(self._linkid,LinkParams.cLossOutlet)
    
    @clossoutlet.setter
    def clossoutlet(self, param):
        """
        Set Link Outlet Head Loss

        :param float param: New Parameter value
  
        Examples:

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     link = Links(sim)["C1:C2"]
        ...     print link.clossoutlet
        ...     link.clossoutlet = 0.2
        ...     print link.clossoutlet
        >>> 0
        >>> 0.2    
        """  
        self._model.setLinkParam(self._linkid,LinkParams.cLossOutlet, param)
    
    @property
    def clossave(self):
        """
        Get Average Conduit Loss

        :return: Paramater Value
        :rtype: float

        Examples:

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     link = Links(sim)["C1:C2"]
        ...     print link.clossave
        >>> 0
        """
        return self._model.getLinkParam(self._linkid,LinkParams.cLossAvg)

    @clossave.setter
    def clossave(self, param):
        """
        Set Link Average Head Loss

        :param float param: New Parameter value
  
        Examples:

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     link = Links(sim)["C1:C2"]
        ...     print link.clossave
        ...     link.clossave = 0.2
        ...     print link.clossave
        >>> 0
        >>> 0.2   
        """  
        self._model.setLinkParam(self._linkid,LinkParams.cLossAvg, param)
    
    @property
    def seepagerate(self):
        """
        Get Conduit Seepage Loss

        :return: Paramater Value
        :rtype: float

        Examples:

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     link = Links(sim)["C1:C2"]
        ...     print link.seepagerate
        >>> 0
        """
        return self._model.getLinkParam(self._linkid,LinkParams.seepRate)

    @seepagerate.setter
    def seepagerate(self, param):
        """
        Set Link Average Seepage Loss

        :param float param: New Parameter value
  
        Examples:

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     link = Links(sim)["C1:C2"]
        ...     print link.seepagerate
        ...     link.seepagerate = 0.2
        ...     print link.seepagerate
        >>> 0
        >>> 0.2  
        """  
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
        ...     link = Links(sim)["C1:C2"]
        ...     for step in sim:
        ...         print link.flow
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
        ...     link = Links(sim)["C1:C2"]
        ...     for step in sim:
        ...         print link.depth
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
        ...     link = Links(sim)["C1:C2"]
        ...     for step in sim:
        ...         print link.volume
        >>> 0
        >>> 1.2
        >>> 1.5
        >>> 1.9
        >>> 1.2
        """  
        return self._model.getLinkResult(self._linkid,LinkResults.newVolume)
    
    @property
    def usxsectionarea(self):
        """
        Get Link Results for Upstream X-section Flow Area. If Simulation is not running
        this method will raise a warning and return 0. 

        :return: Paramater Value
        :rtype: float
        
        Examples:

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     link = Links(sim)["C1:C2"]
        ...     for step in sim:
        ...         print link.usxsectionarea
        >>> 0
        >>> 1.2
        >>> 1.5
        >>> 1.9
        >>> 1.2
        """  
        return self._model.getLinkResult(self._linkid,LinkResults.surfArea1)
    
    @property
    def dsxsectionarea(self):
        """
        Get Link Results for Downstream X-section Flow Area. If Simulation is not running
        this method will raise a warning and return 0. 

        :return: Paramater Value
        :rtype: float
        
        Examples:

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     link = Links(sim)["C1:C2"]
        ...     for step in sim:
        ...         print link.dsxsectionarea
        >>> 0
        >>> 1.2
        >>> 1.5
        >>> 1.9
        >>> 1.2
        """  
        return self._model.getLinkResult(self._linkid,LinkResults.surfArea2)
    
    @property
    def currentsetting(self):
        """
        Get Link current setting. If Simulation is not running
        this method will raise a warning and return 0. 

        :return: Paramater Value
        :rtype: float
        
        Examples:

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     link = Links(sim)["C1:C2"]
        ...     for step in sim:
        ...         print link.currentsetting
        >>> 0
        >>> 1
        >>> 0
        >>> 0.5
        >>> 1
        """  
        return self._model.getLinkResult(self._linkid,LinkResults.setting)
    
    @property
    def targetsetting(self):
        """
        Get Link Target Setting. If Simulation is not running
        this method will raise a warning and return 0. 

        :return: Paramater Value
        :rtype: float
        
        Examples:

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     link = Links(sim)["C1:C2"]
        ...     for step in sim:
        ...         print link.targetsetting
        >>> 0
        >>> 0
        >>> 1
        >>> 0.5
        >>> 1
        """  
        return self._model.getLinkResult(self._linkid,LinkResults.targetSetting)

    @targetsetting.setter
    def targetsetting(self, setting):
        """
        Set Link Target Setting. If Simulation is not running
        this method will raise a warning and return 0. 

        :return: Paramater Value
        :rtype: float
        
        Examples:

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     link = Links(sim)["C1:C2"]
        ...     for step in sim:
        ...         print link.targetsetting
        ...         if link.flow > 3:
        ...             link.targetsetting = 0.1
        >>> 0
        >>> 0
        >>> 0.1
        >>> 0.1
        >>> 0.1
        """  
        return self._model.setLinkSetting(self._linkid, setting)
    
    @property
    def froude(self):
        """
        Get Link Target Setting. If Simulation is not running
        this method will raise a warning and return 0. 

        :return: Paramater Value
        :rtype: float
        
        Examples:

        >>> from pyswmm import Simulation
        >>>
        >>> with Simulation('../test/TestModel1_weirSetting.inp') as sim:
        ...     link = Links(sim)["C1:C2"]
        ...     for step in sim:
        ...         print link.froude
        >>> 0
        >>> 1.2
        >>> 1.5
        >>> 1.9
        >>> 1.2
        """  
        return self._model.getLinkResult(self._linkid,LinkResults.froude)
