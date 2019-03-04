import time
import sys
import threading
from backend.ports.ports import serial_ports
from backend.modbus.modbus import ModbusThread
from gui.gui import GuiApp
from settings import Settings, ApplicationState


class WxWidgCustomApp:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gui = GuiApp(
                size=(439, 550),
                title='Light Controller',
                port_getter_method=self._port_list_getter,
        )

        self.main_panel_array = list()

        self.app_settings = Settings()
        self.app_state = ApplicationState()

        self.port_list = None

        self.comm_thread = ModbusThread(None, None)

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

    def output_panel_layout_update(self):
        display_list = [0, 1, 0, 1]
        self.gui.main_frame.top_canvas.right_panel.configuration_set(display_list, False)

    def input_panel_layout_update(self):
        self.main_panel_array = [False for _ in range(15)]
        for i in range(4):
            tab_ref = self.gui.main_frame.btm_tab_array[i]
            config_array = tab_ref.right_panel.configuration_get()
            tab_ref.left_panel.array_hidden_state_set(config_array)
            for index, value in enumerate(config_array):
                self.main_panel_array[index] = self.main_panel_array[index] or value

        self.gui.main_frame.top_canvas.right_panel.array_hidden_state_set(self.main_panel_array)

    def _layout_thread_handler(self):
        settings_prev = None
        state = False
        while True:
            sets = self.app_settings.__str__()
            state = not state
            if settings_prev != sets:
                settings_prev = sets
                self.gui.main_frame.settings_update()

            self.input_panel_layout_update()
            self.output_panel_layout_update()
            self.gui.main_frame.state_update(state)
            time.sleep(0.3)

    def _main_logic_handler(self):
        """
            This is where all important operations happen, like:

            -Among-thread data exchange
            -Closing handler polling (where we determine whether
                the app is running or about to be closed)
        """
        while True:
            if self.gui.is_closing:
                print('closing')
                sys.exit()
            time.sleep(1)

    def run(self):
        self.poll_thread.start()
        self.main_logic_thread.start()
        self.comm_thread.start()
        self.layout_thread.start()
        self.gui.start()


if __name__ == '__main__':
    debug = 0

    if not debug:
        app = WxWidgCustomApp()
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
