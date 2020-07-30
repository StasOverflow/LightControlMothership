import wx
from gui.main_frame.a_menu_bar.dialog import SettingsDialog
from settings import Settings
from backend.modbus_backend import ModbusConnectionThreadSingleton


class MenuBarSequence(wx.MenuBar):

    def __init__(self, parent=None):

        # Basic construction stuff
        super().__init__()
        self.parent = parent
        self.settings = Settings()
        self._garbage_event_collector = 0

        instance = ModbusConnectionThreadSingleton()
        self.modbus = instance.thread_instance_get()

        # Start with connect menu
        self.conn_submenu = wx.Menu()
        self.conn_submenu_item_connect = self.conn_submenu.Append(-1, 'Connect...', 'Connect...')
        self.conn_submenu_item_disconnect = self.conn_submenu.Append(-1, 'Disconnect', 'Disconnect')
        self.conn_submenu.AppendSeparator()
        self.conn_submenu_item_quick_conn = self.conn_submenu.Append(-1, 'Quick Connect', 'Quick Connect')

        # TODO: Decide if this one is needed
        # self.help_menu = wx.Menu()
        # self.about = self.help_menu.Append(-1, 'About', 'About')

        self.Append(self.conn_submenu, 'Connection')
        # self.Append(self.help_menu, 'Help')

        self.dialog_window = None

        parent.Bind(wx.EVT_MENU, self.on_click_conn, self.conn_submenu_item_connect)
        parent.Bind(wx.EVT_MENU, self.on_clock_dc, self.conn_submenu_item_disconnect)
        parent.Bind(wx.EVT_MENU, self.on_click_quick_conn, self.conn_submenu_item_quick_conn)

        # Insert a certain delay for refresh button
        self.timer = wx.Timer()
        self.timer_evt_handler = wx.EvtHandler()
        self.timer.SetOwner(self.timer_evt_handler, id=228)
        self.timer_evt_handler.Bind(wx.EVT_TIMER, self._refresh, self.timer, id=228)

        self._refresh(wx.EVT_TIMER)

    # Refresh callback, which is called every _some_time
    def _refresh(self, event):
        self._garbage_evt_collector = event

        if self.modbus.is_connected:
            self.conn_submenu_item_connect.Enable(False)
            self.conn_submenu_item_disconnect.Enable(True)
            self.conn_submenu_item_quick_conn.Enable(False)
        else:
            self.conn_submenu_item_connect.Enable(True)
            self.conn_submenu_item_disconnect.Enable(False)
            self.conn_submenu_item_quick_conn.Enable(True)
        self.timer.Start(200, True)

    def on_click_conn(self, event):
        self._garbage_event_collector = event

        self.dialog_window = SettingsDialog(
                                title='Connection setup',
                            )
        self.dialog_window.ShowModal()
        self.dialog_window.Close()
        self.dialog_window.Destroy()

    def on_clock_dc(self, event):
        self._garbage_event_collector = event
        self.modbus.is_connected_state_set(False)

    def on_click_quick_conn(self, event):
        self._garbage_event_collector = event

        if not self.modbus.is_connected:
            if self.settings.device_port is not None and self.settings.slave_id is not None:
                self.modbus.com_port_update(self.settings.device_port)
                self.modbus.slave_id_update(self.settings.slave_id)
                self.modbus.is_connected_state_set(True)


# In case we need to debug menu separately
def main():
    app = wx.App()

    settings = Settings()
    settings.settings_load()

    frame = wx.Frame(None, -1, 'win.py', size=(400, 400))

    menu_bar = MenuBarSequence(parent=frame)
    frame.SetMenuBar(menu_bar)
    frame.Show()

    app.MainLoop()


if __name__ == '__main__':
    main()
