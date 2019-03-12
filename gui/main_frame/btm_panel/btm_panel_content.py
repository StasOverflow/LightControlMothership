import wx
from gui.basis.tabs.tab import BaseTwoSplitTab
from gui.main_frame.btm_panel.left_panel.left_panel_content import BtmLeftPanel
from gui.main_frame.btm_panel.right_panel.right_panel_content import BtmRightPanel
from defs import *


class _BtmSubPanel(BaseTwoSplitTab):

    def __init__(self, parent=None, *args, aydi=None, **kwargs):
        super().__init__(parent=parent, iface_types=(DISPLAY_INTERFACE, INPUT_INTERFACE),
                         outlined=False, aydi=aydi)

    def _left_panel_create(self, *args, **kwargs):
        self.left_panel = BtmLeftPanel(self.top_page_splitter, *args, inner_title='Status',
                                       style=wx.RAISED_BORDER, aydi=self.left_panel_id, **kwargs)

    def _right_panel_create(self, *args, **kwargs):
        self.right_panel = BtmRightPanel(self.top_page_splitter, *args, style=wx.BORDER_DEFAULT,
                                         aydi=self.left_panel_id, inner_title='Setup')


class _BtmPanel(wx.Panel):

    def __init__(self, *args, parent=None, **kwargs):

        bottom_page_sizer = wx.BoxSizer(wx.HORIZONTAL)

        super().__init__(parent=parent)

        bottom_inner_sizer = wx.BoxSizer(wx.HORIZONTAL)

        notebook = wx.Notebook(self, **kwargs)
        self.sub_canvases = list()
        for i in range(4):
            self.sub_canvases.append(_BtmSubPanel(parent=notebook, aydi=i))
            notebook.AddPage(self.sub_canvases[i], "Relay: K" + str(1 + i))

        '''
            Here goes a very important line of a code, setting notebook
            item's color to default window color instead of white color,
            chosen by default, when creating widget
        '''
        notebook.SetOwnBackgroundColour(self.GetBackgroundColour())

        bottom_inner_sizer.Add(notebook, 5, wx.EXPAND | wx.CENTER)

        bottom_page_sizer.Add(bottom_inner_sizer, 1, wx.EXPAND)
        self.SetSizer(bottom_page_sizer)


class BtmPanel(wx.BoxSizer):

    def __init__(self, *args, parent=None, **kwargs):
        super().__init__(wx.HORIZONTAL)

        self.canvas = _BtmPanel(parent=parent, **kwargs)

        self.sub_canvases = self.canvas.sub_canvases
        self.Add(self.canvas, 1, wx.EXPAND)
