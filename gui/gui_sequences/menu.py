import wx
from gui.gui_sequences.menu_source.dialog import SettingsDialog


class MenuBarSequence(wx.MenuBar):

    def __init__(self, parent=None, label=None, *args, **kwargs):
        print(parent)
        super().__init__()

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
        self.dialog_window = SettingsDialog(title='Connection setup')
        self.dialog_window.ShowModal()
        self.dialog_window.Close()
        self.dialog_window.Destroy()


def main():
    app = wx.App()

    frame = wx.Frame(None, -1, 'win.py', size=(600, 500))

    menu_bar = MenuBarSequence(parent=frame)
    frame.SetMenuBar(menu_bar)
    frame.Show()

    app.MainLoop()


if __name__ == '__main__':
    main()
