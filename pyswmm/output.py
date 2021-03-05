from datetime import timedelta

# Third party imports
from swmm.toolkit import output, shared_enum
from julian import from_jd


def output_open_handler(func):
    def inner_function(self, *arg, **kwargs):
        if not self.loaded:
            self.open()

    return inner_function


class Output(object):
    def __init__(self, binfile):
        self.binfile = binfile

        self.handle = None
        self.loaded = False
        self.delete_handle = False
        self.num_period = None
        self.report = None
        self.start_time = None
        self._times = None

    def open(self):
        """
        Open a binary file
        """
        if self.handle is None:
            self.handle = output.init()

        if not self.loaded:
            self.loaded = True
            output.open(self.handle, self.binfile)
            self.start_time = from_jd(output.get_start_date(self.handle) + 2415018.5)
            self.report = output.get_times(self.handle, shared_enum.Time.REPORT_STEP)
            self.num_period = output.get_times(self.handle, shared_enum.Time.NUM_PERIODS)

    def close(self):
        """
        Close an opened binary file
        """
        if self.handle or self.loaded:
            self.loaded = False
            self.delete_handle = True
            output.close(self.handle)

    def __enter__(self):
        self.open()

        return self

    def __exit__(self, *arg):
        self.close()

    @property
    def times(self):
        if not self._times:
            start_date_time = self.start_time
            num_steps = self.num_period
            report_step = self.report
            self._times = [start_date_time + timedelta(report_step) * step for step in range(num_steps)]
        return self._times

    @output_open_handler
    def project_size(self):
        return output.get_proj_size(self.handle)

    @output_open_handler
    @property
    def links(self):
        pass

    @output_open_handler
    @property
    def nodes(self):
        pass

    @output_open_handler
    @property
    def subcatchments(self):
        pass

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
        if not start_index:
            start_index = 0

        if not end_index:
            end_index = self.num_period

        return output.get_subcatch_series(self.handle, index, attribute, start_index, end_index)

    @output_open_handler
    def node_series(self, index, attribute, start_index=None, end_index=None):
        if not start_index:
            start_index = 0

        if not end_index:
            end_index = self.num_period

        return output.get_node_series(self.handle, index, attribute, start_index, end_index)

    @output_open_handler
    def link_series(self, index, attribute, start_index=None, end_index=None):
        if not start_index:
            start_index = 0

        if not end_index:
            end_index = self.num_period

        return output.get_link_series(self.handle, index, attribute, start_index, end_index)

    @output_open_handler
    def system_series(self, attribute, start_index=None, end_index=None):
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
        if not time_index:
            time_index = 0

        return output.get_subcatch_result(self.handle, time_index, index)

    @output_open_handler
    def node_result(self, index, time_index=0):
        if not time_index:
            time_index = 0

        return output.get_node_result(self.handle, time_index, index)

    @output_open_handler
    def link_result(self, index, time_index=0):
        if not time_index:
            time_index = 0

        return output.get_link_result(self.handle, time_index, index)

    @output_open_handler
    def system_result(self, index, time_index=0):
        if not time_index:
            time_index = 0

        return output.get_system_result(self.handle, time_index, index)
