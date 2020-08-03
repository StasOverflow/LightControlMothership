import wx
from settings import Settings
from backend.modbus_backend import ModbusConnectionThreadSingleton


class RadioBoxWrapper(wx.RadioBox):

    def __init__(self, *args, secret_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = secret_id


class RelayDialog(wx.Dialog):

    def __init__(self, *args, parent=None, title=None, settings=None, **kwargs):
        super().__init__(parent=parent)

        self.settings = None

        self.SetSize((300, 180))
        self.SetTitle(title)
        self.CenterOnParent()

        self.settings = Settings()
        self._pending_dev_port = None

        self.panel = wx.Panel(self)
        self.panel_sizer = wx.BoxSizer(wx.VERTICAL)

        self.relay_cfg_byte = 0

        self.radio_boxes_list = list()

        self.box_style = wx.VERTICAL
        self.radio_boxes_sizer = wx.BoxSizer(self.box_style)
        rows_or_cols = wx.RA_SPECIFY_COLS if self.box_style == wx.VERTICAL else wx.RA_SPECIFY_ROWS

        for i in range(4):
            self.radio_boxes_list.append(RadioBoxWrapper(parent=self.panel, id=wx.ID_ANY, label="Relay " + str(i + 1),
                                                         choices=['Auto', 'On', 'Off'], majorDimension=3,
                                                         style=rows_or_cols, name=str(i + 1), secret_id=i))
            self.radio_boxes_list[i].Bind(wx.EVT_RADIOBOX, self.radio_box_handler)
            self.radio_boxes_sizer.Add(self.radio_boxes_list[i], 0, wx.ALL, 5)

        self.button_accept = wx.Button(parent=self.panel, label='Accept')

        modbus_singleton = ModbusConnectionThreadSingleton()
        self.modbus = modbus_singleton.modbus_comm_instance

        self.panel.Bind(wx.EVT_BUTTON, self.on_accept, self.button_accept)
        self.panel_sizer.Add(self.radio_boxes_sizer, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL,)
        self.panel_sizer.Add(self.button_accept, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 3)

        self.panel.SetSizer(self.panel_sizer)

    def radio_box_handler(self, event):
        self.relay_cfg_byte &= ~(3 << event.GetEventObject().id*2)
        self.relay_cfg_byte |= event.GetSelection() << 2 * event.GetEventObject().id
        print("{0:b}".format(self.relay_cfg_byte))
        self.modbus.queue_data_set(self.relay_cfg_byte, 4)

    def on_accept(self, event):
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

        self.dialog_window = RelayDialog(title='Relay mode setup', *args, **kwargs)

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
