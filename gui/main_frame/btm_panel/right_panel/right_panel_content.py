import wx
from gui.basis.tabs.inner_tab import BaseInnerTab
from settings import AppData
from settings import Settings


class BtmRightPanel(BaseInnerTab):

    def __init__(self, *args, **kwargs):
        super(BtmRightPanel, self).__init__(*args, with_radiopanel=True, **kwargs)

        if 0:
            button_sizer = wx.BoxSizer(wx.HORIZONTAL)
            self.getter_button = wx.Button(parent=self, label='Get', size=(85, 27))
            self.Bind(wx.EVT_BUTTON, self.configuration_receive, self.getter_button)
            self.getter_button.Disable()
            button_sizer.Add(self.getter_button, 1, wx.LEFT | wx.RIGHT | wx.BOTTOM, 8)

            self.setter_button = wx.Button(parent=self, label='Set', size=(85, 27))
            self.Bind(wx.EVT_BUTTON, self.configuration_send, self.setter_button)
            self.setter_button.Disable()
            button_sizer.Add(self.setter_button, 0, wx.RIGHT | wx.LEFT | wx.BOTTOM, 8)

            self.inner_panel_sizer.Add(button_sizer, 5, wx.TOP | wx.ALIGN_CENTER, 30)

            self.app_data.iface_handler_register(self._buttons_update)


        self.SetSizer(self.inner_panel_sizer)

        self.settings = Settings()
        self.app_data = AppData()

        self.app_data.iface_handler_register(self._conf_receive)

        self.data_received = False

        self.mbus_data = self.app_data.separate_inputs_visibility_get_by_index(self.id)

    def _ins_outs_state_update(self, force=False):
        separate_inputs_visibility_array = self.app_data.separate_inputs_visibility_get_by_index(self.id)
        if separate_inputs_visibility_array is not None:
            self.configuration_set(separate_inputs_visibility_array)

    def _conf_receive(self, force=False):
        if self.modbus.is_connected:
            mbus_data_new = self.app_data.separate_inputs_visibility_get_by_index(self.id)
            if self.mbus_data != mbus_data_new:
                self.mbus_data = mbus_data_new
                self._ins_outs_state_update()
        else:
            self.mbus_data = None

    def _buttons_update(self):
        if self.modbus.is_connected:
            if self.setter_button:
                self.setter_button.Enable()
            if self.getter_button:
                self.getter_button.Enable()
        else:
            if self.setter_button:
                self.setter_button.Disable()
            if self.getter_button:
                self.getter_button.Disable()

    def configuration_receive(self, *args, **kwargs):
        print(self.id)
        self._ins_outs_state_update(force=True)
        print('receiving configurations')

    def configuration_send(self, *args, **kwargs):
        print(self.id)
        print('sending configurations')
