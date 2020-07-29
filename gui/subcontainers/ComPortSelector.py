import os
import wx
from gui.utils.label_types import *
from gui.utils.utils import execute_every
from settings import Settings
from backend.ports.ports import serial_ports


class _ComPortChoice(wx.BoxSizer):  # wx.Choices

    def __init__(self, parent=None):

        # Initial Create
        super().__init__(wx.HORIZONTAL)
        self.settings = Settings()
        self.choices_data = None
        self.timer = None
        self.port_index = 0
        self._garbage_evt_collector = 0

        # Create COM port drop down list
        self.choicer = wx.Choice(parent=parent, size=(73, -1))

        # Handle choicer selection
        self.update_choices()
        self.port_index = self.choicer.FindString(self.settings.device_port, False)
        if self.port_index == -1:
            self.port_index = 0
        self.choicer.SetSelection(self.port_index)

        # Assign choice callback
        parent.Bind(wx.EVT_CHOICE, self._choice_cb, self.choicer)

        # Add choicer to a sizer (which is this class itself)
        self.Add(self.choicer, 1, wx.LEFT, 0)

        # Insert a certain delay for refresh button
        self._can_be_refreshed = 1
        self.timer = wx.Timer()
        self.timer_evt_handler = wx.EvtHandler()
        self.timer.SetOwner(self.timer_evt_handler, id=228)
        self.timer_evt_handler.Bind(wx.EVT_TIMER, self._refresh, self.timer, id=228)

        self.timer.Start(1000, True)

    def _refresh(self, event):
        self._garbage_evt_collector = event
        self.timer.Start(1000, True)
        self._can_be_refreshed = 1

    def _choice_cb(self, event):
        self._garbage_evt_collector = event
        if self.port_index:
            self.port_index = self.choicer.GetSelection()

    def update_cb(self, event):
        if self._can_be_refreshed == 1:
            self._can_be_refreshed = 0
            self._garbage_evt_collector = event
            self.update_choices()

    def update_choices(self):
            if self.choicer:
                self.settings.port_list = serial_ports()
                self.choices_data = self.settings.port_list

                self.choicer.Clear()
                self.choicer.Append(self.choices_data)
                self.choices_data = self.settings.port_list

                string_id = self.port_index
                if string_id == -1:
                    string_id = 0

                self.choicer.SetSelection(string_id)
                self.choicer.Layout()


class ComPortSelector(wx.BoxSizer):

    def __init__(self, label_caption, parent=None, margin=3):

        # Initial constructions
        super().__init__(wx.HORIZONTAL)

        self.item = None
        self.label = None
        self.margin = margin

        self.label = wx.StaticText(parent=parent, label=str(label_caption + ':'), size=(95, -1))
        self.item = _ComPortChoice(parent=parent)

        label_style = wx.ALL
        value_style = wx.ALL

        label_margin = self.margin
        value_margin = self.margin

        # To add top margin, wrap label into a sizer
        label_sizer = wx.BoxSizer(wx.HORIZONTAL)
        label_sizer.Add(self.label, 0, wx.TOP, 3)
        self.label = label_sizer

        self.Add(self.label, 0, label_style, label_margin)
        self.Add(self.item, 0, value_style, value_margin)
