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
        self.output_mode_rb_change = wx.RadioButton(parent=self, id=3, label='Change')

        self.output_state_label = wx.StaticText(parent=self, label='State:')
        self.output_led = InputArray(parent=self, dimension=(1, 1),
                                     interface=DISPLAY_INTERFACE, outlined=False)

        # Create both panels
        self._left_panel_create(self)
        self._right_panel_create(self)

        # Prepare led state sizer
        self.led_state_sizer = wx.BoxSizer(wx.HORIZONTAL)
        led_inter_sizer = wx.BoxSizer(wx.VERTICAL)
        led_inter_sizer.Add(self.output_led, 1, wx.RIGHT | wx.ALIGN_RIGHT, 20)
        label_inter_sizer = wx.BoxSizer(wx.VERTICAL)
        label_inter_sizer.Add(self.output_state_label, 1, wx.LEFT, 45)
        self.led_state_sizer.Add(label_inter_sizer, 1, wx.ALL)
        self.led_state_sizer.Add(led_inter_sizer, 1, wx.ALL)

        # Wrap data into upper sizer
        self.upper_radio_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.upper_radio_sizer.Add(self.output_mode_label, 0, wx.LEFT, 15)
        self.upper_radio_sizer.Add(self.output_mode_rb_auto, 0, wx.LEFT, 5)
        self.upper_radio_sizer.Add(self.output_mode_rb_off, 0, wx.LEFT, 5)
        self.upper_radio_sizer.Add(self.output_mode_rb_on, 0, wx.LEFT, 5)
        self.upper_radio_sizer.Add(self.output_mode_rb_change, 0, wx.LEFT, 5)

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
        self.output_mode_rb_change.Disable()

        # Bind Callbacks
        self.Bind(wx.EVT_RADIOBUTTON, self._radio_button_callback, self.output_mode_rb_auto)
        self.Bind(wx.EVT_RADIOBUTTON, self._radio_button_callback, self.output_mode_rb_off)
        self.Bind(wx.EVT_RADIOBUTTON, self._radio_button_callback, self.output_mode_rb_on)
        self.Bind(wx.EVT_RADIOBUTTON, self._radio_button_callback, self.output_mode_rb_change)

        self.app_data.iface_handler_register(self._radio_buttons_visibility_handler)

    def _radio_buttons_visibility_handler(self):
        if self.modbus.is_connected:
            try:
                if self.output_mode_rb_auto:
                    self.output_mode_rb_auto.Enable()
                if self.output_mode_rb_off:
                    self.output_mode_rb_off.Enable()
                if self.output_mode_rb_on:
                    self.output_mode_rb_on.Enable()
                if self.output_mode_rb_change:
                    self.output_mode_rb_change.Enable()
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
                if self.output_mode_rb_change:
                    self.output_mode_rb_change.Disable()
            except Exception as e:
                print(e)

    def _left_panel_create(self, parent):
        self.left_panel = BtmLeftPanel(parent)

    def _right_panel_create(self, parent):
        self.right_panel = BtmRightPanel(parent)

    def _radio_button_callback(self, event):
        if self.modbus.is_connected and self.app_data.modbus_data is not None:
            print('handled', event.GetId())
        #     data_byte = self.app_data.modbus_data[6]
        #     data_bits = event.GetId()
        #     shifting_val = 0    # self.id * 2
        #     data_byte &= ~(3 << shifting_val)
        #     data_byte |= (data_bits << shifting_val)
        #     self.modbus.queue_insert(data_byte, 4)


class _BtmPanel(wx.Panel):

    def __init__(self, parent=None):

        super().__init__(parent=parent)
        self.btm_page_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.notebook_sizer = wx.BoxSizer(wx.HORIZONTAL)

        notebook = wx.Notebook(self)
        self.sub_canvases = list()
        for i in range(8):
            self.sub_canvases.append(_BtmSubPanel(parent=notebook))
            notebook.AddPage(self.sub_canvases[i], "Relay " + str(1 + i))

        '''
            Here goes a very important line of a code, setting notebook
            item's color to default window color instead of white color,
            chosen by default, when creating widget
        '''
        notebook.SetOwnBackgroundColour(self.GetBackgroundColour())
        self.notebook_sizer.Add(notebook, 0, wx.EXPAND)

        self.btm_page_sizer.Add(self.notebook_sizer, 0, wx.EXPAND)
        self.SetSizer(self.btm_page_sizer)


class BtmPanel(wx.BoxSizer):

    def __init__(self, parent=None):
        super().__init__(wx.HORIZONTAL)
        self.canvas = _BtmPanel(parent=parent)

        self.Add(self.canvas, 1, wx.ALL)
