import wx
import defs


class BaseTwoSplitTab(wx.Panel):
    def __init__(self, parent, *args, aydi=None, iface_types=(defs.INPUT_INTERFACE, defs.INPUT_INTERFACE), **kwargs):
        super().__init__(parent)

        self.left_panel_id = aydi

        self.top_page_inner_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.top_page_splitter = wx.SplitterWindow(self, style=wx.SP_BORDER)
        self.top_page_splitter.SetSashInvisible(invisible=False)

        self.left_panel = None
        self.right_panel = None

        self._left_panel_create(*args, interface=iface_types[0], **kwargs)
        self._right_panel_create(*args, interface=iface_types[1], **kwargs)

        try:
            self.top_page_splitter.SplitVertically(self.left_panel, self.right_panel)
        except NameError as e:
            print(e)

        self.top_page_splitter.SetSashGravity(.5)

        self.top_page_inner_sizer.Add(self.top_page_splitter, 1, wx.EXPAND)
        self.SetSizer(self.top_page_inner_sizer)

    def _left_panel_create(self, *args, **kwargs):
        pass

    def _right_panel_create(self, *args, **kwargs):
        pass
