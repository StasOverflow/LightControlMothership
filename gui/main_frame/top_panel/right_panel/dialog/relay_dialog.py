import wx
from gui.utils.label_types import *
from gui.utils.labeled_data import LabelValueSequence
from settings import Settings


class RadioBoxWrapper(wx.RadioBox):

    def __init__(self, *args, secret_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = secret_id


class RelayDialog(wx.Dialog):

    def __init__(self, *args, parent=None, title=None, settings=None, **kwargs):
        getter_method = None
        super().__init__(parent=parent)

        self.settings = None

        self.SetSize((300, 185))
        self.SetTitle(title)
        self.CenterOnParent()

        self.settings = Settings()
        self._pending_dev_port = None

        self.panel = wx.Panel(self)
        self.panel_sizer = wx.BoxSizer(wx.VERTICAL)

        self.radio_boxes_list = list()
        self.radio_boxes_sizer = wx.BoxSizer(wx.HORIZONTAL)
        for i in range(4):

            self.radio_boxes_list.append(RadioBoxWrapper(parent=self.panel, id=wx.ID_ANY, label="Relay " + str(i + 1),
                                                         choices=['Auto', 'Set 0', 'Set 1'],
                                                         majorDimension=3, style=wx.RA_SPECIFY_ROWS,
                                                         name=str(i + 1), secret_id=i))
            self.radio_boxes_list[i].Bind(wx.EVT_RADIOBOX, self.radio_box_handler)
            self.radio_boxes_sizer.Add(self.radio_boxes_list[i], 0, wx.ALL, 5)

        # self.static_box_sizer = wx.StaticBoxSizer(self.static_box, wx.VERTICAL)
        #
        # self.port_setup = LabelValueSequence(
        #                             parent=self.panel,
        #                             label='Device port',
        #                             interface=LABELED_CHOICE_BOX,
        #                             port_getter_method=getter_method,
        #                             initial_value=self.settings.device_port,
        #                             **kwargs
        #                 )

        # self.Bind(self.port_setup.item.event, self.on_choice, self.port_setup.item.choicer)

        # self.slave_address = LabelValueSequence(
        #                             parent=self.panel,
        #                             label='Slave ID',
        #                             interface=LABELED_SPIN_CONTROL,
        #                             button_required=False,
        #                             initial_value=self.settings.slave_id,
        #                             **kwargs,
        #                 )
        #
        self.button_accept = wx.Button(parent=self.panel, label='Accept')

        self.panel.Bind(wx.EVT_BUTTON, self.on_accept, self.button_accept)

        # self.static_box_sizer.Add(self.port_setup)
        # self.static_box_sizer.Add(self.slave_address)

        self.panel_sizer.Add(self.radio_boxes_sizer, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL,)
        self.panel_sizer.Add(self.button_accept, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 3)

        self.panel.SetSizer(self.panel_sizer)

    def radio_box_handler(self, event):
        print('handled ', event.GetEventObject().id, event.GetSelection())

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

        self.dialog_window = RelayDialog(title='Relay mode setup',
                                         *args, **kwargs)

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
