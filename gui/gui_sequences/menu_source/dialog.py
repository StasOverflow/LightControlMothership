import wx
from gui.utils.label_types import *
from gui.utils.labeled_data import LabelValueSequence


class SettingsDialog(wx.Dialog):

    def __init__(self, *args, parent=None, title=None, **kwargs):
        getter_method = None
        if 'port_getter_method' in kwargs:
            getter_method = kwargs.pop('port_getter_method')
        super().__init__(parent=parent)
        self.SetSize((250, 230))
        self.SetTitle(title)
        self.CenterOnParent()

        self.panel = wx.Panel(self)
        self.panel_sizer = wx.BoxSizer(wx.VERTICAL)

        self.static_box = wx.StaticBox(self.panel, wx.ID_ANY, 'Settings')
        self.static_box_sizer = wx.StaticBoxSizer(self.static_box, wx.VERTICAL)

        self.port_setup = LabelValueSequence(
                                    parent=self.panel,
                                    label='Device port',
                                    interface=LABELED_CHOICE_BOX,
                                    port_getter_method=getter_method,
                                    **kwargs
                        )
        self.slave_address = LabelValueSequence(
                                    parent=self.panel,
                                    label='Slave ID',
                                    interface=LABELED_SPIN_CONTROL,
                                    button_required=False,
                                    **kwargs,
                        )
        self.refresh_time_setter = LabelValueSequence(
                                    parent=self.panel,
                                    label='Refresh rate',
                                    interface=LABELED_TEXT_INPUT,
                                    value='0'
                        )

        self.button_accept = wx.Button(parent=self.panel, label='Accept')

        self.static_box_sizer.Add(self.port_setup)
        self.static_box_sizer.Add(self.slave_address)
        self.static_box_sizer.Add(self.refresh_time_setter)

        self.panel_sizer.Add(self.static_box_sizer, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 15)
        self.panel_sizer.Add(self.button_accept, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 3)

        self.panel.SetSizer(self.panel_sizer)


    def inner_canvas_add(self):

        labeled_box = wx.StaticBox(parent=self.panel, label='Serial settings')
        labeled_box_sizer = wx.StaticBoxSizer(labeled_box, orient=wx.VERTICAL)

        labeled_box_sizer.Add(wx.RadioButton(self.panel, label='Slave ID', style=wx.RB_GROUP))
        # sbs.Add(wx.RadioButton(pnl, label='Com )
        labeled_box_sizer.Add(wx.RadioButton(self.panel, label='2 Colors'))

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox1.Add(wx.RadioButton(self.panel, label='Custom'))
        hbox1.Add(wx.TextCtrl(self.panel), flag=wx.LEFT, border=5)
        labeled_box_sizer.Add(hbox1)

        self.panel.SetSizer(labeled_box_sizer)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(self, label='Ok')
        closeButton = wx.Button(self, label='Close')
        hbox2.Add(okButton)
        hbox2.Add(closeButton, flag=wx.LEFT, border=5)

        self.inner_panel_sizer.Add(self.panel, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)
        self.inner_panel_sizer.Add(hbox2, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)

        self.SetSizer(self.inner_panel_sizer)

        okButton.Bind(wx.EVT_BUTTON, self.OnClose)
        closeButton.Bind(wx.EVT_BUTTON, self.OnClose)


    def OnClose(self, e):

        self.Destroy()


class Ponel(wx.Panel):

    def __init__(self, *args, parent=None, **kwargs):
        super().__init__(parent=parent)

        self.button = wx.Button(parent=self)
        parent.Bind(event=wx.EVT_BUTTON, handler=self.button_handler, source=self.button)

        self.dialog_window = SettingsDialog(
                                title='Connection setup',
                                port_getter_method=self.method,
                                *args,
                                **kwargs
                            )

    def button_handler(self, event):
        self.dialog_window.ShowModal()
        self.dialog_window.Close()

    def method(self):
        return ['COM1', 'COM2', 'COMCOM', 'CAPCOM', 'SAMSON']


def main():
    app = wx.App()

    frame = wx.Frame(None, -1, 'win.py', size=(600, 500))
    panel = Ponel(parent=frame)
    frame.Show()

    app.MainLoop()


if __name__ == '__main__':
    main()
