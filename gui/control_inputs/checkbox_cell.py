import wx


class CheckBoxCell(wx.BoxSizer):

    def __init__(self, parent, initial_checked_status=False, visible=True, *args, **kwargs):
        super().__init__(wx.HORIZONTAL)
        self.checkbox = None

        self.parent = parent
        self.is_visible = visible

        self.checkbox = wx.CheckBox(self.parent, *args)

        self.checked = initial_checked_status
        self.Add(self.checkbox)

        self.checked = initial_checked_status

    @property
    def checked(self):
        if self.checkbox:
            self._checked = self.checkbox.IsChecked()
        return self._checked

    @checked.setter
    def checked(self, new_state):
        self._checked = new_state
        if self.checkbox:
            self.checkbox.SetValue(self._checked)

    def hide(self):
        if self.checkbox:
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
