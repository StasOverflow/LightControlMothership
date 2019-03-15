import wx
from gui.utils.label_types import *
from gui.utils.labeled_data import LabelValueSequence
from settings import Settings


class SettingsDialog(wx.Dialog):

    def __init__(self, *args, parent=None, title=None, settings=None, **kwargs):
        getter_method = None
        if 'port_getter_method' in kwargs:
            getter_method = kwargs.pop('port_getter_method')
        super().__init__(parent=parent)

        self.settings = None

        self.SetSize((250, 200))
        self.SetTitle(title)
        self.CenterOnParent()

        self.settings = Settings()
        self._pending_dev_port = None

        self.panel = wx.Panel(self)
        self.panel_sizer = wx.BoxSizer(wx.VERTICAL)

        self.static_box = wx.StaticBox(self.panel, wx.ID_ANY, 'Settings')
        self.static_box_sizer = wx.StaticBoxSizer(self.static_box, wx.VERTICAL)

        self.port_setup = LabelValueSequence(
                                    parent=self.panel,
                                    label='Device port',
                                    interface=LABELED_CHOICE_BOX,
                                    port_getter_method=getter_method,
                                    initial_value=self.settings.device_port,
                                    **kwargs
                        )
        self.Bind(self.port_setup.item.event, self.on_choice, self.port_setup.item.choicer)

        self.slave_address = LabelValueSequence(
                                    parent=self.panel,
                                    label='Slave ID',
                                    interface=LABELED_SPIN_CONTROL,
                                    button_required=False,
                                    initial_value=self.settings.slave_id,
                                    **kwargs,
                        )

        self.button_accept = wx.Button(parent=self.panel, label='Accept')

        self.panel.Bind(wx.EVT_BUTTON, self.on_accept, self.button_accept)

        self.static_box_sizer.Add(self.port_setup)
        self.static_box_sizer.Add(self.slave_address)

        self.panel_sizer.Add(self.static_box_sizer, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 15)
        self.panel_sizer.Add(self.button_accept, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 3)

        self.panel.SetSizer(self.panel_sizer)

    def on_accept(self, event):
        if self._pending_dev_port is not None:
            self.settings.device_port = self._pending_dev_port
            self._pending_dev_port = None
        else:
            self.settings.device_port = self.port_setup.value
        self.settings.slave_id = self.slave_address.value
        self.Close()

    def on_choice(self, event):
        val = event.GetString()
        if val is None or val == 'None':
            val = None
        self._pending_dev_port = val


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
