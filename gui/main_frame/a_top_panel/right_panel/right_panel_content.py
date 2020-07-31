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

        self.app_data.iface_handler_register(self._inputs_state_update)

        self.SetSizer(inner_panel_sizer)

    def _inputs_state_update(self):
        if self.app_data.modbus_data:
            self.configuration_set(self.app_data.inputs_combined_data)
            # self.configuration_set(self.app_data.outputs_combined_data, input_cfg=False)
        else:
            pass

    def configuration_get(self):
        return self.input_matrix.values

    def configuration_set(self, new_array):
        self.input_matrix.values = new_array

    # def _inputs_visibility_update(self):
    #     if self.app_data.modbus_data:
    #         self.visibility_set(self.app_data.inputs_combined_visibility)

    def array_hidden_state_set(self, new_order):
        self.input_matrix.visible_instances = new_order

    def array_hidden_state_update(self):
        pass

    def array_hidden_state_get(self):
        return self.input_matrix.visible_instances

    '''
    def _on_mouse_down(self, event):
        if self.mbus.is_connected and self.app_data.modbus_data is not None:
            aydi = event.GetEventObject().parent_class.secret_id
            aydi_shifted = (aydi - 1) * 2
            mode_auto = self.app_data.output_mode_get()
            if not (mode_auto & 3 << aydi_shifted):
                print(aydi-1)
                status_byte = mode_auto | (3 << aydi_shifted)
                print('{:08b}'.format(status_byte))
                self.mbus.queue_insert(status_byte, 4)
        # print('pressed', event.GetEventObject().parent_class.secret_id)
    '''