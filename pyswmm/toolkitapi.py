# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014 Bryant E. McDonnell
#
# Licensed under the terms of the BSD2 License
# See LICENSE.txt for details
# -----------------------------------------------------------------------------
"""SWMM Object Enum."""

# Standard library imports
from enum import Enum


class SimulationTime(Enum):
    StartDateTime = 0
    EndDateTime = 1
    ReportStart = 2


class SimulationUnits(Enum):
    UnitSystem = 0  # (0-US, 1-SI)
    FlowUnits = 1


class SimAnalysisSettings(Enum):
    AllowPonding = 0  # No ponding at nodes
    SkipSteadyState = 1  # Do flow routing in steady state periods
    IgnoreRainfall = 2  # Analyze rainfall/runoff
    IgnoreRDII = 3  # Analyze RDII
    IgnoreSnowmelt = 4  # Analyze snowmelt
    IgnoreGwater = 5  # Analyze groundwater
    IgnoreRouting = 6  # Analyze flow routing
    IgnoreQuality = 7  # Analyze water quality


class SimulationParameters(Enum):
    RouteStep = 0  # Routing time step (sec)
    MinRouteStep = 1  # Minimum variable time step (sec)
    LengtheningStep = 2  # Time step for lengthening (sec)
    StartDryDays = 3  # Antecedent dry days
    CourantFactor = 4  # Courant time step factor
    MinSurfArea = 5  # Minimum nodal surface area
    MinSlope = 6  # Minimum conduit slope
    RunoffError = 7  # Runoff continuity error
    GwaterError = 8  # Groundwater continuity error
    FlowError = 9  # Flow routing error
    QualError = 10  # Quality routing error
    HeadTol = 11  # DW routing head tolerance (ft)
    SysFlowTol = 12  # Tolerance for steady system flow
    LatFlowTol = 13  # Tolerance for steady nodal inflow


class ObjectType(Enum):
    GAGE = 0  # rain gage
    SUBCATCH = 1  # subcatchment
    NODE = 2  # conveyance system node
    LINK = 3  # conveyance system link
    POLLUT = 4  # pollutant
    LANDUSE = 5  # land use category
    TIMEPATTERN = 6  # dry weather flow time pattern
    CURVE = 7  # generic table of values
    TSERIES = 8  # generic time series of values
    CONTROL = 9  # conveyance system control rules
    TRANSECT = 10  # irregular channel cross-section
    AQUIFER = 11  # groundwater aquifer
    UNITHYD = 12  # RDII unit hydrograph
    SNOWMELT = 13  # snowmelt parameter set
    SHAPE = 14  # custom conduit shape
    LID = 15  # LID treatment units
    MAX_OBJ_TYPES = 16  # MaximumObjectTypes


class NodeParams(Enum):
    invertElev = 0  # double
    fullDepth = 1  # double
    surDepth = 2  # double
    pondedArea = 3  # double
    initDepth = 4  # double


class NodeResults(Enum):
    totalinflow = 0  # Total Inflow
    outflow = 1  # Total Outflow
    losses = 2  # Losses (evap + exfiltration loss)
    newVolume = 3  # Current Volume
    overflow = 4  # overflow
    newDepth = 5  # Current water depth
    newHead = 6  # Current water head
    newLatFlow = 7  # Current Lateral Inflow


class NodeType(Enum):
    junction = 0  # Junction Type
    outfall = 1  # Outfall Type
    storage = 2  # Storage Type
    divider = 3  # Divider Type


class LinkParams(Enum):
    offset1 = 0  # double
    offset2 = 1  # double
    q0 = 2  # double
    qLimit = 3  # double
    cLossInlet = 4  # double
    cLossOutlet = 5  # double
    cLossAvg = 6  # double
    seepRate = 7  # double


class LinkResults(Enum):
    newFlow = 0  # double
    newDepth = 1  # double
    newVolume = 2  # double
    surfArea1 = 3  # double
    surfArea2 = 4  # double
    setting = 5  # double
    targetSetting = 6  # double
    froude = 7  # double


class LinkType(Enum):
    conduit = 0  # Conduit Type
    pump = 1  # Pump Type
    orifice = 2  # Orifice Type
    weir = 3  # Weir Type
    outlet = 4  # Outlet Type


class SubcParams(Enum):
    width = 0  # double
    area = 1  # double
    fracImperv = 2  # double
    slope = 3  # double
    curbLength = 4  # double
    # initBuildup = 5  # double


class SubcResults(Enum):
    rainfall = 0  # Current Rainfall
    evapLoss = 1  # Current Evaporation Loss
    infilLoss = 2  # Current Infiltration Loss
    runon = 3  # Subcatchment Runon
    newRunoff = 4  # Current Runoff
    newSnowDepth = 5  # Current Snow Depth


# --- SWMM Output API
# -----------------------------------------------------------------------------
DLLErrorKeys = {
    411: "Input Error 411: no memory allocated for results.",
    412: "Input Error 412: no results; binary file hasn't been opened.",
    421: "Input Error 421: invalid parameter code.",
    434: "File Error  434: unable to open binary output file.",
    435: "File Error  435: run terminated; no results in binary file.",
    441: "Error 441: need to call SMR_open before calling this function"
}


class SMO_elementCount(Enum):
    subcatchCount = 0
    nodeCount = 1
    linkCount = 2
    pollutantCount = 3


class SMO_unit(Enum):
    flow_rate = 0
    concentration = 1


class SMO_apiFunction(Enum):
    getAttribute = 0
    getResult = 1


class SMO_elementType(Enum):
    SM_subcatch = 0
    SM_node = 1
    SM_link = 2
    SM_sys = 3


class SMO_time(Enum):
    reportStep = 0
    numPeriods = 1


class SMO_subcatchAttribute(Enum):
    rainfall_subcatch = 0
    snow_depth_subcatch = 1
    evap_loss = 2
    infil_loss = 3
    runoff_rate = 4
    gwoutflow_rate = 5
    gwtable_elev = 6
    soil_moisture = 7
    pollutant_conc_subcatch = 8


class SMO_nodeAttribute(Enum):
    invert_depth = 0
    hydraulic_head = 1
    stored_ponded_volume = 2
    lateral_inflow = 3
    total_inflow = 4
    flooding_losses = 5
    pollutant_conc_node = 6


class SMO_linkAttribute(Enum):
    flow_rate_link = 0
    flow_depth = 1
    flow_velocity = 2
    flow_volume = 3
    capacity = 4
    pollutant_conc_link = 5


class SMO_systemAttribute(Enum):
    air_temp = 0
    rainfall_system = 1
    snow_depth_system = 2
    evap_infil_loss = 3
    runoff_flow = 4
    dry_weather_inflow = 5
    groundwater_inflow = 6
    RDII_inflow = 7
    direct_inflow = 8
    total_lateral_inflow = 9
    flood_losses = 10
    outfall_flows = 11
    volume_stored = 12
    evap_rate = 13
