import wx
from gui.basis.tabs.tab import BaseTwoSplitTab
from gui.main_frame.b_btm_panel.left_panel.left_panel_content import BtmLeftPanel
from gui.main_frame.b_btm_panel.right_panel.right_panel_content import BtmRightPanel
from defs import *


class _MidPanelContent(wx.Panel):

    def __init__(self, parent=None):

        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        super().__init__(parent=parent)

        # notebook = wx.Notebook(self, **kwargs)
        # self.sub_canvases = list()
        # for i in range(8):
        #     self.sub_canvases.append(_BtmSubPanel(parent=notebook, aydi=i))
        #     notebook.AddPage(self.sub_canvases[i], "Relay " + str(1 + i))

        '''
            Here goes a very important line of a code, setting notebook
            item's color to default window color instead of white color,
            chosen by default, when creating widget
        '''
        # notebook.SetOwnBackgroundColour(self.GetBackgroundColour())
        #
        # bottom_inner_sizer.Add(notebook, 5, wx.EXPAND | wx.CENTER)

        # self.sizer.Add(bottom_inner_sizer, 1, wx.EXPAND)
        self.SetSizer(self.sizer)


class MidPanel(wx.BoxSizer):

    def __init__(self, parent=None):
        super().__init__(wx.HORIZONTAL)

        self.canvas = _MidPanelContent(parent=parent)

        # self.sub_canvases = self.canvas.sub_canvases
        self.Add(self.canvas, 1, wx.ALL)
