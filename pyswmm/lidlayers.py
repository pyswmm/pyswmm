# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2018 Jennifer Wu
#
# Licensed under the terms of the BSD2 License
# See LICENSE.txt for details
# -----------------------------------------------------------------------------
from pyswmm.toolkitapi import LidLayers, LidLayersProperty


class Surface(object):
    """
    Methods and properties of the surface layer associated with an LID 

    +--------------------+--------------------+--------------------+--------------------+
    | Layer              | Parameter          | Setter Before Sim  | Setter During Sim  |
    +====================+====================+====================+====================+
    | Surface            | thickness          | enabled            | disabled           |
    +--------------------+--------------------+--------------------+--------------------+
    | Surface            | void_fraction      | enabled            | disabled           |
    +--------------------+--------------------+--------------------+--------------------+
    | Surface            | roughness          | enabled            | enabled            |
    +--------------------+--------------------+--------------------+--------------------+
    | Surface            | slope              | enabled            | disabled           |
    +--------------------+--------------------+--------------------+--------------------+
    | Surface            | side_slope         | enabled            | disabled           |
    +--------------------+--------------------+--------------------+--------------------+
    | Surface            | alpha              | enabled            | disabled           |
    +--------------------+--------------------+--------------------+--------------------+
    """

    def __init__(self, model, lidcontrol):
        self._model = model
        self._lidcontrol = lidcontrol
        self._lidcontrolid = lidcontrol._lidcontrolid

    @property
    def thickness(self):
        """
        Get lid control surface layer thickness

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidCParam(self._lidcontrolid,
                                        LidLayers.surface.value,
                                        LidLayersProperty.thickness.value)

    @thickness.setter
    def thickness(self, param):
        """Set lid control surface layer thickness"""
        return self._model.setLidCParam(self._lidcontrolid,
                                        LidLayers.surface.value,
                                        LidLayersProperty.thickness.value,
                                        param)

    @property
    def void_fraction(self):
        """
        Get lid control surface layer available fraction of storage volume

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidCParam(self._lidcontrolid,
                                        LidLayers.surface.value,
                                        LidLayersProperty.voidFrac.value)

    @void_fraction.setter
    def void_fraction(self, param):
        """Set lid control surface layer available fraction of storage volume"""
        return self._model.setLidCParam(self._lidcontrolid,
                                        LidLayers.surface.value,
                                        LidLayersProperty.voidFrac.value,
                                        param)

    @property
    def roughness(self):
        """
        Get lid control surface layer surface Mannings n

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidCParam(self._lidcontrolid,
                                        LidLayers.surface.value,
                                        LidLayersProperty.roughness.value)

    @roughness.setter
    def roughness(self, param):
        """Set lid control surface layer surface Mannings n"""
        return self._model.setLidCParam(self._lidcontrolid,
                                        LidLayers.surface.value,
                                        LidLayersProperty.roughness.value,
                                        param)

    @property
    def slope(self):
        """
        Get lid control surface layer land surface slope (fraction)

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidCParam(self._lidcontrolid,
                                        LidLayers.surface.value,
                                        LidLayersProperty.surfSlope.value)

    @slope.setter
    def slope(self, param):
        """Set lid control surface layer land surface slope (fraction)"""
        return self._model.setLidCParam(self._lidcontrolid,
                                        LidLayers.surface.value,
                                        LidLayersProperty.surfSlope.value,
                                        param)

    @property
    def side_slope(self):
        """
        Get lid control surface layer swale side slope (run/rise)

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidCParam(self._lidcontrolid,
                                        LidLayers.surface.value,
                                        LidLayersProperty.sideSlope.value)

    @side_slope.setter
    def side_slope(self, param):
        """Set lid control surface layer swale side slope (run/rise)"""
        return self._model.setLidCParam(self._lidcontrolid,
                                        LidLayers.surface.value,
                                        LidLayersProperty.sideSlope.value,
                                        param)

    @property
    def alpha(self):
        """
        Get lid control surface layer swale side slope (run/rise)

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidCParam(self._lidcontrolid,
                                        LidLayers.surface.value,
                                        LidLayersProperty.alpha.value)


class Soil(object):
    """
    Methods and properties of the soil layer associated with an LID 

    +--------------------+--------------------+--------------------+--------------------+
    | Layer              | Parameter          | Setter Before Sim  | Setter During Sim  |
    +====================+====================+====================+====================+
    | Soil               | thickness          | enabled            | disabled           |
    +--------------------+--------------------+--------------------+--------------------+
    | Soil               | porosity           | enabled            | disabled           |
    +--------------------+--------------------+--------------------+--------------------+
    | Soil               | field_capacity     | enabled            | disabled           |
    +--------------------+--------------------+--------------------+--------------------+
    | Soil               | wilting_point      | enabled            | disabled           |
    +--------------------+--------------------+--------------------+--------------------+
    | Soil               | k_saturated        | enabled            | disabled           |
    +--------------------+--------------------+--------------------+--------------------+
    | Soil               | k_slope            | enabled            | disabled           |
    +--------------------+--------------------+--------------------+--------------------+
    | Soil               | suction_head       | enabled            | disabled           |
    +--------------------+--------------------+--------------------+--------------------+
    """

    def __init__(self, model, lidcontrol):
        self._model = model
        self._lidcontrol = lidcontrol
        self._lidcontrolid = lidcontrol._lidcontrolid

    @property
    def thickness(self):
        """
        Get lid control soil layer thickness

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidCParam(self._lidcontrolid,
                                        LidLayers.soil.value,
                                        LidLayersProperty.thickness.value)

    @thickness.setter
    def thickness(self, param):
        """Set lid control soil layer thickness """
        return self._model.setLidCParam(self._lidcontrolid,
                                        LidLayers.soil.value,
                                        LidLayersProperty.thickness.value,
                                        param)

    @property
    def porosity(self):
        """
        Get lid control soil layer void volume / total volume

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidCParam(self._lidcontrolid,
                                        LidLayers.soil.value,
                                        LidLayersProperty.porosity.value)

    @porosity.setter
    def porosity(self, param):
        """Set lid control soil layer void volume / total volume"""
        return self._model.setLidCParam(self._lidcontrolid,
                                        LidLayers.soil.value,
                                        LidLayersProperty.porosity.value,
                                        param)

    @property
    def field_capacity(self):
        """
        Get lid control soil layer field capacity

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidCParam(self._lidcontrolid,
                                        LidLayers.soil.value,
                                        LidLayersProperty.fieldCap.value)

    @field_capacity.setter
    def field_capacity(self, param):
        """Set lid control soil layer field capacity"""
        return self._model.setLidCParam(self._lidcontrolid,
                                        LidLayers.soil.value,
                                        LidLayersProperty.fieldCap.value,
                                        param)

    @property
    def wilting_point(self):
        """
        Get lid control soil layer wilting point

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidCParam(self._lidcontrolid,
                                        LidLayers.soil.value,
                                        LidLayersProperty.wiltPoint.value)

    @wilting_point.setter
    def wilting_point(self, param):
        """Set lid control soil layer wilting point"""
        return self._model.setLidCParam(self._lidcontrolid,
                                        LidLayers.soil.value,
                                        LidLayersProperty.wiltPoint.value,
                                        param)

    @property
    def k_saturated(self):
        """
        Get lid control soil layer saturated hydraulic conductivity

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidCParam(self._lidcontrolid,
                                        LidLayers.soil.value,
                                        LidLayersProperty.kSat.value)

    @k_saturated.setter
    def k_saturated(self, param):
        """Set lid control soil layer saturated hydraulic conductivity"""
        return self._model.setLidCParam(self._lidcontrolid,
                                        LidLayers.soil.value,
                                        LidLayersProperty.kSat.value,
                                        param)

    @property
    def k_slope(self):
        """
        Get lid control soil layer slope of log(k) v. moisture content curve

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidCParam(self._lidcontrolid,
                                        LidLayers.soil.value,
                                        LidLayersProperty.kSlope.value)

    @k_slope.setter
    def k_slope(self, param):
        """Set lid control soil layer slope of log(k) v. moisture content curve"""
        return self._model.setLidCParam(self._lidcontrolid,
                                        LidLayers.soil.value,
                                        LidLayersProperty.kSlope.value,
                                        param)

    @property
    def suction_head(self):
        """
        Get lid control soil layer suction head at wetting front

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidCParam(self._lidcontrolid,
                                        LidLayers.soil.value,
                                        LidLayersProperty.suction.value)

    @suction_head.setter
    def suction_head(self, param):
        """Set lid control soil layer suction head at wetting front"""
        return self._model.setLidCParam(self._lidcontrolid,
                                        LidLayers.soil.value,
                                        LidLayersProperty.suction.value,
                                        param)


class Storage(object):
    """
    Methods and properties of the storage layer associated with an LID 

    +--------------------+--------------------+--------------------+--------------------+
    | Layer              | Parameter          | Setter Before Sim  | Setter During Sim  |
    +====================+====================+====================+====================+
    | Storage            | thickness          | enabled            | disabled           |
    +--------------------+--------------------+--------------------+--------------------+
    | Storage            | void_fraction      | enabled            | disabled           |
    +--------------------+--------------------+--------------------+--------------------+
    | Storage            | k_saturated        | enabled            | disabled           |
    +--------------------+--------------------+--------------------+--------------------+
    | Storage            | clog_factor        | enabled            | enabled            |
    +--------------------+--------------------+--------------------+--------------------+
    """

    def __init__(self, model, lidcontrol):
        self._model = model
        self._lidcontrol = lidcontrol
        self._lidcontrolid = lidcontrol._lidcontrolid

    @property
    def thickness(self):
        """
        Get lid control storage layer thickness

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidCParam(self._lidcontrolid,
                                        LidLayers.storage.value,
                                        LidLayersProperty.thickness.value)

    @thickness.setter
    def thickness(self, param):
        """Set lid control storage layer thickness"""
        return self._model.setLidCParam(self._lidcontrolid,
                                        LidLayers.storage.value,
                                        LidLayersProperty.thickness.value,
                                        param)

    @property
    def void_fraction(self):
        """
        Get lid control storage layer void volume / total volume

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidCParam(self._lidcontrolid,
                                        LidLayers.storage.value,
                                        LidLayersProperty.voidFrac.value)

    @void_fraction.setter
    def void_fraction(self, param):
        """Set lid control storage layer void volume / total volume"""
        return self._model.setLidCParam(self._lidcontrolid,
                                        LidLayers.storage.value,
                                        LidLayersProperty.voidFrac.value,
                                        param)

    @property
    def k_saturated(self):
        """
        Get lid control storage layer saturated hydraulic conductivity

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidCParam(self._lidcontrolid,
                                        LidLayers.storage.value,
                                        LidLayersProperty.kSat.value)

    @k_saturated.setter
    def k_saturated(self, param):
        """Set lid control storage layer saturated hydraulic conductivity"""
        return self._model.setLidCParam(self._lidcontrolid,
                                        LidLayers.storage.value,
                                        LidLayersProperty.kSat.value,
                                        param)

    @property
    def clog_factor(self):
        """
        Get lid control storage layer clogging factor

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidCParam(self._lidcontrolid,
                                        LidLayers.storage.value,
                                        LidLayersProperty.clogFactor.value)

    @clog_factor.setter
    def clog_factor(self, param):
        """Set lid control storage layer clogging factor"""
        return self._model.setLidCParam(self._lidcontrolid,
                                        LidLayers.storage.value,
                                        LidLayersProperty.clogFactor.value,
                                        param)


class Pavement(object):
    """
    Methods and properties of the pavement layer associated with an LID 

    +--------------------+--------------------+--------------------+--------------------+
    | Layer              | Parameter          | Setter Before Sim  | Setter During Sim  |
    +====================+====================+====================+====================+
    | Pavement           | thickness          | enabled            | disabled           |
    +--------------------+--------------------+--------------------+--------------------+
    | Pavement           | void_fraction      | enabled            | disabled           |
    +--------------------+--------------------+--------------------+--------------------+
    | Pavement           | impervious_fraction| enabled            | disabled           |
    +--------------------+--------------------+--------------------+--------------------+
    | Pavement           | k_saturated        | enabled            | disabled           |
    +--------------------+--------------------+--------------------+--------------------+
    | Pavement           | clog_factor        | enabled            | enabled            |
    +--------------------+--------------------+--------------------+--------------------+
    | Pavement           | regeneration       | enabled            | disabled           |
    +--------------------+--------------------+--------------------+--------------------+
    | Pavement           | regeneration_degree| enabled            | disabled           |
    +--------------------+--------------------+--------------------+--------------------+
    """

    def __init__(self, model, lidcontrol):
        self._model = model
        self._lidcontrol = lidcontrol
        self._lidcontrolid = lidcontrol._lidcontrolid

    @property
    def thickness(self):
        """
        Get lid control pavement layer thickness

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidCParam(self._lidcontrolid,
                                        LidLayers.pavement.value,
                                        LidLayersProperty.thickness.value)

    @thickness.setter
    def thickness(self, param):
        """Get lid control pavement layer thickness"""
        return self._model.setLidCParam(self._lidcontrolid,
                                        LidLayers.pavement.value,
                                        LidLayersProperty.thickness.value,
                                        param)

    @property
    def void_fraction(self):
        """
        Get lid control pavement layer void volume / total volume

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidCParam(self._lidcontrolid,
                                        LidLayers.pavement.value,
                                        LidLayersProperty.voidFrac.value)

    @void_fraction.setter
    def void_fraction(self, param):
        """Set lid control pavement layer void volume / total volume"""
        return self._model.setLidCParam(self._lidcontrolid,
                                        LidLayers.pavement.value,
                                        LidLayersProperty.voidFrac.value,
                                        param)

    @property
    def impervious_fraction(self):
        """
        Get lid control pavement layer impervious area fraction

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidCParam(self._lidcontrolid,
                                        LidLayers.pavement.value,
                                        LidLayersProperty.impervFrac.value)

    @impervious_fraction.setter
    def impervious_fraction(self, param):
        """Set lid control pavement layer impervious area fraction"""
        return self._model.setLidCParam(self._lidcontrolid,
                                        LidLayers.pavement.value,
                                        LidLayersProperty.impervFrac.value,
                                        param)

    @property
    def k_saturated(self):
        """
        Get lid control pavement layer permeability

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidCParam(self._lidcontrolid,
                                        LidLayers.pavement.value,
                                        LidLayersProperty.kSat.value)

    @k_saturated.setter
    def k_saturated(self, param):
        """Get lid control pavement layer permeability """
        return self._model.setLidCParam(self._lidcontrolid,
                                        LidLayers.pavement.value,
                                        LidLayersProperty.kSat.value,
                                        param)

    @property
    def clog_factor(self):
        """
        Get lid control pavement layer clogging factor

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidCParam(self._lidcontrolid,
                                        LidLayers.pavement.value,
                                        LidLayersProperty.clogFactor.value)

    @clog_factor.setter
    def clog_factor(self, param):
        """Get lid control pavement layer clogging factor"""
        return self._model.setLidCParam(self._sim._isStarted,
                                        self._lidcontrolid,
                                        LidLayers.pavement.value,
                                        LidLayersProperty.clogFactor.value,
                                        param)

    @property
    def regeneration(self):
        """
        Get lid control pavement layer clogging regeneration interval (days)

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidCParam(self._lidcontrolid,
                                        LidLayers.pavement.value,
                                        LidLayersProperty.regenDays.value)

    @regeneration.setter
    def regeneration(self, param):
        """Get lid control pavement layer clogging regeneration interval (days)"""
        return self._model.setLidCParam(self._lidcontrolid,
                                        LidLayers.pavement.value,
                                        LidLayersProperty.regenDays.value,
                                        param)

    @property
    def regeneration_degree(self):
        """
        Get lid control pavement layer clogging regeneration degree

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidCParam(self._lidcontrolid,
                                        LidLayers.pavement.value,
                                        LidLayersProperty.regenDegree.value)

    @regeneration_degree.setter
    def regeneration_degree(self, param):
        """Get lid control pavement layer clogging regeneration degree"""
        return self._model.setLidCParam(self._lidcontrolid,
                                        LidLayers.pavement.value,
                                        LidLayersProperty.regenDegree.value,
                                        param)


class Drain(object):
    """
    Methods and properties of the under drain layer associated with an LID 

    +--------------------+--------------------+--------------------+--------------------+
    | Layer              | Parameter          | Setter Before Sim  | Setter During Sim  |
    +====================+====================+====================+====================+
    | Drain              | coefficient        | enabled            | enabled            |
    +--------------------+--------------------+--------------------+--------------------+
    | Drain              | exponent           | enabled            | enabled            |
    +--------------------+--------------------+--------------------+--------------------+
    | Drain              | offset             | enabled            | enabled            |
    +--------------------+--------------------+--------------------+--------------------+
    | Drain              | delay              | enabled            | enabled            |
    +--------------------+--------------------+--------------------+--------------------+
    | Drain              | open_head          | enabled            | enabled            |
    +--------------------+--------------------+--------------------+--------------------+
    | Drain              | close_head         | enabled            | enabled            |
    +--------------------+--------------------+--------------------+--------------------+
    """

    def __init__(self, model, lidcontrol):
        self._model = model
        self._lidcontrol = lidcontrol
        self._lidcontrolid = lidcontrol._lidcontrolid

    @property
    def coefficient(self):
        """
        Get lid control drain layer underdrain flow coefficient

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidCParam(self._lidcontrolid,
                                        LidLayers.drain.value,
                                        LidLayersProperty.coeff.value)

    @coefficient.setter
    def coefficient(self, param):
        """Set lid control drain layer underdrain flow coefficient"""
        return self._model.setLidCParam(self._lidcontrolid,
                                        LidLayers.drain.value,
                                        LidLayersProperty.coeff.value,
                                        param)

    @property
    def exponent(self):
        """
        Get lid control drain layer underdrain head exponent

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidCParam(self._lidcontrolid,
                                        LidLayers.drain.value,
                                        LidLayersProperty.expon.value)

    @exponent.setter
    def exponent(self, param):
        """Set lid control drain layer underdrain head exponent"""
        return self._model.setLidCParam(self._lidcontrolid,
                                        LidLayers.drain.value,
                                        LidLayersProperty.expon.value,
                                        param)

    @property
    def offset(self):
        """
        Get lid control drain layer offset height of underdrain

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidCParam(self._lidcontrolid,
                                        LidLayers.drain.value,
                                        LidLayersProperty.offset.value)

    @offset.setter
    def offset(self, param):
        """Set lid control drain layer offset height of underdrain"""
        return self._model.setLidCParam(self._lidcontrolid,
                                        LidLayers.drain.value,
                                        LidLayersProperty.offset.value,
                                        param)

    @property
    def delay(self):
        """
        Get lid control drain layer rain barrel drain delay time (sec)

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidCParam(self._lidcontrolid,
                                        LidLayers.drain.value,
                                        LidLayersProperty.delay.value)

    @delay.setter
    def delay(self, param):
        """Set lid control drain layer rain barrel drain delay time (sec)"""
        return self._model.setLidCParam(self._lidcontrolid,
                                        LidLayers.drain.value,
                                        LidLayersProperty.delay.value,
                                        param)

    @property
    def open_head(self):
        """
        Get lid control drain layer head when drain opens (ft)

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidCParam(self._lidcontrolid,
                                        LidLayers.drain.value,
                                        LidLayersProperty.hOpen.value)

    @open_head.setter
    def open_head(self, param):
        """Set lid control drain layer head when drain opens (ft)"""
        return self._model.setLidCParam(self._lidcontrolid,
                                        LidLayers.drain.value,
                                        LidLayersProperty.hOpen.value,
                                        param)

    @property
    def close_head(self):
        """
        Get lid control drain layer head when drain closes (ft)

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidCParam(self._lidcontrolid,
                                        LidLayers.drain.value,
                                        LidLayersProperty.hClose.value)

    @close_head.setter
    def close_head(self, param):
        """Set lid control drain layer drain closes (ft)"""
        return self._model.setLidCParam(self._lidcontrolid,
                                        LidLayers.drain.value,
                                        LidLayersProperty.hClose.value,
                                        param)


class DrainMat(object):
    """
    Methods and properties of the drain mat layer associated with an LID 

    +--------------------+--------------------+--------------------+--------------------+
    | Layer              | Parameter          | Setter Before Sim  | Setter During Sim  |
    +====================+====================+====================+====================+
    | DrainMat           | thickness          | enabled            | disabled           |
    +--------------------+--------------------+--------------------+--------------------+
    | DrainMat           | void_fraction      | enabled            | disabled           |
    +--------------------+--------------------+--------------------+--------------------+
    | DrainMat           | roughness          | enabled            | enabled            |
    +--------------------+--------------------+--------------------+--------------------+
    | DrainMat           | alpha              | enabled            | disabled           |
    +--------------------+--------------------+--------------------+--------------------+
    """

    def __init__(self, model, lidcontrol):
        self._model = model
        self._lidcontrol = lidcontrol
        self._lidcontrolid = lidcontrol._lidcontrolid

    @property
    def thickness(self):
        """
        Get lid control drainmat layer thickness

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidCParam(self._lidcontrolid,
                                        LidLayers.drainMat.value,
                                        LidLayersProperty.thickness.value)

    @thickness.setter
    def thickness(self, param):
        """Set lid control drainmat layer thickness"""
        return self._model.setLidCParam(self._lidcontrolid,
                                        LidLayers.drainMat.value,
                                        LidLayersProperty.thickness.value,
                                        param)

    @property
    def void_fraction(self):
        """
        Get lid control drainmat layer void volume / total volume

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidCParam(self._lidcontrolid,
                                        LidLayers.drainMat.value,
                                        LidLayersProperty.voidFrac.value)

    @void_fraction.setter
    def void_fraction(self, param):
        """Set lid control drainmat layer void volume / total volume"""
        return self._model.setLidCParam(self._lidcontrolid,
                                        LidLayers.drainMat.value,
                                        LidLayersProperty.voidFrac.value,
                                        param)

    @property
    def roughness(self):
        """
        Get lid control drainmat layer Mannings n for green roof drainage mats

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidCParam(self._lidcontrolid,
                                        LidLayers.drainMat.value,
                                        LidLayersProperty.roughness.value)

    @roughness.setter
    def roughness(self, param):
        """Set lid control drainmat layer Mannings n for green roof drainage mats"""
        return self._model.setLidCParam(self._lidcontrolid,
                                        LidLayers.drainMat.value,
                                        LidLayersProperty.roughness.value,
                                        param)

    @property
    def alpha(self):
        """
        Get lid control drainmat layer slope/roughness term in Manning equation

        :return: Parameter Value
        :rtype: double
        """
        return self._model.getLidCParam(self._lidcontrolid,
                                        LidLayers.drainMat.value,
                                        LidLayersProperty.alpha.value)
