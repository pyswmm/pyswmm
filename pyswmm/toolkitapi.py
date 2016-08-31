
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
    Type            = 0# int
    invertElev      = 1# double
    fullDepth       = 2# double
    surDepth        = 3# double
    pondedArea      = 4# double
    initDepth       = 5# double
    rptFlag         = 6# char
    
class LinkParams:
    Type            = 0#  
    subIndex        = 0#   
    rptFlag         = 0#
    node1           = 0#
    node2           = 0#
    offset1         = 0#
    offset2         = 0#
    xsect           = 0#
    q0              = 0#
    qLimit          = 0#
    cLossInlet      = 0#
    cLossOutlet     = 0#
    cLossAvg        = 0#
    seepRate        = 0#
    hasFlapGate     = 0#

class SubcParams:
    rptFlag         = 1
    gage            = 1
    outNode         = 1
    outSubcatch     = 1
    infil           = 1
    subArea         = 1
    width           = 1
    area            = 1
    fracImperv      = 1
    slope           = 1
    curbLength      = 1
    initBuildup     = 1
    landFactor      = 1
    groundwater     = 1
    gwLatFlowExpr   = 1
    gwDeepFlowExpr  = 1
    snowpack        = 1

