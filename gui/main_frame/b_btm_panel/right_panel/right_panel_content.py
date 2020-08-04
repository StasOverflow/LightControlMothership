import wx
from defs import *
from settings import AppData
from settings import Settings
from gui.control_inputs.input_array_box import InputArray
from backend.modbus_backend import ModbusConnectionThreadSingleton


class BtmRightPanel(wx.Panel):

    def __init__(self, parent):
        super().__init__(parent)
        self.app_data = AppData()
        self._output_garbage_collector = 0

        # Create modbus instance, to have access to its props
        instance = ModbusConnectionThreadSingleton()
        self.modbus = instance.thread_instance_get()

        # Create content for
        self.input_matrix = InputArray(parent=self, title='Corresponding inputs state:',
                                       dimension=(3, 5), interface=DISPLAY_INTERFACE,
                                       col_titles=['1', '2', '3', '4', '5'],
                                       row_titles=['X1', 'X2', 'X3'])

        self.inner_panel_sizer = wx.BoxSizer(wx.VERTICAL)
        self.inner_panel_sizer.Add(self.input_matrix, 0, wx.ALL | wx.ALIGN_CENTER, 10)
        self.SetSizer(self.inner_panel_sizer)
