class _Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(_Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Settings(metaclass=_Singleton):

    def __init__(self):
        self.connected = False
        self.settings_changed = False
        self.device_port = None
        self.slave_id = 0
        self.refresh_rate = 200

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

    def __str__(self):
        pretty = '{\"device_port\": ' + str(self.device_port) + '},' + \
                 '{\"slave_id\": ' + str(self.slave_id) + '},' + \
                 '{\"refresh_rate\": ' + str(self.refresh_rate) + '},'
        return pretty


class ApplicationState(metaclass=_Singleton):

    class RelayAttr:

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

    def __init__(self):
        self.relay_array = list()
        self.output_matrix = None
        self.combined_inputs_array_instance = None
        self.combined_inputs_visibility = list()
        self.combined_inputs_values = list()

    def relay_register(self, display_instance, input_instance, index=None):
        self.relay_array.append(self.RelayAttr(display_instance, input_instance))

    def combined_array_matrix_register(self, instance):
        self.combined_inputs_array_instance = instance
        self.output_matrix = self.combined_inputs_array_instance.configuration_get(False)

    def display_icon_visibility_update(self, index, values_array):
        self.relay_array[index].visibility = values_array

    def display_icon_visibility_update_all(self):
        self.combined_inputs_visibility = [False for _ in range(15)]
        for index, instance in enumerate(self.relay_array):
            config_array = self.relay_array[index].input_data
            self.display_icon_visibility_update(index, config_array)
            for sub_index, value in enumerate(config_array):
                self.combined_inputs_visibility[sub_index] = self.combined_inputs_visibility[sub_index] or value
        self.combined_inputs_array_instance.array_hidden_state_set(self.combined_inputs_visibility)

    def display_icon_value_update(self, index, values_array):
        self.relay_array[index].display_data = values_array

    def display_icon_combined_value_update(self):
        self.combined_inputs_values = [False for _ in range(15)]
        for index, instance in enumerate(self.relay_array):
            self.relay_array[index].display_instance.configuration_update()
            values_array = self.relay_array[index].display_data
            for sub_index, value in enumerate(values_array):
                self.combined_inputs_values[sub_index] = self.combined_inputs_values[sub_index] or value
        self.combined_inputs_array_instance.configuration_set(self.combined_inputs_values)

    def displayed_relay_state_update(self, index, value):
        self.output_matrix[index] = value
        self.combined_inputs_array_instance.configuration_set(self.output_matrix, False)

    def displayed_relay_array_state_update(self, matrix):
        for index, value in enumerate(matrix):
            self.displayed_relay_state_update(index, value)

    def __str__(self):
        pretty = self.relay_array
        return pretty
