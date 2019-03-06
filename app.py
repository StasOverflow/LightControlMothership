import time
import sys
import threading
from backend.ports.ports import serial_ports
from backend.modbus_backend import ModbusConnectionThread
from gui.gui import GuiApp
from settings import Settings, ApplicationPresets
import random


class WxWidgetCustomApp:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        '''
            Define two singletones, containing data to share across application
        '''
        self.app_settings = Settings()
        self.app_state = ApplicationPresets()

        '''
            Create a gui application with main frame\
        '''
        self.gui = GuiApp(size=(439, 550), title='Light Controller')
        frame_alias = self.gui.main_frame

        '''
            Register both input and output table widgets to display data
        '''
        for i in range(4):
            self.app_state.inputs_iface_reg(display_instance=frame_alias.btm_tab_array[i].left_panel,
                                            input_instance=frame_alias.btm_tab_array[i].right_panel)
        self.app_state.in_out_comb_iface_reg(self.gui.main_frame.top_canvas.right_panel)

        '''Create threads'''
        modbus_singleton = ModbusConnectionThread()
        self.modbus_connection = modbus_singleton.modbus_comm_instance

        self.poll_thread = threading.Thread(target=self._poll_thread_handler)
        self.poll_thread.daemon = True

        self.main_logic_thread = threading.Thread(target=self._main_logic_handler)
        self.main_logic_thread.daemon = True

        self.layout_thread = threading.Thread(target=self._layout_thread_handler)
        self.layout_thread.daemon = True

    '''
        Helper logic-wrapping functions
    '''
    def _poll_close(self):
        if self.gui.is_closing:
            sys.exit()

    def _app_state_update(self):
        self.app_state.mbus_data = self.modbus_connection.queue_data_get()

    def _inner_tables_update(self):
        """Get data for every displayed array, and use it to render displayed interfaces with actual values"""

        '''
            Combined inputs visibility
        '''
        combined_inputs_visibility_array = self.app_state.inputs_combined_visibility
        if combined_inputs_visibility_array is not None:
            self.app_state.combined_inps_visibility_set(combined_inputs_visibility_array)

        '''
            Separate inputs visibility
        '''
        # for index in range(4):
        #     separate_inputs_visibility_array = self.app_state.separate_inputs_visibility_get_by_index(index)
        #     if separate_inputs_visibility_array is not None:
        #         self.app_state.input_config[index].visibility = separate_inputs_visibility_array

        '''
            Outputs state (red labels, bottom of the top right panel)
        '''
        out_data_array = self.app_state.outputs_combined_data
        if out_data_array is not None:
            self.app_state.combined_outs_conf_set(out_data_array)

        '''
            Combined inputs state (green labels, top of the top right panel)
        '''
        input_data_array = self.app_state.inputs_combined_data
        if input_data_array is not None:
            self.app_state.combined_inps_conf_set(input_data_array)

        '''
            Separate inputs state (green labels, bottom left panel, x4 sheets)
        '''
        for index in range(4):
            separate_input_data_array = self.app_state.separate_inputs_state_get_by_index(index)
            if separate_input_data_array is not None:
                self.app_state.input_config[index].display_data = separate_input_data_array

    def _layout_update(self):
        self._inner_tables_update()

        if self.app_settings.settings_changed:
            self.gui.main_frame.settings_update()
            self.app_settings.settings_changed = False

    '''
        Thread handler list
    '''
    def _poll_thread_handler(self):
        while True:
            self.app_settings.port_list = serial_ports()
            time.sleep(0.2)

    def _layout_thread_handler(self):
        while True:
            self._layout_update()
            time.sleep(0.1)

    def _main_logic_handler(self):
        while True:
            self._poll_close()
            self._app_state_update()
            time.sleep(.05)

    def run(self):
        """
            Manually launch every thread defined in __init__()
            GUI.start() should always be the last one**
            _________________________________________________
              **blocks everything, called after
        """
        self.poll_thread.start()
        self.main_logic_thread.start()
        self.modbus_connection.start()
        self.layout_thread.start()
        self.gui.start()


if __name__ == '__main__':
    debug = 0

    if not debug:
        '''Start the app'''
        app = WxWidgetCustomApp()
        app.run()
    elif debug == 1:
        import wx


        class MainFrame(wx.Frame):
            def __init__(self):
                wx.Frame.__init__(self, None, title="wxPython tabs example @pythonspot.com")

                # Create a panel and notebook (tabs holder)
                panel = wx.Panel(self)
                nb = wx.Notebook(panel)

                hbox = wx.BoxSizer(wx.HORIZONTAL)
                okButton = wx.Button(panel, -1, 'ok')
                cancelButton = wx.Button(panel, -1, 'cancel')

                hbox.Add(okButton, 0, wx.ALL | wx.Right)
                hbox.Add(cancelButton, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL)

                # Create the tab windows
                tab1 = TabOne(nb)
                tab2 = TabTwo(nb)
                tab3 = TabThree(nb)
                tab4 = TabFour(nb)

                # Add the windows to tabs and name them.
                nb.AddPage(tab1, "Tab 1")
                nb.AddPage(tab2, "Tab 2")
                nb.AddPage(tab3, "Tab 3")
                nb.AddPage(tab4, "Tab 4")

                # Set noteboook in a sizer to create the layout
                sizer = wx.BoxSizer(wx.VERTICAL)
                sizer.Add(hbox, 1, wx.EXPAND | wx.CENTER)
                sizer.Add(nb, 1, wx.EXPAND | wx.CENTER)
                panel.SetSizer(sizer)
                sizer.Layout()

        app = wx.App()
        MainFrame().Show()
        app.MainLoop()

    # elif debug == 2:
