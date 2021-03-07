# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2021 Jennifer Wu
#
# Licensed under the terms of the BSD2 License
# See LICENSE.txt for details
# -----------------------------------------------------------------------------
from pyswmm.errors import OutputException
from pyswmm.toolkitapi import subcatch_attribute, node_attribute, link_attribute, system_attribute
from datetime import timedelta

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
        self.num_period = None
        self.report = None
        self.start_time = None
        self._times = None

        self._project_size = None
        self._subcatchments = None
        self._nodes = None
        self._links = None
        self._pollutants = None

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
            self.start_time = from_jd(output.get_start_date(self.handle) + 2415018.5)
            self.start_time = self.start_time.replace(microsecond=0)
            self.report = output.get_times(self.handle, shared_enum.Time.REPORT_STEP)
            self.num_period = output.get_times(self.handle, shared_enum.Time.NUM_PERIODS)

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
        if not self._times:
            self._times = list()
            for step in range(1, self.num_period + 1):
                self._times.append(self.start_time + timedelta(seconds=self.report) * step)
        return self._times

    @property
    def project_size(self):
        """
        Returns project size for model elements in the following order: [subcatchment, node, link, system, pollutant]
        :return: list of model elements sizes
        :rtype: list
        """
        if not self._project_size:
            self._project_size = output.get_proj_size(self.handle)
        return self._project_size

    @property
    def subcatchments(self):
        if not self._subcatchments:
            self._subcatchments = dict()
            total = self.project_size[0]
            for index in range(total):
                name = self.object_name(shared_enum.ElementType.SUBCATCH, index)
                self._subcatchments[name] = index
        return self._subcatchments

    @property
    def nodes(self):
        if not self._nodes:
            self._nodes = dict()
            total = self.project_size[1]
            for index in range(total):
                name = self.object_name(shared_enum.ElementType.NODE, index)
                self._nodes[name] = index
        return self._nodes

    @property
    def links(self):
        if not self._links:
            self._links = dict()
            total = self.project_size[2]
            for index in range(total):
                name = self.object_name(shared_enum.ElementType.LINK, index)
                self._links[name] = index
        return self._links

    @property
    def pollutants(self):
        if not self._pollutants:
            self._pollutants = dict()
            total = self.project_size[4]
            for index in range(total):
                name = self.object_name(shared_enum.ElementType.POLLUT, index)
                self._pollutants[name] = index
        return self._pollutants

    @output_open_handler
    def unit(self):
        return output.get_units(self.handle)

    @output_open_handler
    def version(self):
        return output.get_version(self.handle)

    @output_open_handler
    def object_name(self, object_type, index):
        return output.get_elem_name(self.handle, object_type, index)

    @output_open_handler
    def subcatch_series(self, index, attribute, start_index=None, end_index=None):
        """
        Get subcatchment time series results for particular attribute. Specify series
        start index and end index to get desired time range.
        :param index:
        :param attribute:
        :param start_index:
        :param end_index:
        :return:
        :rtype:
        """
        if isinstance(index, str):
            index = self.subcatchments.get(index, None)

        if isinstance(attribute, str):
            attribute = subcatch_attribute.get(attribute.lower(), None)

        if not start_index:
            start_index = 0

        if not end_index:
            end_index = self.num_period

        if attribute is None:
            raise OutputException(f"Attribute: {attribute} does not exist in subcatch attribute list.")

        if index is None:
            raise OutputException(f"Subcatch ID: {index} does not exist in model output.")

        values = output.get_subcatch_series(self.handle, index, attribute, start_index, end_index)
        return {time: value for time, value in zip(self.times, values)}

    @output_open_handler
    def node_series(self, index, attribute, start_index=None, end_index=None):
        if isinstance(index, str):
            index = self.nodes.get(index, None)

        if isinstance(attribute, str):
            attribute = node_attribute.get(attribute.lower(), None)

        if not start_index:
            start_index = 0

        if not end_index:
            end_index = self.num_period

        if attribute is None:
            raise OutputException(f"Attribute: {attribute} does not exist in node attribute list.")

        if index is None:
            raise OutputException(f"Node ID: {index} does not exist in model output.")

        values = output.get_node_series(self.handle, index, attribute, start_index, end_index)
        return {time: value for time, value in zip(self.times, values)}

    @output_open_handler
    def link_series(self, index, attribute, start_index=None, end_index=None):
        if isinstance(index, str):
            index = self.links.get(index, None)

        if isinstance(attribute, str):
            attribute = link_attribute.get(attribute.lower(), None)

        if not start_index:
            start_index = 0

        if not end_index:
            end_index = self.num_period

        if attribute is None:
            raise OutputException(f"Attribute: {attribute} does not exist in link attribute list.")

        if index is None:
            raise OutputException(f"Link ID: {index} does not exist in model output.")

        values = output.get_link_series(self.handle, index, attribute, start_index, end_index)
        return {time: value for time, value in zip(self.times, values)}

    @output_open_handler
    def system_series(self, attribute, start_index=None, end_index=None):
        if isinstance(attribute, str):
            attribute = system_attribute.get(attribute.lower(), None)

        if not start_index:
            start_index = 0

        if not end_index:
            end_index = self.num_period

        if attribute is None:
            raise OutputException(f"Attribute: {attribute} does not exist in system attribute list.")

        values = output.get_system_series(self.handle, attribute, start_index, end_index)
        return {time: value for time, value in zip(self.times, values)}

    @output_open_handler
    def subcatch_attribute(self, attribute, time_index=None):
        """
        For all subcatchments at given time, get a particular attribute.
        :param attribute:
        :param time_index:
        :return:
        :rtype: dict of node values
        """
        if isinstance(attribute, str):
            attribute = subcatch_attribute.get(attribute.lower(), None)

        if not time_index:
            time_index = 0

        if attribute is None:
            raise OutputException(f"Attribute: {attribute} does not exist in subcatch attribute list.")

        values = output.get_subcatch_attribute(self.handle, time_index, attribute)
        return {sub: value for sub, value in zip(self.subcatchments, values)}

    @output_open_handler
    def node_attribute(self, attribute, time_index=None):
        if isinstance(attribute, str):
            attribute = node_attribute.get(attribute.lower(), None)

        if not time_index:
            time_index = 0

        if attribute is None:
            raise OutputException(f"Attribute: {attribute} does not exist in node attribute list.")

        values = output.get_node_attribute(self.handle, time_index, attribute)
        return {node: value for node, value in zip(self.nodes, values)}

    @output_open_handler
    def link_attribute(self, attribute, time_index=None):
        if isinstance(attribute, str):
            attribute = link_attribute.get(attribute.lower(), None)

        if not time_index:
            time_index = 0

        if attribute is None:
            raise OutputException(f"Attribute: {attribute} does not exist in link attribute list.")

        values = output.get_link_attribute(self.handle, time_index, attribute)
        return {link: value for link, value in zip(self.links, values)}

    @output_open_handler
    def system_attribute(self, attribute, time_index=None):
        if isinstance(attribute, str):
            attribute = system_attribute.get(attribute.lower(), None)

        if not time_index:
            time_index = 0

        if attribute is None:
            raise OutputException(f"Attribute: {attribute} does not exist in system attribute list.")

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
        if isinstance(index, str):
            index = self.subcatchments.get(index, None)

        if not time_index:
            time_index = 0

        if index is None:
            raise OutputException(f"Subcatch ID: {index} does not exist in model output.")

        values = output.get_subcatch_result(self.handle, time_index, index)
        return {attr: value for attr, value in zip(subcatch_attribute, values)}

    @output_open_handler
    def node_result(self, index, time_index=None):
        """
        For a node at given time, get all attributes.
        :param index: node index
        :param time_index: datetime index
        :return: dict of attributes for a node at given timestep
        :rtype: dict
        """
        if isinstance(index, str):
            index = self.nodes.get(index, None)

        if not time_index:
            time_index = 0

        if index is None:
            raise OutputException(f"Node ID: {index} does not exist in model output.")

        values = output.get_node_result(self.handle, time_index, index)
        return {attr: value for attr, value in zip(node_attribute, values)}

    @output_open_handler
    def link_result(self, index, time_index=None):
        """
        For a link at given time, get all attributes.
        :param index: link index
        :param time_index: datetime index
        :return: dict of attributes for a link at given timestep
        :rtype: dict
        """
        if isinstance(index, str):
            index = self.links.get(index, None)

        if not time_index:
            time_index = 0

        if index is None:
            raise OutputException(f"Link ID: {index} does not exist in model output.")

        values = output.get_link_result(self.handle, time_index, index)
        return {attr: value for attr, value in zip(link_attribute, values)}

    @output_open_handler
    def system_result(self, time_index=None):
        """
        At a given time, get all system attributes.
        :param time_index: datetime index
        :return: dict of attributes for the system at given timestep
        :rtype: dict
        """
        dummy_index = 0
        if not time_index:
            time_index = 0

        values = output.get_system_result(self.handle, time_index, dummy_index)
        return {attr: value for attr, value in zip(system_attribute, values)}
