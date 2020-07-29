import os
import wx
from gui.utils.label_types import *
from gui.utils.utils import execute_every
from settings import Settings


class _RightColumnLabel(wx.StaticText):

    def __init__(self, *args, parent=None, **kwargs):
        super(_RightColumnLabel, self).__init__(parent=parent, *args, **kwargs)
        self.value = self.GetLabel()

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if self:
            if type(new_value) is not str:
                new_value = str(new_value)
            if new_value is None or new_value == 'None' or new_value == '':
                self._value = 'None'
            else:
                self._value = new_value
            self.SetLabel(self._value)


class _RightColumnCheckbox(wx.CheckBox):

    def __init__(self, *args, parent=None, label=None, **kwargs):
        super(_RightColumnCheckbox, self).__init__(*args, parent=parent, label='', **kwargs)
        self.value = self.IsChecked()

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if isinstance(new_value, bool):  # returns True if boolean
            self._value = new_value
            self.SetValue(self._value)


class _RightColumnChoice(wx.BoxSizer):  # wx.Choices

    event = wx.EVT_CHOICE

    def __init__(self, *args, parent=None, button_required=True, label=None, size=None, initial_value=None, **kwargs):

        super().__init__(wx.HORIZONTAL)

        self.choices_data = None
        self.settings = Settings()

        self.choicer = wx.Choice(parent, size=(73, -1), choices=self.choices_data)

        if button_required:
            self.button = wx.Button(*args, parent=parent, size=(25, 23))

            path_to_file = './static/images/refresh_3.png'
            if os.path.isfile(path_to_file):
                self.image = wx.Image(path_to_file, wx.BITMAP_TYPE_PNG)
                self.image = self.image.ConvertToBitmap()
            else:
                raise FileNotFoundError
            self.button.SetBitmap(self.image, wx.LEFT)

            self.Add(self.button, 0, wx.BOTTOM, 5)

        self.Add(self.choicer, 1, wx.LEFT, 0)

        self.data_special_setter()
        self.update_choices()
        self.value = initial_value

    @execute_every
    def update_choices(self):
        if self.choicer:
            self.data_special_setter()
            if self.choicer.GetItems() != self.choices_data:
                self.choicer.Clear()
                self.choicer.Append(self.choices_data)

    @property
    def choices_data(self):
        data = ['']
        if self._choices_data is not None:
            if self.settings.port_list:
                data = self._choices_data
        return data

    @choices_data.setter
    def choices_data(self, choices):
        self._choices_data = choices

    def data_special_setter(self):
        self.choices_data = self.settings.port_list

    @property
    def value(self):
        return self.choices_data[self.choicer.GetCurrentSelection()]

    @value.setter
    def value(self, new_value):
        print(new_value)

        if new_value is not None:
            try:
                self.choicer.SetSelection(self.choices_data.index(new_value))
                self.button.Layout()
            except ValueError:
                pass


class _RightColumnSpinCtrl(wx.BoxSizer):
    """
        SPIN CONTROL
    """

    def __init__(
            self,
            *args,
            parent=None,
            label=None,
            size=None,
            button_required=False,
            style=None,
            **kwargs
    ):
        super().__init__(wx.HORIZONTAL)
        self.spin = wx.SpinCtrl(
                        *args,
                        parent=parent,
                        size=(47 + 25*(not button_required), -1),
                        style=wx.TE_LEFT,
                        max=999,
                        **kwargs
                    )
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
            self.button.SetBitmapMargins((2, 2))

            self.Add(self.button)

    @property
    def value(self):
        if self.spin:
            try:
                value = self.spin.GetValue()
            except Exception as e:
                value = None
            return value

    @value.setter
    def value(self, new_value):
        if self.spin:
            self.spin.SetValue(new_value)


class _RightColumnTextInput(wx.BoxSizer):

    def __init__(self, *args, parent=None, label=None, size=None, style=None, **kwargs):
        super().__init__(wx.HORIZONTAL)

        self.text_field = wx.TextCtrl(parent=parent, size=(71, 20), style=wx.TE_LEFT, **kwargs)
        self.Add(self.text_field, 0, wx.ALIGN_RIGHT, 2)

    @property
    def value(self):
        return self.text_field.GetValue()

    @value.setter
    def value(self, new_value):
        if type(new_value) is not str:
            new_value = str(new_value)
        self.text_field.SetValue(new_value)


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

        x_size = 95

        self.label = wx.StaticText(parent=parent, label=colon_label, size=(x_size, -1))

        item_class = self.ITEM_LIST[interface]

        self.item = item_class(
                    *args,
                    parent=parent,
                    style=wx.ALIGN_RIGHT,
                    size=(60, -1),
                    **kwargs
        )

        self.value = initial_value

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

    @property
    def value(self):
        return self.item.value

    @value.setter
    def value(self, new_value):
        if self.item.value != new_value:
            self.item.value = new_value
            if self.item:
                self.item.Layout()


class LabeledIFaceInput(LabelValueSequence):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)

        self.input_checkbox = wx.CheckBox(
                        parent=parent,
                        style=wx.ALIGN_RIGHT,
                        size=(60, -1)
        )

        self.Add(self.input_checkbox, 0, wx.ALL, self.margin)
