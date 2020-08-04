import wx
from defs import *
from settings import AppData, Settings
from gui.control_inputs.input_array_box import InputArray
from backend.modbus_backend import ModbusConnectionThreadSingleton


class BtmLeftPanel(wx.Panel):

    def __init__(self, parent):

        # Basic Construction stuff
        super().__init__(parent)
        self.app_data = AppData()
        self._output_garbage_collector = 0
        self._input_matrix_enabled = False

        # Create modbus instance, to have access to its props
        instance = ModbusConnectionThreadSingleton()
        self.modbus = instance.thread_instance_get()

        # Create content for
        self.input_matrix = InputArray(parent=self, title='Associated inputs:',
                                       dimension=(3, 5),
                                       col_titles=['1', '2', '3', '4', '5'],
                                       row_titles=['X1', 'X2', 'X3'])

        self.inner_panel_sizer = wx.BoxSizer(wx.VERTICAL)
        self.inner_panel_sizer.Add(self.input_matrix, 0, wx.ALL | wx.ALIGN_CENTER, 10)
        self.SetSizer(self.inner_panel_sizer)

        self.input_matrix.disable()
        self.app_data.iface_output_handler_register(self._matrix_visibility_update)
        for instance in self.input_matrix.instance_array:
            self.Bind(wx.EVT_CHECKBOX, self._checkbox_pressed_handle, instance.cell_instance.checkbox)

    def _checkbox_pressed_handle(self, event):
        self.app_data.user_interaction = True

    def _matrix_visibility_update(self):
        if self.modbus.is_connected:
            if self._input_matrix_enabled is False:
                self.input_matrix.enable()
                self._input_matrix_enabled = True
        else:
            if self._input_matrix_enabled is True:
                self.input_matrix.disable()
                self._input_matrix_enabled = False
