import wx
import os


class BitmapImageCustom(wx.StaticBitmap):

    def __init__(self, parent, path_to_file, parent_class, **kwargs):
        self.path_to_file = path_to_file
        if os.path.isfile(self.path_to_file):
            self.image = wx.Image(self.path_to_file, wx.BITMAP_TYPE_PNG)
        else:
            raise FileNotFoundError
        self.parent_class = parent_class
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
            true_image_path=None, false_image_path=None, is_button=False,
            *args, secret_id=None, **kwargs
    ):
        super().__init__(wx.HORIZONTAL)

        self.cur_invisible_state = False
        self.is_visible = None
        self.cur_state = None
        self.parent = parent

        if secret_id is not None:
            print(self)
            self.secret_id = secret_id

        self.true_image_address = true_image_path
        self.false_image_address = false_image_path

        self.image = list()
        self.true_state_image_set(path_to_file=true_image_path)
        self.false_state_image_set(path_to_file=false_image_path)
        self.invisible_image = BitmapImageCustom(parent=self.parent,
                                                 path_to_file='./static/images/removed_button_5.png',
                                                 parent_class=self, **kwargs)
        self.Add(self.invisible_image)
        self.invisible_image.Hide()

        self.checked = initial_checked_status
        self.is_visible = visible

        self.cur_state = self.checked
        self.cur_invisible_state = self.is_visible

        self.is_button = is_button

    def method(self, event):
        pass

    @property
    def checked(self):
        return self._checked

    @checked.setter
    def checked(self, new_state):
        self._checked = new_state
        self.state_image_update()

    def _image_set(self, image_type, path):
        if path is not None:
            self.instance = BitmapImageCustom(parent=self.parent, path_to_file=path, parent_class=self)
            self.image.append(self.instance)
            index = self.image.index(self.instance)
            if image_type:      # Actually should look like 'if image_type == True:'
                self.true_image_address = index
            else:
                self.false_image_address = index
            self.Add(self.image[index])
            self.image[index].Hide()

    def true_state_image_set(self, path_to_file=None):
        self._image_set(True, path_to_file)

    def false_state_image_set(self, path_to_file=None):
        self._image_set(False, path_to_file)

    def safe_image_dsiplaying_method(self):
        if bool(self.image[self.true_image_address]):
            self.image[self.true_image_address].Show()
        if bool(self.image[self.false_image_address]):
            self.image[self.false_image_address].Show()
        if self.checked:
            if bool(self.image[self.false_image_address]):
                self.image[self.false_image_address].Hide()
        else:
            if bool(self.image[self.true_image_address]):
                self.image[self.true_image_address].Hide()

    def state_image_update(self):
        if self.true_image_address is not None and self.false_image_address is not None:
            if self.is_visible:
                if self.instance:
                    if self.cur_state != self.checked:
                        self.cur_state = self.checked
                        self.safe_image_dsiplaying_method()
                        self.Layout()

    def hide(self):
        if self:
            self.ShowItems(False)

    def show(self):
        # Just an alias to self.render()
        if self:
            self.render()

    def render(self):
        if self:
            self.state_image_update()

    @property
    def is_visible(self):
        return self._is_visible

    @is_visible.setter
    def is_visible(self, visible):
        self._is_visible = visible
        if self.cur_invisible_state != self._is_visible:
            self.cur_invisible_state = self._is_visible
            if self._is_visible:
                self.safe_image_dsiplaying_method()
                self.invisible_image.Hide()
            elif self._is_visible is not None:
                self.image[self.true_image_address].Hide()
                self.image[self.false_image_address].Hide()
                self.invisible_image.Show()
            self.Layout()

