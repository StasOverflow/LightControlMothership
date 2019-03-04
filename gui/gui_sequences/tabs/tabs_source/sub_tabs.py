import wx
from gui.utils.labeled_data import LabelValueSequence
from gui.utils.label_types import *
from gui.control_inputs.input_array_box import InputArray
from gui.control_inputs.defs import *
from settings import Settings


class ConnectButton(wx.BoxSizer):

    def __init__(self, parent, connect_label='Connect', disconnect_label='Disconnect'):
        super().__init__(wx.HORIZONTAL)

        self.button = wx.Button(parent=parent, label=connect_label, style=wx.EXPAND, size=(90, 27))
        self.Add(self.button, 1, wx.TOP, 18)


class TopLeftPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.settings = Settings()

        self.top_left_sizer_main = wx.BoxSizer(wx.HORIZONTAL)
        self.top_left_sizer_v = wx.BoxSizer(wx.VERTICAL)
        self.top_inputs_sizer = wx.BoxSizer(wx.VERTICAL)

        self.status = LabelValueSequence(parent=self, label='Status', interface=LABELED_LABEL)
        self.device_port = LabelValueSequence(parent=self, label='Device Port', interface=LABELED_LABEL)
        self.slave_id = LabelValueSequence(
                            parent=self,
                            label='Slave ID',
                            interface=LABELED_SPIN_CONTROL,
                            initial_value=0
                        )
        self.Bind(wx.EVT_BUTTON, self.slave_id_update, self.slave_id.item.button)
        self.Bind(wx.EVT_SPINCTRL, self.slave_id_update, self.slave_id.item.spin)

        self.refresh_rate = LabelValueSequence(parent=self, label='Refresh rate', interface=LABELED_LABEL)
        self.checkbox = LabelValueSequence(parent=self, label='Show unused', interface=LABELED_CHECK_BOX)

        self.conn_button = ConnectButton(parent=self)

        self.top_inputs_sizer.Add(self.status)
        self.top_inputs_sizer.Add(self.device_port)
        self.top_inputs_sizer.Add(self.slave_id)
        self.top_inputs_sizer.Add(self.refresh_rate)
        self.top_inputs_sizer.Add(self.checkbox, 0, wx.TOP, 2)

        self.top_left_sizer_v.Add(self.top_inputs_sizer, 5, wx.BOTTOM, 15)
        self.top_left_sizer_v.Add(self.conn_button, 2, wx.BOTTOM | wx.ALIGN_RIGHT, 5)

        self.line = wx.StaticLine(self, wx.ID_ANY, style=wx.LI_VERTICAL)

        self.top_left_sizer_h = wx.BoxSizer(wx.HORIZONTAL)

        self.top_left_sizer_h.Add(self.top_left_sizer_v, 0, wx.LEFT, 25)

        self.top_left_sizer_main.Add(self.top_left_sizer_h, wx.EXPAND, wx.TOP, 16)
        self.top_left_sizer_main.Add(self.line, 0, wx.LEFT | wx.EXPAND, 14)

        self.SetSizer(self.top_left_sizer_main)

    def slave_id_update(self, event):
        self.settings.slave_id = self.slave_id.value


class TopRightPanel(wx.Panel):

    def __init__(self, parent=None, *args, **kwargs):
        style = None
        if 'style' in kwargs:
            style = kwargs['style']
        if style is not None:
            super().__init__(parent, style=style)
        else:
            super().__init__(parent)

        self.inner_title = None
        self.setup_button = None

        self.input_matrix = InputArray(
            parent=self,
            title='State of inputs:',
            interface=DISPLAY_INTERFACE,
            dimension=(3, 5),
            col_titles=['1', '2', '3', '4', '5'],
            row_titles=['X3', 'X2', 'X1'],
            orientation=wx.VERTICAL,
            *args,
            **kwargs,
        )

        self.output_matrix = InputArray(
            parent=self,
            title='State of outputs:',
            dimension=(1, 4),
            col_titles=['K4', 'K3', 'K2', 'K1'],
            orientation=wx.VERTICAL,
            interface=DISPLAY_INTERFACE,
            is_input_indication=False,
            *args,
            **kwargs,
        )

        inner_panel_sizer = wx.BoxSizer(wx.VERTICAL)

        inner_panel_sizer.Add(self.input_matrix, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)
        inner_panel_sizer.Add(self.output_matrix, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.SetSizer(inner_panel_sizer)

    def array_hidden_state_set(self, new_order):
        self.input_matrix.visible_instances = new_order

    def array_hidden_state_update(self):
        pass

    def array_hidden_state_get(self):
        return self.input_matrix.visible_instances

    def configuration_set(self, new_array, matrix_inputs=True):
        """
            Didn't manage to come up with a better way of determining, which matrix to configure
            then pass a Bool value, indicating that we either DO or DO NOT use input_matrix(which
            is top one
        """
        if matrix_inputs:
            self.input_matrix.values = new_array
        else:
            self.output_matrix.values = new_array

    def configuration_update(self, *args, **kwargs):
        pass

    def configuration_get(self, matrix_inputs=True):
        if matrix_inputs:
            return self.input_matrix.values
        else:
            return self.output_matrix.values
