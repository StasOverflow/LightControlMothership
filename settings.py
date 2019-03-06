class _Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(_Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Settings(metaclass=_Singleton):

    def __init__(self):
        self.settings_changed = False
        self.device_port = None
        self.port_list = None
        self.refresh_rate = 200
        self.slave_id = 0
        self.connected = False

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
    def connected(self):
        return self._connected

    @connected.setter
    def connected(self, value):
        self._connected = value

    def connection_status_update(self):
        self.connected = not self.connected

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
        self.output_matrix = None
        self.inputs_combined = None
        self.is_visible_combined = list()
        self.config_combined = list()

        self.mbus_data = None

    '''
        Register interface instances, which will be used by GUI visualize
        incoming modbus data
    '''
    def output_iface_reg(self, display_instance, input_instance, index=None):
        self.input_config.append(_RelayAttr(display_instance, input_instance))

    def inputs_comb_iface_reg(self, instance):
        self.inputs_combined = instance
        self.output_matrix = self.inputs_combined.configuration_get(False)

    @property
    def mbus_data(self):
        return self._mbus_data

    @mbus_data.setter
    def mbus_data(self, value):
        self._mbus_data = value

    def input_data(self, relay):
        pass

    def inputs_state_is_shown(self, index, values_array):
        self.input_config[index].visibility = values_array

    def inputs_state_iface_update(self):
        self.is_visible_combined = [False for _ in range(15)]
        for index, instance in enumerate(self.input_config):
            config = self.input_config[index].input_data
            self.inputs_state_is_shown(index, config)
            for sub_index, value in enumerate(config):
                self.is_visible_combined[sub_index] = self.is_visible_combined[sub_index] or value
        self.inputs_combined.array_hidden_state_set(self.is_visible_combined)

    def tab_input_matrix_update(self, index, values_array):
        self.input_config[index].display_data = values_array

    def combined_input_state(self, new_array, bitwise=False):
        """
            Render combined input data to upper right panel
        """
        array = list()
        if bitwise:
            for i in range(15):
                array.append(bool(new_array & (1 << i)))
        else:
            array = new_array
        self.inputs_combined.configuration_set(array)

    def relay_state_update_by_index(self, index, value):
        self.output_matrix[index] = value
        self.inputs_combined.configuration_set(self.output_matrix, False)

    def relay_state_update(self, matrix):
        for index, value in enumerate(matrix):
            self.relay_state_update_by_index(index, value)

    def relay_state_update_bitwise(self, value):
        for index in range(len(self.output_matrix)):
            self.output_matrix[3 - index] = bool(value & (1 << index))

            self.inputs_combined.configuration_set(self.output_matrix, False)

    def __str__(self):
        pretty = self.input_config
        return pretty
