import wx


class TopLeftPanel(wx.Panel):

    def __init__(self, parent, color):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(color)
