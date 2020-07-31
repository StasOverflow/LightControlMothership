import wx
from gui.main_frame.b_btm_panel.left_panel.left_panel_content import BtmLeftPanel
from gui.main_frame.b_btm_panel.right_panel.right_panel_content import BtmRightPanel
from defs import *


class _BtmSubPanel(wx.Panel):

    def __init__(self, parent=None, aydi=None):
        super().__init__(parent)

        self.left_panel_id = aydi

        self.top_page_inner_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.top_page_splitter = wx.SplitterWindow(self, style=wx.SP_BORDER)
        self.top_page_splitter.SetSashInvisible(invisible=False)

        self.left_panel = None
        self.right_panel = None

        self._left_panel_create()
        self._right_panel_create()

        try:
            self.top_page_splitter.SplitVertically(self.left_panel, self.right_panel)
        except NameError as e:
            print(e)

        self.top_page_splitter.SetMinimumPaneSize(212)
        self.top_page_splitter.SetSashGravity(.5)

        self.top_page_inner_sizer.Add(self.top_page_splitter, 1, wx.EXPAND)
        self.SetSizer(self.top_page_inner_sizer)

    def _left_panel_create(self):
        self.left_panel = BtmLeftPanel(self.top_page_splitter)

    def _right_panel_create(self):
        pass
        self.right_panel = BtmRightPanel(self.top_page_splitter,
                                         inner_title='Setup',
                                         style=wx.BORDER_RAISED,
                                         aydi=self.left_panel_id)


class _BtmPanel(wx.Panel):

    def __init__(self, parent=None):

        super().__init__(parent=parent)
        self.btm_page_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.notebook_sizer = wx.BoxSizer(wx.HORIZONTAL)

        notebook = wx.Notebook(self)
        self.sub_canvases = list()
        for i in range(8):
            self.sub_canvases.append(_BtmSubPanel(parent=notebook, aydi=i))
            notebook.AddPage(self.sub_canvases[i], "Relay " + str(1 + i))

        '''
            Here goes a very important line of a code, setting notebook
            item's color to default window color instead of white color,
            chosen by default, when creating widget
        '''
        notebook.SetOwnBackgroundColour(self.GetBackgroundColour())
        self.notebook_sizer.Add(notebook, 5, wx.EXPAND | wx.CENTER)

        self.btm_page_sizer.Add(self.notebook_sizer, 1, wx.EXPAND)
        self.SetSizer(self.btm_page_sizer)


class BtmPanel(wx.BoxSizer):

    def __init__(self, parent=None):
        super().__init__(wx.HORIZONTAL)
        self.canvas = _BtmPanel(parent=parent)

        self.Add(self.canvas, 1, wx.ALL)
