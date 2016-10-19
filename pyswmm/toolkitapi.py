
'''
SWMM Object Enum
'''

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


