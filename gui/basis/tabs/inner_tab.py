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

        modbus_singleton = ModbusConnectionThreadSingleton()
        self.modbus = modbus_singleton.modbus_comm_instance

        self.app_data = AppData()

        intermediate_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.inter_title = wx.StaticText(parent=self, label='Output State')
        self.inter_instance = InputArray(parent=self, dimension=(1, 1), outlined=False,
                                         interface=DISPLAY_INTERFACE)
        intermediate_sizer.Add(self.inter_title, 0, wx.LEFT, 15)
        intermediate_sizer.Add(self.inter_instance, 0, wx.LEFT, 30)

        if 'interface' in kwargs:
            if kwargs['interface'] == DISPLAY_INTERFACE:
                self.interface = DISPLAY_INTERFACE
        else:
            self.interface = INPUT_INTERFACE

        title = 'Inputs state:'
        self.inner_matrix = InputArray(parent=self, title=title, dimension=(3, 5),
                                       col_titles=['1', '2', '3', '4', '5'],
                                       row_titles=['X1', 'X2', 'X3'])

        self.inner_panel_sizer = wx.BoxSizer(wx.VERTICAL)
        self.inner_panel_sizer.Add(self.inner_title, 0, wx.ALL, 5)
        if with_indicator or with_radio_panel:
            self.inner_panel_sizer.Add(intermediate_sizer, 0, wx.RIGHT | wx.ALIGN_RIGHT, 18)
        self.inner_panel_sizer.Add(self.inner_matrix, 0, wx.ALL | wx.CENTER, 10)

        if with_size:
            self.SetSizer(self.inner_panel_sizer)

    def configuration_set(self, new_array, out_state=None):
        self.inner_matrix.values = new_array
        if hasattr(self, 'inter_instance') and out_state is not None:
            self.inter_instance.values = (out_state, )

    def visibility_set(self, new_array):
        self.inner_matrix.visible_instances = new_array

    def configuration_get(self):
        return self.inner_matrix.values
