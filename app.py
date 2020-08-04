import time
import sys
import threading
from itertools import accumulate

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
        self.modbus_connection.daemon = True

        self.poll_thread = threading.Thread(target=self._app_settings_poll)
        self.poll_thread.daemon = True

        self.main_logic_thread = threading.Thread(target=self._main_logic_handler)
        self.main_logic_thread.daemon = True

        self.data_thread = threading.Thread(target=self._modbus_data_handler)
        self.data_thread.daemon = True

        self.conn_state_prev = None
        self.app_stage = 0

    def _poll_close_event(self):
        # TODO: Resolve access violation
        closed = False
        if self.gui.is_closing:
            self.modbus_connection.disconnect()
            self.modbus_connection.stop()
            self.modbus_connection.join()
            self.poll_thread.join()
            self.data_thread.join(0.5)
            closed = True
            # self.gui.application.Destroy()
            # self.gui.application.Close()

        return closed

    def _modbus_data_get(self):
        data = self.modbus_connection.queue_data_get()
        if data is not None:
            self.app_data.modbus_data = data

    def _modbus_data_put(self):
        if self.modbus_connection.is_connected:
            if self.app_data.modbus_send_data:
                self.modbus_connection.queue_data_set(self.app_data.modbus_send_data)

    # Thread handler list
    def _app_settings_poll(self):
        while True:
            if self.gui.is_closing:
                print('poll thread closing')
                break
            self.app_settings.settings_save()
            time.sleep(0.1)

    def _main_logic_handler(self):
        while True:
            if self._poll_close_event():
                break
            time.sleep(.2)

        try:
            self.gui.main_frame.Destroy()
        except Exception as e:
            print(e)

    def _modbus_data_handler(self):
        while True:
            if self.gui.is_closing:
                print('data handler closing')
                break

            with self.modbus_connection.reconnect_lock:
                if self.modbus_connection.reconnect_requested:
                    self.modbus_connection.reconnect_requested = False
                    self.app_stage = 0

                if self.app_stage == 0:
                    if self.modbus_connection.is_connected and self.modbus_connection.data_renewed:
                        self.app_data.conn_data_apply()
                        self.app_stage = 1
                    else:
                        self.app_data.output_data_update()

                elif self.app_stage == 1:
                    if self.modbus_connection.is_connected:
                        self._modbus_data_get()
                        self.app_data.output_data_update()

                        self.app_data.input_data_gather()
                        if self.app_data.user_interaction:
                            self.app_data.user_interaction = False
                            self._modbus_data_put()
                    else:
                        self.app_stage = 0

                elif self.app_stage == 3:
                    pass

            time.sleep(.1)

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
