import wx
from gui.utils.labeled_data import LabelValueSequence
from gui.utils.label_types import *
from defs import *
from settings import Settings, AppData
from gui.control_inputs.input_array_box import InputArray


class TopLeftPanel(wx.Panel):

    def __init__(self, parent):
        # Initial Constructor routines
        wx.Panel.__init__(self, parent)
        self.settings = Settings()
        self.app_data = AppData()
        self.output_garbage_collector = 0

        # Create sizers
        self.top_left_sizer_main = wx.BoxSizer(wx.HORIZONTAL)
        self.top_inputs_sizer = wx.BoxSizer(wx.VERTICAL)

        # Create window sequences
        self.device_port = LabelValueSequence(parent=self, label='Device Port',
                                              interface=LABELED_LABEL)
        self.slave_id = LabelValueSequence(parent=self,
                                           label='Slave ID',
                                           interface=LABELED_SPIN_CONTROL,
                                           button_required=False,
                                           initial_value=self.settings.slave_id)

        # Wrap top inputs
        self.top_inputs_sizer.Add(self.device_port)
        self.top_inputs_sizer.Add(self.slave_id)
        # self.top_inputs_sizer.Add(self.act_indicator_wrapper, 1, wx.TOP | wx.ALIGN_LEFT, 25)

        # Wrap existing into intermediate sizer, to add padding
        self.top_left_sizer_main.Add(self.top_inputs_sizer, 1, wx.ALL, 20)
        self.SetSizer(self.top_left_sizer_main)

        self.app_data.iface_handler_register(self._port_update)

    def _port_update(self):
        self.device_port.value = self.settings.device_port
