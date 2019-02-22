import wx
import os
from gui.control_inputs import defs


class BitmapImageCustom(wx.StaticBitmap):

    def __init__(self, parent, path_to_file):
        self.path_to_file = path_to_file
        if os.path.isfile(self.path_to_file):
            self.image = wx.Image(self.path_to_file, wx.BITMAP_TYPE_PNG)
        else:
            raise FileNotFoundError
        # self.png = self.png.Scale(self.MaxImageSize, self.MaxImageSize, wx.IMAGE_QUALITY_HIGH)
        self.image = self.image.ConvertToBitmap()
        super().__init__(parent, -1, self.image, size=(self.image.GetWidth(), self.image.GetHeight()))


class VariableImageCell(wx.BoxSizer):
    """
        Class represents a box sizer, which contaings an image.
        Image can be changed by changing state of a Cell

        Because this class is subclassed from wx.BoxSizer, i think it would
        be reasonable to 'Add' its child elements to itself:
            methods 'true_state_image_set' and 'false_state_image_set' are
            used for that purpose, instead of 'Add'-ing directly
    """

    def __init__(
            self, parent, initial_checked_status=True, visible=True,
            two_state=True, true_image_path=None, false_image_path=None,
            *args, **kwargs
    ):
        super().__init__(wx.HORIZONTAL)
        self.two_state = None

        self.parent = parent
        self.is_visible = visible

        self.image = list()
        self.true_image_address = None
        self.false_image_address = None
        self.two_state = two_state
        print(self.two_state)

        self.true_state_image_set(path_to_file=true_image_path)
        self.false_state_image_set(path_to_file=false_image_path)

        self.checked = initial_checked_status

    @property
    def checked(self):
        return self._checked

    @checked.setter
    def checked(self, new_state):
        self._checked = new_state
        self.state_image_update()

    def _image_set(self, image_type, path):
        if path is not None:
            instance = BitmapImageCustom(parent=self.parent, path_to_file=path)
            self.image.append(instance)
            index = self.image.index(instance)
            if image_type:      # Actually looks like 'if image_type == True:'
                self.true_image_address = index
            else:
                self.false_image_address = index
            self.image[index].Hide()
            self.Add(self.image[index])

    def true_state_image_set(self, path_to_file=None):
        self._image_set(True, path_to_file)

    def false_state_image_set(self, path_to_file=None):
        self._image_set(False, path_to_file)

    def state_image_update(self):
        if self.two_state:
            if self.true_image_address is not None and self.false_image_address is not None:
                if self.is_visible:
                    self.image[self.true_image_address].Show()
                    self.image[self.false_image_address].Show()
                    if self.checked:
                        self.image[self.false_image_address].Hide()
                    else:
                        self.image[self.true_image_address].Hide()
        else:
            pass
            # implement behavior where we determine if we have at least one image set up and render it

    def hide(self):
        self.ShowItems(False)

    def show(self):
        # Just an alias to self.render()
        self.render()

    def render(self):
        self.state_image_update()

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


class AppSpecificImageCell(VariableImageCell):

    def __init__(self, parent, is_input_indication=True, *args, **kwargs):
        if is_input_indication:
            img_true = './static/images/green_led_button_5.png'
        else:
            img_true = './static/images/red_led_button_5.png'
        img_false = './static/images/disabled_button_5.png'
        print('calling to super')
        super().__init__(parent, true_image_path=img_true, false_image_path=img_false, *args, **kwargs)


class CheckBoxCell(wx.BoxSizer):

    def __init__(self, parent, initial_checked_status=True, visible=True, *args, **kwargs):
        super().__init__(wx.HORIZONTAL)
        print('called to checbkox cell')
        self.checkbox = None

        self.parent = parent
        self.is_visible = visible

        self.checkbox = wx.CheckBox(self.parent, *args, **kwargs)

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


class Cell(wx.BoxSizer):

    def __init__(self, *args, interface_type=defs.DISPLAY_INTERFACE, **kwargs):
        super().__init__(wx.HORIZONTAL)
        if interface_type == defs.DISPLAY_INTERFACE:
            instance_class = AppSpecificImageCell
        else:
            instance_class = CheckBoxCell

        self.cell_instance = instance_class(*args, **kwargs)
        self.Add(self.cell_instance)

    @property
    def checked(self):
        return self.cell_instance.checked

    @checked.setter
    def checked(self, new_state):
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
        # self.png1 = AppSpecificImageCell(parent=self)
        # self.png1.render()

        self.cell = Cell(parent=self, interface_type=defs.INPUT_INTERFACE)
        # png2 = CellImage(parent=self, path_to_file='./static/images/green_led_button_5.png')
        # png3 = CellImage(parent=self, path_to_file='./static/images/disabled_button_5.png')

        self.button = wx.Button(parent=self, label='switch', pos=(40, 40))

        self.hide_button = wx.Button(parent=self, label='hide', pos=(40, 80))
        self.show_button = wx.Button(parent=self, label='show', pos=(150, 80))

        self.Bind(wx.EVT_BUTTON, self.on_button, self.button)
        self.Bind(wx.EVT_BUTTON, self.on_hide, self.hide_button)
        self.Bind(wx.EVT_BUTTON, self.on_show, self.show_button)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        # sizer.Add(self.png1)
        sizer.Add(self.cell)
        # sizer.Add(png2)
        # sizer.Add(png3)

        self.SetSizer(sizer)

    def on_button(self, event):
        self.cell.checked = (not self.cell.checked)

    def on_hide(self, event):
        self.cell.is_visible = False

    def on_show(self, event):
        self.cell.is_visible = True


def main():

    app = wx.App()
    da_frame = wx.Frame(parent=None, title='Calculator')
    da_panel = SuperPanel(parent=da_frame)

    da_panel.Centre()

    da_panel.Fit()

    da_frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
