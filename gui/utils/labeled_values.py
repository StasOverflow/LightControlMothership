import wx


class LabelValueSequence(wx.BoxSizer):

    def __init__(self, parent, label, margin=3):
        super().__init__(wx.HORIZONTAL)
        self.margin = margin

        colon_label = str(label + ':')

        self.static_text = wx.StaticText(parent=parent, label=colon_label, size=(95, -1))
        self.Add(self.static_text, 0, wx.ALL, self.margin)


class LabeledVisualIFace(LabelValueSequence):
    def __init__(self, parent, *args, initial_value='None', **kwargs):
        super().__init__(parent=parent, *args, **kwargs)

        self.value_label = wx.StaticText(parent=parent, label='', style=wx.ALIGN_RIGHT, size=(60, -1))
        self.value = initial_value
        self.Add(self.value_label, 0, wx.ALL, self.margin)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if type(new_value) is not str:
            new_value = str(new_value)
        self._value = new_value
        self.value_label.SetLabel(self._value)


class LabeledInputIFace(LabelValueSequence):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)

        self.input_checkbox = wx.CheckBox(
                        parent=parent,
                        style=wx.ALIGN_RIGHT,
                        size=(60, -1)
        )

        self.Add(self.input_checkbox, 0, wx.ALL, self.margin)