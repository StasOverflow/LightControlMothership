from gui.gui_sequences.tabs.tabs_source.base_tab import BaseTwoSplitTab
from gui.gui_sequences.tabs.tabs_source.sub_tabs import TopLeftPanel, TopRightPanel
from gui.control_inputs.defs import *


class TopTab(BaseTwoSplitTab):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

    def _left_panel_create(self, *args, **kwargs):
        self.left_panel = TopLeftPanel(self.top_page_splitter)

    def _right_panel_create(self, *args, **kwargs):
        self.right_panel = TopRightPanel(self.top_page_splitter)


class BtmTab(BaseTwoSplitTab):

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(
            parent=parent,
            iface_types=(DISPLAY_INTERFACE, INPUT_INTERFACE),
            outlined=False,
            left_panel_title='Status:',
            right_panel_title='Setup:',
            right_panel_button_title='Configure'
        )