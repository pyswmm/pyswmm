# Local imports
from pyswmm.swmm5 import PYSWMMException
from pyswmm.toolkitapi import ObjectType, LidLayers, LidLayersProperty

class LidControls(object):
    """
    Lid Control Iterator Methods.
    
    :param object model: Open Model Instance
    """
    
    def __init__(self, model):
        if not model._model.fileLoaded:
            raise PYSWMMException("SWMM Model Not Open")
        self._model = model._model
        self._cuindex = 0
        self._nlidcontrols = self._model.getProjectSize(ObjectType.LID.value)

    def __len__(self):
        """
        Return number of lid controls.

        Use the expression 'len(LidControls)'.

        :return: Number of Lid Controls
        :rtype: int

        """
        return self._model.getProjectSize(ObjectType.LID.value)

    def __contains__(self, lidcontrolid):
        """
        Checks if Lid Control ID exists.

        :return: ID Exists
        :rtype: bool
        """
        return self._model.ObjectIDexist(ObjectType.LID.value,
                                         lidcontrolid)

    def __getitem__(self, lidcontrolid):
        if self.__contains__(lidcontrolid):
            return LidControl(self._model, lidcontrolid)
        else:
            raise PYSWMMException("Lid Control ID Does not Exist")

    def __iter__(self):
        return self

    def __next__(self):
        if self._cuindex < self._nlidcontrols:
            lidcontrolobject = self.__getitem__(self._lidcontrolid)
            self._cuindex += 1  # Next Iteration
            return lidcontrolobject
        else:
            raise StopIteration()

    next = __next__  # Python 2

    @property
    def _lidcontrolid(self):
        """Lid Control ID."""
        return self._model.getObjectId(ObjectType.LID.value,
                                       self._cuindex)

class LidControl(object):
    def __init__(self, model, lidcontrolid):
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
    @surface_thickness.setter
    def surface_thickness(self, param):
        """Set lid control surface layer thickness"""
        return self._model.setLidCParam(self._lidcontrolid,
                                        LidLayers.surface.value,
                                        LidLayersProperty.thickness.value,
                                        param)      
        
    @property
    def surface_voidFrac(self):
        """
        Get lid control surface layer available fraction of storage volume

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidCParam(self._lidcontrolid,
                                        LidLayers.surface.value,
                                        LidLayersProperty.voidFrac.value)    
    @surface_voidFrac.setter
    def surface_voidFrac(self, param):
        """Set lid control surface layer available fraction of storage volume"""
        return self._model.setLidCParam(self._lidcontrolid,
                                        LidLayers.surface.value,
                                        LidLayersProperty.voidFrac.value,
                                        param)   
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
    @surface_roughness.setter
    def surface_roughness(self, param):
        """Set lid control surface layer surface Mannings n"""
        return self._model.setLidCParam(self._lidcontrolid,
                                        LidLayers.surface.value,
                                        LidLayersProperty.roughness.value,
                                        param)    
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
    @surface_surfSlope.setter
    def surface_surfSlope(self, param):
        """Set lid control surface layer land surface slope (fraction)"""
        return self._model.setLidCParam(self._lidcontrolid,
                                        LidLayers.surface.value,
                                        LidLayersProperty.surfSlope.value,
                                        param)
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
    @surface_sideSlope.setter
    def surface_sideSlope(self, param):
        """Set lid control surface layer swale side slope (run/rise)"""
        return self._model.setLidCParam(self._lidcontrolid,
                                        LidLayers.surface.value,
                                        LidLayersProperty.sideSlope.value,
                                        param)   
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
    @surface_alpha.setter
    def surface_alpha(self, param):
        """Set lid control surface layer swale side slope (run/rise)"""
        return self._model.setLidCParam(self._lidcontrolid,
                                        LidLayers.surface.value,
                                        LidLayersProperty.alpha.value,
                                        param)
    @property
    def surface_canOverflow(self):
        """
        Get lid control surface layer option for immediate outflow of excess water

        :return: Parameter Value
        :rtype: char
        """
        return self._model.getLidCOverflow(self._lidcontrolid)
    
    @surface_canOverflow.setter
    def surface_canOverflow(self, param):
        """Set lid control surface layer option for immediate outflow of excess water"""
        return self._model.setLidCOverflow(self._lidcontrolid, param)
    
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
    @soil_thickness.setter
    def soil_thickness(self, param):
        """Set lid control soil layer thickness """
        return self._model.setLidCParam(self._lidcontrolid,
                                        LidLayers.soil.value,
                                        LidLayersProperty.thickness.value,
                                        param)   
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
    @soil_porosity.setter
    def soil_porosity(self, param):
        """Set lid control soil layer void volume / total volume"""
        return self._model.setLidCParam(self._lidcontrolid,
                                        LidLayers.soil.value,
                                        LidLayersProperty.porosity.value,
                                        param)
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
    @soil_fieldCap.setter
    def soil_fieldCap(self, param):
        """Set lid control soil layer field capacity"""
        return self._model.setLidCParam(self._lidcontrolid,
                                        LidLayers.soil.value,
                                        LidLayersProperty.fieldCap.value,
                                        param)    
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
    @soil_wiltPoint.setter
    def soil_wiltPoint(self, param):
        """Set lid control soil layer wilting point"""
        return self._model.setLidCParam(self._lidcontrolid,
                                        LidLayers.soil.value,
                                        LidLayersProperty.wiltPoint.value,
                                        param)    
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
    @soil_suction.setter
    def soil_suction(self, param):
        """Set lid control soil layer suction head at wetting front"""
        return self._model.setLidCParam(self._lidcontrolid,
                                        LidLayers.soil.value,
                                        LidLayersProperty.suction.value,
                                        param)
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
    @soil_kSat.setter
    def soil_kSat(self, param):
        """Set lid control soil layer saturated hydraulic conductivity"""
        return self._model.setLidCParam(self._lidcontrolid,
                                        LidLayers.soil.value,
                                        LidLayersProperty.kSat.value,
                                        param)
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
    @soil_kSlope.setter
    def soil_kSlope(self, param):
        """Set lid control soil layer slope of log(k) v. moisture content curve"""
        return self._model.setLidCParam(self._lidcontrolid,
                                        LidLayers.soil.value,
                                        LidLayersProperty.kSlope.value,
                                        param)  
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
    @storage_thickness.setter
    def storage_thickness(self, param):
        """Set lid control storage layer thickness"""
        return self._model.setLidCParam(self._lidcontrolid,
                                        LidLayers.storage.value,
                                        LidLayersProperty.thickness.value,
                                        param)
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
    @storage_voidFrac.setter
    def storage_voidFrac(self, param):
        """Set lid control storage layer void volume / total volume"""
        return self._model.setLidCParam(self._lidcontrolid,
                                        LidLayers.storage.value,
                                        LidLayersProperty.voidFrac.value,
                                        param)
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
    @storage_kSat.setter
    def storage_kSat(self, param):
        """Set lid control storage layer saturated hydraulic conductivity"""
        return self._model.setLidCParam(self._lidcontrolid,
                                        LidLayers.storage.value,
                                        LidLayersProperty.kSat.value,
                                        param)
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
    @storage_clogFactor.setter
    def storage_clogFactor(self, param):
        """Set lid control storage layer clogging factor"""
        return self._model.setLidCParam(self._lidcontrolid,
                                        LidLayers.storage.value,
                                        LidLayersProperty.clogFactor.value,
                                        param)
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
    @pavement_thickness.setter
    def pavement_thickness(self, param):
        """Get lid control pavement layer thickness"""
        return self._model.setLidCParam(self._lidcontrolid,
                                        LidLayers.pavement.value,
                                        LidLayersProperty.thickness.value,
                                        param)
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
    @pavement_voidFrac.setter
    def pavement_voidFrac(self, param):
        """Set lid control pavement layer void volume / total volume"""
        return self._model.setLidCParam(self._lidcontrolid,
                                        LidLayers.pavement.value,
                                        LidLayersProperty.voidFrac.value,
                                        param)
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
    @pavement_impervFrac.setter
    def pavement_impervFrac(self, param):
        """Set lid control pavement layer impervious area fraction"""
        return self._model.setLidCParam(self._lidcontrolid,
                                        LidLayers.pavement.value,
                                        LidLayersProperty.impervFrac.value,
                                        param)
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
    @pavement_kSat.setter
    def pavement_kSat(self, param):
        """Get lid control pavement layer permeability """
        return self._model.setLidCParam(self._lidcontrolid,
                                        LidLayers.pavement.value,
                                        LidLayersProperty.kSat.value,
                                        param)
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
    @pavement_clogFactor.setter
    def pavement_clogFactor(self, param):
        """Get lid control pavement layer clogging factor"""
        return self._model.setLidCParam(self._lidcontrolid,
                                        LidLayers.pavement.value,
                                        LidLayersProperty.clogFactor.value,
                                        param)
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
    @drain_coeff.setter
    def drain_coeff(self, param):
        """Set lid control drain layer underdrain flow coefficient"""
        return self._model.setLidCParam(self._lidcontrolid,
                                        LidLayers.drain.value,
                                        LidLayersProperty.coeff.value,
                                        param)
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
    @drain_expon.setter
    def drain_expon(self, param):
        """Set lid control drain layer underdrain head exponent"""
        return self._model.setLidCParam(self._lidcontrolid,
                                        LidLayers.drain.value,
                                        LidLayersProperty.expon.value,
                                        param)
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
    @drain_offset.setter
    def drain_offset(self, param):
        """Set lid control drain layer offset height of underdrain"""
        return self._model.setLidCParam(self._lidcontrolid,
                                        LidLayers.drain.value,
                                        LidLayersProperty.offset.value,
                                        param)
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
    @drain_delay.setter
    def drain_delay(self, param):
        """Set lid control drain layer rain barrel drain delay time (sec)"""
        return self._model.setLidCParam(self._lidcontrolid,
                                        LidLayers.drain.value,
                                        LidLayersProperty.delay.value,
                                        param)
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
    @drainmat_thickness.setter
    def drainmat_thickness(self, param):
        """Set lid control drainmat layer thickness"""
        return self._model.setLidCParam(self._lidcontrolid,
                                        LidLayers.drainMat.value,
                                        LidLayersProperty.thickness.value,
                                        param)
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
    @drainmat_voidFrac.setter
    def drainmat_voidFrac(self, param):
        """Set lid control drainmat layer void volume / total volume"""
        return self._model.setLidCParam(self._lidcontrolid,
                                        LidLayers.drainMat.value,
                                        LidLayersProperty.voidFrac.value,
                                        param)
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
    @drainmat_roughness.setter
    def drainmat_roughness(self, param):
        """Set lid control drainmat layer Mannings n for green roof drainage mats"""
        return self._model.setLidCParam(self._lidcontrolid,
                                        LidLayers.drainMat.value,
                                        LidLayersProperty.roughness.value,
                                        param)
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
    @drainmat_alpha.setter
    def drainmat_alpha(self, param):
        """Set lid control drainmat layer slope/roughness term in Manning equation"""
        return self._model.setLidCParam(self._lidcontrolid,
                                        LidLayers.drainMat.value,
                                        LidLayersProperty.alpha.value,
                                        param)
