import wx
from gui.control_inputs.input_array_box import InputArray
from defs import *


class _MidPanelContent(wx.Panel):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Create display matrix for Relays
        self.output_matrix = InputArray(parent=self, title='State of outputs:',
                                        dimension=(1, 8),
                                        col_titles=['K1', 'K2', 'K3', 'K4',
                                                    'K5', 'K6', 'K7', 'K8'],
                                        interface=DISPLAY_INTERFACE,
                                        secret_ids=[1, 2, 3, 4, 5, 6, 7, 8], )
        self.output_matrix_wrapper = wx.BoxSizer(wx.VERTICAL)
        self.output_matrix_wrapper.Add(self.output_matrix, 0, wx.RIGHT | wx.ALIGN_RIGHT, 18)

        # Create an override button
        self.override_btn = wx.Button(parent=self, label='Override')

        # Assemble panel sizer
        self.sizer.Add(self.override_btn, 2, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 40)
        self.sizer.Add(self.output_matrix_wrapper, 6, wx.TOP | wx.BOTTOM, 10)

        # Apply panel sizer
        self.SetSizer(self.sizer)


class MidPanel(wx.BoxSizer):

    def __init__(self, parent=None):
        super().__init__(wx.HORIZONTAL)

        self.canvas = _MidPanelContent(parent=parent)

        self.Add(self.canvas, 1, wx.EXPAND)
