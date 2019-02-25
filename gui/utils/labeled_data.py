import os
import wx
from gui.utils.label_types import *


class _RightColumnLabel(wx.StaticText):

    def __init__(self, *args, parent=None, **kwargs):
        super(_RightColumnLabel, self).__init__(parent=parent, *args, **kwargs)


class _RightColumnCheckbox(wx.CheckBox):

    def __init__(self, *args, parent=None, label=None, **kwargs):
        super(_RightColumnCheckbox, self).__init__(*args, parent=parent, label='', **kwargs)


class _RightColumnChoice(wx.Choice):
    
    def __init__(self, *args, parent=None, **kwargs):
        super(_RightColumnChoice, self).__init__(*args, parent=parent, **kwargs)


class _RightColumnSpinCtrl(wx.BoxSizer):

    def __init__(self, *args, parent=None, label=None, size=None, **kwargs):
        super().__init__(wx.HORIZONTAL)
        self.spin = wx.SpinCtrl(*args, parent=parent, size=(40, -1), **kwargs)

        self.button = wx.Button(parent=parent, *args, **kwargs, size=(25, 24))

        path_to_file = './static/images/arrow_5.png'
        if os.path.isfile(path_to_file):
            self.image = wx.Image(path_to_file, wx.BITMAP_TYPE_PNG)
            self.image = self.image.ConvertToBitmap()
        else:
            raise FileNotFoundError
        self.button.SetBitmap(self.image, wx.LEFT)
        self.button.SetBitmapMargins((2, 2))  # default is 4 but that seems too big to me.

        self.Add(self.spin)
        self.Add(self.button)


class LabelValueSequence(wx.BoxSizer):

    ITEM_LIST = {
        LABELED_LABEL: _RightColumnLabel,
        LABELED_CHECK_BOX: _RightColumnCheckbox,
        LABELED_CHOICE_BOX: _RightColumnChoice,
        LABELED_SPIN_CONTROL: _RightColumnSpinCtrl,
    }

    def __init__(self, label, *args, parent=None, initial_value='None', margin=3, interface=LABELED_LABEL, **kwargs):
        # super().__init__(parent=parent, *args, **kwargs)
        super().__init__(wx.HORIZONTAL)
        self.margin = margin

        colon_label = str(label + ':')

        self.label = wx.StaticText(parent=parent, label=colon_label, size=(95, -1))

        self.value = initial_value

        item_class = self.ITEM_LIST[interface]

        self.item = item_class(
                    *args,
                    parent=parent,
                    label=initial_value,
                    style=wx.ALIGN_RIGHT,
                    size=(60, -1),
                    **kwargs
        )

        label_style = wx.ALL
        value_style = wx.ALL

        label_margin = self.margin
        value_margin = self.margin

        if interface == LABELED_SPIN_CONTROL:
            sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer.Add(self.label, 0, wx.TOP, 3)
            self.label = sizer

        self.Add(self.label, 0, label_style, label_margin)
        self.Add(self.item, 0, value_style, value_margin)

    # @property
    # def value(self):
    #     return self._value
    #
    # @value.setter
    # def value(self, new_value):
    #     if type(new_value) is not str:
    #         new_value = str(new_value)
    #     self._value = new_value
    #     self.item.SetLabel(self._value)


class LabeledIFaceInput(LabelValueSequence):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)

        self.input_checkbox = wx.CheckBox(
                        parent=parent,
                        style=wx.ALIGN_RIGHT,
                        size=(60, -1)
        )

        self.Add(self.input_checkbox, 0, wx.ALL, self.margin)
