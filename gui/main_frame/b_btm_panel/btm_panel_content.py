import wx
from defs import *
from settings import AppData, Settings
from gui.control_inputs.input_array_box import InputArray
from backend.modbus_backend import ModbusConnectionThreadSingleton
from gui.main_frame.b_btm_panel.left_panel.left_panel_content import BtmLeftPanel
from gui.main_frame.b_btm_panel.right_panel.right_panel_content import BtmRightPanel


class _BtmSubPanel(wx.Panel):

    def __init__(self, parent):
        # Basic Construction procedure
        super().__init__(parent)
        self.left_panel = None
        self.right_panel = None
        self.app_data = AppData()
        self.rb_value = 0

        # Create modbus instance, to have access to its props
        instance = ModbusConnectionThreadSingleton()
        self.modbus = instance.thread_instance_get()

        # Create sizers
        self.panel_sizer = wx.BoxSizer(wx.VERTICAL)
        self.upper_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.bottom_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Create upper sequence items
        self.output_mode_label = wx.StaticText(parent=self, label='Mode:')
        self.output_mode_rb_auto = wx.RadioButton(parent=self, id=0, label='Auto', style=wx.RB_GROUP)
        self.output_mode_rb_off = wx.RadioButton(parent=self, id=1, label='Off')
        self.output_mode_rb_on = wx.RadioButton(parent=self, id=2, label='On')
        # self.output_mode_rb_change = wx.RadioButton(parent=self, id=3, label='Change')

        self.output_state_label = wx.StaticText(parent=self, label='State:')
        self.output_led = InputArray(parent=self, dimension=(1, 1),
                                     interface=DISPLAY_INTERFACE, outlined=False,
                                     is_input_indication=False)

        # Create both panels
        self._left_panel_create(self)
        self._right_panel_create(self)

        # Prepare led state sizer
        self.led_state_sizer = wx.BoxSizer(wx.HORIZONTAL)
        led_inter_sizer = wx.BoxSizer(wx.VERTICAL)
        led_inter_sizer.Add(self.output_led, 1, wx.RIGHT | wx.ALIGN_RIGHT, 20)
        label_inter_sizer = wx.BoxSizer(wx.VERTICAL)
        label_inter_sizer.Add(self.output_state_label, 1, wx.LEFT, 85)
        self.led_state_sizer.Add(label_inter_sizer, 1, wx.ALL)
        self.led_state_sizer.Add(led_inter_sizer, 1, wx.ALL)

        # Wrap data into upper sizer
        self.upper_radio_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.upper_radio_sizer.Add(self.output_mode_label, 0, wx.LEFT, 15)
        self.upper_radio_sizer.Add(self.output_mode_rb_auto, 0, wx.LEFT, 5)
        self.upper_radio_sizer.Add(self.output_mode_rb_off, 0, wx.LEFT, 5)
        self.upper_radio_sizer.Add(self.output_mode_rb_on, 0, wx.LEFT, 5)
        # self.upper_radio_sizer.Add(self.output_mode_rb_change, 0, wx.LEFT, 5)

        self.upper_sizer.Add(self.upper_radio_sizer, 1, wx.TOP | wx.BOTTOM, 15)
        self.upper_sizer.Add(self.led_state_sizer, 5, wx.ALL, 15)

        # Wrap data into bottom sizer
        self.bottom_sizer.Add(self.left_panel, 1, wx.EXPAND | wx.LEFT, 2)
        self.bottom_sizer.Add(self.right_panel, 1, wx.EXPAND | wx.RIGHT, 2)

        # Wrap data into self sizer
        self.panel_sizer.Add(self.upper_sizer, 1, wx.EXPAND | wx.TOP, 5)
        self.panel_sizer.Add(self.bottom_sizer, 3, wx.EXPAND)

        # Apply self sizer
        self.SetSizer(self.panel_sizer)

        # Beautify
        self.output_mode_rb_auto.Disable()
        self.output_mode_rb_off.Disable()
        self.output_mode_rb_on.Disable()
        # self.output_mode_rb_change.Disable()

        # Bind Callbacks
        self.Bind(wx.EVT_RADIOBUTTON, self._radio_button_callback, self.output_mode_rb_auto)
        self.Bind(wx.EVT_RADIOBUTTON, self._radio_button_callback, self.output_mode_rb_off)
        self.Bind(wx.EVT_RADIOBUTTON, self._radio_button_callback, self.output_mode_rb_on)
        # self.Bind(wx.EVT_RADIOBUTTON, self._radio_button_callback, self.output_mode_rb_change)

        self.app_data.iface_output_handler_register(self.radio_buttons_visibility_handler)

    def radio_buttons_visibility_handler(self):
        if self.modbus.is_connected:
            try:
                if self.output_mode_rb_auto:
                    self.output_mode_rb_auto.Enable()
                if self.output_mode_rb_off:
                    self.output_mode_rb_off.Enable()
                if self.output_mode_rb_on:
                    self.output_mode_rb_on.Enable()
                # if self.output_mode_rb_change:
                #     self.output_mode_rb_change.Enable()
            except Exception as e:
                print(e)
        else:
            try:
                if self.output_mode_rb_auto:
                    self.output_mode_rb_auto.Disable()
                if self.output_mode_rb_off:
                    self.output_mode_rb_off.Disable()
                if self.output_mode_rb_on:
                    self.output_mode_rb_on.Disable()
                # if self.output_mode_rb_change:
                #     self.output_mode_rb_change.Disable()
            except Exception as e:
                print(e)
            self.rb_value = -1

    def rb_layout(self):
        if self.rb_value == 0:
            if self.output_mode_rb_auto:
                self.output_mode_rb_auto.SetValue(True)
                self.output_mode_rb_auto.Layout()
        elif self.rb_value == 1:
            if self.output_mode_rb_off:
                self.output_mode_rb_off.SetValue(True)
                self.output_mode_rb_off.Layout()
        elif self.rb_value == 2:
            if self.output_mode_rb_on:
                self.output_mode_rb_on.SetValue(True)
                self.output_mode_rb_on.Layout()
        # elif self.rb_value == 3:
        #     if self.output_mode_rb_change:
        #         self.output_mode_rb_change.SetValue(True)
        #         self.output_mode_rb_change.Layout()

    def _left_panel_create(self, parent):
        self.left_panel = BtmLeftPanel(parent)

    def _right_panel_create(self, parent):
        self.right_panel = BtmRightPanel(parent)

    def _radio_button_callback(self, event):
        self.app_data.user_interaction = True
        if self.modbus.is_connected and self.app_data.modbus_data is not None:
            self.rb_value = event.GetId()


class _BtmPanel(wx.Panel):

    def __init__(self, parent=None):

        super().__init__(parent=parent)

        self.app_data = AppData()

        self.modbus = ModbusConnectionThreadSingleton()
        self.modbus = self.modbus.thread_instance_get()

        self.btm_page_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.notebook_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.notebook = wx.Notebook(self)
        self.sub_canvases = list()
        for i in range(8):
            self.sub_canvases.append(_BtmSubPanel(parent=self.notebook))
            self.notebook.AddPage(self.sub_canvases[i], "Relay " + str(1 + i))

        '''
            Here goes a very important line of a code, setting notebook
            item's color to default window color instead of white color,
            chosen by default, when creating widget
        '''
        self.notebook.SetOwnBackgroundColour(self.GetBackgroundColour())
        self.notebook_sizer.Add(self.notebook, 0, wx.EXPAND)

        self.btm_page_sizer.Add(self.notebook_sizer, 0, wx.EXPAND)
        self.SetSizer(self.btm_page_sizer)

        # Apply data on connection
        self.app_data.iface_conn_handler_register(self._input_left_matrix_update_on_conn)
        self.app_data.iface_conn_handler_register(self._input_radio_data_set_on_conn)

        # Interface handlers, always called to update data on screen
        self.app_data.iface_output_handler_register(self._out_led_update)
        self.app_data.iface_output_handler_register(self._matrix_visibility_update)
        self.app_data.iface_output_handler_register(self._input_right_matrix_update)

        # Gather input data handlers
        self.app_data.iface_input_handler_register(self._input_left_matrix_data_gather)
        self.app_data.iface_input_handler_register(self._input_radio_data_gather)

        self._input_matrix_enabled = 0

        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.on_page_change)

    def on_page_change(self, event):
        page = event.GetSelection()
        if self.modbus.is_connected:
            self.sub_canvases[page].rb_value = self.app_data.output_mode_get(page)
            self.sub_canvases[page].rb_layout()

    def _input_left_matrix_data_gather(self):
        for out_id in range(8):
            val_list = []
            left_panel = self.sub_canvases[out_id].left_panel
            for in_id in range(15):
                value = left_panel.input_matrix.value_get_by_index(in_id)
                val_list.append(value)

            self.app_data.output_associated_input_set_mask(out_id, val_list)

    def _input_left_matrix_update_on_conn(self):
        # Update left matrix when we acquire connection
        for out_id in range(8):
            left_panel = self.sub_canvases[out_id].left_panel

            for in_id in range(15):
                value = self.app_data.output_associated_input_get(out_id, in_id)
                left_panel.input_matrix.value_set_by_index(in_id, value)

    def _input_right_matrix_update(self):
        # Update right matrix when we acquire connection
        for out_id in range(8):
            right_panel = self.sub_canvases[out_id].right_panel

            for in_id in range(15):
                is_visible = self.app_data.output_associated_input_get(out_id, in_id)
                right_panel.input_matrix.visibility_set_by_index(in_id, is_visible)

                value = self.app_data.input_state_get(in_id)
                right_panel.input_matrix.value_set_by_index(in_id, value)

    def _input_radio_data_set_on_conn(self):
        val_list = list()
        for out_id, sub_cvs in enumerate(self.sub_canvases):
            sub_cvs.rb_value = self.app_data.output_mode_get(out_id)
            val_list.append(sub_cvs.rb_value)
            sub_cvs.rb_layout()

    def _input_radio_data_gather(self):
        val_list = list()
        for out_id, sub_cvs in enumerate(self.sub_canvases):
            val_list.append(sub_cvs.rb_value)
            self.app_data.output_mode_set(out_id, sub_cvs.rb_value)

    def _matrix_visibility_update(self):
        if self.modbus.is_connected:
            for out_id in range(8):
                left_panel = self.sub_canvases[out_id].left_panel
                if self._input_matrix_enabled is False:
                    left_panel.input_matrix.enable()
                    self._input_matrix_enabled = True
        else:
            for out_id in range(8):
                left_panel = self.sub_canvases[out_id].left_panel
                if self._input_matrix_enabled is True:
                    left_panel.input_matrix.disable()
                    self._input_matrix_enabled = False

    def _out_led_update(self):
        for i in range(8):
            self.sub_canvases[i].output_led.values = [self.app_data.output_state_get(i), ]


class BtmPanel(wx.BoxSizer):

    def __init__(self, parent=None):
        super().__init__(wx.HORIZONTAL)
        self.canvas = _BtmPanel(parent=parent)

        self.Add(self.canvas, 1, wx.ALL)
