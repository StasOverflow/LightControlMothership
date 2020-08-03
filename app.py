import time
import sys
import threading
from backend.ports.ports import serial_ports
from backend.modbus_backend import ModbusConnectionThreadSingleton
from gui.gui import GuiApp
from settings import Settings, AppData


class WxWidgetCustomApp:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Define two singletones, containing data to share across application
        self.app_settings = Settings()
        self.app_settings.settings_load()
        self.app_data = AppData()
        self.modbus_singleton = None

        # Create a gui application with main frame
        self.gui = GuiApp(size=(439, 565), title="Light Controller")

        # Create threads
        self.modbus_singleton = ModbusConnectionThreadSingleton()
        self.modbus_connection = self.modbus_singleton.modbus_comm_instance

        self.poll_thread = threading.Thread(target=self._app_settings_poll)
        self.poll_thread.daemon = True

        self.main_logic_thread = threading.Thread(target=self._main_logic_handler)
        self.main_logic_thread.daemon = True

        self.data_thread = threading.Thread(target=self._modbus_data_handler)
        self.data_thread.daemon = True

        self.layout_thread = threading.Thread(target=self._layout_thread_handler)
        self.layout_thread.daemon = True

    def _poll_close_event(self):
        # TODO: Resolve access violation
        if self.gui.is_closing:
            self.gui.application.Destroy()
            # sys.exit()

    def _modbus_data_get(self):
        self.app_data.modbus_data = self.modbus_connection.queue_data_get()

    def _modbus_data_put(self):
        data = list()
        for data_id in range(2, 11):
            data = self.app_data.modbus_data[data_id]
        self.modbus_connection.queue_data_set(data)

    # Thread handler list
    def _app_settings_poll(self):
        while True:
            self.app_settings.settings_save()
            time.sleep(0.5)

    def _layout_thread_handler(self):
        while True:
            self.app_data.layout_update()
            time.sleep(0.1)

    def _main_logic_handler(self):
        while True:
            self._poll_close_event()
            time.sleep(.05)

    def _modbus_data_handler(self):
        while True:
            self._modbus_data_get()
            self._modbus_data_put()
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
        self.data_thread.start()
        self.layout_thread.start()

        # GUI.start() Called at the end, as mentioned everywhere
        self.gui.start()


if __name__ == '__main__':
    debug = 0

    if not debug:
        # Start the app
        app = WxWidgetCustomApp()
        app.run()
    elif debug == 1:
        pass
