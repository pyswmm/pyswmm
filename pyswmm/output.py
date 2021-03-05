# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2021 Jennifer Wu
#
# Licensed under the terms of the BSD2 License
# See LICENSE.txt for details
# -----------------------------------------------------------------------------
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
        if isinstance(index, str):
            index = self.subcatchments[index]

        if isinstance(attribute, str):
            attribute_enum = dict(
                rainfall=shared_enum.SubcatchAttribute.RAINFALL,
                snow_depth=shared_enum.SubcatchAttribute.SNOW_DEPTH,
                evap_loss=shared_enum.SubcatchAttribute.EVAP_LOSS,
                infil_loss=shared_enum.SubcatchAttribute.INFIL_LOSS,
                runoff_rate=shared_enum.SubcatchAttribute.RUNOFF_RATE,
                gw_outflow_rate=shared_enum.SubcatchAttribute.GW_OUTFLOW_RATE,
                gw_table_elev=shared_enum.SubcatchAttribute.GW_TABLE_ELEV,
                soil_moisture=shared_enum.SubcatchAttribute.SOIL_MOISTURE,
                pollutant_concentration=shared_enum.SubcatchAttribute.POLLUT_CONC_0,
            )
            attribute = attribute_enum.get(attribute.lower(), None)

        if not start_index:
            start_index = 0

        if not end_index:
            end_index = self.num_period

        return output.get_subcatch_series(self.handle, index, attribute, start_index, end_index)

    @output_open_handler
    def node_series(self, index, attribute, start_index=None, end_index=None):
        if isinstance(index, str):
            index = self.nodes[index]

        if isinstance(attribute, str):
            attribute_enum = dict(
                invert_depth=shared_enum.NodeAttribute.INVERT_DEPTH,
                hydraulic_head=shared_enum.NodeAttribute.HYDRAULIC_HEAD,
                ponded_volume=shared_enum.NodeAttribute.PONDED_VOLUME,
                lateral_inflow=shared_enum.NodeAttribute.LATERAL_INFLOW,
                total_inflow=shared_enum.NodeAttribute.TOTAL_INFLOW,
                flooding_losses=shared_enum.NodeAttribute.FLOODING_LOSSES,
                pollutant_concentration=shared_enum.NodeAttribute.POLLUT_CONC_0,
            )
            attribute = attribute_enum.get(attribute.lower(), None)

        if not start_index:
            start_index = 0

        if not end_index:
            end_index = self.num_period

        return output.get_node_series(self.handle, index, attribute, start_index, end_index)

    @output_open_handler
    def link_series(self, index, attribute, start_index=None, end_index=None):
        if isinstance(index, str):
            index = self.links[index]

        if isinstance(attribute, str):
            attribute_enum = dict(
                flow_rate=shared_enum.LinkAttribute.FLOW_RATE,
                flow_depth=shared_enum.LinkAttribute.FLOW_DEPTH,
                flow_velocity=shared_enum.LinkAttribute.FLOW_VELOCITY,
                flow_volume=shared_enum.LinkAttribute.FLOW_VOLUME,
                capacity=shared_enum.LinkAttribute.CAPACITY,
                pollutant_concentration=shared_enum.LinkAttribute.POLLUT_CONC_0,
            )
            attribute = attribute_enum.get(attribute.lower(), None)

        if not start_index:
            start_index = 0

        if not end_index:
            end_index = self.num_period

        values = output.get_link_series(self.handle, index, attribute, start_index, end_index)

        return {time: value for time, value in zip(self.times, values)}

    @output_open_handler
    def system_series(self, attribute, start_index=None, end_index=None):
        if isinstance(attribute, str):
            attribute_enum = dict(
                air_temp=shared_enum.SystemAttribute.AIR_TEMP,
                rainfall=shared_enum.SystemAttribute.RAINFALL,
                snow_depth=shared_enum.SystemAttribute.SNOW_DEPTH,
                evap_infil_loss=shared_enum.SystemAttribute.EVAP_INFIL_LOSS,
                runoff_flow=shared_enum.SystemAttribute.RUNOFF_FLOW,
                dry_weather_inflow=shared_enum.SystemAttribute.DRY_WEATHER_INFLOW,
                gw_inflow=shared_enum.SystemAttribute.GW_INFLOW,
                rdii_inflow=shared_enum.SystemAttribute.RDII_INFLOW,
                direct_inflow=shared_enum.SystemAttribute.DIRECT_INFLOW,
                total_lateral_inflow=shared_enum.SystemAttribute.TOTAL_LATERAL_INFLOW,
                flood_losses=shared_enum.SystemAttribute.FLOOD_LOSSES,
                outfall_flows=shared_enum.SystemAttribute.OUTFALL_FLOWS,
                volume_stored=shared_enum.SystemAttribute.VOLUME_STORED,
                evap_rate=shared_enum.SystemAttribute.EVAP_RATE,
            )
            attribute = attribute_enum.get(attribute.lower(), None)

        if not start_index:
            start_index = 0

        if not end_index:
            end_index = self.num_period

        return output.get_system_series(self.handle, attribute, start_index, end_index)

    @output_open_handler
    def subcatch_attribute(self, attribute, time_index=0):
        if not time_index:
            time_index = 0

        return output.get_subcatch_attribute(self.handle, time_index, attribute)

    @output_open_handler
    def node_attribute(self, attribute, time_index=0):
        if not time_index:
            time_index = 0

        return output.get_node_attribute(self.handle, time_index, attribute)

    @output_open_handler
    def link_attribute(self, attribute, time_index=0):
        if not time_index:
            time_index = 0

        return output.get_link_attribute(self.handle, time_index, attribute)

    @output_open_handler
    def system_attribute(self, attribute, time_index=0):
        if not time_index:
            time_index = 0

        return output.get_system_attribute(self.handle, time_index, attribute)

    @output_open_handler
    def subcatch_result(self, index, time_index=0):
        if isinstance(index, str):
            index = self.subcatchments[index]

        if not time_index:
            time_index = 0

        return output.get_subcatch_result(self.handle, time_index, index)

    @output_open_handler
    def node_result(self, index, time_index=0):
        if isinstance(index, str):
            index = self.nodes[index]

        if not time_index:
            time_index = 0

        return output.get_node_result(self.handle, time_index, index)

    @output_open_handler
    def link_result(self, index, time_index=0):
        if isinstance(index, str):
            index = self.links[index]

        if not time_index:
            time_index = 0

        return output.get_link_result(self.handle, time_index, index)

    @output_open_handler
    def system_result(self, index, time_index=0):
        if not time_index:
            time_index = 0

        return output.get_system_result(self.handle, time_index, index)
