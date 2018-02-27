# Local imports
from pyswmm.swmm5 import PYSWMMException
from pyswmm.toolkitapi import ObjectType, LidUParams, LidUOptions, LidUResults

class LidUnit(object):
    """
    Lid Unit Methods.

    :param object model: Open Model Instance
    :param str subcatchmentid: Subcatchment ID
    :param str lidid: Lid unit ID
    
    """

    def __init__(self, model, subcatchmentid, lidid):
        model = model._model
        
        if not model.fileLoaded:
            raise PYSWMMException("SWMM Model Not Open")
        if subcatchmentid not in model.getObjectIDList(ObjectType.SUBCATCH.value):
            raise PYSWMMException("Subcatchment ID not valid")
        # add an error for lid unit not found
        
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

    @property
    def inflow(self):
        """
        Get lid water balance total inflow 

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidUResult(self._subcatchmentid,
                                         self._lidid,
                                         LidUResults.inflow.value)

    @property
    def evap(self):
        """
        Get lid water balance total evaporation

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidUResult(self._subcatchmentid,
                                         self._lidid,
                                         LidUResults.evap.value)

    @property
    def infil(self):
        """
        Get lid water balance total infiltration

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidUResult(self._subcatchmentid,
                                         self._lidid,
                                         LidUResults.infil.value)

    @property
    def surfFlow(self):
        """
        Get lid water balance total surface runoff

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidUResult(self._subcatchmentid,
                                         self._lidid,
                                         LidUResults.surfFlow.value)

    @property
    def drainFlow(self):
        """
        Get lid water balance total underdrain flow

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidUResult(self._subcatchmentid,
                                         self._lidid,
                                         LidUResults.drainFlow.value)

    @property
    def initVol(self):
        """
        Get lid water balance initial stored volume

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidUResult(self._subcatchmentid,
                                         self._lidid,
                                         LidUResults.drainFlow.value)

    @property
    def finalVol(self):
        """
        Get lid water balance final stored volume 

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidUResult(self._subcatchmentid,
                                         self._lidid,
                                         LidUResults.drainFlow.value)
