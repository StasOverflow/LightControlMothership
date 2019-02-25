from gui.gui_sequences.tabs_source.base_tab import BaseTwoSplitTab
from gui.gui_sequences.tabs_source.sub_tabs import TopLeftPanel


class TopTab(BaseTwoSplitTab):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

    def _left_panel_create(self, *args, **kwargs):
        self.left_panel = TopLeftPanel(self.top_page_splitter)


class BtmTab(BaseTwoSplitTab):
    pass