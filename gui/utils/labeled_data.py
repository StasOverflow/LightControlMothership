import os
import wx
from gui.utils.label_types import *
from gui.utils.utils import execute_every


class _RightColumnLabel(wx.StaticText):

    def __init__(self, *args, parent=None, **kwargs):
        super(_RightColumnLabel, self).__init__(parent=parent, *args, **kwargs)


class _RightColumnCheckbox(wx.CheckBox):

    def __init__(self, *args, parent=None, label=None, **kwargs):
        super(_RightColumnCheckbox, self).__init__(*args, parent=parent, label='', **kwargs)


class _RightColumnChoice(wx.BoxSizer):
    
    def __init__(self, *args, parent=None, label=None, port_getter_method=None, size=None, **kwargs):

        super().__init__(wx.HORIZONTAL)

        self.choices_data = None
        self.port_getter_method = port_getter_method
        self.data_spectial_setter()

        self.choicer = wx.Choice(parent, size=(71, -1), choices=self.choices_data, **kwargs)
        self.choicer.SetLabel(self.choices_data[0])
        self.choicer.SetSelection(0)

        self.Add(self.choicer, 0, wx.LEFT, 0)

        self.update_choices()

    @property
    def choices_data(self):
        if self._choices_data is not None:
            return self._choices_data
        else:
            return ['Sample 1', 'Sample 2']

    @choices_data.setter
    def choices_data(self, choices):
        self._choices_data = choices

    def data_spectial_setter(self):
        if self.port_getter_method is not None and callable(self.port_getter_method):
            self.choices_data = self.port_getter_method()

    @execute_every
    def update_choices(self):
        self.data_spectial_setter()
        if self.choicer.GetItems() != self.choices_data:
            pass
            self.choicer.Clear()
            self.choicer.Append(self.choices_data)


class _RightColumnSpinCtrl(wx.BoxSizer):

    def __init__(
            self,
            *args,
            parent=None,
            label=None,
            size=None,
            button_required=True,
            style=None,
            **kwargs
    ):
        super().__init__(wx.HORIZONTAL)
        self.spin = wx.SpinCtrl(
                        *args,
                        parent=parent,
                        size=(47 + 25*(not button_required), -1),
                        style=wx.TE_LEFT,
                        **kwargs)
        self.Add(self.spin, 0, wx.LEFT)

        if button_required:
            self.button = wx.Button(*args, parent=parent, size=(25, 24), **kwargs)

            path_to_file = './static/images/arrow_5.png'
            if os.path.isfile(path_to_file):
                self.image = wx.Image(path_to_file, wx.BITMAP_TYPE_PNG)
                self.image = self.image.ConvertToBitmap()
            else:
                raise FileNotFoundError
            self.button.SetBitmap(self.image, wx.LEFT)
            self.button.SetBitmapMargins((2, 2))  # default is 4 but that seems too big to me.

            self.Add(self.button)


class _RightColumnTextInput(wx.BoxSizer):

    def __init__(self, *args, parent=None, label=None, size=None, style=None, **kwargs):
        super().__init__(wx.HORIZONTAL)

        self.text_field = wx.TextCtrl(parent=parent, size=(71, 20), style=wx.TE_LEFT, **kwargs)
        self.Add(self.text_field, 0, wx.ALIGN_RIGHT, 2)
    #
    # hbox1.Add(self.t1, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
    # self.t1.Bind(wx.EVT_TEXT, self.OnKeyTyped)
    # vbox.Add(hbox1)

class LabelValueSequence(wx.BoxSizer):

    ITEM_LIST = {
        LABELED_LABEL: _RightColumnLabel,
        LABELED_CHECK_BOX: _RightColumnCheckbox,
        LABELED_CHOICE_BOX: _RightColumnChoice,
        LABELED_SPIN_CONTROL: _RightColumnSpinCtrl,
        LABELED_TEXT_INPUT: _RightColumnTextInput,
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

        if (
                interface == LABELED_SPIN_CONTROL
                or interface == LABELED_CHOICE_BOX
                or interface == LABELED_TEXT_INPUT
        ):
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
