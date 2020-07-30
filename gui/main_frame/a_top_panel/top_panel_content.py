import wx
from gui.basis.tabs.tab import BaseTwoSplitTab
from gui.main_frame.a_top_panel.left_panel.left_panel_content import TopLeftPanel
from gui.main_frame.a_top_panel.right_panel.right_panel_content import TopRightPanel


class _TopPanel(BaseTwoSplitTab):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

    def _left_panel_create(self, *args, **kwargs):
        self.left_panel = TopLeftPanel(self.top_page_splitter)

    def _right_panel_create(self, *args, **kwargs):
        self.right_panel = TopRightPanel(self.top_page_splitter)


class TopPanel(wx.BoxSizer):

    def __init__(self, *args, **kwargs):
        super().__init__(wx.HORIZONTAL)

        '''
            We use a list of sub_canvases to make top panel code look more like bottom panel's one 
        '''
        self.canvas = _TopPanel(*args, **kwargs)
        self.sub_canvases = list()
        self.sub_canvases.append(self.canvas)

        for canvas in self.sub_canvases:
            self.Add(canvas, 1, wx.ALL)
