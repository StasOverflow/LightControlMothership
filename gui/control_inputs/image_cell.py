import wx
import os


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
        be reasonable to '.Add' its child elements to itself:
            methods 'true_state_image_set' and 'false_state_image_set' are
            used for that purpose, instead of '.Add'ing directly
    """

    def __init__(
            self, parent, initial_checked_status=False, visible=True,
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
            if image_type:      # Actually should look like 'if image_type == True:'
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

