# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2021 Jennifer Wu
#
# Licensed under the terms of the BSD2 License
# See LICENSE.txt for details
# -----------------------------------------------------------------------------
from pyswmm.errors import OutputException
from datetime import datetime, timedelta

# Third party imports
from swmm.toolkit import output, shared_enum
from julian import from_jd


def output_open_handler(func):
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
        Validate index parameter passed to Output methods
        """
        arg_index = index

        if isinstance(index, str):
            index = index_dict.get(index, None)

        if index is None:
            raise OutputException(f"{index_type} ID: {arg_index} does not exist in model output.")

        return index

    @staticmethod
    def verify_time(time_index, time_list, start, end, report, default_time):
        """
        Validate time parameter passed to Output methods
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
                datetime_format = '%Y-%m-%d %H:%M:%S'
                msg = f"{arg_time_index} does not exist in model output reporting time steps."
                msg += f" The reporting time range is {start.strftime(datetime_format)} to " \
                       f"{end.strftime(datetime_format)} at increments of " \
                       f"{report} seconds."
                raise OutputException(msg)

        return time_index

    def open(self):
        """
        Open a binary file
        :return: if binary file was opened successfully
        :rtype: boolean
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

    def close(self):
        """
        Close an opened binary file
        :return: if binary file was closed successfully
        :rtype: boolean
        """
        if self.handle or self.loaded:
            self.loaded = False
            self.delete_handle = True
            output.close(self.handle)

        return True

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, *arg):
        self.close()

    @property
    def times(self):
        """
        Returns list of reporting timestep stored in model binary file
        :return: list of reporting timesteps
        :rtype: list
        """
        if self._times is None:
            self._times = list()
            for step in range(1, self.period + 1):
                self._times.append(self.start + timedelta(seconds=self.report) * step)
        return self._times

    @property
    def project_size(self):
        """
        Returns project size for model elements in the following order: [subcatchment, node, link, system, pollutant]
        :return: list of model elements sizes
        :rtype: list
        """
        if self._project_size is None:
            self._project_size = output.get_proj_size(self.handle)
        return self._project_size

    @property
    def subcatchments(self):
        """
        Return a list of subcatchments stored in SWMM output binary file
        """
        if self._subcatchments is None:
            self._subcatchments = dict()
            total = self.project_size[0]
            for index in range(total):
                name = self.object_name(shared_enum.ElementType.SUBCATCH, index)
                self._subcatchments[name] = index
        return self._subcatchments

    @property
    def nodes(self):
        """
        Return a list of nodes stored in SWMM output binary file
        """
        if self._nodes is None:
            self._nodes = dict()
            total = self.project_size[1]
            for index in range(total):
                name = self.object_name(shared_enum.ElementType.NODE, index)
                self._nodes[name] = index
        return self._nodes

    @property
    def links(self):
        """
        Return a list of links stored in SWMM output binary file
        """
        if self._links is None:
            self._links = dict()
            total = self.project_size[2]
            for index in range(total):
                name = self.object_name(shared_enum.ElementType.LINK, index)
                self._links[name] = index
        return self._links

    @property
    def pollutants(self):
        """
        Return a list of pollutants stored in SWMM output binary file
        """
        if self._pollutants is None:
            self._pollutants = dict()
            total = self.project_size[4]
            for index in range(total):
                name = self.object_name(shared_enum.ElementType.POLLUT, index)
                self._pollutants[name] = index
        return self._pollutants

    @output_open_handler
    def unit(self):
        """
        Return SWMM output binary file unit type from swmm.toolkit.shared_enum.UnitSystem
        """
        return output.get_units(self.handle)

    @output_open_handler
    def version(self):
        """
        Return SWMM version used to generate SWMM output binary file results
        """
        return output.get_version(self.handle)

    @output_open_handler
    def object_name(self, object_type, index):
        """
        Get object name from SWMM output binary file using object index and object type
        :param object_type: object type from swmm.toolkit.shared_enum.ElementType
        :param index: object index
        :return: object name
        :rtype: str
        """
        return output.get_elem_name(self.handle, object_type, index)

    @output_open_handler
    def subcatch_series(self, index, attribute, start_index=None, end_index=None):
        """
        Get subcatchment time series results for particular attribute. Specify series
        start index and end index to get desired time range.
        Note: you can use pandas to convert dict to a pandas Series object with dict keys as index
        :param index: subcatchment index
        :param attribute: attribute from swmm.toolkit.shared_enum.SubcatchAttribute
        :param start_index: start datetime index
        :param end_index: end datetime index
        :return: attribute values for a subcatchment between start_index and end_index
        :rtype: dict with reporting timesteps as keys
        """
        index = self.verify_index(index, self.subcatchments, 'subcatchment')
        start_index = self.verify_time(start_index, self.times, self.start, self.end, self.report, 0)
        end_index = self.verify_time(end_index, self.times, self.start, self.end, self.report, self.period)

        values = output.get_subcatch_series(self.handle, index, attribute, start_index, end_index)
        return {time: value for time, value in zip(self.times[start_index:end_index], values)}

    @output_open_handler
    def node_series(self, index, attribute, start_index=None, end_index=None):
        """
        Get node time series results for particular attribute. Specify series
        start index and end index to get desired time range.
        Note: you can use pandas to convert dict to a pandas Series object with dict keys as index
        :param index: node index
        :param attribute: attribute from swmm.toolkit.shared_enum.NodeAttribute
        :param start_index: start datetime index
        :param end_index: end datetime index
        :return: attribute values for a node between start_index and end_index
        :rtype: dict with reporting timesteps as keys
        """
        index = self.verify_index(index, self.nodes, 'node')
        start_index = self.verify_time(start_index, self.times, self.start, self.end, self.report, 0)
        end_index = self.verify_time(end_index, self.times, self.start, self.end, self.report, self.period)

        values = output.get_node_series(self.handle, index, attribute, start_index, end_index)
        return {time: value for time, value in zip(self.times[start_index:end_index], values)}

    @output_open_handler
    def link_series(self, index, attribute, start_index=None, end_index=None):
        """
        Get link time series results for particular attribute. Specify series
        start index and end index to get desired time range.
        Note: you can use pandas to convert dict to a pandas Series object with dict keys as index
        :param index: link index
        :param attribute: attribute from swmm.toolkit.shared_enum.NodeAttribute
        :param start_index: start datetime index
        :param end_index: end datetime index
        :return: attribute values for a link between start_index and end_index
        :rtype: dict with reporting timesteps as keys
        """
        index = self.verify_index(index, self.links, 'link')
        start_index = self.verify_time(start_index, self.times, self.start, self.end, self.report, 0)
        end_index = self.verify_time(end_index, self.times, self.start, self.end, self.report, self.period)

        values = output.get_link_series(self.handle, index, attribute, start_index, end_index)
        return {time: value for time, value in zip(self.times[start_index:end_index], values)}

    @output_open_handler
    def system_series(self, attribute, start_index=None, end_index=None):
        """
        Get system time series results for particular attribute. Specify series
        start index and end index to get desired time range.
        Note: you can use pandas to convert dict to a pandas Series object with dict keys as index
        :param attribute: attribute from swmm.toolkit.shared_enum.SystemAttribute
        :param start_index: start datetime index
        :param end_index: end datetime index
        :return: attribute values for system between start_index and end_index
        :rtype: dict with reporting timesteps as keys
        """
        start_index = self.verify_time(start_index, self.times, self.start, self.end, self.report, 0)
        end_index = self.verify_time(end_index, self.times, self.start, self.end, self.report, self.period)

        values = output.get_system_series(self.handle, attribute, start_index, end_index)
        return {time: value for time, value in zip(self.times[start_index:end_index], values)}

    @output_open_handler
    def subcatch_attribute(self, attribute, time_index=None):
        """
        For all subcatchments at given time, get a particular attribute.
        :param attribute: attribute from swmm.toolkit.shared_enum.SubcatchAttribute
        :param time_index: datetime index
        :return: attribute value for all subcatchments at given timestep
        :rtype: dict of all subcatchments for one attribute
        """
        time_index = self.verify_time(time_index, self.times, self.start, self.end, self.report, 0)

        values = output.get_subcatch_attribute(self.handle, time_index, attribute)
        return {sub: value for sub, value in zip(self.subcatchments, values)}

    @output_open_handler
    def node_attribute(self, attribute, time_index=None):
        """
        For all nodes at given time, get a particular attribute.
        :param attribute: attribute from swmm.toolkit.shared_enum.NodeAttribute
        :param time_index: datetime index
        :return: attribute value for all nodes at given timestep
        :rtype: dict of all nodes for one attribute
        """
        time_index = self.verify_time(time_index, self.times, self.start, self.end, self.report, 0)

        values = output.get_node_attribute(self.handle, time_index, attribute)
        return {node: value for node, value in zip(self.nodes, values)}

    @output_open_handler
    def link_attribute(self, attribute, time_index=None):
        """
        For all links at given time, get a particular attribute.
        :param attribute: attribute from swmm.toolkit.shared_enum.LinkAttribute
        :param time_index: datetime index
        :return: attribute value for all links at given timestep
        :rtype: dict of all links for one attribute
        """
        time_index = self.verify_time(time_index, self.times, self.start, self.end, self.report, 0)

        values = output.get_link_attribute(self.handle, time_index, attribute)
        return {link: value for link, value in zip(self.links, values)}

    @output_open_handler
    def system_attribute(self, attribute, time_index=None):
        """
        At given time, get a particular system attribute.
        :param attribute: attribute from swmm.toolkit.shared_enum.SystemAttribute
        :param time_index: datetime index
        :return: attribute value for system at given timestep
        :rtype: dict of system attribute
        """
        time_index = self.verify_time(time_index, self.times, self.start, self.end, self.report, 0)

        value = output.get_system_attribute(self.handle, time_index, attribute)
        return {'system': value}

    @output_open_handler
    def subcatch_result(self, index, time_index=None):
        """
        For a subcatchment at given time, get all attributes.
        :param index: subcatchment index
        :param time_index: datetime index
        :return: dict of attributes for a subcatchment at given timestep
        :rtype: dict
        """
        index = self.verify_index(index, self.subcatchments, 'subcatchment')
        time_index = self.verify_time(time_index, self.times, self.start, self.end, self.report, 0)

        values = output.get_subcatch_result(self.handle, time_index, index)
        return {attr: value for attr, value in zip(shared_enum.SubcatchAttribute, values)}

    @output_open_handler
    def node_result(self, index, time_index=None):
        """
        For a node at given time, get all attributes.
        :param index: node index
        :param time_index: datetime index
        :return: dict of attributes for a node at given timestep
        :rtype: dict
        """
        index = self.verify_index(index, self.nodes, 'node')
        time_index = self.verify_time(time_index, self.times, self.start, self.end, self.report, 0)

        values = output.get_node_result(self.handle, time_index, index)
        return {attr: value for attr, value in zip(shared_enum.NodeAttribute, values)}

    @output_open_handler
    def link_result(self, index, time_index=None):
        """
        For a link at given time, get all attributes.
        :param index: link index
        :param time_index: datetime index
        :return: dict of attributes for a link at given timestep
        :rtype: dict
        """
        index = self.verify_index(index, self.links, 'link')
        time_index = self.verify_time(time_index, self.times, self.start, self.end, self.report, 0)

        values = output.get_link_result(self.handle, time_index, index)
        return {attr: value for attr, value in zip(shared_enum.LinkAttribute, values)}

    @output_open_handler
    def system_result(self, time_index=None):
        """
        At a given time, get all system attributes.
        :param time_index: datetime index
        :return: dict of attributes for the system at given timestep
        :rtype: dict
        """
        dummy_index = 0
        time_index = self.verify_time(time_index, self.times, self.start, self.end, self.report, 0)

        values = output.get_system_result(self.handle, time_index, dummy_index)
        return {attr: value for attr, value in zip(shared_enum.SystemAttribute, values)}
