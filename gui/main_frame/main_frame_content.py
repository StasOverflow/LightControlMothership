import wx
from gui.main_frame.a_top_panel.top_panel_content import TopPanel
from gui.main_frame.aa_mid_panel.mid_panel_content import MidPanel
from gui.main_frame.b_btm_panel.btm_panel_content import BtmPanel
from gui.main_frame.c_status_panel.staus_panel_content import StatusPanel
import defs
from gui.main_frame.a_menu_bar.menu import MenuBarSequence
from settings import Settings, AppData


class MainFrame(wx.Frame):

    def __init__(self, pos=(0, 0), size=(400, 300), title=""):
        self.size = size
        self.pos = pos

        # FIXME: Why this self.super_sizer is still present
        # self.super_sizer = wx.BoxSizer(wx.VERTICAL)

        self.app_data = AppData()
        self.settings = Settings()

        style = wx.DEFAULT_FRAME_STYLE  # Create a Frame style
        style ^= wx.RESIZE_BORDER       # Restrict resizing actions
        style ^= wx.MAXIMIZE_BOX        # Disable Maximize Button

        # Create Centered application frame
        wx.Frame.__init__(self, None, title=title, style=style,
                          size=self.size, pos=self.pos)
        self.Center()

        # Create Menu Bar
        self.menu_bar = MenuBarSequence(parent=self)

        main_panel = wx.Panel(parent=self, size=self.size)
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # Top of the page sequence
        self.top_canvas = TopPanel(parent=main_panel)

        # Mid of the page sequence
        self.mid_canvas = MidPanel(parent=main_panel)

        # Bottom of the page sequence
        self.btm_canvas = BtmPanel(parent=main_panel)

        # Under bottom of the page sequence
        self.status_bottom_panel = StatusPanel(parent=main_panel)

        main_sizer.Add(self.top_canvas, 0,  wx.EXPAND)
        main_sizer.Add(self.mid_canvas, 0, wx.EXPAND)
        main_sizer.Add(self.btm_canvas, 0, wx.EXPAND)
        main_sizer.Add(self.status_bottom_panel, 0, wx.EXPAND)

        main_panel.SetSizer(main_sizer)
        main_panel.Layout()

        """
            Must be called after all items are set, according to doc files. 
            If not, any items, initialized after calling SetMenuBar method
            won't be rendered
        """
        self.SetMenuBar(self.menu_bar)

    def render(self):
        self.Show()

