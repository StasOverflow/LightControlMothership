import wx
from gui.utils.labeled_values import LabeledVisualIFace, LabeledInputIFace


class ConnectButton(wx.BoxSizer):

    def __init__(self, parent, connect_label='Connect', disconnect_label='Disconnect'):
        super().__init__(wx.HORIZONTAL)

        self.button = wx.Button(parent=parent, label=connect_label, style=wx.EXPAND, size=(90, 27))
        self.Add(self.button, 1, wx.TOP, 18)

        # self.Add(self.button, 0, wx.ALL | wx.EXPAND , 6)


class TopLeftPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.top_left_sizer_main = wx.BoxSizer(wx.HORIZONTAL)
        self.top_left_sizer_v = wx.BoxSizer(wx.VERTICAL)

        self.status = LabeledVisualIFace(parent=self, label='Status')
        self.port = LabeledVisualIFace(parent=self, label='Device port', initial_value='0')
        self.slave_id = LabeledVisualIFace(parent=self, label='Slave ID')
        self.rate = LabeledVisualIFace(parent=self, label='Refresh rate')
        self.checkbox = LabeledInputIFace(parent=self, label='Show unused')

        self.conn_button = ConnectButton(parent=self)

        self.top_left_sizer_v.Add(self.status)
        self.top_left_sizer_v.Add(self.port)
        self.top_left_sizer_v.Add(self.slave_id)
        self.top_left_sizer_v.Add(self.rate)
        self.top_left_sizer_v.Add(self.checkbox)
        self.top_left_sizer_v.Add(self.conn_button, 0, wx.BOTTOM | wx.ALIGN_RIGHT, 5)

        self.line = wx.StaticLine(self, wx.ID_ANY, style=wx.LI_VERTICAL)

        self.top_left_sizer_h = wx.BoxSizer(wx.HORIZONTAL)

        self.top_left_sizer_h.Add(self.top_left_sizer_v, 0, wx.LEFT, 25)

        self.top_left_sizer_main.Add(self.top_left_sizer_h, wx.EXPAND, wx.TOP, 16)
        self.top_left_sizer_main.Add(self.line, 0, wx.LEFT | wx.EXPAND, 14)

        self.SetSizer(self.top_left_sizer_main)
