import wx
from gui.control_inputs.input_array_box import InputArray
import gui.control_inputs.defs as defs


class TopLeftPanel(wx.Panel):

    def __init__(self, parent, color):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(color)


class InnerPanel(wx.Panel):

    def __init__(self, parent, *args, **kwargs):

        style = None
        if 'style' in kwargs:
            style = kwargs['style']
        if style is not None:
            super().__init__(parent, style=style)
        else:
            super().__init__(parent)

        self.inner_title = None
        self.setup_button = None

        if 'inner_title' in kwargs:
            self.inner_title = wx.StaticText(parent=self, label=kwargs['inner_title'])

        self.checkbox_matrix = InputArray(
            parent=self,
            title='State of inputs:',
            dimension=(3, 5),
            col_titles=['1', '2', '3', '4', '5'],
            row_titles=['X3', 'X2', 'X1'],
            orientation=wx.VERTICAL,
            *args,
            **kwargs,
        )

        if 'button_title' in kwargs:
            label = kwargs['button_title']
            if label is not None:
                self.setup_button = wx.Button(parent=self, label=label, size=(90, 30))

        # In this sequence we add elements (if they exists) to panel
        inner_panel_sizer = wx.BoxSizer(wx.VERTICAL)
        if self.inner_title is not None:
            inner_panel_sizer.Add(self.inner_title, .5, wx.ALL, 5)

        inner_panel_sizer.Add(self.checkbox_matrix, 8, wx.ALL | wx.CENTER, 15)
        if self.setup_button is not None:
            button_sizer = wx.BoxSizer(wx.HORIZONTAL)
            button_sizer.Add(self.setup_button, 1, wx.RIGHT, 22)
            inner_panel_sizer.Add(button_sizer, .7, wx.BOTTOM | wx.ALIGN_RIGHT, 10)

        self.SetSizer(inner_panel_sizer)


# Define the tab content as classes:
class TwoSplitTab(wx.Panel):
    def __init__(self, parent, *args, iface_types=(defs.INPUT_INTERFACE, defs.INPUT_INTERFACE), **kwargs):
        super().__init__(parent)

        self.top_page_inner_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.top_page_splitter = wx.SplitterWindow(self, style=wx.SP_BORDER)
        self.top_page_splitter.SetSashInvisible(invisible=False)

        # print('kwargos in two-tab are:', kwargs)
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
        self.left_panel = InnerPanel(self.top_page_splitter, *args, **kwargs)

    def _right_panel_create(self, *args, **kwargs):
        if 'right_panel_title' in kwargs:
            kwargs['style'] = wx.BORDER_DEFAULT
            self.right_panel_title = kwargs['right_panel_title']
            kwargs['inner_title'] = self.right_panel_title

        if 'right_panel_button_title' in kwargs:
            kwargs['button_title'] = kwargs['right_panel_button_title']
        self.right_panel = InnerPanel(self.top_page_splitter, *args, **kwargs)


class TopTab(TwoSplitTab):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

    def _left_panel_create(self, *args, **kwargs):
        self.left_panel = TopLeftPanel(self.top_page_splitter, 'blue')
