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
        self._input_matrix_enabled = False
        self._in_matrix_update_stage = 0

        self.modbus = ModbusConnectionThreadSingleton()
        self.modbus = self.modbus.thread_instance_get()

        self.input_matrix = InputArray(parent=self, title='Inputs mode toggle:',
                                       interface=INPUT_INTERFACE, dimension=(3, 5),
                                       col_titles=['1', '2', '3', '4', '5'],
                                       row_titles=['X1', 'X2', 'X3'])

        inner_panel_sizer = wx.BoxSizer(wx.VERTICAL)
        inner_panel_sizer.Add(self.input_matrix, 0, wx.ALL | wx.CENTER, 15)

        self.input_matrix.disable()
        self.app_data.iface_conn_handler_register(self._matrix_initial_data_setup)
        self.app_data.iface_output_handler_register(self._matrix_visibility_update)
        self.app_data.iface_input_handler_register(self._in_matrix_data_gather)

        self.SetSizer(inner_panel_sizer)

        for instance in self.input_matrix.instance_array:
            self.Bind(wx.EVT_CHECKBOX, self._checkbox_pressed_handle, instance.cell_instance.checkbox)

    def _checkbox_pressed_handle(self, event):
        self.app_data.user_interaction = True

    def _matrix_initial_data_setup(self):
        for i in range(15):
            toggle = self.app_data.input_trigger_type_is_toggle_get(i)
            self.input_matrix.value_set_by_index(i, toggle)

    def _matrix_visibility_update(self):
        if self.modbus.is_connected:
            if self._input_matrix_enabled is False:
                self.input_matrix.enable()
                self._input_matrix_enabled = True
        else:
            if self._input_matrix_enabled is True:
                self.input_matrix.disable()
                self._input_matrix_enabled = False

    def _in_matrix_data_gather(self):
        val_list = []
        for in_id in range(15):
            value = self.input_matrix.value_get_by_index(in_id)
            val_list.append(value)

        self.app_data.input_trigger_type_is_toggle_set_mask(val_list)


def main():
    app = wx.App()

    frame = wx.Frame(None, -1, 'win.py', size=(600, 500))
    TopLeftPanel(parent=frame)
    frame.Show()

    app.MainLoop()


if __name__ == '__main__':
    main()