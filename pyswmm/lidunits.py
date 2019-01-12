from pyswmm.toolkitapi import LidLayers, LidResults

def _flux_rate(model, subcatchment, lid_index, layer):
    """
    Get lid net inflow - outflow from previous time step for each lid layer
    ONLY FOR for surface, soil, storage, pave 
    :param int layerIndex: layer type (toolkitapi.LidLayers member variable)
    :return: Parameter Value
    :rtype: double
    """
    return model.getLidUFluxRates(subcatchment,
                                  lid_index,
                                  layer)
    
class Surface(object):
    def __init__(self, model, lidunit):
        self._model = model
        self._lidunit = lidunit
        self._subcatchmentid = lidunit._subcatchmentid
        self._lidid = lidunit._lidid

    @property
    def depth(self):
        """
        Get lid depth of ponded water on surface layer

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidUResult(self._subcatchmentid,
                                         self._lidid,
                                         LidResults.surfDepth.value)
    @property
    def inflow(self):
        """
        Get lid precip. + runon to LID unit

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidUResult(self._subcatchmentid,
                                         self._lidid,
                                         LidResults.surfInflow.value)
    @property
    def infiltration(self):
        """
        Get lid infiltration rate from surface layer

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidUResult(self._subcatchmentid,
                                         self._lidid,
                                         LidResults.surfInfil.value)
    @property
    def evporation(self):
        """
        Get lid evaporation rate from surface layer

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidUResult(self._subcatchmentid,
                                         self._lidid,
                                         LidResults.surfEvap.value)
    @property
    def outflow(self):
        """
        Get lid outflow from surface layer

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidUResult(self._subcatchmentid,
                                         self._lidid,
                                         LidResults.surfOutflow.value)
    @property
    def flux_rate(self):
        """
        Get lid flux rate from surface layer

        :return: Parameter Value
        :rtype: double
        """
        return _flux_rate(self._model,
                          self._subcatchmentid,
                          self._lidid,
                          LidLayers.surface.value)

    
class Pavement(object):
    def __init__(self, model, lidunit):
        self._model = model
        self._lidunit = lidunit
        self._subcatchmentid = lidunit._subcatchmentid
        self._lidid = lidunit._lidid

    @property
    def depth(self):
        """
        Get lid depth of water in poroous pavement layer

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidUResult(self._subcatchmentid,
                                         self._lidid,
                                         LidResults.paveDepth.value)
    @property
    def evaporation(self):
        """
        Get lid evaporation from pavement layer

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidUResult(self._subcatchmentid,
                                         self._lidid,
                                         LidResults.paveEvap.value)
    @property
    def percolation(self):
        """
        Get lid percolation from pavement layer

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidUResult(self._subcatchmentid,
                                         self._lidid,
                                         LidResults.pavePerc.value)
    @property
    def flux_rate(self):
        """
        Get lid flux rate from pavement layer

        :return: Parameter Value
        :rtype: double
        """
        return _flux_rate(self._model,
                          self._subcatchmentid,
                          self._lidid,
                          LidLayers.pavement.value)
            
    
class Storage(object):
    def __init__(self, model, lidunit):
        self._model = model
        self._lidunit = lidunit
        self._subcatchmentid = lidunit._subcatchmentid
        self._lidid = lidunit._lidid

    @property
    def depth(self):
        """
        Get lid depth of water in storage layer

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidUResult(self._subcatchmentid,
                                         self._lidid,
                                         LidResults.storDepth.value)
    @property
    def inflow(self):
        """
        Get lid inflow rate to storage rate

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidUResult(self._subcatchmentid,
                                         self._lidid,
                                         LidResults.storInflow.value)
    @property
    def exfiltration(self):
        """
        Get lid exfiltration rate from storage layer

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidUResult(self._subcatchmentid,
                                         self._lidid,
                                         LidResults.storExfil.value)
    @property
    def evporation(self):
        """
        Get lid evaporation rate from storage layer

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidUResult(self._subcatchmentid,
                                         self._lidid,
                                         LidResults.storEvap.value)
    @property
    def drain(self):
        """
        Get lid drain rate from storage layer

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidUResult(self._subcatchmentid,
                                         self._lidid,
                                         LidResults.storDrain.value)
    @property
    def flux_rate(self):
        """
        Get lid flux rate from storage layer

        :return: Parameter Value
        :rtype: double
        """
        return _flux_rate(self._model,
                          self._subcatchmentid,
                          self._lidid,
                          LidLayers.storage.value)

            
class Soil(object):
    def __init__(self, model, lidunit):
        self._model = model
        self._lidunit = lidunit
        self._subcatchmentid = lidunit._subcatchmentid
        self._lidid = lidunit._lidid

    @property
    def moisture(self):
        """
        Get lid moisture content of biocell soil layer

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidUResult(self._subcatchmentid,
                                         self._lidid,
                                         LidResults.soilMoist.value)
    @property
    def evaporation(self):
        """
        Get lid evaporation from soil layer

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidUResult(self._subcatchmentid,
                                         self._lidid,
                                         LidResults.soilEvap.value)
    @property
    def percolation(self):
        """
        Get lid percolation from soil layer

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidUResult(self._subcatchmentid,
                                         self._lidid,
                                         LidResults.soilPerc.value)
    @property
    def flux_rate(self):
        """
        Get lid flux rate from soil layer

        :return: Parameter Value
        :rtype: double
        """
        return _flux_rate(self._model,
                          self._subcatchmentid,
                          self._lidid,
                          LidLayers.soil.value)

    
class WaterBalance(object):
    def __init__(self, model, lidunit):
        self._model = model
        self._lidunit = lidunit
        self._subcatchmentid = lidunit._subcatchmentid
        self._lidid = lidunit._lidid
        
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
    def evaporation(self):
        """
        Get lid water balance total evaporation

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidUResult(self._subcatchmentid,
                                         self._lidid,
                                         LidResults.evap.value)
    @property
    def infiltration(self):
        """
        Get lid water balance total infiltration

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidUResult(self._subcatchmentid,
                                         self._lidid,
                                         LidResults.infil.value)
    @property
    def surface_flow(self):
        """
        Get lid water balance total surface runoff

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidUResult(self._subcatchmentid,
                                         self._lidid,
                                         LidResults.surfFlow.value)
    @property
    def drain_flow(self):
        """
        Get lid water balance total underdrain flow

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidUResult(self._subcatchmentid,
                                         self._lidid,
                                         LidResults.drainFlow.value)

    @property
    def initial_volume(self):
        """
        Get lid water balance initial stored volume

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidUResult(self._subcatchmentid,
                                         self._lidid,
                                         LidResults.initVol.value)
    @property
    def final_volume(self):
        """
        Get lid water balance final stored volume 

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidUResult(self._subcatchmentid,
                                         self._lidid,
                                         LidResults.finalVol.value)
