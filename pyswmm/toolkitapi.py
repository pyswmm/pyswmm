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
import ctypes


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


class NodePollut(Enum):
    nodeQual = 0  # Current Water Quality Value


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


class LinkPollut(Enum):
    linkQual = 0  # Current Water Quality Value
    totalLoad = 1  # Total Quality Mass Loading


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


class SubcPollut(Enum):
    buildup = 0  # Subcatchment Surface Buildup
    concPonded = 1  # Ponded Pollutant Concentration
    subcQual = 2  # Current Pollutant Runoff Quality
    subcTotalLoad = 3  # Total Pollutant Washoff Load


class LidUParams(Enum):
    unitArea = 0  # double
    fullWidth = 1  # double
    botWidth = 2  # double
    initSat = 3  # double
    fromImperv = 4  # double
    fromPerv = 5  # double


class LidResults(Enum):
    inflow = 0  # double
    evap = 1  # double
    infil = 2  # double
    surfFlow = 3  # double
    drainFlow = 4  # double
    initVol = 5  # double
    finalVol = 6  # double
    surfDepth = 7  # double
    paveDepth = 8  # double
    soilMoist = 9  # double
    storDepth = 10  # double
    dryTime = 11  # double
    oldDrainFlow = 12  # double
    newDrainFlow = 13  # double
    pervArea = 14  # double
    flowToPerv = 15  # double
    evapRate = 16  # double
    nativeInfil = 17  # double
    surfInflow = 18  # double
    surfInfil = 19  # double
    surfEvap = 20  # double
    surfOutflow = 21  # double
    paveEvap = 22  # double
    pavePerc = 23  # double
    soilEvap = 24  # double
    soilPerc = 25  # double
    storInflow = 26  # double
    storExfil = 27  # double
    storEvap = 28  # double
    storDrain = 29  # double


class LidUOptions(Enum):
    index = 0  # int
    number = 1  # int
    toPerv = 2  # int
    drainSub = 3  # int
    drainNode = 4  # int


class LidLayers(Enum):
    surface = 0  # int
    soil = 1  # int
    storage = 2  # int
    pavement = 3  # int
    drain = 4  # int
    drainMat = 5  # int


class LidLayersProperty(Enum):
    thickness = 0  # double
    voidFrac = 1  # double
    roughness = 2  # double
    surfSlope = 3  # double
    sideSlope = 4  # double
    alpha = 5  # double
    porosity = 6  # double
    fieldCap = 7  # double
    wiltPoint = 8  # double
    suction = 9  # double
    kSat = 10  # double
    kSlope = 11  # double
    clogFactor = 12  # double
    impervFrac = 13  # double
    coeff = 14  # double
    expon = 15  # double
    offset = 16  # double
    delay = 17  # double
    hOpen = 18  # double
    hClose = 19  # double
    qCurve = 20  # integer
    regenDays = 21  # double
    regenDegree = 22  # double


class RainGageResults(Enum):
    total_precip = 0
    rainfall = 1
    snowfall = 2


class NodeStats(ctypes.Structure):
    _fields_ = [
        ("avgDepth", ctypes.c_double), ("maxDepth", ctypes.c_double),
        ("maxDepthDate", ctypes.c_double), ("maxRptDepth", ctypes.c_double),
        ("volFlooded", ctypes.c_double), ("timeFlooded", ctypes.c_double),
        ("timeSurcharged", ctypes.c_double),
        ("timeCourantCritical", ctypes.c_double),
        ("totLatFlow", ctypes.c_double), ("maxLatFlow", ctypes.c_double),
        ("maxInflow", ctypes.c_double), ("maxOverflow", ctypes.c_double),
        ("maxPondedVol", ctypes.c_double), ("maxInflowDate", ctypes.c_double),
        ("maxOverflowDate", ctypes.c_double)
    ]
    _py_alias_ids = {
        "avgDepth": "average_depth",
        "maxDepth": "max_depth",
        "maxDepthDate": "max_depth_date",
        "maxRptDepth": "max_report_depth",
        "volFlooded": "flooding_volume",
        "timeFlooded": "flooding_duration",
        "timeSurcharged": "surcharge_duration",
        "timeCourantCritical": "courant_crit_duration",
        "totLatFlow": "lateral_infow_vol",
        "maxLatFlow": "peak_lateral_inflowrate",
        "maxInflow": "peak_total_inflow",
        "maxOverflow": "peak_flooding_rate",
        "maxPondedVol": "max_ponded_volume",
        "maxInflowDate": "max_inflow_date",
        "maxOverflowDate": "max_flooding_date",
        "loads": "pollutant_loading"
    }


class StorageStats(ctypes.Structure):
    _fields_ = [("initVol", ctypes.c_double), ("avgVol", ctypes.c_double),
                ("maxVol", ctypes.c_double), ("maxFlow", ctypes.c_double),
                ("evapLosses", ctypes.c_double),
                ("exfilLosses", ctypes.c_double),
                ("maxVolDate", ctypes.c_double)]
    _py_alias_ids = {
        "initVol": "initial_volume",
        "avgVol": "average_volume",
        "maxVol": "max_volume",
        "maxFlow": "peak_flowrate",
        "evapLosses": "evap_loss",
        "exfilLosses": "exfil_loss",
        "maxVolDate": "max_vol_date"
    }


PollutArray = ctypes.POINTER(ctypes.c_double)


class OutfallStats(ctypes.Structure):
    _fields_ = [("avgFlow", ctypes.c_double), ("maxFlow", ctypes.c_double),
                ("totalLoad", PollutArray), ("totalPeriods", ctypes.c_int)]
    _py_alias_ids = {
        "avgFlow": "average_flowrate",
        "maxFlow": "peak_flowrate",
        "totalLoad": "pollutant_loading",
        "totalPeriods": "total_periods",
        "loads": "pollutant_loading"
    }


FlowClassArray = ctypes.c_double * 7


class LinkStats(ctypes.Structure):
    _fields_ = [("maxFlow", ctypes.c_double), ("maxFlowDate", ctypes.c_double),
                ("maxVeloc", ctypes.c_double), ("maxDepth", ctypes.c_double),
                ("timeNormalFlow", ctypes.c_double),
                ("timeInletControl", ctypes.c_double),
                ("timeSurcharged", ctypes.c_double),
                ("timeFullUpstream", ctypes.c_double),
                ("timeFullDnstream", ctypes.c_double),
                ("timeFullFlow", ctypes.c_double),
                ("timeCapacityLimited", ctypes.c_double),
                ("timeInFlowClass", FlowClassArray),
                ("timeCourantCritical", ctypes.c_double),
                ("flowTurns", ctypes.c_long), ("flowTurnSign", ctypes.c_int)]
    _py_alias_ids = {
        "maxFlow": "peak_flow",
        "maxFlowDate": "peak_flow_date",
        "maxVeloc": "peak_velocity",
        "maxDepth": "peak_depth",
        "timeNormalFlow": "time_normal_flow",
        "timeInletControl": "time_inlet_control",
        "timeSurcharged": "time_surcharged",
        "timeFullUpstream": "time_full_upstream",
        "timeFullDnstream": "time_full_downstream",
        "timeFullFlow": "time_full_flow",
        "timeCapacityLimited": "time_capacity_limited",
        "timeInFlowClass": "time_in_flow_class",
        "timeCourantCritical": "time_courant_crit",
        "flowTurns": "flow_turns",
        "flowTurnSign": "flow_turn_sign"
    }


class PumpStats(ctypes.Structure):
    _fields_ = [
        ("utilized", ctypes.c_double),
        ("minFlow", ctypes.c_double),
        ("avgFlow", ctypes.c_double),
        ("maxFlow", ctypes.c_double),
        ("volume", ctypes.c_double),
        ("energy", ctypes.c_double),
        ("offCurveLow", ctypes.c_double),
        ("offCurveHigh", ctypes.c_double),
        ("startUps", ctypes.c_int),
        ("totalPeriods", ctypes.c_int),
    ]
    _py_alias_ids = {
        "utilized": "percent_utilized",
        "minFlow": "min_flowrate",
        "avgFlow": "average_flowrate",
        "maxFlow": "max_flowrate",
        "volume": "total_volume",
        "energy": "energy_consumed",
        "offCurveLow": "off_curve_low",
        "offCurveHigh": "off_curve_high",
        "startUps": "number_startups",
        "totalPeriods": "total_periods"
    }


class SubcStats(ctypes.Structure):
    _fields_ = [("precip", ctypes.c_double), ("runon", ctypes.c_double),
                ("evap", ctypes.c_double), ("infil", ctypes.c_double),
                ("runoff", ctypes.c_double), ("maxFlow", ctypes.c_double)]
    _py_alias_ids = {
        "precip": "precipitation",
        "runon": "runon",
        "evap": "evaporation",
        "infil": "infiltration",
        "runoff": "runoff",
        "maxFlow": "peak_runoff_rate",
    }


class RoutingTotals(ctypes.Structure):
    _fields_ = [("dwInflow", ctypes.c_double), ("wwInflow", ctypes.c_double),
                ("gwInflow", ctypes.c_double), ("iiInflow", ctypes.c_double),
                ("exInflow", ctypes.c_double), ("flooding", ctypes.c_double),
                ("outflow", ctypes.c_double), ("evapLoss", ctypes.c_double),
                ("seepLoss", ctypes.c_double), ("reacted", ctypes.c_double),
                ("initStorage", ctypes.c_double),
                ("finalStorage", ctypes.c_double),
                ("pctError", ctypes.c_double)]
    _py_alias_ids = {
        "dwInflow": "dry_weather_inflow",
        "wwInflow": "wet_weather_inflow",
        "gwInflow": "groundwater_inflow",
        "iiInflow": "II_inflow",
        "exInflow": "external_inflow",
        "flooding": "flooding",
        "outflow": "outflow",
        "evapLoss": "evaporation_loss",
        "seepLoss": "seepage_loss",
        "reacted": "reacted",
        "initStorage": "initial_storage",
        "finalStorage": "final_storage",
        "pctError": "routing_error"
    }


class RunoffTotals(ctypes.Structure):
    _fields_ = [
        ("rainfall", ctypes.c_double), ("evap", ctypes.c_double),
        ("infil", ctypes.c_double), ("runoff", ctypes.c_double),
        ("drains", ctypes.c_double), ("runon", ctypes.c_double),
        ("initStorage", ctypes.c_double), ("finalStorage", ctypes.c_double),
        ("initSnowCover", ctypes.c_double),
        ("finalSnowCover", ctypes.c_double), ("snowRemoved", ctypes.c_double),
        ("pctError", ctypes.c_double)
    ]
    _py_alias_ids = {
        "rainfall": "rainfall",
        "evap": "evaporation",
        "infil": "infiltration",
        "runoff": "runoff",
        "drains": "drains",
        "runon": "runon",
        "initStorage": "init_storage",
        "finalStorage": "final_storage",
        "initSnowCover": "init_snow_cover",
        "finalSnowCover": "final_snow_cover",
        "snowRemoved": "snow_removed",
        "pctError": "routing_error"
    }


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
