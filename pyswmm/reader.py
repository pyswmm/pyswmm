# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014 Bryant E. McDonnell
#
# Licensed under the terms of the BSD2 License
# See LICENSE.txt for details
# -----------------------------------------------------------------------------
"""SWMM ouput toolkit api."""

# Standard library imports
from datetime import datetime, timedelta
import ctypes
import os

# Local imports
from toolkitapi import (DLLErrorKeys, SMO_apiFunction, SMO_elementCount,
                        SMO_elementType, SMO_systemAttribute, SMO_time,
                        SMO_unit)


class _Opaque(ctypes.Structure):
    """Used soley for passing the pointer to the smoapu struct to API."""
    pass


class SWMMBinReader(object):
    """Instantiate python Wrapper Object and build Wrapper functions."""

    def __init__(self):
        """Instantiate python Wrapper Object and build Wrapper functions."""
        def get_pkgpath():
            import toolkitapi as tkp
            return os.path.dirname(tkp.__file__.replace('\\', '/'))

        try:
            # Later Check for OS Type
            dllname = 'outputAPI_winx86.dll'
            # when platform detection is enabled, dllname can be changed
            dllLoc = get_pkgpath() + '/data/' + dllname
            self.swmmdll = ctypes.CDLL(dllLoc)
        except:
            raise Exception('Failed to Open Linked Library')

        # Initializing DLL Function List
        # Initialize Pointer to smoapi
        self._initsmoapi = self.swmmdll.SMO_init
        self._initsmoapi.restype = ctypes.POINTER(_Opaque)

        # Open File Function Handle
        self._openBinFile = self.swmmdll.SMO_open
        self._free = self.swmmdll.SMO_free
        self._close = self.swmmdll.SMO_close

        # Project Data
        self._getProjectSize = self.swmmdll.SMO_getProjectSize
        self._getTimes = self.swmmdll.SMO_getTimes
        self._getStartTime = self.swmmdll.SMO_getStartTime
        self._getUnits = self.swmmdll.SMO_getUnits

        # Object ID Function Handles
        self._getIDs = self.swmmdll.SMO_getElementName

        # Object Series Function Handles
        self._getSubcatchSeries = self.swmmdll.SMO_getSubcatchSeries
        self._getNodeSeries = self.swmmdll.SMO_getNodeSeries
        self._getLinkSeries = self.swmmdll.SMO_getLinkSeries
        self._getSystemSeries = self.swmmdll.SMO_getSystemSeries

        # Object Attribure Function Handles
        self._getSubcatchAttribute = self.swmmdll.SMO_getSubcatchAttribute
        self._getNodeAttribute = self.swmmdll.SMO_getNodeAttribute
        self._getLinkAttribute = self.swmmdll.SMO_getLinkAttribute
        self._getSystemAttribute = self.swmmdll.SMO_getSystemAttribute

        # Object Result Function Handles
        self._getSubcatchResult = self.swmmdll.SMO_getSubcatchResult
        self._getNodeResult = self.swmmdll.SMO_getNodeResult
        self._getLinkResult = self.swmmdll.SMO_getLinkResult
        self._getSystemResult = self.swmmdll.SMO_getSystemResult

        # Array Builder
        self._newOutValueArray = self.swmmdll.SMO_newOutValueArray
        self._newOutValueArray.argtypes = [
            ctypes.POINTER(_Opaque),
            ctypes.c_int,
            ctypes.c_int,
            ctypes.POINTER(ctypes.c_int),
            ctypes.POINTER(ctypes.c_int),
            ]
        self._newOutValueArray.restype = ctypes.POINTER(ctypes.c_float)

        # Series Builder
        self._newOutValueSeries = self.swmmdll.SMO_newOutValueSeries
        self._newOutValueSeries.argtypes = [
            ctypes.POINTER(_Opaque),
            ctypes.c_int,
            ctypes.c_int,
            ctypes.POINTER(ctypes.c_int),
            ctypes.POINTER(ctypes.c_int),
            ]
        self._newOutValueSeries.restype = ctypes.POINTER(ctypes.c_float)

        # SWMM Date num 2 String
        self.SWMMdateToStr = self.swmmdll.datetime_dateToStr

        # SWMM Time num 2 String
        self.SWMMtimeToStr = self.swmmdll.datetime_timeToStr

    def OpenBinFile(self, OutLoc):
        """
        Opens SWMM5 binary output file.

        :param str OutLoc: Path to Binary output file

        :return: None

        Examples:

        >>> OutputFile = SWMMBinReader()
        >>> OutputFile.OpenBinFile(r"C:\\PROJECTCODE\\SWMMOutputAPI\\testing\\outputfile.out")
        """
        self.smoapi = self._initsmoapi()
        ErrNo = self._openBinFile(self.smoapi, OutLoc)
        if ErrNo != 0:
            error_msg = "API ErrNo {0}:{1}".format(ErrNo, DLLErrorKeys[ErrNo])
            raise Exception(error_msg)

    def CloseBinFile(self):
        """
        Closes binary output file and cleans up member variables.

        :returns: None

        Examples:

        >>> OutputFile = SWMMBinReader()
        >>> OutputFile.OpenBinFile(r"C:\\PROJECTCODE\\SWMMOutputAPI\\testing\\outputfile.out")
        >>> OutputFile.CloseBinFile()
        """
        ErrNo = self._close(self.smoapi)

        if hasattr(self, 'SubcatchmentIDs'):
            delattr(self, 'SubcatchmentIDs')
        if hasattr(self, 'NodeIDs'):
            delattr(self, 'NodeIDs')
        if hasattr(self, 'LinkIDs'):
            delattr(self, 'LinkIDs')
        if hasattr(self, 'PollutantIDs'):
            delattr(self, 'PollutantIDs')

        if ErrNo != 0:
            error_msg = "API ErrNo {0}:{1}".format(ErrNo.value,
                                                   DLLErrorKeys[ErrNo.value])
            raise Exception(error_msg)

    def _get_SubcatchIDs(self):
        """Generates member Element IDs dictionary for Subcatchments."""
        self.SubcatchmentIDs = {}
        for i in range(self.get_ProjectSize(SMO_elementCount.subcatchCount)):
            NAME = ctypes.create_string_buffer(46)
            LEN = ctypes.c_int(46)
            ErrNo1 = self._getIDs(self.smoapi,
                                  SMO_elementType.SM_subcatch,
                                  i,
                                  ctypes.byref(NAME),
                                  ctypes.byref(LEN))
            if ErrNo1 != 0:
                error_msg = "API ErrNo {0}:{1}".format(
                    ErrNo1.value, DLLErrorKeys[ErrNo1.value])
                raise Exception(error_msg)
            self.SubcatchmentIDs[str(NAME.value)] = i

    def _get_NodeIDs(self):
        """Generates member Element IDs dictionary for Nodes."""
        self.NodeIDs = {}
        for i in range(self.get_ProjectSize(SMO_elementCount.nodeCount)):
            NAME = ctypes.create_string_buffer(46)
            LEN = ctypes.c_int(46)
            ErrNo1 = self._getIDs(self.smoapi,
                                  SMO_elementType.SM_node,
                                  i,
                                  ctypes.byref(NAME),
                                  ctypes.byref(LEN))
            if ErrNo1 != 0:
                error_msg = "API ErrNo {0}:{1}".format(
                    ErrNo1.value, DLLErrorKeys[ErrNo1.value])
                raise Exception(error_msg)
            self.NodeIDs[str(NAME.value)] = i

    def _get_LinkIDs(self):
        """Generates member Element IDs dictionary for Links."""
        self.LinkIDs = {}
        for i in range(self.get_ProjectSize(SMO_elementCount.linkCount)):
            NAME = ctypes.create_string_buffer(46)
            LEN = ctypes.c_int(46)
            ErrNo1 = self._getIDs(self.smoapi,
                                  SMO_elementType.SM_link,
                                  i,
                                  ctypes.byref(NAME),
                                  ctypes.byref(LEN))
            if ErrNo1 != 0:
                error_msg = "API ErrNo {0}:{1}".format(
                    ErrNo1.value, DLLErrorKeys[ErrNo1.value])
                raise Exception(error_msg)
            self.LinkIDs[str(NAME.value)] = i

    def _get_PollutantIDs(self):
        """Generates member Element IDs dictionary for Pollutants."""
        self.PollutantIDs = {}
        for i in range(self.get_ProjectSize(SMO_elementCount.pollutantCount)):
            NAME = ctypes.create_string_buffer(46)
            LEN = ctypes.c_int(46)
            ErrNo1 = self._getIDs(self.smoapi,
                                  SMO_elementType.SM_sys,
                                  i,
                                  ctypes.byref(NAME),
                                  ctypes.byref(LEN))
            if ErrNo1 != 0:
                error_msg = "API ErrNo {0}:{1}".format(
                    ErrNo1.value, DLLErrorKeys[ErrNo1.value])
                raise Exception(error_msg)
            self.PollutantIDs[str(NAME.value)] = i

    def get_IDs(self, SMO_elementIDType):
        """
        Returns List Type of Element IDs.

        :param int SMO_elementCount: element ID type :doc:`/keyrefs`

        :return: list ordered List of IDs
        :rtype: list

        Examples:

        >>> OutputFile = SWMMBinReader()
        >>> OutputFile.OpenBinFile(r"C:\\PROJECTCODE\\SWMMOutputAPI\\testing\\outputfile.out")
        >>> Test.get_IDs(SM_subcatch)
        >>> ['S3', 'S2', 'S1']
        >>> Test.get_IDs(SM_node)
        >>> ['J4', 'J1', 'J2', 'J3']
        >>> Test.get_IDs(SM_link)
        >>> ['C3', 'C2', 'C1']
        """
        if SMO_elementIDType == SMO_elementType.subcatchCount:
            if not hasattr(self, 'SubcatchmentIDs'):
                self._get_SubcatchIDs()
            IDlist = self.SubcatchmentIDs.keys()
        elif SMO_elementIDType == SMO_elementType.SM_node:
            if not hasattr(self, 'NodeIDs'):
                self._get_NodeIDs()
            IDlist = self.NodeIDs.keys()
        elif SMO_elementIDType == SMO_elementType.SM_link:
            if not hasattr(self, 'LinkIDs'):
                self._get_LinkIDs()
            IDlist = self.LinkIDs.keys()
        elif SMO_elementIDType == SMO_elementType.SM_sys:
            if not hasattr(self, 'PollutantIDs'):
                self._get_PollutantIDs()
            IDlist = self.PollutantIDs.keys()
        else:
            error_msg = "SMO_elementType: {} Outside Valid Types".format(
                SMO_elementType)
            raise Exception(error_msg)
            return 0

        # Do not sort lists
        return IDlist

    def get_Units(self, unit):
        """
        Returns flow units and Concentration.

        :param int SMO_unit: element ID type :doc:`/keyrefs`

        :return: Unit Type
        :rtype: str

        Examples:

        >>> OutputFile = SWMMBinReader()
        >>> OutputFile.OpenBinFile(r"C:\\PROJECTCODE\\SWMMOutputAPI\\testing\\outputfile.out")
        >>> OutputFile.get_Units(flow_rate)
        >>> 'CFS'
        """
        FlowUnitsType = [
            'CFS',  # cubic feet per second
            'GPM',  # gallons per minute
            'MGD',  # million gallons per day
            'CMS',  # cubic meters per second
            'LPS',  # liters per second
            'MLD',  # million liters per day
            ]

        ConcUnitsType = [
            'mg',  # Milligrams / L
            'ug',  # Micrograms / L
            'COUNT',  # Counts / L
            ]

        x = ctypes.c_int()
        ErrNo1 = self._getUnits(self.smoapi,
                                SMO_unit,
                                ctypes.byref(x))
        if ErrNo1 != 0:
            error_msg = "API ErrNo {0}:{1}".format(ErrNo1,
                                                   DLLErrorKeys[ErrNo1])
            raise Exception(error_msg)
        if unit == SMO_unit.flow_rate:
            return FlowUnitsType[x.value]
        elif unit == SMO_unit.concentration:
            return ConcUnitsType[x.value]
        else:
            error_msg = "SMO_unit: {} Outside Valid Types".format(unit)
            raise Exception(error_msg)

    def get_Times(self, SMO_timeElementType):
        """
        Returns report and simulation time related parameters.

        :param int SMO_timeElementType: element ID type :doc:`/keyrefs`

        :return: Report Step (seconds) or Number of Time Steps
        :rtype: int

        Examples:

        >>> OutputFile = SWMMBinReader()
        >>> OutputFile.OpenBinFile(r"C:\\PROJECTCODE\\SWMMOutputAPI\\testing\\outputfile.out")
        >>> OutputFile.get_Times(reportStep)
        >>> 300
        """
        timeElement = ctypes.c_int()
        ErrNo1 = self._getTimes(self.smoapi,
                                SMO_timeElementType,
                                ctypes.byref(timeElement))
        if ErrNo1 != 0:
            error_msg = "API ErrNo {0}:{1}".format(ErrNo1,
                                                   DLLErrorKeys[ErrNo1])
            raise Exception(error_msg)
        return timeElement.value

    def _get_StartTimeSWMM(self):
        """Returns the simulation start datetime as double."""
        StartTime = ctypes.c_double()
        ErrNo1 = self._getStartTime(self.smoapi, ctypes.byref(StartTime))
        if ErrNo1 != 0:
            error_msg = "API ErrNo {0}:{1}".format(ErrNo1,
                                                   DLLErrorKeys[ErrNo1])
            raise Exception(error_msg)
        return StartTime.value

    def get_StartTime(self):
        """
        Uses SWMM5 Conversion Functions to Pull DateTime String.

        This converts to Python datetime format.

        :return: Simulation start time.
        :rtype: datetime

        Examples:

        >>> OutputFile = SWMMBinReader()
        >>> OutputFile.OpenBinFile(r"C:\\PROJECTCODE\\SWMMOutputAPI\\testing\\outputfile.out")
        >>> OutputFile.get_StartTime()
        >>> datetime.datetime(2016,10,4,12,4,0)
        """
        _StartTime = self._get_StartTimeSWMM()
        _date = int(_StartTime)
        _time = _StartTime - _date

        # Pull Date String
        DateStr = ctypes.create_string_buffer(50)
        self.SWMMdateToStr(ctypes.c_double(_date), ctypes.byref(DateStr))
        DATE = DateStr.value

        # Pull Time String
        TimeStr = ctypes.create_string_buffer(50)
        self.SWMMtimeToStr(ctypes.c_double(_time), ctypes.byref(TimeStr))
        TIME = TimeStr.value
        DTime = datetime.strptime(DATE + ' ' + TIME, '%Y-%b-%d %H:%M:%S')
        return DTime

    def get_TimeSeries(self):
        """
        Gets simulation start time and builds timeseries array based step.

        :return: Simulation time series.
        :rtype: list of datetime

        Examples:

        >>> OutputFile = SWMMBinReader()
        >>> OutputFile.OpenBinFile(r"C:\\PROJECTCODE\\SWMMOutputAPI\\testing\\outputfile.out")
        >>> OutputFile.get_TimeSeries()
        >>> [datetime.datetime(2015, 11, 29, 14, 0), datetime.datetime(2015, 11, 29, 14, 1), ..., datetime.datetime(2015, 11, 29, 14, 9)]
        """
        return [self.get_StartTime() +
                timedelta(seconds=ind*self.get_Times(SMO_time.reportStep))
                for ind in range(self.get_Times(SMO_time.numPeriods))]

    def get_ProjectSize(self, SMO_elementCount):
        """
        Returns number of elements of a specific element type.

        :param int SMO_elementCount: element ID type :doc:`/keyrefs`

        :return: Number of Objects
        :rtype: int

        Examples:

        >>> OutputFile = SWMMBinReader()
        >>> OutputFile.OpenBinFile(r"C:\\PROJECTCODE\\SWMMOutputAPI\\testing\\outputfile.out")
        >>> OutputFile.get_ProjectSize(nodeCount)
        >>> 10
        """
        numel = ctypes.c_int()
        ErrNo1 = self._getProjectSize(self.smoapi,
                                      SMO_elementCount,
                                      ctypes.byref(numel))
        if ErrNo1 != 0:
            error_msg = "API ErrNo {0}:{1}".format(ErrNo1,
                                                   DLLErrorKeys[ErrNo1])
            raise Exception(error_msg)
        return numel.value

    def get_Series(self,
                   element_type,
                   SMO_Attribute,
                   IDName=None,
                   TimeStartInd=0,
                   TimeEndInd=-1):
        """
        Get time series results for particular attribute for an object.

        Specify series start and length using TimeStartInd and TimeEndInd
        respectively.

        :param int SMO_elementType: Element type :doc:`/keyrefs`.
        :param int SMO_Attribute: Attribute Type :doc:`/keyrefs`.
        :param str IDName: Element ID name (Default is None for to reach sys variables) (ID Names are case sensitive).
        :param int TimeStartInd: Starting index for the time series data period (default is 0).
        :param int TimeEndInd: Array index for the time series data period (defualt is -1 for end).

        :return: data series
        :rtype: list

        Examples:

        >>> OutputFile = SWMMBinReader()
        >>> OutputFile.OpenBinFile(r"C:\\PROJECTCODE\\SWMMOutputAPI\\testing\\outputfile.out")
        >>> OutputFile.get_Series(SM_subcatch, runoff_rate, 'S3', 0, 50)
        >>> [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, .... 0.0]

        >>> OutputFile.get_Series(SM_node, invert_depth, 'J1', 0, 50)
        >>> [3.908519983291626, 4.6215434074401855, 4.594745635986328, 4.595311641693115, ...,  4.595311641693115]

        >>> OutputFile.get_Series(SM_link, rainfall_subcatch, 'C2', 0, 50)
        >>> [10.2869873046875, 10.04793643951416, 9.997148513793945, 10.000744819641113, ..., 10.011372566223145]

        >>> OutputFile.get_Series(SM_sys, rainfall_system, TimeStartInd = 0, TimeEndInd = 50)
        >>> [0.017500000074505806, 0.017500000074505806, 0.017500000074505806, 0.017500000074505806, ..., 0.017500000074505806]        
        """        
        if TimeEndInd > self.get_Times(SMO_time.numPeriods):
            raise Exception("Outside Number of TimeSteps")
        elif TimeEndInd == -1:
            TimeEndInd = self.get_Times(SMO_time.numPeriods) + 1 - TimeEndInd

        sLength = ctypes.c_int()
        ErrNo1 = ctypes.c_int()
        SeriesPtr = self._newOutValueSeries(self.smoapi,
                                            TimeStartInd,
                                            TimeEndInd,
                                            ctypes.byref(sLength),
                                            ctypes.byref(ErrNo1))
        if ErrNo1.value != 0:
            error_msg = "API ErrNo {0}:{1}".format(
                ErrNo1.value, DLLErrorKeys[ErrNo1.value])
            raise Exception(error_msg)

        if element_type == SMO_elementType.SM_subcatch:
            if not hasattr(self, 'SubcatchmentIDs'):
                self._get_SubcatchIDs()
            ErrNo2 = self._getSubcatchSeries(self.smoapi,
                                             self.SubcatchmentIDs[IDName],
                                             SMO_Attribute,
                                             TimeStartInd, sLength.value,
                                             SeriesPtr)
        elif element_type == SMO_elementType.SM_node:
            if not hasattr(self, 'NodeIDs'):
                self._get_NodeIDs()
            ErrNo2 = self._getNodeSeries(self.smoapi,
                                         self.NodeIDs[IDName],
                                         SMO_Attribute,
                                         TimeStartInd,
                                         sLength.value,
                                         SeriesPtr)
        elif element_type == SMO_elementType.SM_link:
            if not hasattr(self, 'LinkIDs'):
                self._get_LinkIDs()
            ErrNo2 = self._getLinkSeries(self.smoapi,
                                         self.LinkIDs[IDName],
                                         SMO_Attribute,
                                         TimeStartInd,
                                         sLength.value,
                                         SeriesPtr)
        # Add Pollutants Later
        elif element_type == SMO_elementType.SM_sys:
            ErrNo2 = self._getSystemSeries(self.smoapi,
                                           SMO_Attribute,
                                           TimeStartInd,
                                           sLength.value,
                                           SeriesPtr)
        else:
            error_msg = "SMO_elementType: {} Outside Valid Types".format(
                SMO_elementType)
            raise Exception(error_msg)

        if ErrNo2 != 0:
            error_msg = "API ErrNo {0}:{1}".format(ErrNo2,
                                                   DLLErrorKeys[ErrNo2])
            raise Exception(error_msg)

        BldArray = [SeriesPtr[i] for i in range(sLength.value)]
        self._free(SeriesPtr)
        return BldArray

    def get_Attribute(self, element_type, SMO_Attribute, TimeInd):
        """
        Get results for attribute for elements at a specific time.

        :param int SMO_elementType: Element type :doc:`/keyrefs`.
        :param int SMO_Attribute: Attribute Type :doc:`/keyrefs`.
        :param int TimeInd: TimeInd

        :return: data list in order of the IDs of the SMO_elementType
        :rtype: list

        Examples:

        >>> OutputFile = SWMMBinReader()
        >>> OutputFile.OpenBinFile(r"C:\\PROJECTCODE\\SWMMOutputAPI\\testing\\outputfile.out")
        >>> OutputFile.get_Attribute(SM_subcatch, rainfall_subcatch, 0) 
        >>> [0.017500000074505806, 0.017500000074505806, 0.017500000074505806]

        >>> OutputFile.get_Attribute(SM_node, invert_depth, 10)
        >>> [4.596884250640869, 0.720202624797821, 0.6315776705741882, 0.6312257051467896]

        >>> OutputFile.get_Attribute(SM_link, flow_rate_link, 50)
        >>> [9.00419807434082, 10.011459350585938, 11.020767211914062]
        """
        if TimeInd > self.get_Times(SMO_time.numPeriods)-1:
            raise Exception("Outside Number of TimeSteps")

        aLength = ctypes.c_int()
        ErrNo1 = ctypes.c_int()            
        ValArrayPtr = self._newOutValueArray(self.smoapi,
                                             SMO_apiFunction.getAttribute,
                                             SMO_elementType,
                                             ctypes.byref(aLength),
                                             ctypes.byref(ErrNo1))
        if ErrNo1.value != 0:
            error_msg = "API ErrNo {0}:{1}".format(
                ErrNo1.value, DLLErrorKeys[ErrNo1.value])
            raise Exception(error_msg)

        if element_type == SMO_elementType.SM_subcatch:
            ErrNo2 = self._getSubcatchAttribute(self.smoapi,
                                                TimeInd,
                                                SMO_Attribute,
                                                ValArrayPtr)
        elif element_type == SMO_elementType.SM_link:
            ErrNo2 = self._getLinkAttribute(self.smoapi,
                                            TimeInd,
                                            SMO_Attribute,
                                            ValArrayPtr)
        elif element_type == SMO_elementType.SM_node:
            ErrNo2 = self._getNodeAttribute(self.smoapi,
                                            TimeInd,
                                            SMO_Attribute,
                                            ValArrayPtr)
        # Add Pollutants Later
        else:
            error_msg = "SMO_elementType: {} Outside Valid Types".format(
                SMO_elementType)
            raise Exception(error_msg)

        if ErrNo2 != 0:
            error_msg = "API ErrNo {0}:{1}".format(ErrNo2,
                                                   DLLErrorKeys[ErrNo2])
            raise Exception(error_msg)

        BldArray = [ValArrayPtr[i] for i in range(aLength.value)]
        self._free(ValArrayPtr)
        return BldArray

    def get_Result(self, element_type, TimeInd, IDName=None):
        """
        For a element ID at given time, get all attributes.

        :param int SMO_elementType: Element type :doc:`/keyrefs`.
        :param int TimeInd: Time Index
        :param int IDName: IDName (default None for System Variables)

        Examples:

        >>> OutputFile = SWMMBinReader()
        >>> OutputFile.OpenBinFile(r"C:\\PROJECTCODE\\SWMMOutputAPI\\testing\\outputfile.out")
        >>> OutputFile.get_Result(SM_subcatch,3000,'S3')
        >>> [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

        >>> OutputFile.get_Result(SM_node,3000,'J1')
        >>> [4.594789505004883, 25.322790145874023, 0.0, 9.000000953674316, 9.000000953674316, 0.0]

        >>> OutputFile.get_Result(SM_link,9000,'C3')
        >>> [11.0, 0.6312892436981201, 12.93112564086914, 185.72474670410156, 0.270773708820343]

        >>> OutputFile.get_Result(SM_sys,3000,'S3')
        >>> [70.0, 0.0, 0.0, 0.0, 0.0, 8.0, 0.0, 0.0, 3.0, 11.0, 0.0, 11.000021934509277, 532.2583618164062, 0.0, 0.0]
        """
        if TimeInd > self.get_Times(SMO_time.numPeriods)-1:
            raise Exception("Outside Number of TimeSteps")

        alength = ctypes.c_int()
        ErrNo1 = ctypes.c_int()
        ValArrayPtr = self._newOutValueArray(self.smoapi,
                                             SMO_apiFunction.getResult,
                                             SMO_elementType,
                                             ctypes.byref(alength),
                                             ctypes.byref(ErrNo1))

        if element_type == SMO_elementType.SM_subcatch:
            if not hasattr(self, 'SubcatchmentIDs'):
                self._get_SubcatchIDs()
            ErrNo2 = self._getSubcatchResult(self.smoapi,
                                             TimeInd,
                                             self.SubcatchmentIDs[IDName],
                                             ValArrayPtr)
        elif element_type == SMO_elementType.SM_node:
            if not hasattr(self, 'NodeIDs'):
                self._get_NodeIDs()
            ErrNo2 = self._getNodeResult(self.smoapi,
                                         TimeInd,
                                         self.NodeIDs[IDName],
                                         ValArrayPtr)
        elif element_type == SMO_elementType.SM_link:
            if not hasattr(self, 'LinkIDs'):
                self._get_LinkIDs()
            ErrNo2 = self._getLinkResult(self.smoapi,
                                         TimeInd,
                                         self.LinkIDs[IDName],
                                         ValArrayPtr)
        # Add Pollutants Later
        elif element_type == SMO_elementType.SM_sys:
            # This is not used?
            ErrNo2 = self._getSystemResult(self.smoapi, TimeInd, ValArrayPtr)
        else:
            error_msg = "SMO_elementType: {} Outside Valid Types".format(
                element_type)
            raise Exception(error_msg)

        BldArray = [ValArrayPtr[i] for i in range(alength.value)]
        self._free(ValArrayPtr)
        return BldArray


if __name__ in "__main__":
    # Run Tests

    # Open
    path = r"C:\PROJECTCODE\SWMMOutputAPI\testing\OutputTestModel522_SHORT.out"
    Test = SWMMBinReader()
    Test.OpenBinFile(path)

    # Get IDs
    print("\nProject Element ID Info")
    print(Test.get_IDs(SMO_elementType.SM_subcatch))
    print(Test.get_IDs(SMO_elementType.SM_node))
    print(Test.get_IDs(SMO_elementType.SM_link))

    print("\nGet Units")
    print('flow_rate: {}'.format(Test.get_Units(SMO_unit.flow_rate)))
    print('concentration: {}'.format(Test.get_Units(SMO_unit.concentration)))

    # Get Project Size
    print("\nProject Size Info")
    print("Subcatchments: {}".format(Test.get_ProjectSize(SMO_elementCount.subcatchCount)))
    print("Nodes: {}".format(Test.get_ProjectSize(SMO_elementCount.nodeCount)))
    print("Links: {}".format(Test.get_ProjectSize(SMO_elementCount.linkCount)))
    print("Pollutants: {}".format(Test.get_ProjectSize(SMO_elementCount.pollutantCount)))

    # Project Time Steps
    print("\nProject Time Info")
    print("Report Step: {}".format(Test.get_Times(SMO_time.reportStep)))
    print("Periods: {}".format(Test.get_Times(SMO_time.numPeriods)))

    # Get Time Series
    print("\nGet Time Series")
    TimeSeries = Test.get_TimeSeries()
    print(TimeSeries[:10])

    # Get Series
    print("\nSeries Tests")
    SubcSeries = Test.get_Series(SMO_elementType.SM_subcatch,
                                 SMO_systemAttribute.runoff_rate, 'S3', 0, 50)
    print(SubcSeries)
    NodeSeries = Test.get_Series(SMO_elementType.SM_node,
                                 SMO_systemAttribute.invert_depth, 'J1', 0, 50)
    print(NodeSeries)
    LinkSeries = Test.get_Series(SMO_elementType.SM_link,
                                 SMO_systemAttribute.rainfall_subcatch,
                                 'C2', 0, 50)
    print(LinkSeries)
    SystSeries = Test.get_Series(SMO_elementType.SM_sys,
                                 SMO_systemAttribute.rainfall_system,
                                 TimeStartInd=0, TimeEndInd=50)
    print(SystSeries)

    # Get Attributes
    print("\nAttributes Tests")
    # Check Values.. Might be issue here
    SubcAttributes = Test.get_Attribute(SMO_elementType.SM_subcatch,
                                        SMO_systemAttribute.rainfall_subcatch,
                                        0)
    print(SubcAttributes)
    NodeAttributes = Test.get_Attribute(SMO_elementType.SM_node,
                                        SMO_systemAttribute.invert_depth, 10)
    print(NodeAttributes)
    LinkAttributes = Test.get_Attribute(SMO_elementType.SM_link,
                                        SMO_systemAttribute.flow_rate_link, 50)
    print(LinkAttributes)

    # Get Results
    print("\nResult Tests")
    SubcResults = Test.get_Result(SMO_elementType.SM_subcatch, 3000, 'S3')
    print(SubcResults)
    NodeResults = Test.get_Result(SMO_elementType.SM_node, 3000, 'J1')
    print(NodeResults)
    LinkResults = Test.get_Result(SMO_elementType.SM_link, 9000, 'C3')
    print(LinkResults)
    SystResults = Test.get_Result(SMO_elementType.SM_sys, 3000, 'S3')
    print(SystResults)

    # Close Output File
    Test.CloseBinFile()
    help(SWMMBinReader)
