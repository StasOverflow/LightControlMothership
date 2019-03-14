import wx
from gui.utils.labeled_data import LabelValueSequence
from gui.utils.label_types import *
from settings import Settings, AppData
from backend.modbus_backend import ModbusConnectionThreadSingleton


class ConnectButton(wx.BoxSizer):

    def __init__(self, parent, connect_label='Connect', disconnect_label='Disconnect'):
        super().__init__(wx.HORIZONTAL)

        self.button = wx.Button(parent=parent, label=connect_label, style=wx.EXPAND, size=(90, 27))
        self.Add(self.button, 1, wx.TOP, 18)


class TopLeftPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.settings = Settings()
        self.assets = AppData()

        instance = ModbusConnectionThreadSingleton()
        self.mbus = instance.thread_instance_get()

        self.top_left_sizer_main = wx.BoxSizer(wx.HORIZONTAL)
        self.top_left_sizer_v = wx.BoxSizer(wx.VERTICAL)
        self.top_inputs_sizer = wx.BoxSizer(wx.VERTICAL)

        self.status = LabelValueSequence(parent=self, label='Status', interface=LABELED_LABEL)
        self.device_port = LabelValueSequence(parent=self, label='Device Port', interface=LABELED_LABEL)
        self.slave_id = LabelValueSequence(parent=self, label='Slave ID',
                                           interface=LABELED_SPIN_CONTROL,
                                           initial_value=0)

        self.Bind(wx.EVT_BUTTON, self.slave_id_update, self.slave_id.item.button)
        self.Bind(wx.EVT_SPINCTRL, self.slave_id_update, self.slave_id.item.spin)

        # self.refresh_rate = LabelValueSequence(parent=self, label='Refresh rate', interface=LABELED_LABEL)
        # self.checkbox = LabelValueSequence(parent=self, label='Show unused', interface=LABELED_CHECK_BOX)

        self.conn_button = ConnectButton(parent=self)

        self.Bind(wx.EVT_BUTTON, self.connect_disconnect, self.conn_button.button)

        self.top_inputs_sizer.Add(self.status)
        self.top_inputs_sizer.Add(self.device_port)
        self.top_inputs_sizer.Add(self.slave_id)
        # self.top_inputs_sizer.Add(self.refresh_rate)
        # self.top_inputs_sizer.Add(self.checkbox, 0, wx.TOP, 2)

        self.top_left_sizer_v.Add(self.top_inputs_sizer, 0, wx.BOTTOM, 2)
        self.top_left_sizer_v.Add(self.conn_button, 0, wx.BOTTOM | wx.ALIGN_RIGHT, 5)

        self.line = wx.StaticLine(self, wx.ID_ANY, style=wx.LI_VERTICAL)

        self.top_left_sizer_h = wx.BoxSizer(wx.HORIZONTAL)

        self.top_left_sizer_h.Add(self.top_left_sizer_v, 0, wx.LEFT, 25)

        self.top_left_sizer_main.Add(self.top_left_sizer_h, wx.EXPAND, wx.TOP, 16)
        self.top_left_sizer_main.Add(self.line, 0, wx.LEFT | wx.EXPAND, 14)

        self.SetSizer(self.top_left_sizer_main)

        self.assets.iface_handler_register(self._button_update)
        self.assets.iface_handler_register(self._port_update)
        self.assets.iface_handler_register(self._slave_id_update)
        # self.assets.iface_handler_register(self._refresh_rate_update)

    def _button_update(self):
        if self.conn_button:
            if self.conn_button:
                try:
                    if self.mbus.is_connected:
                        self.conn_button.button.SetLabel('Disconnect')
                    else:
                        self.conn_button.button.SetLabel('Connect')
                except RuntimeError:
                    pass

    def _port_update(self):
        self.device_port.value = self.settings.device_port

    def _slave_id_update(self):
        self.slave_id.value = self.settings.slave_id

    def _refresh_rate_update(self):
        self.refresh_rate.value = self.settings.refresh_rate

    def connect_disconnect(self, event):
        if not self.mbus.is_connected:
            if self.settings.device_port is not None and self.settings.slave_id is not None:
                self.mbus.com_port_update(self.settings.device_port)
                self.mbus.slave_id_update(self.settings.slave_id)
                self.mbus.is_connected_state_set(True)
            else:
                if self.settings.device_port is not None:
                    pass
                else:
                    print('self settings device port is not not None')
                if self.settings.slave_id is not None:
                    pass
                else:
                    print('self.settings.slave_id is not not None')

        else:
            self.mbus.is_connected_state_set(False)

    def slave_id_update(self, event):
        self.settings.slave_id = self.slave_id.value
        if not self.mbus.is_connected:
            self.mbus.slave_id_update(self.settings.slave_id)
        else:
            '''
                implement one more queue method inside of a modbus module for this particular case 
            '''
            pass
            # self.mbus.is_connected_state_set(False)
            # self.mbus.slave_id_update(self.settings.slave_id)
            # self.mbus.is_connected_state_set(True)
