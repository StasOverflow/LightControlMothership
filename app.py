import time
import sys
import threading
from backend.ports.ports import serial_ports
from backend.modbus_backend import ModbusConnectionThreadSingleton
from gui.gui import GuiApp
from settings import Settings, AppData
import random


class WxWidgetCustomApp:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        '''Define two singletones, containing data to share across application'''
        self.app_settings = Settings()
        self.app_settings.settings_load()
        self.app_data = AppData()

        '''Create a gui application with main frame'''
        self.gui = GuiApp(size=(439, 565), title='Light Controller')

        '''Create threads'''
        modbus_singleton = ModbusConnectionThreadSingleton()
        self.modbus_connection = modbus_singleton.modbus_comm_instance

        self.poll_thread = threading.Thread(target=self._app_settings_poll)
        self.poll_thread.daemon = True

        self.main_logic_thread = threading.Thread(target=self._main_logic_handler)
        self.main_logic_thread.daemon = True

        self.layout_thread = threading.Thread(target=self._layout_thread_handler)
        self.layout_thread.daemon = True

    '''Helper logic-wrapping functions'''
    def _poll_close_event(self):
        if self.gui.is_closing:
            sys.exit()

    def _mbus_data_get(self):
        self.app_data.mbus_data = self.modbus_connection.queue_data_get()

    def _mbus_data_put(self):
        pass

    '''Thread handler list'''
    def _app_settings_poll(self):
        while True:
            self.app_settings.settings_save()
            self.app_settings.port_list = serial_ports()
            time.sleep(0.5)

    def _layout_thread_handler(self):
        while True:
            self.app_data.layout_update()
            time.sleep(0.1)

    def _main_logic_handler(self):
        while True:
            self._poll_close_event()
            self._mbus_data_get()
            self._mbus_data_put()
            time.sleep(.05)

    def run(self):
        """
            Manually launch every thread defined in __init__()
            GUI.start() should always be the last one**
            __________________________________________________
              **blocks every call after itself, until finished
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
        pass
