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
        self.inner_matrix = InputArray(parent=self, title='Corresponding inputs state:',
                                       dimension=(3, 5), interface=DISPLAY_INTERFACE,
                                       col_titles=['1', '2', '3', '4', '5'],
                                       row_titles=['X1', 'X2', 'X3'])

        self.inner_panel_sizer = wx.BoxSizer(wx.VERTICAL)
        self.inner_panel_sizer.Add(self.inner_matrix, 0, wx.ALL | wx.ALIGN_CENTER, 10)
        self.SetSizer(self.inner_panel_sizer)
    #
    #     self.SetSizer(self.inner_panel_sizer)
    #
    #     self.settings = Settings()
    #
    #     self.app_data = AppData()
    #
    #     self.app_data.iface_handler_register(self._conf_receive)
    #
    #     self.data_received = False
    #
    #     self.modbus_data = self.app_data.separate_inputs_visibility_get_by_index(self.id)
    #
    # def _ins_outs_state_update(self, force=False):
    #     separate_inputs_visibility_array = self.app_data.separate_inputs_visibility_get_by_index(self.id)
    #     if separate_inputs_visibility_array is not None:
    #         self.configuration_set(separate_inputs_visibility_array)
    #
    # def _conf_receive(self, force=False):
    #     if self.modbus.is_connected:
    #         modbus_data_new = self.app_data.separate_inputs_visibility_get_by_index(self.id)
    #         if self.modbus_data != modbus_data_new:
    #             self.modbus_data = modbus_data_new
    #             self._ins_outs_state_update()
    #     else:
    #         self.modbus_data = None
    #
    # def configuration_receive(self, *args, **kwargs):
    #     print(self.id)
    #     self._ins_outs_state_update(force=True)
    #     print('receiving configurations')
    #
    # def configuration_send(self, *args, **kwargs):
    #     print(self.id)
    #     print('sending configurations')
