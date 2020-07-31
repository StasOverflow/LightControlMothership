import wx
from defs import *
from gui.control_inputs.input_array_box import InputArray
from backend.modbus_backend import ModbusConnectionThreadSingleton


class _MidPanelContent(wx.Panel):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.conn_blink_state = 0
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.act_indicator_wrapper = wx.BoxSizer(wx.HORIZONTAL)

        # Create display matrix for Relays
        self.output_matrix = InputArray(parent=self, title='State of outputs:',
                                        dimension=(1, 8),
                                        col_titles=['K1', 'K2', 'K3', 'K4',
                                                    'K5', 'K6', 'K7', 'K8'],
                                        interface=DISPLAY_INTERFACE,
                                        secret_ids=[1, 2, 3, 4, 5, 6, 7, 8], )
        self.output_matrix_wrapper = wx.BoxSizer(wx.VERTICAL)
        self.output_matrix_wrapper.Add(self.output_matrix, 0, wx.RIGHT | wx.ALIGN_RIGHT, 18)

        # Assign instance of modbus singleton, to have access to its props
        instance = ModbusConnectionThreadSingleton()
        self.modbus = instance.thread_instance_get()

        # Create an override button
        # self.override_btn = wx.Button(parent=self, label='Override')

        # Create an activity Led
        self.act_label = wx.StaticText(parent=self, label='Activity')
        self.activity_led = InputArray(parent=self, dimension=(1, 1), is_conn=True,
                                       interface=DISPLAY_INTERFACE, outlined=False)

        # Wrap indicator
        self.act_indicator_wrapper.Add(self.act_label, 5, wx.ALL, 5)
        self.act_indicator_wrapper.Add(self.activity_led, 0, wx.ALL, 5)

        # Assemble panel sizer
        self.sizer.Add(self.act_indicator_wrapper, 2, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 20)
        self.sizer.Add(self.output_matrix_wrapper, 6, wx.TOP | wx.BOTTOM | wx.EXPAND, 10)

        # Apply panel sizer
        self.SetSizer(self.sizer)

        # Insert a certain delay for refresh button
        self.timer = wx.Timer()
        self.timer_evt_handler = wx.EvtHandler()
        self.timer.SetOwner(self.timer_evt_handler, id=228)
        self.timer_evt_handler.Bind(wx.EVT_TIMER, self._refresh_conn_activity, self.timer, id=228)

        self.timer.Start(100, True)

    # Refresh callback, which is called every 100
    def _refresh_conn_activity(self, event):
        self._garbage_evt_collector = event
        self.timer.Start(100, True)
        self._can_be_refreshed = 1
        self._conn_indication()

    def _conn_indication(self):
        modbus_conn_state = 1 if self.modbus.is_connected else 0
        self.activity_led.visible_instances = (modbus_conn_state,)
        if modbus_conn_state:
            if not self.modbus.exception_state:
                if self._can_be_refreshed == 1:
                    self._can_be_refreshed = 0
                    self.conn_blink_state = not self.conn_blink_state
                    self.activity_led.values = (self.conn_blink_state,)
            else:
                self.activity_led.values = (0,)
                self.conn_blink_state = 0


class MidPanel(wx.BoxSizer):

    def __init__(self, parent=None):
        super().__init__(wx.HORIZONTAL)
        self.canvas = _MidPanelContent(parent=parent)

        self.Add(self.canvas, 1, wx.EXPAND)
