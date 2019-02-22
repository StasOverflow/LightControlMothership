import wx
from gui.control_inputs.input_matrix.input_array_box import InputArray


class BaseSubTab(wx.Panel):

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

