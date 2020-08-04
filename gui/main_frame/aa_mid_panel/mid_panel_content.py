import wx
from defs import *
from settings import Settings, AppData
from gui.control_inputs.input_array_box import InputArray
from backend.modbus_backend import ModbusConnectionThreadSingleton


class _MidPanelContent(wx.Panel):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.conn_blink_state = 0
        self.settings = Settings()
        self.app_data = AppData()
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self._output_garbage_collector = 0
        self.act_indicator_wrapper = wx.BoxSizer(wx.VERTICAL)
        self.slave_id_sequence_wrapper = wx.BoxSizer(wx.VERTICAL)

        # Create display matrix for Relays
        self.output_matrix = InputArray(parent=self, title='Outputs state:',
                                        dimension=(1, 8),
                                        col_titles=['K1', 'K2', 'K3', 'K4',
                                                    'K5', 'K6', 'K7', 'K8'],
                                        interface=DISPLAY_INTERFACE,
                                        secret_ids=[1, 2, 3, 4, 5, 6, 7, 8],
                                        is_input_indication=False)
        self.output_matrix_wrapper = wx.BoxSizer(wx.VERTICAL)
        self.output_matrix_wrapper.Add(self.output_matrix, 0, wx.RIGHT | wx.ALIGN_RIGHT, 18)

        # Assign instance of modbus singleton, to have access to its props
        instance = ModbusConnectionThreadSingleton()
        self.modbus = instance.thread_instance_get()

        # Create an activity Led
        self.act_label = wx.StaticText(parent=self, label='Activity')
        self.activity_led = InputArray(parent=self, dimension=(1, 1), is_conn=True,
                                       interface=DISPLAY_INTERFACE, outlined=False)

        # Create Slave id sequence
        self.slave_id_label = wx.StaticText(parent=self, label='Slave ID')
        self.slave_id_control = wx.SpinCtrl(parent=self, size=(60, -1),
                                            style=wx.TE_LEFT, max=999)

        # Wrap indicator
        act_label_wrapper = wx.BoxSizer(wx.HORIZONTAL)
        led_activity_wrapper = wx.BoxSizer(wx.HORIZONTAL)
        act_label_wrapper.Add(self.act_label, 1, wx.LEFT, 8)
        led_activity_wrapper.Add(self.activity_led, 1, wx.LEFT, 21)
        self.act_indicator_wrapper.Add(act_label_wrapper, 2,  wx.TOP, 12)
        self.act_indicator_wrapper.Add(led_activity_wrapper, 2, wx.TOP, 14)

        # Wrap slave id
        slave_id_label_wrapper = wx.BoxSizer(wx.HORIZONTAL)
        slave_id_control_wrapper = wx.BoxSizer(wx.HORIZONTAL)
        slave_id_label_wrapper.Add(self.slave_id_label, 1, wx.LEFT, 3)
        slave_id_control_wrapper.Add(self.slave_id_control, 1, wx.LEFT, 8)
        self.slave_id_sequence_wrapper.Add(slave_id_label_wrapper, 3, wx.TOP, 18)
        self.slave_id_sequence_wrapper.Add(slave_id_control_wrapper, 2, wx.TOP, 4)

        # Bind events
        self.Bind(wx.EVT_SPINCTRL, self.slave_id_update, self.slave_id_control)
        self.app_data.iface_output_handler_register(self._slave_id_update)

        # Assemble panel sizer
        self.sizer.Add(self.act_indicator_wrapper, 1, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 20)
        self.sizer.Add(self.slave_id_sequence_wrapper, 1, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 20)
        self.sizer.Add(self.output_matrix_wrapper, 6, wx.EXPAND, 0)

        # Apply panel sizer
        self.SetSizer(self.sizer)

        # Register handler to update output state
        self.app_data.iface_output_handler_register(self._output_indication_update)

        # Insert a certain delay for refresh button
        self.timer = wx.Timer()
        self.timer_evt_handler = wx.EvtHandler()
        self.timer.SetOwner(self.timer_evt_handler, id=228)
        self.timer_evt_handler.Bind(wx.EVT_TIMER, self._refresh_conn_activity, self.timer, id=228)

        self.timer.Start(100, True)

    def _slave_id_update(self):
        self.value = self.settings.slave_id

    def slave_id_update(self, event):
        self._output_garbage_collector = event
        self.settings.slave_id = self.value
        self.modbus.slave_id_update(self.settings.slave_id)

    def _output_indication_update(self):
        for i in range(8):
            self.output_matrix.value_set_by_index(i, self.app_data.output_state_get(i))

    # Refresh callback, which is called every 100
    def _refresh_conn_activity(self, event):
        self._garbage_evt_collector = event
        self.timer.Start(100, True)
        self._can_be_refreshed = 1
        self._conn_indication()

    def _conn_indication(self):
        modbus_conn_state = self.modbus.is_connected
        self.activity_led.visible_instances = (modbus_conn_state,)
        if modbus_conn_state:
            if self._can_be_refreshed == 1:
                self._can_be_refreshed = 0
                self.conn_blink_state = not self.conn_blink_state
                self.activity_led.values = (self.conn_blink_state,)
            else:
                self.activity_led.values = (0,)
                self.conn_blink_state = 0

    @property
    def value(self):
        if self.slave_id_control:
            try:
                value = self.slave_id_control.GetValue()
            except Exception as e:
                print(e)
                value = None
            return value

    @value.setter
    def value(self, new_value):
        if self.slave_id_control:
            self.slave_id_control.SetValue(new_value)


class MidPanel(wx.BoxSizer):

    def __init__(self, parent=None):
        super().__init__(wx.HORIZONTAL)
        self.canvas = _MidPanelContent(parent=parent)

        self.Add(self.canvas, 1, wx.EXPAND)
