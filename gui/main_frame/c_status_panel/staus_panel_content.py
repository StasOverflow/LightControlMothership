import wx
from settings import AppData
from settings import Settings
from backend.modbus_backend import ModbusConnectionThreadSingleton


class StatusPanel(wx.Panel):

    STATUSES = {
        0: 'Connected',
        1: 'Disconnected',
        2: 'Connection timeout'
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        inner_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.modbus_label = ' '
        self.conn_static_text = wx.StaticText(parent=self, label='Connection status')
        self.modbus_status_text = wx.StaticText(parent=self, label='')

        inner_sizer.Add(self.conn_static_text, 2, wx.LEFT | wx.ALIGN_LEFT, 10)
        inner_sizer.Add(self.modbus_status_text, 4, wx.LEFT | wx.ALIGN_LEFT, 120)

        self.main_sizer.Add(inner_sizer, 1, wx.ALL | wx.EXPAND, 2)

        self.appdata = AppData()
        self.modbus = ModbusConnectionThreadSingleton().modbus_comm_instance
        self.SetSizer(self.main_sizer)

        self.appdata.iface_handler_register(self._conn_status_update)
        self.appdata.iface_handler_register(self._modbus_data_update)

        self.status = 1
        self.conn_static_text.SetLabel(self.STATUSES[self.status])

    def _conn_status_update(self):
        if self.modbus.is_connected:
            status = 0
            if self.modbus.exception_state_get():
                status = 2
        else:
            status = 1
        if status != self.status:
            self.status = status
            try:
                self.conn_static_text.SetLabel(self.STATUSES[self.status])
            except RuntimeError:
                pass

    def _modbus_data_update(self):
        if self.modbus.is_connected:
            label = 'Port: ' + str(self.modbus.port) + '; ' + str(self.modbus.baudrate) + '-' + \
                    str(self.modbus.bytesize) + '-' + str(self.modbus.parity) + '-' + \
                    str(self.modbus.stopbits)
            if label != self.modbus_label:
                self.modbus_label = label
                try:
                    self.modbus_status_text.SetLabel(self.modbus_label)
                except RuntimeError:
                    pass
