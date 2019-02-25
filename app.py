from backend.modbus.modbus import ModbusThread
from gui.gui import GuiApp
import threading
import time
import sys


class WxWidgCustomApp:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gui = GuiApp(size=(439, 520), title='Light Controller')
        self.comm_thread = ModbusThread(None, None)
        self.main_logic_thread = threading.Thread(target=self._main_logic_handler)
        self.main_logic_thread.daemon = True

    def _main_logic_handler(self):
        """
            This is where all important operations happen, like:

            -Among-thread data exchange
            -Closing handler polling (where we determine whether
                the app is running or about to be closed)
        """
        while True:
            input_vals = self.gui.main_frame.combined_inputs_states_get()
            if self.gui.is_closing:
                print('closing')
                sys.exit()
            # print('staying alive')
            time.sleep(1)

    def run(self):
        self.main_logic_thread.start()
        self.comm_thread.start()
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
