import wx
from gui.basis.tabs.inner_tab import BaseInnerTab
from settings import AppData
from settings import Settings


class BtmRightPanel(BaseInnerTab):

    def __init__(self, *args, **kwargs):
        super(BtmRightPanel, self).__init__(*args, with_radio_panel=True, **kwargs)

        self.SetSizer(self.inner_panel_sizer)

        self.settings = Settings()

        self.app_data = AppData()

        self.app_data.iface_handler_register(self._conf_receive)

        self.data_received = False

        self.mbus_data = self.app_data.separate_inputs_visibility_get_by_index(self.id)

    def _ins_outs_state_update(self, force=False):
        separate_inputs_visibility_array = self.app_data.separate_inputs_visibility_get_by_index(self.id)
        if separate_inputs_visibility_array is not None:
            self.configuration_set(separate_inputs_visibility_array)

    def _conf_receive(self, force=False):
        if self.modbus.is_connected:
            mbus_data_new = self.app_data.separate_inputs_visibility_get_by_index(self.id)
            if self.mbus_data != mbus_data_new:
                self.mbus_data = mbus_data_new
                self._ins_outs_state_update()
        else:
            self.mbus_data = None

    def configuration_receive(self, *args, **kwargs):
        print(self.id)
        self._ins_outs_state_update(force=True)
        print('receiving configurations')

    def configuration_send(self, *args, **kwargs):
        print(self.id)
        print('sending configurations')
