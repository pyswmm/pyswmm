# Local imports
from pyswmm.swmm5 import PYSWMMException
from pyswmm.toolkitapi import ObjectType, LidUParams, LidUOptions, LidUResults, LidLayers, LidLayersProperty

##class LidControls(object):
##    """
##    Lid Control Methods.
##    
##    :param object model: Open Model Instance
##    :param str controlid: lid control ID
##    """
##    
##    def __init__(self, model):
##        if not model._model.fileLoaded:
##            raise PYSWMMException("SWMM Model Not Open")
##        self._model = model._model
##        self._cuindex = 0
##        self._nlidcontrols = self._model.getProjectSize(ObjectType.LID.value)
##
##    def __len__(self):
##        """
##        Return number of subcatchments.
##
##        Use the expression 'len(Subcatchments)'.
##
##        :return: Number of Subcatchments
##        :rtype: int
##
##        """
##        return self._model.getProjectSize(ObjectType.LID.value)
##
##    def __contains__(self, lidcontrolid):
##        """
##        Checks if Subcatchment ID exists.
##
##        :return: ID Exists
##        :rtype: bool
##        """
##        return self._model.ObjectIDexist(ObjectType.LID.value,
##                                         lidcontrolid)
##
##    def __getitem__(self, lidcontrolid):
##        if self.__contains__(lidcontrolid):
##            return LidControl(self._model, lidcontrolid)
##        else:
##            raise PYSWMMException("Subcatchment ID Does not Exist")
##
##    def __iter__(self):
##        return self
##
##    def __next__(self):
##        if self._cuindex < self._nlidcontrols:
##            lidcontrolobject = self.__getitem__(self._lidcontrolid)
##            self._cuindex += 1  # Next Iteration
##            return lidcontrolobject
##        else:
##            raise StopIteration()
##
##    next = __next__  # Python 2
##
##    @property
##    def _lidcontrolid(self):
##        """Subcatchment ID."""
##        return self._model.getObjectId(ObjectType.LID.value,
##                                       self._cuindex)

class LidControl(object):
    def __init__(self, model, lidcontrolid):
        model = model._model
        if not model.fileLoaded:
            raise PYSWMMException("SWMM Model Not Open")
        if lidcontrolid not in model.getObjectIDList(ObjectType.LID.value):
            raise PYSWMMException("ID Not valid")
        self._model = model
        self._lidcontrolid = lidcontrolid

    # --- Get Parameters
    # -------------------------------------------------------------------------
    @property
    def surface_thickness(self):
        """
        Get lid control surface layer thickness

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidCParam(self._lidcontrolid,
                                        LidLayers.surface.value,
                                        LidLayersProperty.thickness.value)
    @property
    def surface_voidFrac(self):
        """
        Get lid control surface layer avilable fraction of storage volume

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidCParam(self._lidcontrolid,
                                        LidLayers.surface.value,
                                        LidLayersProperty.voidFrac.value)    
    @property
    def surface_roughness(self):
        """
        Get lid control surface layer surface Mannings n

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidCParam(self._lidcontrolid,
                                        LidLayers.surface.value,
                                        LidLayersProperty.roughness.value)    
    @property
    def surface_surfSlope(self):
        """
        Get lid control surface layer land surface slope (fraction)

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidCParam(self._lidcontrolid,
                                        LidLayers.surface.value,
                                        LidLayersProperty.surfSlope.value)
    @property
    def surface_sideSlope(self):
        """
        Get lid control surface layer swale side slope (run/rise)

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidCParam(self._lidcontrolid,
                                        LidLayers.surface.value,
                                        LidLayersProperty.sideSlope.value)    
    @property
    def surface_alpha(self):
        """
        Get lid control surface layer swale side slope (run/rise)

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidCParam(self._lidcontrolid,
                                        LidLayers.surface.value,
                                        LidLayersProperty.alpha.value)    

    @property
    def soil_thickness(self):
        """
        Get lid control soil layer thickness

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidCParam(self._lidcontrolid,
                                        LidLayers.soil.value,
                                        LidLayersProperty.thickness.value)    
    @property
    def soil_porosity(self):
        """
        Get lid control soil layer void volume / total volume

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidCParam(self._lidcontrolid,
                                        LidLayers.soil.value,
                                        LidLayersProperty.porosity.value)
    @property
    def soil_fieldCap(self):
        """
        Get lid control soil layer field capacity

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidCParam(self._lidcontrolid,
                                        LidLayers.soil.value,
                                        LidLayersProperty.fieldCap.value)    
    @property
    def soil_wiltPoint(self):
        """
        Get lid control soil layer wilting point

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidCParam(self._lidcontrolid,
                                        LidLayers.soil.value,
                                        LidLayersProperty.wiltPoint.value)    
    @property
    def soil_suction(self):
        """
        Get lid control soil layer suction head at wetting front

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidCParam(self._lidcontrolid,
                                        LidLayers.soil.value,
                                        LidLayersProperty.suction.value)
    @property
    def soil_kSat(self):
        """
        Get lid control soil layer saturated hydraulic conductivity

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidCParam(self._lidcontrolid,
                                        LidLayers.soil.value,
                                        LidLayersProperty.kSat.value)
    @property
    def soil_kSlope(self):
        """
        Get lid control soil layer slope of log(k) v. moisture content curve

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidCParam(self._lidcontrolid,
                                        LidLayers.soil.value,
                                        LidLayersProperty.kSlope.value)  
    @property
    def storage_thickness(self):
        """
        Get lid control storage layer thickness

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidCParam(self._lidcontrolid,
                                        LidLayers.storage.value,
                                        LidLayersProperty.thickness.value)
    @property
    def storage_voidFrac(self):
        """
        Get lid control storage layer void volume / total volume

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidCParam(self._lidcontrolid,
                                        LidLayers.storage.value,
                                        LidLayersProperty.voidFrac.value)
    @property
    def storage_kSat(self):
        """
        Get lid control storage layer saturated hydraulic conductivity

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidCParam(self._lidcontrolid,
                                        LidLayers.storage.value,
                                        LidLayersProperty.kSat.value)
    @property
    def storage_clogFactor(self):
        """
        Get lid control storage layer clogging factor

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidCParam(self._lidcontrolid,
                                        LidLayers.storage.value,
                                        LidLayersProperty.clogFactor.value)
    @property
    def pavement_thickness(self):
        """
        Get lid control pavement layer thickness

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidCParam(self._lidcontrolid,
                                        LidLayers.pavement.value,
                                        LidLayersProperty.thickness.value)
    @property
    def pavement_voidFrac(self):
        """
        Get lid control pavement layer void volume / total volume

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidCParam(self._lidcontrolid,
                                        LidLayers.pavement.value,
                                        LidLayersProperty.voidFrac.value)
    @property
    def pavement_impervFrac(self):
        """
        Get lid control pavement layer impervious area fraction

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidCParam(self._lidcontrolid,
                                        LidLayers.pavement.value,
                                        LidLayersProperty.impervFrac.value)
    @property
    def pavement_kSat(self):
        """
        Get lid control pavement layer permeability 

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidCParam(self._lidcontrolid,
                                        LidLayers.pavement.value,
                                        LidLayersProperty.kSat.value)
    @property
    def pavement_clogFactor(self):
        """
        Get lid control pavement layer clogging factor

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidCParam(self._lidcontrolid,
                                        LidLayers.pavement.value,
                                        LidLayersProperty.clogFactor.value)
    @property
    def drain_coeff(self):
        """
        Get lid control drain layer underdrain flow coefficient

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidCParam(self._lidcontrolid,
                                        LidLayers.drain.value,
                                        LidLayersProperty.coeff.value)
    @property
    def drain_expon(self):
        """
        Get lid control drain layer underdrain head exponent

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidCParam(self._lidcontrolid,
                                        LidLayers.drain.value,
                                        LidLayersProperty.expon.value)
    @property
    def drain_offset(self):
        """
        Get lid control drain layer offset height of underdrain

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidCParam(self._lidcontrolid,
                                        LidLayers.drain.value,
                                        LidLayersProperty.offset.value)
    @property
    def drain_delay(self):
        """
        Get lid control drain layer rain barrel drain delay time (sec)

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidCParam(self._lidcontrolid,
                                        LidLayers.drain.value,
                                        LidLayersProperty.delay.value)
    @property
    def drainmat_thickness(self):
        """
        Get lid control drainmat layer thickness

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidCParam(self._lidcontrolid,
                                        LidLayers.drainMat.value,
                                        LidLayersProperty.thickness.value)
    @property
    def drainmat_voidFrac(self):
        """
        Get lid control drainmat layer void volume / total volume

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidCParam(self._lidcontrolid,
                                        LidLayers.drainMat.value,
                                        LidLayersProperty.voidFrac.value)
    @property
    def drainmat_roughness(self):
        """
        Get lid control drainmat layer Mannings n for green roof drainage mats

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidCParam(self._lidcontrolid,
                                        LidLayers.drainMat.value,
                                        LidLayersProperty.roughness.value)
    @property
    def drainmat_alpha(self):
        """
        Get lid control drainmat layer slope/roughness term in Manning equation

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidCParam(self._lidcontrolid,
                                        LidLayers.drainMat.value,
                                        LidLayersProperty.alpha.value)
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
    @property
    def surfDepth(self):
        """
        Get lid depth of ponded water on surface layer

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidUResult(self._subcatchmentid,
                                         self._lidid,
                                         LidUResults.surfDepth.value)
    @property
    def paveDepth(self):
        """
        Get lid depth of water in poroous pavement layer

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidUResult(self._subcatchmentid,
                                         self._lidid,
                                         LidUResults.paveDepth.value)
    @property
    def soilMoist(self):
        """
        Get lid moisture content of biocell soil layer

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidUResult(self._subcatchmentid,
                                         self._lidid,
                                         LidUResults.soilMoist.value)
    @property
    def storDepth(self):
        """
        Get lid depth of water in storage layer

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidUResult(self._subcatchmentid,
                                         self._lidid,
                                         LidUResults.storDepth.value)
    @property
    def dryTime(self):
        """
        Get lid time since last rainfall (sec)

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidUResult(self._subcatchmentid,
                                         self._lidid,
                                         LidUResults.dryTime.value)
    @property
    def oldDrainFlow(self):
        """
        Get lid previous drain flow

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidUResult(self._subcatchmentid,
                                         self._lidid,
                                         LidUResults.oldDrainFlow.value)
    @property
    def newDrainFlow(self):
        """
        Get lid current drain flow

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidUResult(self._subcatchmentid,
                                         self._lidid,
                                         LidUResults.newDrainFlow.value)
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
