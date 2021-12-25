# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2021 Jennifer Wu
#
# Licensed under the terms of the BSD2 License
# See LICENSE.txt for details
# -----------------------------------------------------------------------------
from pyswmm.errors import OutputException
from datetime import datetime, timedelta
from functools import wraps
from typing import NoReturn, Optional, Union

# Third party imports
from swmm.toolkit import output, shared_enum
from julian import from_jd


def output_open_handler(func):
    """
    Checks if output file is open before running function.

    :param func : function method of Output class
    """

    @wraps(func)
    def inner_function(self, *args, **kwargs):
        if not self.loaded:
            self.open()

        return func(self, *args, **kwargs)

    return inner_function


class Output(object):
    def __init__(self, binfile):
        """
        Base class for a SWMM Output binary file.

        The output object provides several options to process timeseries within output binary file.

        Initialize the Output class.
        :param binfile: model binary file path
        """
        self.binfile = binfile

        self.handle = None
        self.loaded = False
        self.delete_handle = False
        self.period = None
        self.report = None
        self.start = None
        self.end = None
        self._times = None

        self._project_size = None
        self._subcatchments = None
        self._nodes = None
        self._links = None
        self._pollutants = None

    @staticmethod
    def verify_index(index, index_dict, index_type):
        """
        Validate the index of a model element passed to Output methods. Used to
        convert model element names to their index in the out file.

        :param index: The name or index of the model element listed in the index_dict dict
        :type index: Union[str, int]
        :param index_dict: The dict against which to validate the index
                           (one of self.nodes, self.links, self.subcatchments)
        :type index_dict: dict
        :param index_type: The type of model element (e.g. node, link, etc.)
                           Only used to print the exception if an attribute cannot be found
        :type index_type: str
        :raises OutputException: Exception if element cannot be found in dict
        :return: The integer index of the requested element
        :rtype: int
        """

        arg_index = index

        if isinstance(index, str):
            index = index_dict.get(index, None)

        if index is None:
            raise OutputException(
                f"{index_type} ID: {arg_index} does not exist in model output."
            )

        return index

    @staticmethod
    def verify_time(
        time_index: Optional[Union[datetime, int]],
        time_list: list,
        start: datetime,
        end: datetime,
        report: int,
        default_time: Union[datetime, int],
    ) -> int:
        """
        Validate time parameter passed to Output methods. Used to convert a datetime value to
        the period index in model time.

        :param time_index: The datetime to validate
        :type time_index: Optional[Union[datetime, int]]
        :param time_list: A list of datetimes against which to validate time_index
        :type time_list: list
        :param start: The starting datetime in the out file
                      (only used to print the exception if the datetime cannot be found)
        :type start: datetime
        :param end: The ending datetime in the out file
                    (only used to print the exception if the datetime cannot be found)
        :type end: datetime
        :param report: The reporting interval in the out file
                       (only used to print the exception if the datetime cannot be found)
        :type report: int
        :param default_time: The default time_index to use of time_index is None
        :type default_time: Union[datetime, int]
        :raises OutputException: Exception raised of time_index cannot be found intime_index
        :return: The integer index of the datetime given
        :rtype: int
        """

        arg_time_index = time_index

        if time_index is None:
            time_index = default_time
        else:
            if isinstance(time_index, datetime):
                if time_index in time_list:
                    time_index = time_list.index(time_index)
                else:
                    time_index = None

            if time_index is None:
                datetime_format = "%Y-%m-%d %H:%M:%S"
                msg = f"{arg_time_index} does not exist in model output reporting time steps."
                msg += (
                    f" The reporting time range is {start.strftime(datetime_format)} to "
                    f"{end.strftime(datetime_format)} at increments of "
                    f"{report} seconds."
                )
                raise OutputException(msg)

        return time_index

    def open(self) -> bool:
        """
        Open a binary file

        :return: True if binary file was opened successfully
        :rtype: bool
        """
        if self.handle is None:
            self.handle = output.init()

        if not self.loaded:
            self.loaded = True
            output.open(self.handle, self.binfile)
            self.start = from_jd(output.get_start_date(self.handle) + 2415018.5)
            self.start = self.start.replace(microsecond=0)
            self.report = output.get_times(self.handle, shared_enum.Time.REPORT_STEP)
            self.period = output.get_times(self.handle, shared_enum.Time.NUM_PERIODS)
            self.end = self.start + timedelta(seconds=self.period * self.report)

        return True

    def close(self) -> bool:
        """
        Close an opened binary file

        :returns: True if binary file was closed successfully
        :rtype: bool
        """
        if self.handle or self.loaded:
            self.loaded = False
            self.delete_handle = True
            output.close(self.handle)

        return True

    # method used for context manager with statement
    def __enter__(self):
        self.open()
        return self

    # method used for context manager with statement
    def __exit__(self, *arg) -> NoReturn:
        self.close()

    @property
    def times(self) -> list:
        """
        Returns list of reporting timestep stored in model binary file

        :returns: list of datetime values for each reporting timestep
        :rtype: list
        """
        if self._times is None:
            self._load_times()
        return self._times

    @output_open_handler
    def _load_times(self) -> NoReturn:
        """Load model reporting times into self._times"""
        self._times = list()
        for step in range(1, self.period + 1):
            self._times.append(self.start + timedelta(seconds=self.report) * step)

    @property
    def project_size(self) -> list:
        """
        Returns project size for model elements in the following order:
        [subcatchment, node, link, system, pollutant]

        :returns: list of numbers of each model type
                  [nSubcatchments, nNodes, nLinks, nSystems(1), nPollutants]
        :rtype: list
        """
        if self._project_size is None:
            self._load_project_size()
        return self._project_size

    @output_open_handler
    def _load_project_size(self) -> NoReturn:
        """Load model size into self._project_size"""
        self._project_size = output.get_proj_size(self.handle)

    @property
    def subcatchments(self) -> dict:
        """
        Return a dict of subcatchments stored in SWMM output binary file

        :returns: dict of model subcatchment names with their indices as values
        :rtype: dict
        """
        if self._subcatchments is None:
            self._load_subcatchments()
        return self._subcatchments

    @output_open_handler
    def _load_subcatchments(self) -> NoReturn:
        """Load model size into self._project_size"""
        total = self.project_size[0]
        self._subcatchments = {
            self.object_name(shared_enum.ElementType.SUBCATCH, index): index
            for index in range(total)
        }

    @property
    def nodes(self) -> dict:
        """
        Return a dict of nodes stored in SWMM output binary file

        :returns: dict of model node names with their indices as values
        :rtype: dict
        """
        if self._nodes is None:
            self._load_nodes()
        return self._nodes

    @output_open_handler
    def _load_nodes(self) -> NoReturn:
        """Load model nodes into self._nodes"""
        total = self.project_size[1]
        self._nodes = {
            self.object_name(shared_enum.ElementType.NODE, index): index
            for index in range(total)
        }

    @property
    def links(self) -> dict:
        """Return a dict of links stored in SWMM output binary file

        :returns: dict of model link names with their indices as values
        :rtype: dict
        """
        if self._links is None:
            self._load_links()
        return self._links

    @output_open_handler
    def _load_links(self) -> NoReturn:
        """Load model links into self._links"""
        total = self.project_size[2]
        self._links = {
            self.object_name(shared_enum.ElementType.LINK, index): index
            for index in range(total)
        }

    @property
    def pollutants(self) -> dict:
        """
        Return a dict of pollutants stored in SWMM output binary file

        :returns: dict of pollutant names with their indices as values
        :rtype: dict
        """
        if self._pollutants is None:
            self._load_pollutants()
        return self._pollutants

    @output_open_handler
    def _load_pollutants(self) -> NoReturn:
        """Load model size into self._project_size"""
        total = self.project_size[4]
        self._pollutants = {
            self.object_name(shared_enum.ElementType.POLLUT, index): index
            for index in range(total)
        }

    @property
    @output_open_handler
    def unit(self) -> int:
        """
        Return SWMM output binary file unit type from swmm.toolkit.shared_enum.UnitSystem

        :returns: integer indicating unit system (0 = US, 1 = SI)
        :rtype: int
        """
        return output.get_units(self.handle)

    @property
    @output_open_handler
    def version(self) -> int:
        """
        Return SWMM version used to generate SWMM output binary file results

        :returns: integer representation of SWMM version used to make out file
        :rtype: int
        """
        return output.get_version(self.handle)

    @output_open_handler
    def object_name(self, object_type: int, index: int) -> str:
        """
        Get object name from SWMM output binary file using object index and object type

        :param object_type: object type from swmm.toolkit.shared_enum.ElementType
        :type object_type: int
        :param index: object index
        :type index: int
        :returns: object name
        :rtype: str
        """
        return output.get_elem_name(self.handle, object_type, index)

    @output_open_handler
    def subcatch_series(
        self,
        index: Union[int, str],
        attribute: shared_enum.SubcatchAttribute,
        start_index: Union[int, datetime, None] = None,
        end_index: Union[int, datetime, None] = None,
    ) -> dict:
        """
        Get subcatchment time series results for particular attribute. Specify series
        start index and end index to get desired time range.
        Note: you can use pandas to convert dict to a pandas Series object with dict keys as index
        :param index: subcatchment index or name
        :type index: Union[int, str]
        :param attribute: attribute from swmm.toolkit.shared_enum.SubcatchAttribute
        :type attribute: swmm.toolkit.shared_enum.SubcatchAttribute
        :param start_index: start datetime or index from which to return series, defaults to None
        :type start_index: Union[int, datetime, None], optional
        :param end_index: end datetime or index from which to return series, defaults to None
        :type end_index: Union[int, datetime, None], optional
        :return: dict of attribute values with between start_index and end_index
                 with reporting timesteps as keys {datetime : value}
        :rtype: dict
        """
        index = self.verify_index(index, self.subcatchments, "subcatchment")
        start_index = self.verify_time(
            start_index, self.times, self.start, self.end, self.report, 0
        )
        end_index = self.verify_time(
            end_index, self.times, self.start, self.end, self.report, self.period
        )

        values = output.get_subcatch_series(
            self.handle, index, attribute, start_index, end_index
        )
        return {
            time: value
            for time, value in zip(self.times[start_index:end_index], values)
        }

    @output_open_handler
    def node_series(
        self,
        index: Union[int, str],
        attribute: shared_enum.NodeAttribute,
        start_index: Union[int, datetime, None] = None,
        end_index: Union[int, datetime, None] = None,
    ) -> dict:
        """
        Get node time series results for particular attribute. Specify series
        start index and end index to get desired time range.
        Note: you can use pandas to convert dict to a pandas Series object with dict keys as index
        :param index: node index or name
        :type index: Union[int, str]
        :param attribute: attribute from swmm.toolkit.shared_enum.NodeAttribute
        :type attribute: swmm.toolkit.shared_enum.NodeAttribute
        :param start_index: start datetime or index from which to return series, defaults to None
        :type start_index: Union[int, datetime, None], optional
        :param end_index: end datetime or index from which to return series, defaults to None
        :type end_index: Union[int, datetime, None], optional
        :return: dict of attribute values with between start_index and end_index
                 with reporting timesteps as keys
        :rtype: dict {datetime : value}
        """

        index = self.verify_index(index, self.nodes, "node")
        start_index = self.verify_time(
            start_index, self.times, self.start, self.end, self.report, 0
        )
        end_index = self.verify_time(
            end_index, self.times, self.start, self.end, self.report, self.period
        )

        values = output.get_node_series(
            self.handle, index, attribute, start_index, end_index
        )
        return {
            time: value
            for time, value in zip(self.times[start_index:end_index], values)
        }

    @output_open_handler
    def link_series(
        self,
        index: Union[int, str],
        attribute: shared_enum.LinkAttribute,
        start_index: Union[int, datetime, None] = None,
        end_index: Union[int, datetime, None] = None,
    ) -> dict:
        """
        Get link time series results for particular attribute. Specify series
        start index and end index to get desired time range.

        Note: you can use pandas to convert dict to a pandas Series object with dict keys as index

        :param index: link index or name
        :type index: Union[int, str]
        :param attribute: attribute from swmm.toolkit.shared_enum.LinkAttribute
        :type attribute: swmm.toolkit.shared_enum.LinkAttribute
        :param start_index: start datetime or index from which to return series, defaults to None
        :type start_index: Union[int, datetime, None], optional
        :param end_index: end datetime or index from which to return series, defaults to None
        :type end_index: Union[int, datetime, None], optional
        :return: dict of attribute values with between start_index and end_index
                 with reporting timesteps as keys
        :rtype: dict {datetime : value}
        """
        index = self.verify_index(index, self.links, "link")
        start_index = self.verify_time(
            start_index, self.times, self.start, self.end, self.report, 0
        )
        end_index = self.verify_time(
            end_index, self.times, self.start, self.end, self.report, self.period
        )

        values = output.get_link_series(
            self.handle, index, attribute, start_index, end_index
        )
        return {
            time: value
            for time, value in zip(self.times[start_index:end_index], values)
        }

    @output_open_handler
    def system_series(
        self,
        attribute: shared_enum.SystemAttribute,
        start_index: Union[int, datetime, None] = None,
        end_index: Union[int, datetime, None] = None,
    ) -> dict:
        """
        Get system time series results for particular attribute. Specify series
        start index and end index to get desired time range.

        Note: you can use pandas to convert dict to a pandas Series object with dict keys as index

        :param attribute: attribute from swmm.toolkit.shared_enum.SystemAttribute
        :type attribute: swmm.toolkit.shared_enum.SystemAttribute
        :param start_index: start datetime or index from which to return series, defaults to None
        :type start_index: Union[int, datetime, None], optional
        :param end_index: end datetime or index from which to return series, defaults to None
        :type end_index: Union[int, datetime, None], optional
        :return: dict of attribute values with between start_index and end_index
                 with reporting timesteps as keys
        :rtype: dict {datetime : value}
        """
        start_index = self.verify_time(
            start_index, self.times, self.start, self.end, self.report, 0
        )
        end_index = self.verify_time(
            end_index, self.times, self.start, self.end, self.report, self.period
        )

        values = output.get_system_series(
            self.handle, attribute, start_index, end_index
        )
        return {
            time: value
            for time, value in zip(self.times[start_index:end_index], values)
        }

    @output_open_handler
    def subcatch_attribute(
        self,
        attribute: shared_enum.SubcatchAttribute,
        time_index: Union[int, datetime, None] = None,
    ) -> dict:
        """
        For all subcatchments at given time, get a particular attribute.

        :param attribute: attribute from swmm.toolkit.shared_enum.SubcatchAttribute
        :type attribute: swmm.toolkit.shared_enum.SubcatchAttribute
        :param time_index: datetime or simulation index, defaults to None
        :type time_index: Union[int, datetime, None]
        :returns: dict of attribute value for all subcatchments at given timestep
        :rtype: dict {subcatchment: value}
        """

        time_index = self.verify_time(
            time_index, self.times, self.start, self.end, self.report, 0
        )

        values = output.get_subcatch_attribute(self.handle, time_index, attribute)
        return {sub: value for sub, value in zip(self.subcatchments, values)}

    @output_open_handler
    def node_attribute(
        self,
        attribute: shared_enum.NodeAttribute,
        time_index: Union[int, datetime, None] = None,
    ) -> dict:
        """
        For all nodes at given time, get a particular attribute.

        :param attribute: attribute from swmm.toolkit.shared_enum.NodeAttribute
        :type attribute: swmm.toolkit.shared_enum.NodeAttribute
        :param time_index: datetime or simulation index, defaults to None
        :type time_index: Union[int, datetime, None]
        :returns: dict of attribute values for all nodes at given timestep
        :rtype: dict {node:value}
        """

        time_index = self.verify_time(
            time_index, self.times, self.start, self.end, self.report, 0
        )

        values = output.get_node_attribute(self.handle, time_index, attribute)
        return {node: value for node, value in zip(self.nodes, values)}

    @output_open_handler
    def link_attribute(
        self,
        attribute: shared_enum.LinkAttribute,
        time_index: Union[int, datetime, None] = None,
    ):
        """
        For all links at given time, get a particular attribute.

         :param attribute: attribute from swmm.toolkit.shared_enum.LinkAttribute
        :type attribute: swmm.toolkit.shared_enum.LinkAttribute
        :param time_index: datetime or simulation index, defaults to None
        :type time_index: Union[int, datetime, None]
        :returns: dict of attribute values for all nodes at given timestep
        :rtype: dict {link : value}
        """

        time_index = self.verify_time(
            time_index, self.times, self.start, self.end, self.report, 0
        )

        values = output.get_link_attribute(self.handle, time_index, attribute)
        return {link: value for link, value in zip(self.links, values)}

    @output_open_handler
    def system_attribute(
        self,
        attribute: shared_enum.SystemAttribute,
        time_index: Union[int, datetime, None] = None,
    ):
        """
         At given time, get a particular system attribute.

        :param attribute: attribute from swmm.toolkit.shared_enum.SystemAttribute
         :type attribute: swmm.toolkit.shared_enum.SystemAttribute
         :param time_index: datetime or simulation index, defaults to None
         :type time_index: Union[int, datetime, None]
         :returns: dict of attribute value for system at given timestep
         :rtype: dict of {"system",value}
        """

        time_index = self.verify_time(
            time_index, self.times, self.start, self.end, self.report, 0
        )

        value = output.get_system_attribute(self.handle, time_index, attribute)
        return {"system": value}

    @output_open_handler
    def subcatch_result(
        self, index: Union[int, str], time_index: Union[int, datetime, None] = None
    ):
        """
        For a subcatchment at given time, get all attributes.

        :param index: subcatchment name or index
        :type index: Union[int, str]
        :param time_index: datetime or simulation index, defaults to None
        :type time_index: Union[int, datetime, None]
        :returns: dict of attributes for a subcatchment at given timestep
        :rtype: dict {attribute:value}
        """
        index = self.verify_index(index, self.subcatchments, "subcatchment")
        time_index = self.verify_time(
            time_index, self.times, self.start, self.end, self.report, 0
        )

        values = output.get_subcatch_result(self.handle, time_index, index)
        return {
            attr: value for attr, value in zip(shared_enum.SubcatchAttribute, values)
        }

    @output_open_handler
    def node_result(
        self, index: Union[int, str], time_index: Union[int, datetime, None] = None
    ):
        """
        For a node at given time, get all attributes.

        :param index: node name or index
        :type index: Union[int, str]
        :param time_index: datetime or simulation index, defaults to None
        :type time_index: Union[int, datetime, None]
        :returns: dict of attributes for a node at given timestep
        :rtype: dict {attribute:value}
        """
        index = self.verify_index(index, self.nodes, "node")
        time_index = self.verify_time(
            time_index, self.times, self.start, self.end, self.report, 0
        )

        values = output.get_node_result(self.handle, time_index, index)
        return {attr: value for attr, value in zip(shared_enum.NodeAttribute, values)}

    @output_open_handler
    def link_result(
        self, index: Union[int, str], time_index: Union[int, datetime, None] = None
    ):
        """
        For a link at given time, get all attributes.

        :param index: link name or index
        :type index: Union[int, str]
        :param time_index: datetime or simulation index, defaults to None
        :type time_index: Union[int, datetime, None]
        :returns: dict of attributes for a link at given timestep
        :rtype: dict {attribute:value}
        """
        index = self.verify_index(index, self.links, "link")
        time_index = self.verify_time(
            time_index, self.times, self.start, self.end, self.report, 0
        )

        values = output.get_link_result(self.handle, time_index, index)
        return {attr: value for attr, value in zip(shared_enum.LinkAttribute, values)}

    @output_open_handler
    def system_result(self, time_index: Union[int, datetime, None] = None):
        """
        At a given time, get all system attributes.

        :param time_index: datetime or simulation index, defaults to None
        :type time_index: Union[int, datetime, None]
        :returns: dict of attributes for the system at given timestep
        :rtype: dict {attribute:value}
        """
        dummy_index = 0
        time_index = self.verify_time(
            time_index, self.times, self.start, self.end, self.report, 0
        )

        values = output.get_system_result(self.handle, time_index, dummy_index)
        return {attr: value for attr, value in zip(shared_enum.SystemAttribute, values)}
