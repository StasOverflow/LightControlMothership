import wx
from gui.control_inputs.input_array_box import InputArray
from gui.utils.utils import execute_rapidly
from settings import ApplicationPresets


class BaseSubTab(wx.Panel):

    def __init__(self, parent, *args, **kwargs):

        style = None
        if 'style' in kwargs:
            style = kwargs['style']
        if style is not None:
            super().__init__(parent, style=style)
        else:
            super().__init__(parent)

        self.inner_title = None
        self.setup_button = None
        self._configuration = None

        if 'inner_title' in kwargs:
            self.inner_title = wx.StaticText(parent=self, label=kwargs['inner_title'])

        self.inner_matrix = InputArray(
            parent=self,
            title='State of inputs:',
            dimension=(3, 5),
            col_titles=['1', '2', '3', '4', '5'],
            row_titles=['X3', 'X2', 'X1'],
            orientation=wx.VERTICAL,
            *args,
            **kwargs,
        )

        if 'button_title' in kwargs:
            label = kwargs['button_title']
            if label is not None:
                self.setup_button = wx.Button(parent=self, label=label, size=(85, 27))
                self.getter_button = wx.Button(parent=self, label='Get', size=(85, 27))

                self.setup_button.Disable()
                self.getter_button.Disable()

                self.Bind(wx.EVT_BUTTON, self.configuration_send, self.setup_button)
                self.Bind(wx.EVT_BUTTON, self.configuration_receive, self.getter_button)

                self.update_visibility()

        # In this sequence we add elements (if they exists) to panel
        inner_panel_sizer = wx.BoxSizer(wx.VERTICAL)
        if self.inner_title is not None:
            inner_panel_sizer.Add(self.inner_title, .5, wx.ALL, 5)

        inner_panel_sizer.Add(self.inner_matrix, 8, wx.ALL | wx.CENTER, 15)
        if self.setup_button is not None:
            button_sizer = wx.BoxSizer(wx.HORIZONTAL)
            button_sizer.Add(self.getter_button, 0, wx.LEFT | wx.RIGHT, 12)
            button_sizer.Add(self.setup_button, 0, wx.RIGHT, 12)
            inner_panel_sizer.Add(button_sizer, .7, wx.BOTTOM | wx.ALIGN_RIGHT, 10)

        self.configuration_update()
        self.SetSizer(inner_panel_sizer)

    @execute_rapidly
    def update_visibility(self):
        sets = ApplicationPresets()
        if sets.connected:
            self.setup_button.Enable()
            self.getter_button.Enable()
        else:
            self.setup_button.Disable()
            self.getter_button.Disable()

    def array_hidden_state_set(self, new_order):
        self.inner_matrix.visible_instances = new_order

    def array_hidden_state_update(self):
        pass

    def array_hidden_state_get(self):
        return self.inner_matrix.visible_instances

    def configuration_set(self, new_array):
        self.inner_matrix.values = new_array

    def configuration_receive(self, *args, **kwargs):
        print('receiving configurations')

    def configuration_send(self, *args, **kwargs):
        print('sending configurations')

    def configuration_update(self, *args, **kwargs):
        self._configuration = self.inner_matrix.values
        # print('updating cfg' + str(self._configuration))

    def configuration_get(self):
        return self._configuration
