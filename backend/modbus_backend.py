from settings import _Singleton
from backend.modbus.modbus import ModbusThread


class ModbusConnectionThread(metaclass=_Singleton):
    """
        Wraps modbus thread into a singleton class, allowing to call
        the same object from different parts of code.

        Usage: assign thread callback to self.modbus_comm_instance, not self
    """

    def __init__(self):
        self.modbus_comm_instance = ModbusThread(None, None)

    def thread_instance_get(self):
        return self.modbus_comm_instance
