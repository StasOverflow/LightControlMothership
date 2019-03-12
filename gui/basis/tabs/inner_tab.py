import wx
from gui.control_inputs.input_array_box import InputArray
from settings import AppData
from backend.modbus_backend import ModbusConnectionThreadSingleton
from defs import *


class BaseInnerTab(wx.Panel):

    def __init__(self, parent, *args, aydi=None, **kwargs):
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

        if 'inner_title' in kwargs:
            self.inner_title = wx.StaticText(parent=self, label=kwargs['inner_title'])

        self.inner_matrix = InputArray(
            parent=self,
            title='State of inputs:',
            dimension=(3, 5),
            col_titles=['1', '2', '3', '4', '5'],
            row_titles=['X3', 'X2', 'X1'],
            orientation=wx.VERTICAL,
            *args,
            **kwargs,
        )

        modbus_singleton = ModbusConnectionThreadSingleton()
        self.modbus = modbus_singleton.modbus_comm_instance

        self.app_data = AppData()

        # In this sequence we add elements (if they exists) to panel
        self.inner_panel_sizer = wx.BoxSizer(wx.VERTICAL)
        if self.inner_title is not None:
            self.inner_panel_sizer.Add(self.inner_title, 0, wx.ALL, 5)

        self.inner_panel_sizer.Add(self.inner_matrix, 0, wx.ALL | wx.CENTER, 2)

        self.configuration_update()
        self.SetSizer(self.inner_panel_sizer)

        if self.id is not None:
            if 'interface' in kwargs:
                if kwargs['interface'] == DISPLAY_INTERFACE:
                    self.app_data.iface_handler_register(self._inputs_state_update)
                    self.app_data.iface_handler_register(self._inputs_visibility_update)
            else:
                print('input interface')

    def _inputs_state_update(self):
        separate_input_data_array = self.app_data.separate_inputs_state_get_by_index(self.id)
        if separate_input_data_array is not None:
            self.configuration_set(separate_input_data_array)

    def _inputs_visibility_update(self):
        separate_inputs_visibility_array = self.app_data.separate_inputs_visibility_get_by_index(self.id)
        if separate_inputs_visibility_array is not None:
            self.visibility_set(separate_inputs_visibility_array)

    def configuration_set(self, new_array):
        self.inner_matrix.values = new_array

    def visibility_set(self, new_array):
        self.inner_matrix.visible_instances = new_array

    def configuration_update(self, *args, **kwargs):
        self._configuration = self.inner_matrix.values

    def configuration_get(self):
        return self._configuration
