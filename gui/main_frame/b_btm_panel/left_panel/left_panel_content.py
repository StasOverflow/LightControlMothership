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

        # Create modbus instance, to have access to its props
        instance = ModbusConnectionThreadSingleton()
        self.modbus = instance.thread_instance_get()

        # Create content for
        self.inner_matrix = InputArray(parent=self, title='Associated inputs:',
                                       dimension=(3, 5),
                                       col_titles=['1', '2', '3', '4', '5'],
                                       row_titles=['X1', 'X2', 'X3'])

        self.inner_panel_sizer = wx.BoxSizer(wx.VERTICAL)
        self.inner_panel_sizer.Add(self.inner_matrix, 0, wx.ALL | wx.ALIGN_CENTER, 10)
        self.SetSizer(self.inner_panel_sizer)

        self.app_data.iface_handler_register(self._radio_buttons_visibility_handler)

    def _radio_button_callback(self, event):
        if self.modbus.is_connected and self.app_data.modbus_data is not None:
            pass
            # print('handled', event.GetId())
            # data_byte = self.app_data.modbus_data[6]
            # data_bits = event.GetId()
            # shifting_val = self.id * 2
            # data_byte &= ~(3 << shifting_val)
            # data_byte |= (data_bits << shifting_val)
            # self.modbus.queue_insert(data_byte, 4)

    def _radio_buttons_visibility_handler(self):
        if self.modbus.is_connected:
            # if self.app_data.modbus_data is not None:
            #     data_bits = (self.app_data.modbus_data[6] >> self.id * 2) & 3
            #     if self.data_bits_prev != data_bits:
            #         self.data_bits_prev = data_bits
            #         if not data_bits:
            #             self.direct_mode_radio.SetValue(True)
            #         elif data_bits == 1:
            #             self.toggle_mode_radio.SetValue(True)
            # try:
            #     self.direct_mode_radio.Enable()
            #     self.toggle_mode_radio.Enable()
            # except RuntimeError:
                pass
        else:
            # try:
            #     self.direct_mode_radio.Disable()
            #     self.toggle_mode_radio.Disable()
            # except RuntimeError:
                pass

    # def _ins_outs_state_update(self):
    #     separate_input_data_array = self.app_data.separate_inputs_state_get_by_index(self.id)
    #     out_data = self.app_data.output_data_by_index(self.id)
    #     if separate_input_data_array is not None:
    #         self.configuration_set(separate_input_data_array, out_data)
    #
    # def _inputs_visibility_update(self):
    #     separate_inputs_visibility_array = self.app_data.separate_inputs_visibility_get_by_index(self.id)
    #     if separate_inputs_visibility_array is not None:
    #         self.visibility_set(separate_inputs_visibility_array)

    # def _inputs_state_set(self):
    #     if self.interface == INPUT_INTERFACE:
    #         values = self.configuration_get()
    #         if values != self.conf_prev:
    #             self.conf_prev = values
    #             values = 0
    #             for i in range(len(self.conf_prev)):
    #                 values |= int(self.conf_prev[i] << i)
    #             if self.modbus.is_connected:
    #                 kostil_byte = self.app_data.modbus_data[6]
    #                 self.modbus.queue_insert(values, self.id)
    #                 self.modbus.queue_insert(kostil_byte, 4)
    #
    # def configuration_set(self, new_array, out_state=None):
    #     self.inner_matrix.values = new_array
    #     if hasattr(self, 'inter_instance') and out_state is not None:
    #         self.inter_instance.values = (out_state, )
    #
    # def visibility_set(self, new_array):
    #     self.inner_matrix.visible_instances = new_array
    #
    # def configuration_get(self):
    #     return self.inner_matrix.values
