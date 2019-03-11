class _Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(_Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Settings(metaclass=_Singleton):

    def __init__(self):
        self.app_assets = ApplicationPresets
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

    def connection_status_update(self, value):
        self.app_assets.connected = value

    @property
    def port_list(self):
        return self._port_list

    @port_list.setter
    def port_list(self, choices):
        self._port_list = choices

    def __str__(self):
        pretty = '{\"device_port\": ' + str(self.device_port) + '},' + \
                 '{\"slave_id\": ' + str(self.slave_id) + '},' + \
                 '{\"refresh_rate\": ' + str(self.refresh_rate) + '},'
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


class ApplicationPresets(metaclass=_Singleton):

    def __init__(self):
        self.input_config = list()
        self.config_combined_instance = None
        self.output_combined_state = [False for _ in range(4)]
        self.inputs_combined_state = [False for _ in range(15)]
        self.inputs_combined_visibility_state = [False for _ in range(15)]
        self.connected = False

        for i in range(4):
            self.separate_inputs_checkboxes_state = None

        self.mbus_data = None

    '''
        Register interface instances, which will be used by GUI visualize
        incoming modbus data
    '''
    def inputs_iface_reg(self, display_instance, input_instance, index=None):
        self.input_config.append(_RelayAttr(display_instance, input_instance))

    def in_out_comb_iface_reg(self, instance):
        self.config_combined_instance = instance
        # self.inputs_combined_state = instance.configuration_get()

    def combined_outs_conf_set(self, value):
        self.config_combined_instance.configuration_set(value, False)

    def combined_inps_conf_set(self, value):
        self.config_combined_instance.configuration_set(value)

    def combined_inps_visibility_set(self, value):
        self.config_combined_instance.array_hidden_state_set(value)

    @property
    def connected(self):
        return self._connected

    @connected.setter
    def connected(self, value):
        self._connected = value

    @property
    def mbus_data(self):
        return self._mbus_data

    @mbus_data.setter
    def mbus_data(self, value):
        self._mbus_data = value

    '''
        Combined data getters
    '''
    @property
    def outputs_combined_data(self):
        if self.mbus_data is not None:
            '''
                Get packed 'output state' data from modbus register 1
            '''
            data = self.mbus_data[1]
            for index in range(4):
                self.output_combined_state[3 - index] = bool(data & (1 << index))
            return self.output_combined_state
        else:
            return None

    @property
    def inputs_combined_data(self):
        if self.mbus_data is not None:
            '''
                Get packed 'input state' data from modbus register 1
            '''
            data = self.mbus_data[0]
            for index in range(15):
                self.inputs_combined_state[index] = bool(data & (1 << index))
            return self.inputs_combined_state
        else:
            return None
    '''
        Visibility getters
    '''
    @property
    def inputs_combined_visibility(self):
        inputs_combined_visibility = [False for _ in range(15)]
        if self.mbus_data is not None:
            data = 0
            '''
                Assemble data from modbus registers 2, 3, 4, 5
            '''
            for i in range(4):
                data |= self.mbus_data[2 + i]
            '''
                Iterate through visibility array and update with assembled data
            '''
            for index in range(15):
                inputs_combined_visibility[index] = bool(data & (1 << index))

            self.inputs_combined_visibility_state = inputs_combined_visibility
        return self.inputs_combined_visibility_state

    def separate_inputs_visibility_get_by_index(self, relay_index):
        inputs_combined_visibility = [False for _ in range(15)]
        if self.mbus_data is not None:
            '''
                Get inputs_used by a specific relay from modbus register by relay's index
            '''
            data = self.mbus_data[2 + relay_index]
            '''
                Iterate through visibility array and update with assembled data
            '''
            for index in range(15):
                inputs_combined_visibility[index] = bool(data & (1 << index))
            return inputs_combined_visibility
        else:
            return inputs_combined_visibility

    def separate_inputs_state_get_by_index(self, relay_index):
        inputs_state = [False for _ in range(15)]
        if self.mbus_data is not None:
            '''
                Get inputs_used by a specific relay from modbus register by relay's index
            '''
            data = self.mbus_data[2 + relay_index]
            '''
                Iterate through visibility array and update with assembled data
            '''
            for index in range(15):
                inputs_state[index] = self.inputs_combined_data[index] & bool(data & (1 << index))
            return inputs_state
        else:
            return inputs_state

    def separate_inputs_checkboxes_state_update(self, index):

        pass

    def __str__(self):
        pretty = self.input_config
        return pretty
