import wx
from gui.gui_sequences.menu.menu_source.dialog import SettingsDialog


class MenuBarSequence(wx.MenuBar):

    def __init__(self, parent=None, label=None, *args, **kwargs):
        print(parent)
        super().__init__()

        self._settings = None

        if 'default_settings' in kwargs:
            self.settings = kwargs.pop('default_settings')

        self.getter_method = None
        if 'port_getter_method' in kwargs:
            self.getter_method = kwargs.pop('port_getter_method')

        self.parent = parent

        self.connection_menu = wx.Menu()
        self.connect = self.connection_menu.Append(-1, 'Connection', 'Connection')

        self.help_menu = wx.Menu()
        self.about = self.help_menu.Append(-1, 'About', 'About')

        self.Append(self.connection_menu, 'Settings')
        self.Append(self.help_menu, 'Help')

        self.dialog_window = None

        parent.Bind(wx.EVT_MENU, self.on_click_conn, self.connect)

    def on_click_conn(self, event):
        self.dialog_window = SettingsDialog(
                                title='Connection setup',
                                port_getter_method=self.getter_method,
                                settings=self.settings
                            )
        self.dialog_window.ShowModal()
        self.dialog_window.Close()
        self.dialog_window.Destroy()

    @property
    def settings(self):
        if hasattr(self, 'dialog_window'):
            if self.dialog_window:
                self._settings = self.dialog_window.settings
        return self._settings

    @settings.setter
    def settings(self, new_value):
        self._settings = new_value


def main():
    app = wx.App()

    frame = wx.Frame(None, -1, 'win.py', size=(600, 500))

    menu_bar = MenuBarSequence(parent=frame)
    frame.SetMenuBar(menu_bar)
    frame.Show()

    app.MainLoop()


if __name__ == '__main__':
    main()
