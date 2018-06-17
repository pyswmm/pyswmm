  # Local imports
from pyswmm.swmm5 import PYSWMMException
from pyswmm.toolkitapi import ObjectType, LidUParams, LidUOptions, LidResults

class LidGroups(object):
    """
    LidGroups Iterator Methods.

    :param object model: Open Model Instance
    """

    def __init__(self, model):
        if not model._model.fileLoaded:
            raise PYSWMMException("SWMM Model Not Open")
        self._model = model._model
        self._cuindex = 0
        self._nLidGroups = self._model.getProjectSize(ObjectType.SUBCATCH.value)

    def __len__(self):
        """
        Return number of defined LidGroups.
        Note that there are one lidgroup per subcatchment
        Use the expression 'len(LidGroups)'.

        :return: Number of LidGroups
        :rtype: int

        """
        return self._model.getProjectSize(ObjectType.SUBCATCH.value)

    def __contains__(self, subcatchmentid):
        """
        Checks if Subcatchment ID exists.

        :return: ID Exists
        :rtype: bool
        """
        return self._model.ObjectIDexist(ObjectType.SUBCATCH.value, subcatchmentid)

    def __getitem__(self, subcatchmentid):
        if self.__contains__(subcatchmentid):
            return LidGroup(self._model, subcatchmentid)
        else:
            raise PYSWMMException("Subcatchment ID Does not Exist")

    def __iter__(self):
        return self

    def __next__(self):
        if self._cuindex < self._nLidGroups:
            lidgroupobject = self.__getitem__(self._subcatchmentid)
            self._cuindex += 1  # Next Iteration
            return lidgroupobject
        else:
            raise StopIteration()

    next = __next__  # Python 2

    @property
    def _subcatchmentid(self):
        """Subcatchment ID."""
        return self._model.getObjectId(ObjectType.SUBCATCH.value, self._cuindex)


class LidGroup(object):
    def __init__(self, model, subcatchmentid):
        if not model.fileLoaded:
            raise PYSWMMException("SWMM Model Not Open")
        if subcatchmentid not in model.getObjectIDList(ObjectType.SUBCATCH.value):
            raise PYSWMMException("Subcatchment ID Does not Exist")
        self._model = model
        self._subcatchmentid = subcatchmentid
        self._cuindex = 0
        self._nLidUnits = model.getLidUCount(subcatchmentid)
        
    def __len__(self):
        """
        Return number of defined LidUnit per LidGroup.
        Note that there can be multiple LidUnit per subcatchment
        Use the expression 'len(LidGroup)'.

        :return: Number of LidUnit
        :rtype: int

        """
        return self._nLidUnits

    def __contains__(self, index):
        """
        Checks if Subcatchment ID exists.

        :return: ID Exists
        :rtype: bool
        """
        return index < self._nLidUnits

    def __getitem__(self, index):
        if self.__contains__(index):
            return LidUnit(self._model, self._subcatchmentid, index)
        else:
            raise PYSWMMException("Lid Unit Does Not Exist")

    def __iter__(self):
        return self

    def __next__(self):
        if self._cuindex < self._nLidUnits:
            lidunitobject = self.__getitem__(self._cuindex)
            self._cuindex += 1  # Next Iteration
            return lidunitobject
        else:
            raise StopIteration()

    next = __next__  # Python 2

    # --- Get Parameters
    # -------------------------------------------------------------------------
    @property
    def pervArea(self):
        """
        Get lid group amount of pervious area

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidGResult(self._subcatchmentid,
                                         LidResults.pervArea.value)
    @property
    def flowToPerv(self):
        """
        Get lid group total flow sent to pervious area

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidGResult(self._subcatchmentid,
                                         LidResults.flowToPerv.value)

    @property
    def oldDrainFlow(self):
        """
        Get lid group total drain flow in previous period

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidGResult(self._subcatchmentid,
                                         LidResults.oldDrainFlow.value)
    @property
    def newDrainFlow(self):
        """
        Get lid group total drain flow in current period

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidGResult(self._subcatchmentid,
                                         LidResults.newDrainFlow.value)
class LidUnit(object):
    """
    Lid Unit Methods.

    :param object model: Open Model Instance
    :param str subcatchmentid: Subcatchment ID
    :param str lidid: Lid unit ID
    
    """

    def __init__(self, model, subcatchmentid, lidid):
        if not model.fileLoaded:
            raise PYSWMMException("SWMM Model Not Open")
        # add an error for undefined lid unit
        
        self._model = model
        self._subcatchmentid = subcatchmentid
        self._lidid = lidid
        
    # --- Get Parameters
    # -------------------------------------------------------------------------
    @property
    def unitArea(self):
        """
        Get lid unit area.

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidUParam(self._subcatchmentid,
                                        self._lidid,
                                        LidUParams.unitArea.value)
    @unitArea.setter
    def unitArea(self, param):
        """Set lid unit area"""
        return self._model.setLidUParam(self._subcatchmentid,
                                        self._lidid,
                                        LidUParams.unitArea.value,
                                        param)
    @property
    def fullWidth(self):
        """
        Get lid unit full top width.

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidUParam(self._subcatchmentid,
                                        self._lidid,
                                        LidUParams.fullWidth.value)
    @fullWidth.setter
    def fullWidth(self, param):
        """Set lid unit full top width."""
        return self._model.setLidUParam(self._subcatchmentid,
                                        self._lidid,
                                        LidUParams.fullWidth.value,
                                        param)
    @property
    def botWidth(self):
        """
        Get lid unit bottom width.

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidUParam(self._subcatchmentid,
                                        self._lidid,
                                        LidUParams.botWidth.value)
    @botWidth.setter
    def botWidth(self, param):
        """Set lid unit bottom width."""
        return self._model.setLidUParam(self._subcatchmentid,
                                        self._lidid,
                                        LidUParams.botWidth.value,
                                        param)
    @property
    def initSat(self):
        """
        Get lid initial saturation of soil and storage layers.

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidUParam(self._subcatchmentid,
                                        self._lidid,
                                        LidUParams.initSat.value)
    @initSat.setter
    def initSat(self, param):
        """Set lid initial saturation of soil and storage layers."""
        return self._model.setLidUParam(self._subcatchmentid,
                                        self._lidid,
                                        LidUParams.initSat.value,
                                        param)
    @property
    def fromImperv(self):
        """
        Get lid fraction of impervious area runoff treated

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidUParam(self._subcatchmentid,
                                        self._lidid,
                                        LidUParams.fromImperv.value)
    @fromImperv.setter
    def fromImperv(self, param):
        """Set lid fraction of impervious area runoff treated"""
        return self._model.setLidUParam(self._subcatchmentid,
                                        self._lidid,
                                        LidUParams.fromImperv.value,
                                        param)
    @property
    def index(self):
        """
        Get lid control index 

        :return: Parameter Value
        :rtype: int
        """
        return self._model.getLidUOption(self._subcatchmentid,
                                         self._lidid,
                                         LidUOptions.index.value)
    @index.setter
    def index(self, param):
        """Set lid control index """
        if isinstance(param, str) and self._model.ObjectIDexist(ObjectType.LID.value, param):
            controlIndex = self._model.getObjectIDIndex(ObjectType.LID.value, param)    
        elif isinstance(param, int) and param >= 0 and param < self._model.getProjectSize(ObjectType.LID.value):
            controlIndex = param
        else:
            controlIndex = 0
            raise PYSWMMException("Invalid Input")

        return self._model.setLidUOption(self._subcatchmentid,
                                         self._lidid,
                                         LidUOptions.index.value,
                                         controlIndex)
    @property
    def number(self):
        """
        Get lid number of replicate units

        :return: Parameter Value
        :rtype: int
        """
        return self._model.getLidUOption(self._subcatchmentid,
                                         self._lidid,
                                         LidUOptions.number.value)
    @number.setter
    def number(self, param):
        """Set lid number of replicate units"""
        return self._model.setLidUOption(self._subcatchmentid,
                                         self._lidid,
                                         LidUOptions.number.value,
                                         param)
    @property
    def toPerv(self):
        """
        Get lid to pervious area (1 if outflow sent to pervious area)
                                 (0 if not)
                                 
        :return: Parameter Value
        :rtype: int
        """
        return self._model.getLidUOption(self._subcatchmentid,
                                         self._lidid,
                                         LidUOptions.toPerv.value)
    @toPerv.setter
    def toPerv(self, param):
        """
        Set lid to pervious area (1 if outflow sent to pervious area)
                                 (0 if not)
        """
        return self._model.setLidUOption(self._subcatchmentid,
                                         self._lidid,
                                         LidUOptions.toPerv.value,
                                         param)
    @property
    def drainSub(self):
        """
        Get lid drain to subcatchment index
        Negative if no recieving subcatchment

        :return: Parameter Value
        :rtype: int
        """
        return self._model.getLidUOption(self._subcatchmentid,
                                         self._lidid,
                                         LidUOptions.drainSub.value)
    @drainSub.setter
    def drainSub(self, param):
        """Set lid drain to subcatchment index"""
        if isinstance(param, str) and self._model.ObjectIDexist(ObjectType.SUBCATCH.value, param):
            subIndex = self._model.getObjectIDIndex(ObjectType.SUBCATCH.value, param)    
        elif isinstance(param, int) and param >= -1 and param < self._model.getProjectSize(ObjectType.SUBCATCH.value):
            subIndex = param
        else:
            subIndex = 0
            raise PYSWMMException("Invalid Input")

        self._model.setLidUOption(self._subcatchmentid,
                                  self._lidid,
                                  LidUOptions.drainSub.value,
                                  subIndex)
        self._model.setLidUOption(self._subcatchmentid,
                                  self._lidid,
                                  LidUOptions.drainNode.value,
                                  -1)
        
    @property
    def drainNode(self):
        """
        Get lid drain to node index
        Negative if no recieving node

        :return: Parameter Value
        :rtype: int
        """
        return self._model.getLidUOption(self._subcatchmentid,
                                         self._lidid,
                                         LidUOptions.drainNode.value)
    @drainNode.setter
    def drainNode(self, param):
        """Set lid drain to node index"""
        if isinstance(param, str) and self._model.ObjectIDexist(ObjectType.NODE.value, param):
            nodeIndex = self._model.getObjectIDIndex(ObjectType.NODE.value, param)    
        elif isinstance(param, int) and param >= -1 and param < self._model.getProjectSize(ObjectType.NODE.value):
            nodeIndex = param
        else:
            nodeIndex = 0
            raise PYSWMMException("Invalid Input")

        self._model.setLidUOption(self._subcatchmentid,
                                  self._lidid,
                                  LidUOptions.drainNode.value,
                                  nodeIndex)
        self._model.setLidUOption(self._subcatchmentid,
                                  self._lidid,
                                  LidUOptions.drainSub.value,
                                  -1)

        return 
    @property
    def inflow(self):
        """
        Get lid water balance total inflow 

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidUResult(self._subcatchmentid,
                                         self._lidid,
                                         LidResults.inflow.value)
    @property
    def evap(self):
        """
        Get lid water balance total evaporation

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidUResult(self._subcatchmentid,
                                         self._lidid,
                                         LidResults.evap.value)
    @property
    def infil(self):
        """
        Get lid water balance total infiltration

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidUResult(self._subcatchmentid,
                                         self._lidid,
                                         LidResults.infil.value)
    @property
    def surfFlow(self):
        """
        Get lid water balance total surface runoff

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidUResult(self._subcatchmentid,
                                         self._lidid,
                                         LidResults.surfFlow.value)
    @property
    def drainFlow(self):
        """
        Get lid water balance total underdrain flow

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidUResult(self._subcatchmentid,
                                         self._lidid,
                                         LidResults.drainFlow.value)
    @property
    def initVol(self):
        """
        Get lid water balance initial stored volume

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidUResult(self._subcatchmentid,
                                         self._lidid,
                                         LidResults.drainFlow.value)
    @property
    def finalVol(self):
        """
        Get lid water balance final stored volume 

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidUResult(self._subcatchmentid,
                                         self._lidid,
                                         LidResults.drainFlow.value)
    @property
    def surfDepth(self):
        """
        Get lid depth of ponded water on surface layer

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidUResult(self._subcatchmentid,
                                         self._lidid,
                                         LidResults.surfDepth.value)
    @property
    def paveDepth(self):
        """
        Get lid depth of water in poroous pavement layer

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidUResult(self._subcatchmentid,
                                         self._lidid,
                                         LidResults.paveDepth.value)
    @property
    def soilMoist(self):
        """
        Get lid moisture content of biocell soil layer

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidUResult(self._subcatchmentid,
                                         self._lidid,
                                         LidResults.soilMoist.value)
    @property
    def storDepth(self):
        """
        Get lid depth of water in storage layer

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidUResult(self._subcatchmentid,
                                         self._lidid,
                                         LidResults.storDepth.value)
    @property
    def dryTime(self):
        """
        Get lid time since last rainfall (sec)

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidUResult(self._subcatchmentid,
                                         self._lidid,
                                         LidResults.dryTime.value)
    @property
    def oldDrainFlow(self):
        """
        Get lid previous drain flow

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidUResult(self._subcatchmentid,
                                         self._lidid,
                                         LidResults.oldDrainFlow.value)
    @property
    def newDrainFlow(self):
        """
        Get lid current drain flow

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidUResult(self._subcatchmentid,
                                         self._lidid,
                                         LidResults.newDrainFlow.value)
    def fluxRate(self, layerIndex):
        """
        Get lid net inflow - outflow from previous time step for each lid layer
        ONLY FOR for surface, soil, storage, pave 
        :param int layerIndex: layer type (toolkitapi.LidLayers member variable)
        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidUFluxRates(self._subcatchmentid,
                                            self._lidid,
                                            layerIndex)
