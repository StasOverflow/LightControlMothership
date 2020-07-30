import wx
from gui.utils.labeled_data import LabelValueSequence
from gui.utils.label_types import *
from settings import Settings, AppData
from backend.modbus_backend import ModbusConnectionThreadSingleton
from gui.main_frame.a_top_panel.left_panel.dialog.relay_dialog import RelayDialog


class WrappedButton(wx.BoxSizer):

    def __init__(self, parent, label='Connect'):
        super().__init__(wx.HORIZONTAL)

        self.button = wx.Button(parent=parent, label=label, style=wx.EXPAND, size=(80, 27))
        self.Add(self.button, 1, wx.TOP, 18)


class TopLeftPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.settings = Settings()
        self.app_data = AppData()

        instance = ModbusConnectionThreadSingleton()
        self.mbus = instance.thread_instance_get()

        self.top_left_sizer_main = wx.BoxSizer(wx.HORIZONTAL)
        self.top_left_sizer_v = wx.BoxSizer(wx.VERTICAL)
        self.top_inputs_sizer = wx.BoxSizer(wx.VERTICAL)

        self.device_port = LabelValueSequence(parent=self, label='Device Port', interface=LABELED_LABEL)
        self.slave_id = LabelValueSequence(parent=self, label='Slave ID',
                                           interface=LABELED_SPIN_CONTROL,
                                           initial_value=0)

        self.dialog_window = None

        self.top_inputs_sizer.Add(self.device_port)
        self.top_inputs_sizer.Add(self.slave_id)

        self.top_left_sizer_v.Add(self.top_inputs_sizer, 0, wx.BOTTOM, 2)

        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.top_left_sizer_v.Add(button_sizer, 0, wx.TOP, 85)

        self.line = wx.StaticLine(self, wx.ID_ANY, style=wx.LI_VERTICAL)

        self.top_left_sizer_h = wx.BoxSizer(wx.HORIZONTAL)

        self.top_left_sizer_h.Add(self.top_left_sizer_v, 0, wx.LEFT, 25)

        self.top_left_sizer_main.Add(self.top_left_sizer_h, wx.EXPAND, wx.TOP, 16)
        self.top_left_sizer_main.Add(self.line, 0, wx.LEFT | wx.EXPAND, 14)

        self.SetSizer(self.top_left_sizer_main)

        self.app_data.iface_handler_register(self._port_update)
        self.app_data.iface_handler_register(self._slave_id_update)

    def _port_update(self):
        self.device_port.value = self.settings.device_port

    def _slave_id_update(self):
        self.slave_id.value = self.settings.slave_id

    def dialog_handler(self, event):
        self.dialog_window = RelayDialog(title='Relay mode setup')
        self.dialog_window.ShowModal()
        self.dialog_window.Close()
        self.dialog_window.Destroy()

    def slave_id_update(self, event):
        self.settings.slave_id = self.slave_id.value
        self.mbus.slave_id_update(self.settings.slave_id)
