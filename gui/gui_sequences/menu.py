import wx
from gui.gui_sequences.menu_source.dialog import SettingsDialog


class MenuBarSequence(wx.MenuBar):

    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.connection_menu = wx.Menu()
        self.connect = self.connection_menu.Append(-1, 'Connection', 'Connection')

        self.help_menu = wx.Menu()
        self.about = self.help_menu.Append(-1, 'About', 'About')

        self.Append(self.connection_menu, 'Settings')
        self.Append(self.help_menu, 'Help')

        parent.Bind(wx.EVT_MENU, self.on_click_conn, self.connect)

    def on_click_conn(self, event):

        cdDialog = SettingsDialog(None, title='Change Color Depth')
        cdDialog.ShowModal()
        cdDialog.Destroy()


def main():
    app = wx.App()

    frame = wx.Frame(None, -1, 'win.py', size=(600, 500))

    menu_bar = MenuBarSequence(parent=frame)
    frame.SetMenuBar(menu_bar)
    frame.Show()

    app.MainLoop()


if __name__ == '__main__':
    main()
