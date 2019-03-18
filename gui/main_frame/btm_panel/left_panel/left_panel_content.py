from gui.basis.tabs.inner_tab import BaseInnerTab


class BtmLeftPanel(BaseInnerTab):

    def __init__(self, *args, **kwargs):
        super(BtmLeftPanel, self).__init__(*args, with_indicator=True, **kwargs)

