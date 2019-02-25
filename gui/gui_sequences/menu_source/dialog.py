import wx


class SettingsDialog(wx.Dialog):

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        self.InitUI()
        self.SetSize((250, 200))
        self.SetTitle("Change Color Depth")
        self.CenterOnParent()

    def InitUI(self):

        panel = wx.Panel(self)
        panel_sizer = wx.BoxSizer(wx.VERTICAL)

        labeled_box = wx.StaticBox(panel, label='Serial settings')
        labeled_box_sizer = wx.StaticBoxSizer(labeled_box, orient=wx.VERTICAL)

        labeled_box_sizer.Add(wx.RadioButton(panel, label='Slave ID', style=wx.RB_GROUP))
        # sbs.Add(wx.RadioButton(pnl, label='Com )
        labeled_box_sizer.Add(wx.RadioButton(panel, label='2 Colors'))

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox1.Add(wx.RadioButton(panel, label='Custom'))
        hbox1.Add(wx.TextCtrl(panel), flag=wx.LEFT, border=5)
        labeled_box_sizer.Add(hbox1)

        panel.SetSizer(labeled_box_sizer)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(self, label='Ok')
        closeButton = wx.Button(self, label='Close')
        hbox2.Add(okButton)
        hbox2.Add(closeButton, flag=wx.LEFT, border=5)

        panel_sizer.Add(pnl, proportion=1,
            flag=wx.ALL|wx.EXPAND, border=5)
        panel_sizer.Add(hbox2, flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=10)

        self.SetSizer(panel_sizer)

        okButton.Bind(wx.EVT_BUTTON, self.OnClose)
        closeButton.Bind(wx.EVT_BUTTON, self.OnClose)


    def OnClose(self, e):

        self.Destroy()