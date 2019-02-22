import wx
from gui.gui_sequences.base_tab import BaseTwoSplitTab


class TopLeftPanel(wx.Panel):

    def __init__(self, parent, color):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(color)


class TopTab(BaseTwoSplitTab):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

    def _left_panel_create(self, *args, **kwargs):
        self.left_panel = TopLeftPanel(self.top_page_splitter, 'blue')


class BtmTab(BaseTwoSplitTab):
    pass