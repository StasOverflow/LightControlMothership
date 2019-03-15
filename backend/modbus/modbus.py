from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import threading
import queue
import time
import settings
from enum import Enum


class ModbusThread(threading.Thread):

    class Cmd(Enum):
        DISCONNECT = 0
        CONNECT = 1

    def __init__(
            self,
            conn_method='rtu',
            port='COM2',
            baudrate=19200,
            parity='E',
            timeout=1,
            slave_id=32,
            *args,
            **kwargs,
    ):
        self.app_state = settings.AppData()

        super().__init__(*args, **kwargs)
        self.daemon = True

        self.queue_income = queue.Queue()
        self.queue_outcome = queue.Queue()
        self.queue_cmd = queue.Queue()

        self.method = conn_method
        self.port = port
        self.baudrate = baudrate
        self.parity = parity
        self.timeout = timeout
        self.slave_id = slave_id

        self.stopped = False
        self.is_connected = False
        self._inner_mbus_is_conn = self.Cmd.DISCONNECT
        self.client = None

        self.mbus_send_data = [0 for _ in range(4)]

        self.port_lock = threading.Lock()
        self.sl_id_lock = threading.Lock()
        self.queue_lock = threading.Lock()
        self.blink_lock = threading.Lock()

        self.exception_state = False

    @property
    def is_connected(self):
        return self._is_connected

    @is_connected.setter
    def is_connected(self, value):
        self._is_connected = value
        if self._is_connected:
            self._inner_mbus_is_conn = self.Cmd.CONNECT
        else:
            self._inner_mbus_is_conn = self.Cmd.DISCONNECT

    def is_connected_state_set(self, boolean_value):
        self.queue_cmd.put(self.Cmd(boolean_value))

    def queue_data_get(self):
        if self.queue_income:
            data = self.queue_income.get()
            return data

    def queue_insert(self, data, index):
        self.mbus_send_data[index] = data
        self.queue_outcome.put(self.mbus_send_data)

    def com_port_update(self, new_com_port):
        if not self.is_connected:
            with self.port_lock:
                self.port = new_com_port
        else:
            print('Error: PORT cant be changed while connected!')

    def slave_id_update(self, new_slave_id):
        if not self.is_connected:
            with self.sl_id_lock:
                self.slave_id = new_slave_id
        else:
            self.is_connected_state_set(False)
            with self.sl_id_lock:
                self.slave_id = new_slave_id
            self.is_connected_state_set(True)

    def stop(self):
        print('Serial Task: command CLOSE')
        self.is_connected = False
        if self.client is not None:
            self.client.close()
        self.stopped = True

    def connect(self):
        try:
            self.client = ModbusClient(method=self.method, port=self.port, baudrate=self.baudrate,
                                       parity=self.parity, timeout=self.timeout)
            self.is_connected = True
        except Exception as ex:
            print('is connected exception', ex)

    def disconnect(self):
        try:
            if self.client is not None:
                self.client.close()
                self.is_connected = False
        except Exception as ex:
            print('is connected exception', ex)

    def exception_state_get(self):
        return self.exception_state

    def run(self):
        while not self.stopped:
            state = False
            if self.queue_cmd.qsize():
                cmd = self.queue_cmd.get()
                if cmd == self.Cmd.CONNECT:
                    self.connect()
                else:
                    self.disconnect()

            if self._inner_mbus_is_conn == self.Cmd.CONNECT:
                if self.queue_outcome.qsize():
                    try:
                        with self.queue_lock:
                            state = False
                            sets = self.queue_outcome.get()
                            self.client.write_registers(1002, sets, count=4, unit=self.slave_id)
                    except Exception as ex:
                        state = True
                        print(ex)
                else:
                    try:
                        with self.queue_lock:
                            state = False
                            rr = self.client.read_holding_registers(1000, count=13, unit=self.slave_id)
                            self.queue_income.put(rr.registers)
                    except Exception as ex:
                        print(ex)
                        state = True
                time.sleep(0.05)
                print(state)
                self.exception_state = state
            else:
                time.sleep(0.2)
        print('Serial Task: destroyed')
