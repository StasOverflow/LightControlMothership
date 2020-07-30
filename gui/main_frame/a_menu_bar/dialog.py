import wx
from gui.utils.label_types import *
from gui.utils.labeled_data import LabelValueSequence

from gui.subcontainers.com_port_selector import ComPortSelector
from settings import Settings
from backend.ports.ports import serial_ports
from backend.modbus_backend import ModbusConnectionThreadSingleton


class SettingsDialog(wx.Dialog):

    def __init__(self, parent=None, title=None, **kwargs):

        # Initial construction procedure
        super().__init__(parent=parent)
        self.SetSize((250, 250))
        self.SetTitle(title)
        self.CenterOnParent()
        self.settings = Settings()
        self._garbage_evt_collector = 0

        instance = ModbusConnectionThreadSingleton()
        self.modbus = instance.thread_instance_get()

        # Create Background Panel and its sizer
        self.panel = wx.Panel(self)
        self.panel_sizer = wx.BoxSizer(wx.VERTICAL)

        # Create Settings Outline
        self.static_box = wx.StaticBox(self.panel, wx.ID_ANY, 'Settings')
        self.static_box_sizer = wx.StaticBoxSizer(self.static_box, wx.VERTICAL)

        # Create top row
        self.port_setup = ComPortSelector(
                                    parent=self.panel,
                                    label_caption='Device port',
                        )
        # self.panel.Bind(self.port_setup.item.event, self.on_choice, self.port_setup.item.choicer)

        # Create bottom row
        self.slave_address = LabelValueSequence(
                                    parent=self.panel,
                                    label='Slave ID',
                                    interface=LABELED_SPIN_CONTROL,
                                    button_required=False,
                                    initial_value=self.settings.slave_id,
                            )

        # Create Control Buttons
        self.button_accept = wx.Button(parent=self.panel, label='Accept')
        self.button_refresh = wx.Button(parent=self.panel, label='Refresh')
        self.button_connect = wx.Button(parent=self.panel, label='Connect')

        # Bind callbacks to newly created buttons
        self.panel.Bind(wx.EVT_BUTTON, self.port_setup.item.update_cb, self.button_refresh)
        self.panel.Bind(wx.EVT_BUTTON, self.on_accept, self.button_accept)
        self.panel.Bind(wx.EVT_BUTTON, self.on_connect, self.button_connect)

        # Wrap controls
        self.static_box_sizer.Add(self.port_setup)
        self.static_box_sizer.Add(self.slave_address)

        # Wrap buttons into sizer
        self.button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.button_sizer.Add(self.button_accept, 1, wx.ALL | wx.ALIGN_LEFT, 8)
        self.button_sizer.Add(self.button_refresh, 1, wx.ALL | wx.ALIGN_RIGHT, 8)

        self.button_conn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.button_conn_sizer.Add(self.button_connect, 1, wx.ALL | wx.ALIGN_CENTER, 8)

        # Wrap window items into window wrapper
        self.panel_sizer.Add(self.static_box_sizer, 5, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 15)
        self.panel_sizer.Add(self.button_sizer, 2, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 3)
        self.panel_sizer.Add(self.button_conn_sizer, 2, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 3)

        # Set panel sizer
        self.panel.SetSizer(self.panel_sizer)

    def _ports_update(self, event):
        self._garbage_evt_collector = event
        self.settings.port_list = serial_ports()

    def on_accept(self, event):
        self._garbage_evt_collector = event
        idx = self.port_setup.item.port_index
        self.settings.device_port = self.settings.port_list[idx]
        self.settings.slave_id = self.slave_address.value

    def on_connect(self, event):
        self.on_accept(event)

        if not self.modbus.is_connected:
            if self.settings.device_port is not None and self.settings.slave_id is not None:
                self.modbus.com_port_update(self.settings.device_port)
                self.modbus.slave_id_update(self.settings.slave_id)
                self.modbus.is_connected_state_set(True)

        self.Close()


class DebugPanel(wx.Panel):

    def __init__(self, *args, parent=None, **kwargs):
        super().__init__(parent=parent)

        self.dialog_window = SettingsDialog(
                                title='Connection setup',
                                *args,
                                **kwargs
                            )

        self.dialog_window.ShowModal()
        self.dialog_window.Close()


def main():
    app = wx.App()

    frame = wx.Frame(None, -1, 'win.py', size=(400, 400))

    settings = Settings()
    settings.settings_load()

    DebugPanel(parent=frame)

    app.Destroy()


if __name__ == '__main__':
    main()
