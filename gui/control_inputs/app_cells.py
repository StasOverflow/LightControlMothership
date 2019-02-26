import wx
from gui.control_inputs.image_cell import VariableImageCell


class AppSpecificImageCell(VariableImageCell):

    def __init__(self, parent, is_input_indication=True, *args, **kwargs):
        if is_input_indication:
            img_true = './static/images/green_led_button_5.png'
        else:
            img_true = './static/images/red_led_button_5.png'
        img_false = './static/images/disabled_button_5.png'
        super().__init__(parent, true_image_path=img_true, false_image_path=img_false, *args, **kwargs)


class CheckBoxCell(wx.BoxSizer):

    def __init__(self, parent, initial_checked_status=True, visible=True, *args, **kwargs):
        super().__init__(wx.HORIZONTAL)
        self.checkbox = None

        self.parent = parent
        self.is_visible = visible

        self.checkbox = wx.CheckBox(self.parent, *args)

        self.checked = initial_checked_status
        self.Add(self.checkbox)

    @property
    def checked(self):
        return self._checked

    @checked.setter
    def checked(self, new_state):
        self._checked = new_state
        self.checkbox.SetValue(self._checked)

    def hide(self):
        self.checkbox.Hide()

    def show(self):
        # Just an alias to self.render()
        self.render()

    def render(self):
        if self.checkbox is not None:
            self.checkbox.Show()

    @property
    def is_visible(self):
        return self._is_visible

    @is_visible.setter
    def is_visible(self, visible):
        self._is_visible = visible
        if self._is_visible:
            self.show()
        else:
            self.hide()
