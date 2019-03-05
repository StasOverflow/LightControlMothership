import time
import sys
import threading
from backend.ports.ports import serial_ports
from backend.modbus_backend import ModbusConnectionThread
from gui.gui import GuiApp
from settings import Settings, ApplicationState
import random


class WxWidgetCustomApp:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gui = GuiApp(
                size=(439, 550),
                title='Light Controller',
                port_getter_method=self._port_list_getter,
        )

        modbus = ModbusConnectionThread()
        self.modbus_connection = modbus.modbus_comm_instance

        self.main_panel_array = list()

        self.app_settings = Settings()
        self.app_state = ApplicationState()
        frame_alias = self.gui.main_frame

        for i in range(4):
            self.app_state.relay_register(display_instance=frame_alias.btm_tab_array[i].left_panel,
                                          input_instance=frame_alias.btm_tab_array[i].right_panel)

        self.app_state.combined_array_matrix_register(self.gui.main_frame.top_canvas.right_panel)

        self.port_list = None

        self.poll_thread = threading.Thread(target=self._poll_thread_handler)
        self.poll_thread.daemon = True

        self.main_logic_thread = threading.Thread(target=self._main_logic_handler)
        self.main_logic_thread.daemon = True

        self.layout_thread = threading.Thread(target=self._layout_thread_handler)
        self.layout_thread.daemon = True

    def _port_list_getter(self):
        return self.port_list

    def _poll_thread_handler(self):
        while True:
            self.port_list = serial_ports()
            time.sleep(0.1)

    def input_panel_layout_update(self):
        self.app_state.display_icon_visibility_update_all()
        self.app_state.display_icon_combined_value_update()

    def _layout_thread_handler(self):
        state = False
        while True:
            lock = threading.Lock()
            with lock:
                if self.app_settings.settings_changed:
                    self.gui.main_frame.settings_update()
                    self.app_settings.settings_changed = False

            state = not state
            self.input_panel_layout_update()
            # self.output_panel_layout_update()
            self.gui.main_frame.state_update(state)
            array = [True if random.randint(1, 100) > 50 else False for _ in range(15)]
            for i in range(4):
                self.app_state.display_icon_value_update(i, array)
            self.app_state.displayed_relay_array_state_update([state, not state, state, not state])
            time.sleep(0.1)

    def _main_logic_handler(self):
        while True:
            if self.gui.is_closing:
                print('closing')
                sys.exit()
            time.sleep(.2)

    def run(self):
        self.poll_thread.start()
        self.main_logic_thread.start()
        self.modbus_connection.start()
        self.layout_thread.start()
        self.gui.start()


if __name__ == '__main__':
    debug = 0

    if not debug:
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
