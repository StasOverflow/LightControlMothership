import wx
from gui.utils.labeled_data import LabelValueSequence
from gui.utils.label_types import *
from defs import *
from settings import Settings, AppData
from gui.control_inputs.input_array_box import InputArray
from backend.modbus_backend import ModbusConnectionThreadSingleton


class TopLeftPanel(wx.Panel):

    def __init__(self, parent):
        # Initial Constructor routines
        wx.Panel.__init__(self, parent)
        self.settings = Settings()
        self.app_data = AppData()
        self.output_garbage_collector = 0
        self.conn_blink_state = 0

        # Assign instance of modbus singleton, to have access to its props
        instance = ModbusConnectionThreadSingleton()
        self.modbus = instance.thread_instance_get()

        # Create sizers
        self.top_left_sizer_main = wx.BoxSizer(wx.HORIZONTAL)
        self.act_indicator_wrapper = wx.BoxSizer(wx.HORIZONTAL)
        self.top_inputs_sizer = wx.BoxSizer(wx.VERTICAL)

        # Create window sequences
        self.device_port = LabelValueSequence(parent=self, label='Device Port',
                                              interface=LABELED_LABEL)
        self.slave_id = LabelValueSequence(parent=self,
                                           label='Slave ID',
                                           interface=LABELED_SPIN_CONTROL,
                                           button_required=False,
                                           initial_value=self.settings.slave_id)
        self.act_label = wx.StaticText(parent=self, label='Activity')
        self.activity_led = InputArray(parent=self, dimension=(1, 1), is_conn=True,
                                       interface=DISPLAY_INTERFACE, outlined=False)

        # Wrap indicator
        self.act_indicator_wrapper.Add(self.act_label, 5, wx.ALL, 5)
        self.act_indicator_wrapper.Add(self.activity_led, 2, wx.ALL, 5)

        # Wrap top inputs
        self.top_inputs_sizer.Add(self.device_port)
        self.top_inputs_sizer.Add(self.slave_id)
        self.top_inputs_sizer.Add(self.act_indicator_wrapper, 1, wx.TOP | wx.ALIGN_LEFT, 25)

        # Wrap existing into intermediate sizer, to add padding
        self.top_left_sizer_main.Add(self.top_inputs_sizer, 1, wx.ALL, 20)
        self.SetSizer(self.top_left_sizer_main)

        self.Bind(wx.EVT_SPINCTRL, self.slave_id_update, self.slave_id.item.spin)

        self.app_data.iface_handler_register(self._port_update)
        self.app_data.iface_handler_register(self._slave_id_update)

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

    def _port_update(self):
        self.device_port.value = self.settings.device_port

    def _slave_id_update(self):
        self.slave_id.value = self.settings.slave_id

    def slave_id_update(self, event):
        self.output_garbage_collector = event
        self.settings.slave_id = self.slave_id.value
        self.modbus.slave_id_update(self.settings.slave_id)
