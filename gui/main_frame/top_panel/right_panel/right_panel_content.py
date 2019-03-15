import wx
from gui.control_inputs.input_array_box import InputArray
from defs import *
from settings import AppData
from backend.modbus_backend import ModbusConnectionThreadSingleton
import time


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
            col_titles=[' 1', ' 2', ' 3', ' 4', ' 5'],
            row_titles=['X3', 'X2', 'X1'],
            orientation=wx.VERTICAL,
            *args,
            **kwargs,
        )

        self.output_matrix = InputArray(parent=self, title='State of outputs:', dimension=(1, 4),
                                        col_titles=['K4', 'K3', 'K2', 'K1'], orientation=wx.VERTICAL,
                                        interface=DISPLAY_INTERFACE, is_input_indication=False,
                                        *args, is_button=True, secret_ids=[4, 3, 2, 1], **kwargs)

        inner_panel_sizer = wx.BoxSizer(wx.VERTICAL)

        inner_panel_sizer.Add(self.input_matrix, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        output_matrix_wrapper = wx.BoxSizer(wx.HORIZONTAL)
        output_matrix_wrapper.Add(self.output_matrix, 0, wx.LEFT, 10)

        btm_of_page_sizer = wx.BoxSizer(wx.HORIZONTAL)

        for index, instance in enumerate(self.output_matrix.instance_array):
            for image in instance.cell_instance.image:
                image.Bind(wx.EVT_LEFT_DOWN, self._on_mouse_down)

        conn_label = wx.StaticText(parent=self, label='ACT')
        self.connection_matrix = InputArray(parent=self, dimension=(1, 1), orientation=wx.VERTICAL,
                                            interface=DISPLAY_INTERFACE, is_input_indication=False,
                                            *args, is_button=True, secret_ids=[5], row_titles=[''],
                                            outlined=False, is_conn=True,
                                            **kwargs)
        self.prev_state = False
        self.connection_matrix.visible_instances = (self.prev_state, )

        self.blink_state = False
        self.prev_blink_timestamp = 0

        vertical_conn_btn_sizer = wx.BoxSizer(wx.VERTICAL)

        vertical_conn_btn_sizer.Add(conn_label, 0,  wx.LEFT, 25)
        vertical_conn_btn_sizer.Add(self.connection_matrix, 0, wx.TOP | wx.RIGHT, 10)

        btm_of_page_sizer.Add(vertical_conn_btn_sizer, 0, wx.RIGHT | wx.TOP, 10)
        btm_of_page_sizer.Add(output_matrix_wrapper)
        inner_panel_sizer.Add(btm_of_page_sizer)

        self.app_data = AppData()
        self.app_data.iface_handler_register(self._inputs_state_update)
        self.app_data.iface_handler_register(self._conn_indication)

        self.mbus = ModbusConnectionThreadSingleton()
        self.mbus = self.mbus.modbus_comm_instance

        self.SetSizer(inner_panel_sizer)

    def _conn_indication(self):
        state = self.mbus.is_connected
        if state != self.prev_state:
            self.prev_state = state
            if not self.mbus.exception_state:
                self.connection_matrix.visible_instances = (state, )
        if self.mbus.is_connected:
            time_current = time.monotonic()
            if time_current - self.prev_blink_timestamp >= 0.05:
                self.prev_blink_timestamp = time_current
                self.blink_state = not self.blink_state
            self.connection_matrix.values = (self.blink_state, )

    def _on_mouse_down(self, event):
        print('pressed', event.GetEventObject().parent_class.secret_id)

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
