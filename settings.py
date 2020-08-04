import configparser
import threading


class _Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(_Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Settings(metaclass=_Singleton):

    def __init__(self):
        self.app_assets = AppData
        self.settings_changed = False
        self.device_port = None
        self.port_list = None
        self.refresh_rate = 200
        self.slave_id = 0

    @property
    def settings_changed(self):
        return self._settings_changed

    @settings_changed.setter
    def settings_changed(self, value):
        self._settings_changed = value

    @property
    def device_port(self):
        return self._device_port

    @device_port.setter
    def device_port(self, value):
        self.settings_changed = True
        self._device_port = value

    @property
    def slave_id(self):
        return self._slave_id

    @slave_id.setter
    def slave_id(self, value):
        self.settings_changed = True
        self._slave_id = value

    @property
    def refresh_rate(self):
        return self._refresh_rate

    @refresh_rate.setter
    def refresh_rate(self, value):
        self.settings_changed = True
        self._refresh_rate = value

    @property
    def port_list(self):
        return self._port_list

    @port_list.setter
    def port_list(self, choices):
        self._port_list = choices

    def settings_save(self):
        if self.settings_changed:
            self.settings_changed = False
            config = configparser.ConfigParser()
            config['PORT SETTINGS'] = {}
            config['PORT SETTINGS']['port'] = str(self.device_port)
            config['PORT SETTINGS']['slave_id'] = str(self.slave_id)
            config['PORT SETTINGS']['refresh_rate'] = str(self.refresh_rate)
            with open('config.ini', 'w') as configfile:
                config.write(configfile)

    def settings_load(self):
        config = configparser.ConfigParser()
        try:
            config.read('config.ini')
            sets = config['PORT SETTINGS']
            self.device_port = sets['port']
            self.slave_id = int(sets['slave_id'])
            self.refresh_rate = int(sets['refresh_rate'])
        except Exception as e:
            print(e)
        print(self)

    def __str__(self):
        pretty = '\n' + \
                 '{\"device_port\": ' + str(self.device_port) + '},' + '\n' + \
                 '{\"slave_id\": ' + str(self.slave_id) + '},' + '\n' + \
                 '{\"refresh_rate\": ' + str(self.refresh_rate) + '},' + '\n'
        return pretty


class _RelayAttr:

    def __init__(self, display_instance=None, input_instance=None):
        """
            Accepts instances of InputArray as parameters to work with
            (assuming we know how methods of InputArray looks like, and
            how to use them)
        """
        self.input_instance = input_instance
        self.input_data = self.input_instance.configuration_get()

        self.display_instance = display_instance
        self.output_data = self.display_instance.configuration_get()

    @property
    def display_data(self):
        return self.display_instance.configuration_get()

    @display_data.setter
    def display_data(self, values_array):
        self.display_instance.configuration_set(values_array)

    @property
    def input_data(self):
        return self.input_instance.configuration_get()

    @input_data.setter
    def input_data(self, values_array):
        self.input_instance.configuration_set(values_array)

    @property
    def visibility(self):
        return self.display_instance.array_hidden_state_get()

    @visibility.setter
    def visibility(self, visibility_array):
        self.display_instance.array_hidden_state_set(visibility_array)


class AppData(metaclass=_Singleton):

    def __init__(self):
        self.input_config = list()
        self.config_combined_instance = None

        self.modbus_data = None
        self.modbus_online = False
        self.modbus_send_data = None

        self.output_handler_list = list()
        self.input_handler_list = list()
        self.conn_handler_list = list()

        self._user_interaction = False
        self.interaction_lock = threading.Lock()

    @property
    def user_interaction(self):
        with self.interaction_lock:
            interaction = self._user_interaction
        return interaction

    @user_interaction.setter
    def user_interaction(self, value):
        with self.interaction_lock:
            self._user_interaction = value

    def output_data_update(self):
        # Consists of handlers, added in separate layout parts
        if len(self.output_handler_list):
            for handler in self.output_handler_list:
                handler()

    def input_data_gather(self):
        if len(self.input_handler_list):
            for handler in self.input_handler_list:
                handler()

    def conn_data_apply(self):
        if len(self.conn_handler_list):
            for handler in self.conn_handler_list:
                handler()

    def iface_conn_handler_register(self, handler):
        self.conn_handler_list.append(handler)

    def iface_output_handler_register(self, handler):
        self.output_handler_list.append(handler)

    def iface_input_handler_register(self, handler):
        self.input_handler_list.append(handler)

    @property
    def modbus_data(self):
        if self._modbus_data:
            return self._modbus_data

    @modbus_data.setter
    def modbus_data(self, value):
        self._modbus_data = value

    def output_mode_set(self, out_id, value):
        # Get output state by id
        if 0 <= value <= 3 and 0 <= out_id < 8:
            if self.modbus_data:
                try:
                    self.modbus_send_data[8] &= ~(3 << out_id*2)
                    self.modbus_send_data[8] |= (value << out_id*2)
                except TypeError:
                    pass

    def output_mode_get(self, out_id):
        # Get output state by id
        ret = 0
        if self.modbus_data:
            if 0 <= out_id < 8:
                ret = self.modbus_data[10] & (3 << out_id*2)
        return ret >> out_id*2

    def output_associated_input_get(self, out_id, input_id):
        ret = 0
        if self.modbus_data:
            if 0 <= out_id < 8:
                ret = self.modbus_data[2 + out_id] & (1 << input_id)
        return True if ret else False

    def output_associated_input_set_mask(self, out_id, array):
        if 0 <= out_id < 8:
            mask = 0
            for element_id, item in enumerate(array):
                if item:
                    mask |= (1 << element_id)
            try:
                self.modbus_send_data[out_id] = mask
            except TypeError:
                pass

    def output_state_get(self, out_id):
        ret = 0
        if self.modbus_data:
            if 0 <= out_id < 8:
                ret = self.modbus_data[1] & (1 << out_id)
        return True if ret else False

    def input_state_get(self, inp_id):
        ret = 0
        if self.modbus_data:
            if 0 <= inp_id < 15:
                ret = self.modbus_data[0] & (1 << inp_id)
        return True if ret else False

    def input_trigger_type_is_toggle_get(self, inp_id):
        # Get output state by id
        ret = 0
        if self.modbus_data:
            if 0 <= inp_id < 15:
                ret = self.modbus_data[11] & (1 << inp_id)
        return True if ret else False

    def input_trigger_type_is_toggle_set_mask(self, array):
        mask = 0
        for element_id, item in enumerate(array):
            if item:
                mask |= (1 << element_id)
        try:
            self.modbus_send_data[9] = mask
        except TypeError:
            pass

    def __str__(self):
        pretty = self.input_config
        return pretty

