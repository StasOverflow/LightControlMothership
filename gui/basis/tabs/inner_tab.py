import wx
from gui.control_inputs.input_array_box import InputArray
from settings import ApplicationPresets
from backend.modbus_backend import ModbusConnectionThreadSingleton


class BaseInnerTab(wx.Panel):

    def __init__(self, parent, *args, **kwargs):

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

        # In this sequence we add elements (if they exists) to panel
        self.inner_panel_sizer = wx.BoxSizer(wx.VERTICAL)
        if self.inner_title is not None:
            self.inner_panel_sizer.Add(self.inner_title, 0, wx.ALL, 5)

        self.inner_panel_sizer.Add(self.inner_matrix, 0, wx.ALL | wx.CENTER, 2)

        self.configuration_update()
        self.SetSizer(self.inner_panel_sizer)

    def array_hidden_state_set(self, new_order):
        self.inner_matrix.visible_instances = new_order

    def array_hidden_state_update(self):
        pass

    def array_hidden_state_get(self):
        return self.inner_matrix.visible_instances

    def configuration_set(self, new_array):
        self.inner_matrix.values = new_array

    def configuration_receive(self, *args, **kwargs):
        print('receiving configurations')

    def configuration_send(self, *args, **kwargs):
        print('sending configurations')

    def configuration_update(self, *args, **kwargs):
        self._configuration = self.inner_matrix.values
        # print('updating cfg' + str(self._configuration))

    def configuration_get(self):
        return self._configuration
