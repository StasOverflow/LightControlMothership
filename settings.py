class _Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(_Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Settings(metaclass=_Singleton):

    def __init__(self):
        self.device_port = None
        self.slave_id = 0
        self.refresh_rate = 200

    @property
    def device_port(self):
        return self._device_port

    @device_port.setter
    def device_port(self, value):
        self._device_port = value

    @property
    def slave_id(self):
        return self._slave_id

    @slave_id.setter
    def slave_id(self, value):
        self._slave_id = value

    @property
    def refresh_rate(self):
        return self._refresh_rate

    @refresh_rate.setter
    def refresh_rate(self, value):
        self._refresh_rate = value

    def __str__(self):
        pretty = '{\"device_port\": ' + str(self.device_port) + '},' + \
                 '{\"slave_id\": ' + str(self.slave_id) + '},' + \
                 '{\"refresh_rate\": ' + str(self.refresh_rate) + '},'
        return pretty


class ApplicationState(metaclass=_Singleton):

    def __init__(self):
        self.input_shown_tab_array = list()
        for i in range(4):
            self.input_shown_tab_array.append([False if x % 2 + i == 0 else True for x in range(15)])

    def __str__(self):
        pretty = self.input_shown_tab_array
        return pretty
