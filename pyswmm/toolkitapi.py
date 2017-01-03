
'''
SWMM Object Enum
'''


class SimulationTime:    
    StartDateTime   = 0  
    EndDateTime     = 1
    ReportStart     = 2

class SimulationUnits:
    UnitSystem      = 0# (0-US, 1-SI)
    FlowUnits       = 1# 

class SimAnalysisSettings:
    AllowPonding    = 0# // No ponding at nodes
    SkipSteadyState = 1# // Do flow routing in steady state periods 
    IgnoreRainfall  = 2# // Analyze rainfall/runoff
    IgnoreRDII      = 3# // Analyze RDII   
    IgnoreSnowmelt  = 4# // Analyze snowmelt 
    IgnoreGwater    = 5# // Analyze groundwater  
    IgnoreRouting   = 6# // Analyze flow routing
    IgnoreQuality   = 7# // Analyze water quality

class SimulationParameters:
    RouteStep       = 0# // Routing time step (sec)
    MinRouteStep    = 1# // Minimum variable time step (sec)
    LengtheningStep = 2# // Time step for lengthening (sec)
    StartDryDays    = 3# // Antecedent dry days
    CourantFactor   = 4# // Courant time step factor
    MinSurfArea     = 5# // Minimum nodal surface area
    MinSlope        = 6# // Minimum conduit slope
    RunoffError     = 7# // Runoff continuity error
    GwaterError     = 8# // Groundwater continuity error
    FlowError       = 9# // Flow routing error
    QualError       = 10#// Quality routing error
    HeadTol         = 11#// DW routing head tolerance (ft)
    SysFlowTol      = 12#// Tolerance for steady system flow
    LatFlowTol      = 13#// Tolerance for steady nodal inflow   

class ObjectType:
    GAGE            = 0# // rain gage
    SUBCATCH        = 1# // subcatchment
    NODE            = 2# // conveyance system node
    LINK            = 3# // conveyance system link
    POLLUT          = 4# // pollutant
    LANDUSE         = 5# // land use category
    TIMEPATTERN     = 6# // dry weather flow time pattern
    CURVE           = 7# // generic table of values
    TSERIES         = 8# // generic time series of values
    CONTROL         = 9# // conveyance system control rules
    TRANSECT        = 10#// irregular channel cross-section
    AQUIFER         = 11#// groundwater aquifer
    UNITHYD         = 12#// RDII unit hydrograph
    SNOWMELT        = 13#// snowmelt parameter set
    SHAPE           = 14#// custom conduit shape
    LID             = 15#// LID treatment units
    MAX_OBJ_TYPES   = 16#// MaximumObjectTypes

class NodeParams:
    invertElev      = 0# double
    fullDepth       = 1# double
    surDepth        = 2# double
    pondedArea      = 3# double
    initDepth       = 4# double

class NodeResults:
    totalinflow     = 0#// Total Inflow
    outflow         = 1#// Total Outflow
    losses          = 2#// Losses (evap + exfiltration loss)
    newVolume       = 3#// Current Volume
    overflow        = 4#// overflow
    newDepth        = 5#// Current water depth
    newHead         = 6#// Current water head
    newLatFlow      = 7#// Current Lateral Inflow

class NodeType:
    junction        = 0#// Junction Type
    outfall         = 1#// Outfall Type
    storage         = 2#// Storage Type
    divider         = 3#// Divider Type

class LinkParams:
    offset1         = 0# double
    offset2         = 1# double
    q0              = 2# double
    qLimit          = 3# double
    cLossInlet      = 4# double
    cLossOutlet     = 5# double
    cLossAvg        = 6# double
    seepRate        = 7# double

class LinkResults:
    newFlow         = 0# double
    newDepth        = 1# double
    newVolume       = 2# double
    surfArea1       = 3# double
    surfArea2       = 4# double
    setting         = 5# double
    targetSetting   = 6# double
    froude          = 7# double
    
class LinkType:
    conduit         = 0#// Conduit Type
    pump            = 1#// Pump Type
    orifice         = 2#// Orifice Type
    weir            = 3#// Weir Type
    outlet          = 4#// Outlet Type

class SubcParams:
    width           = 0 # double
    area            = 1 # double
    fracImperv      = 2 # double
    slope           = 3 # double
    curbLength      = 4 # double
    #initBuildup     = 5 # double

class SubcResults:
    rainfall        = 0 # // Current Rainfall
    evapLoss        = 1 # // Current Evaporation Loss
    infilLoss       = 2 # // Current Infiltration Loss
    runon           = 3 # // Subcatchment Runon
    newRunoff       = 4 # // Current Runoff
    newSnowDepth    = 5 # // Current Snow Depth


