import wx
from gui.main_frame.a_top_panel.left_panel.left_panel_content import TopLeftPanel
from gui.main_frame.a_top_panel.right_panel.right_panel_content import TopRightPanel


class TopPanel(wx.Panel):

    def __init__(self, parent):

        super().__init__(parent)
        self.left_panel = None
        self.right_panel = None

        self.inner_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self._left_panel_create(self)
        self._right_panel_create(self)

        self.inner_sizer.Add(self.left_panel, 1, wx.EXPAND | wx.LEFT, 2)
        self.inner_sizer.Add(self.right_panel, 1, wx.EXPAND | wx.RIGHT, 2)
        self.SetSizer(self.inner_sizer)

    def _left_panel_create(self, parent):
        self.left_panel = TopLeftPanel(parent)

    def _right_panel_create(self, parent):
        self.right_panel = TopRightPanel(parent)
