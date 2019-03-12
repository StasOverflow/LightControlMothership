import wx
from gui.control_inputs.input_array_box import InputArray
from defs import *
from settings import AppData


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

        self.app_data = AppData()

        self.app_data.iface_handler_register(self._inputs_state_update)

        self.SetSizer(inner_panel_sizer)

    def _inputs_state_update(self):
        if self.app_data.mbus_data:
            self.configuration_set(self.app_data.inputs_combined_data, input_cfg=True)
            self.configuration_set(self.app_data.outputs_combined_data, input_cfg=False)

    def _inputs_visibility_update(self):
        if self.app_data.mbus_data:
            self.visibility_set(self.app_data.inputs_combined_visibility)

    def array_hidden_state_set(self, new_order):
        self.input_matrix.visible_instances = new_order

    def array_hidden_state_update(self):
        pass

    def array_hidden_state_get(self):
        return self.input_matrix.visible_instances

    def configuration_set(self, new_array, input_cfg=True):
        """
            Didn't manage to come up with a better way of determining, which matrix to configure
            then pass a Bool value, indicating that we either DO or DO NOT use input_matrix(which
            is top one
        """
        if input_cfg:
            self.input_matrix.values = new_array
        else:
            self.output_matrix.values = new_array

    def visibility_set(self, new_array):
        self.output_matrix.visible_instances = new_array

    def configuration_update(self, *args, **kwargs):
        pass

    def configuration_get(self, matrix_inputs=True):
        if matrix_inputs:
            return self.input_matrix.values
        else:
            return self.output_matrix.values
