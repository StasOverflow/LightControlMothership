import wx
from gui.control_inputs import defs
from gui.gui_sequences.tabs_source.base_sub_tab import BaseSubTab


# Define the tab content as classes:
class BaseTwoSplitTab(wx.Panel):
    def __init__(self, parent, *args, iface_types=(defs.INPUT_INTERFACE, defs.INPUT_INTERFACE), **kwargs):
        super().__init__(parent)

        self.top_page_inner_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.top_page_splitter = wx.SplitterWindow(self, style=wx.SP_BORDER)
        self.top_page_splitter.SetSashInvisible(invisible=False)

        self._left_panel_create(*args, iface_type=iface_types[0], **kwargs)
        self._right_panel_create(*args, iface_type=iface_types[1], **kwargs)

        self.top_page_splitter.SplitVertically(self.left_panel, self.right_panel)
        self.top_page_splitter.SetSashGravity(.5)

        self.top_page_inner_sizer.Add(self.top_page_splitter, 1, wx.EXPAND)
        self.SetSizer(self.top_page_inner_sizer)

    def _left_panel_create(self, *args, **kwargs):
        self.left_panel_title = None
        self.left_panel_checkbox_matrix = None

        if 'left_panel_title' in kwargs:
            self.left_panel_title = kwargs['left_panel_title']
            kwargs['style'] = wx.RAISED_BORDER
            kwargs['inner_title'] = self.left_panel_title
        self.left_panel = BaseSubTab(self.top_page_splitter, *args, **kwargs)

    def _right_panel_create(self, *args, **kwargs):
        if 'right_panel_title' in kwargs:
            kwargs['style'] = wx.BORDER_DEFAULT
            self.right_panel_title = kwargs['right_panel_title']
            kwargs['inner_title'] = self.right_panel_title

        if 'right_panel_button_title' in kwargs:
            kwargs['button_title'] = kwargs['right_panel_button_title']
        self.right_panel = BaseSubTab(self.top_page_splitter, *args, **kwargs)
