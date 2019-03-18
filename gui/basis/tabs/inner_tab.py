import wx
from gui.control_inputs.input_array_box import InputArray
from settings import AppData
from backend.modbus_backend import ModbusConnectionThreadSingleton
from defs import *


class BaseInnerTab(wx.Panel):

    def __init__(self, parent, *args, aydi=None,
                 with_size=True, with_indicator=False,
                 with_radio_panel=False, **kwargs):
        self.id = aydi

        style = None
        if 'style' in kwargs:
            style = kwargs['style']
        if style is not None:
            super().__init__(parent, style=style)
        else:
            super().__init__(parent)

        self.inner_title = None
        self.setup_button = None
        self._configuration = None

        self.inner_title = wx.StaticText(parent=self, label=kwargs['inner_title'])

        self.app_data = AppData()

        intermediate_sizer = None

        if with_indicator:
            intermediate_sizer = wx.BoxSizer(wx.HORIZONTAL)
            self.inter_title = wx.StaticText(parent=self, label='Output State')
            self.inter_instance = InputArray(parent=self, dimension=(1, 1), outlined=False,
                                             interface=DISPLAY_INTERFACE, is_input_indication=False,)

            intermediate_sizer.Add(self.inter_title, 0, wx.LEFT, 15)
            intermediate_sizer.Add(self.inter_instance, 0, wx.LEFT, 30)
        elif with_radio_panel:
            intermediate_sizer = wx.BoxSizer(wx.HORIZONTAL)
            self.inter_title = wx.StaticText(parent=self, label='Output mode')
            self.auto_mode_radio = wx.RadioButton(parent=self, label='Auto')

            intermediate_sizer.Add(self.inter_title, 0, wx.LEFT, 15)
            intermediate_sizer.Add(self.inter_instance, 0, wx.LEFT, 30)

        if self.id is not None:
            if 'interface' in kwargs:
                if kwargs['interface'] == DISPLAY_INTERFACE:
                    self.interface = DISPLAY_INTERFACE
                    self.app_data.iface_handler_register(self._ins_outs_state_update)
                    self.app_data.iface_handler_register(self._inputs_visibility_update)
            else:
                self.interface = INPUT_INTERFACE

        title = 'Inputs configuration:' if self.interface == INPUT_INTERFACE else 'Inputs state:'
        self.inner_matrix = InputArray(parent=self, title=title, dimension=(3, 5),
                                       col_titles=['1', '2', '3', '4', '5'], row_titles=['X3', 'X2', 'X1'],
                                       orientation=wx.VERTICAL, *args, **kwargs)

        modbus_singleton = ModbusConnectionThreadSingleton()
        self.modbus = modbus_singleton.modbus_comm_instance

        self.inner_panel_sizer = wx.BoxSizer(wx.VERTICAL)
        self.inner_panel_sizer.Add(self.inner_title, 0, wx.ALL, 5)
        if with_indicator or with_radio_panel:
            self.inner_panel_sizer.Add(intermediate_sizer, 0, wx.RIGHT | wx.ALIGN_RIGHT, 15)
        self.inner_panel_sizer.Add(self.inner_matrix, 0, wx.ALL | wx.CENTER, 10)

        if with_size:
            self.SetSizer(self.inner_panel_sizer)

        self.conf_prev = None
        self.app_data.iface_handler_register(self._inputs_state_set)

    def _ins_outs_state_update(self):
        separate_input_data_array = self.app_data.separate_inputs_state_get_by_index(self.id)
        out_data = self.app_data.output_data_by_index(self.id)
        if separate_input_data_array is not None:
            self.configuration_set(separate_input_data_array, out_data)

    def _inputs_visibility_update(self):
        separate_inputs_visibility_array = self.app_data.separate_inputs_visibility_get_by_index(self.id)
        if separate_inputs_visibility_array is not None:
            self.visibility_set(separate_inputs_visibility_array)

    def _inputs_state_set(self):
        if self.interface == INPUT_INTERFACE:
            values = self.configuration_get()
            if values != self.conf_prev:
                self.conf_prev = values
                values = 0
                for i in range(len(self.conf_prev)):
                    values |= int(self.conf_prev[i] << i)
                if self.modbus.is_connected:
                    self.modbus.queue_insert(values, self.id)

    def configuration_set(self, new_array, out_state=None):
        self.inner_matrix.values = new_array
        if hasattr(self, 'inter_instance') and out_state is not None:
            self.inter_instance.values = (out_state, )

    def visibility_set(self, new_array):
        self.inner_matrix.visible_instances = new_array

    def configuration_get(self):
        return self.inner_matrix.values
