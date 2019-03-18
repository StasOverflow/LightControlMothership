import wx
import defs
from gui.control_inputs.app_cells import AppSpecificImageCell
from gui.control_inputs.app_cells import AppSpecificCheckBoxCell


class Cell(wx.BoxSizer):

    def __init__(self, *args, interface_type=defs.DISPLAY_INTERFACE, **kwargs):
        super().__init__(wx.HORIZONTAL)
        self.interface_type = interface_type
        if self.interface_type == defs.DISPLAY_INTERFACE:
            instance_class = AppSpecificImageCell
        else:
            instance_class = AppSpecificCheckBoxCell

        self.cell_instance = instance_class(*args, **kwargs)
        self.Add(self.cell_instance)
        self.cell_prev_state = None

    @property
    def checked(self):
        return self.cell_instance.checked

    @checked.setter
    def checked(self, new_state):
        """
            Setter should be used to check/uncheck output for child cell
        """
        if self.cell_prev_state != new_state:
            self.cell_prev_state = new_state
            self.cell_instance.checked = new_state

    def hide(self):
        self.cell_instance.hide()

    def show(self):
        # Just an alias to self.render()
        self.render()

    def render(self):
        self.cell_instance.render()

    @property
    def is_visible(self):
        return self.cell_instance.is_visible

    @is_visible.setter
    def is_visible(self, visible):
        self.cell_instance.is_visible = visible


class SuperPanel(wx.Panel):

    def __init__(self, parent):
        super().__init__(parent=parent)

        self.cell = Cell(parent=self, interface_type=defs.INPUT_INTERFACE)

        self.button = wx.Button(parent=self, label='switch', pos=(40, 40))

        self.hide_button = wx.Button(parent=self, label='hide', pos=(40, 80))
        self.show_button = wx.Button(parent=self, label='show', pos=(150, 80))

        self.Bind(wx.EVT_BUTTON, self.on_button, self.button)
        self.Bind(wx.EVT_BUTTON, self.on_hide, self.hide_button)
        self.Bind(wx.EVT_BUTTON, self.on_show, self.show_button)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.cell)

        self.SetSizer(sizer)

    def on_button(self, event):
        self.cell.checked = (not self.cell.checked)

    def on_hide(self, event):
        self.cell.is_visible = False

    def on_show(self, event):
        self.cell.is_visible = True


def main():

    app = wx.App()
    da_frame = wx.Frame(parent=None, title='Test')
    da_panel = SuperPanel(parent=da_frame)

    da_panel.Centre()

    da_panel.Fit()

    da_frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
