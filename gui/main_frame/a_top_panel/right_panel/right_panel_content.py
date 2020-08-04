import wx
from defs import *
from settings import AppData
from gui.control_inputs.input_array_box import InputArray
from backend.modbus_backend import ModbusConnectionThreadSingleton


class TopRightPanel(wx.Panel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.app_data = AppData()

        self.modbus = ModbusConnectionThreadSingleton()
        self.modbus = self.modbus.thread_instance_get()

        self.input_matrix = InputArray(parent=self, title='Inputs state:',
                                       interface=DISPLAY_INTERFACE, dimension=(3, 5),
                                       col_titles=['1', '2', '3', '4', '5'],
                                       row_titles=['X1', 'X2', 'X3'])

        inner_panel_sizer = wx.BoxSizer(wx.VERTICAL)
        inner_panel_sizer.Add(self.input_matrix, 0, wx.ALL | wx.CENTER, 15)

        self.app_data.iface_output_handler_register(self._inputs_state_update)

        self.SetSizer(inner_panel_sizer)

    def _inputs_state_update(self):
        for i in range(15):
            self.input_matrix.value_set_by_index(i, self.app_data.input_state_get(i))

