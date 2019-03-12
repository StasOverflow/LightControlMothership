import wx
from gui.main_frame.top_panel.top_panel_content import TopPanel
from gui.main_frame.btm_panel.btm_panel_content import BtmPanel
import defs
from gui.main_frame.menu_bar.menu import MenuBarSequence
from settings import Settings


class MainFrame(wx.Frame):

    def __init__(self, *args, pos=(0,0), size=(400, 300), title="", **kwargs):
        print(size)
        self.size = size
        self.pos = (0, 0)
        self.super_sizer = wx.BoxSizer(wx.VERTICAL)

        style = wx.DEFAULT_FRAME_STYLE & ~wx.RESIZE_BORDER
        style = style ^ wx.MAXIMIZE_BOX
        wx.Frame.__init__(self, None, title=title, style=style,
                          size=self.size, pos=self.pos)

        self.Center()
        self.menu_bar = MenuBarSequence(parent=self, **kwargs)

        self.settings = Settings()

        main_panel = wx.Panel(parent=self, size=self.size)
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # Top of the page sequence
        self.top_canvas = TopPanel(parent=main_panel, iface_types=(defs.INPUT_INTERFACE, defs.DISPLAY_INTERFACE))

        # Bottom of the page sequence
        self.btm_canvas = BtmPanel(parent=main_panel, style=wx.LEFT)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.status_bottom_panel = wx.Panel(parent=main_panel)

        text = wx.StaticText(parent=self.status_bottom_panel, label='alyosha')
        sizer.Add(text)
        self.status_bottom_panel.SetSizer(sizer)

        '''
            Second parameter in every main_sizer.Add method call is a proportion
            value for every element of the window
        '''
        main_sizer.Add(self.top_canvas, 1,  wx.EXPAND)
        main_sizer.Add(self.btm_canvas, 1, wx.EXPAND)
        main_sizer.Add(self.status_bottom_panel, 1, wx.EXPAND)

        main_panel.SetSizer(main_sizer)
        main_panel.Layout()

        '''
            Must be called after all items are set, according to doc files. 
            If not, any items, initialized after calling SetMenuBar method
            won't be rendered
        '''
        self.SetMenuBar(self.menu_bar)

    def settings_update(self):
        """
            Update settings canvas values, specified inside

            Yet unspecified:
                self.top_canvas.left_panel.status.value

        """
        # self.top_canvas.left_panel.device_port.value = self.settings.device_port
        # self.top_canvas.left_panel.slave_id.value = self.settings.slave_id
        # self.top_canvas.left_panel.refresh_rate.value = self.settings.refresh_rate

    def render(self):
        self.Show()

