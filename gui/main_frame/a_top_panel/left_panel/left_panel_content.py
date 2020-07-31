import wx
from gui.utils.labeled_data import LabelValueSequence
from gui.utils.label_types import *
from defs import *
from settings import Settings, AppData
from gui.control_inputs.input_array_box import InputArray
from backend.modbus_backend import ModbusConnectionThreadSingleton


class TopLeftPanel(wx.Panel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.app_data = AppData()

        self.modbus = ModbusConnectionThreadSingleton()
        self.modbus = self.modbus.thread_instance_get()

        self.input_matrix = InputArray(parent=self, title='Inputs mode toggle:',
                                       interface=INPUT_INTERFACE, dimension=(3, 5),
                                       col_titles=['1', '2', '3', '4', '5'],
                                       row_titles=['X1', 'X2', 'X3'])

        inner_panel_sizer = wx.BoxSizer(wx.VERTICAL)
        inner_panel_sizer.Add(self.input_matrix, 0, wx.ALL | wx.CENTER, 15)

        self.input_matrix.disable()
        self.app_data.iface_handler_register(self._matrix_update)

        self.SetSizer(inner_panel_sizer)

    def _matrix_update(self):
        if self.modbus.is_connected:
            self.input_matrix.enable()
            # self.configuration_set(self.app_data.inputs_combined_data)
            # self.configuration_set(self.app_data.outputs_combined_data, input_cfg=False)
        else:
            self.input_matrix.disable()
    #
    # def configuration_get(self):
    #     return self.input_matrix.values
    #
    # def configuration_set(self, new_array):
    #     self.input_matrix.values = new_array
    #
    # def array_hidden_state_set(self, new_order):
    #     self.input_matrix.visible_instances = new_order
    #
    # def array_hidden_state_update(self):
    #     pass
    #
    # def array_hidden_state_get(self):
    #     return self.input_matrix.visible_instances


def main():
    app = wx.App()

    frame = wx.Frame(None, -1, 'win.py', size=(600, 500))
    TopLeftPanel(parent=frame)
    frame.Show()

    app.MainLoop()


if __name__ == '__main__':
    main()