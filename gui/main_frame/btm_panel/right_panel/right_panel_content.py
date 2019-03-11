import wx
from gui.basis.tabs.inner_tab import BaseInnerTab
from gui.utils.utils import execute_rapidly


class BtmRightPanel(BaseInnerTab):

    def __init__(self, *args, **kwargs):
        super(BtmRightPanel, self).__init__(*args, **kwargs)

        button_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.getter_button = wx.Button(parent=self, label='Get', size=(85, 27))
        self.Bind(wx.EVT_BUTTON, self.configuration_receive, self.getter_button)
        self.getter_button.Disable()
        button_sizer.Add(self.getter_button, 1, wx.LEFT | wx.RIGHT, 8)

        self.setter_button = wx.Button(parent=self, label='Set', size=(85, 27))
        self.Bind(wx.EVT_BUTTON, self.configuration_send, self.setter_button)
        self.setter_button.Disable()
        button_sizer.Add(self.setter_button, 0, wx.RIGHT | wx.LEFT, 8)

        self.inner_panel_sizer.Add(button_sizer, 5, wx.TOP | wx.ALIGN_CENTER | wx.BOTTOM, 30)
        self.SetSizer(self.inner_panel_sizer)
        self.update_visibility()

    @execute_rapidly
    def update_visibility(self):
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
