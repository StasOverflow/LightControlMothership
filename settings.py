import configparser


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
        self.output_combined_state = [False for _ in range(4)]
        self.input_state_array = [False for _ in range(15)]
        self.inputs_combined_visibility_state = [False for _ in range(15)]

        for i in range(4):
            self.separate_inputs_checkboxes_state = None

        self.modbus_data = None
        self.modbus_online = False

        self.handler_list = list()

        self.incr = 0

    def layout_update(self):
        # Consists of handlers, added in separate layout parts
        if len(self.handler_list):
            for handler in self.handler_list:
                handler()

    def iface_handler_register(self, handler):
        self.handler_list.append(handler)

    @property
    def modbus_data(self):
        if self._modbus_data:
            return self._modbus_data
        else:
            return [0 for _ in range(12)]

    @modbus_data.setter
    def modbus_data(self, value):
        self._modbus_data = value

    def output_associated_input_get(self, out_id, input_id):
        ret = 0
        if 0 <= out_id < 8:
            ret = self.modbus_data[2 + out_id] & (1 << input_id)
        return True if ret else False

    def output_associated_input_set(self, out_id, input_id, value):
        if 0 <= out_id < 8:
            ret = self.modbus_data[2 + out_id] & (1 << input_id)
        return True if ret else False

    def output_state_get(self, out_id):
        ret = 0
        if 0 <= out_id < 8:
            ret = self.modbus_data[1] & (1 << out_id)
        return True if ret else False

    def input_state_get(self, inp_id):
        ret = 0
        if 0 <= inp_id < 15:
            ret = self.modbus_data[0] & (1 << inp_id)
        return True if ret else False

    def input_trigger_type_is_toggle_get(self, inp_id):
        # Get output state by id
        ret = 0
        if 0 <= inp_id < 15:
            ret = self.modbus_data[11] & (1 << inp_id)
        return True if ret else False

    def __str__(self):
        pretty = self.input_config
        return pretty


'''
    # Combined data getters
    @property
    def outputs_combined_data(self):
        if self.modbus_data is not None:
            # Get packed 'output state' data from modbus register 1
            data = self.modbus_data[1]
            for index in range(4):
                self.output_combined_state[index] = bool(data & (1 << index))
            return self.output_combined_state
        else:
            return None

    @property
    def inputs_combined_data(self):
        if self.modbus_data is not None:
            # Get packed 'input state' data from modbus register 1
            data = self.modbus_data[0]
            for index in range(15):
                self.input_state_array[index] = bool(data & (1 << index))
            return self.input_state_array
        else:
            return None

    # Visibility getters
    @property
    def inputs_combined_visibility(self):
        inputs_combined_visibility = [False for _ in range(15)]
        if self.modbus_data is not None:
            data = 0
            # Assemble data from modbus registers 2, 3, 4, 5
            for i in range(4):
                data |= self.modbus_data[2 + i]

            # Iterate through visibility array and update with assembled data
            for index in range(15):
                inputs_combined_visibility[index] = bool(data & (1 << index))

            self.inputs_combined_visibility_state = inputs_combined_visibility
        return self.inputs_combined_visibility_state

    def separate_inputs_visibility_get_by_index(self, relay_index):
        inputs_combined_visibility = [False for _ in range(15)]
        if self.modbus_data is not None:
            # Get inputs_used by a specific relay from modbus register by relay's index
            # data = self.modbus_data[2 + relay_index]

            # Iterate through visibility array and update with assembled data
            # for index in range(15):
            #     inputs_combined_visibility[index] = bool(data & (1 << index))
            return inputs_combined_visibility
        else:
            return inputs_combined_visibility

    def separate_inputs_state_get_by_index(self, relay_index):
        inputs_state = [False for _ in range(15)]
        if self.modbus_data is not None:
            # Get inputs_used by a specific relay from modbus register by relay's index
            data = self.modbus_data[2 + relay_index]

            # Iterate through visibility array and update with assembled data
            for index in range(15):
                inputs_state[index] = self.inputs_combined_data[index] & bool(data & (1 << index))
            return inputs_state
        else:
            return inputs_state
'''
