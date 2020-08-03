from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import threading
import queue
import time
import settings
from enum import Enum

from settings import AppData


class ModbusThread(threading.Thread):

    class Cmd(Enum):
        DISCONNECT = 0
        CONNECT = 1

    class State(Enum):
        IDLE = 0
        CONN_ESTABLISH = 1
        CONN_CONFIRM = 2
        READ = 3
        WRITE = 4
        CONN_DEMOLISH = 5

    def __init__(
            self,
            conn_method='rtu',
            port='COM2',
            baudrate=19200,
            parity='E',
            timeout=1,
            bytesize=8,
            stopbits=1,
            slave_id=32,
            *args,
            **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.daemon = True

        self.app_data = AppData()

        self.queue_income = queue.Queue()
        self.queue_outcome = queue.Queue()
        self.queue_cmd = queue.Queue()

        self.method = conn_method
        self.port = port
        self.baudrate = baudrate
        self.parity = parity
        self.timeout = timeout
        self.slave_id = slave_id
        self.bytesize = bytesize
        self.stopbits = stopbits

        self.stopped = False
        self.is_connected = False
        self._inner_modbus_is_conn = self.Cmd.DISCONNECT
        self.client = None

        self.port_lock = threading.Lock()
        self.sl_id_lock = threading.Lock()
        self.queue_lock = threading.Lock()
        self.blink_lock = threading.Lock()

        self._rr = None
        self._wr = None

        self.state_machine_state = self.State.IDLE

        self.exception_state = False
        self.data_exchange_in_process = False
        self.connection_cmd_sent = False
        self.state_read = True

        self.cmd_current = None

    @property
    def is_connected(self):
        print('data exchange ', self.data_exchange_in_process)
        return self.data_exchange_in_process

    @property
    def connection_cmd(self):
        return self.cmd_current

    @is_connected.setter
    def is_connected(self, value):
        self._is_connected = value
        if self._is_connected:
            self._inner_modbus_is_conn = self.Cmd.CONNECT
        else:
            self._inner_modbus_is_conn = self.Cmd.DISCONNECT

    def is_connected_state_set(self, boolean_value):
        self.queue_cmd.put(self.Cmd(boolean_value))

    def queue_data_get(self):
        if not self.queue_income.empty():
            data = self.queue_income.get()
            return data
        else:
            return None

    def queue_data_set(self, data):
        if self.queue_outcome:
            self.queue_outcome.put(data)

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
            with self.sl_id_lock:
                self.disconnect()
                self.slave_id = new_slave_id
                self.connect()

    def stop(self):
        print('Serial Task: command CLOSE')
        self.is_connected = False
        if self.client is not None:
            self.client.close()
        self.stopped = True

    def connect(self):
        try:
            self.client = ModbusClient(method=self.method, port=self.port,
                                       baudrate=self.baudrate, parity=self.parity,
                                       timeout=self.timeout, bytesize=self.bytesize,
                                       stopbits=self.stopbits)
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

    def modbus_execution(self):

        if self.queue_cmd.qsize():
            self.cmd_current = self.queue_cmd.get()

        if (self.cmd_current == self.Cmd.DISCONNECT) and \
           (self.state_machine_state != self.State.IDLE):
            self.state_machine_state = self.State.CONN_DEMOLISH

        if self.state_machine_state == self.State.IDLE:
            if self.cmd_current == self.Cmd.CONNECT:
                self.state_machine_state = self.State.CONN_ESTABLISH
            self.data_exchange_in_process = False

        elif self.state_machine_state == self.State.CONN_ESTABLISH:
            self.data_exchange_in_process = False
            self.connect()
            self.state_machine_state = self.State.CONN_CONFIRM

        elif self.state_machine_state == self.State.CONN_CONFIRM:
            try:
                with self.queue_lock:
                    rr = self.client.read_holding_registers(1000, count=13,
                                                            unit=self.slave_id)
                if rr.registers:
                    self.state_machine_state = self.State.READ
                    self.app_data.modbus_data = rr.registers
                    self.app_data.modbus_send_data = rr.registers[2:12]

            except Exception as ex:
                self.state_machine_state = self.State.CONN_DEMOLISH
                self.data_exchange_in_process = False
                print('establish exception ', ex)

        elif self.state_machine_state == self.State.READ:
            try:
                with self.queue_lock:
                    rr = self.client.read_holding_registers(1000, count=13,
                                                            unit=self.slave_id)
                self.queue_income.put(rr.registers)
                self.data_exchange_in_process = True
            except Exception as ex:
                self.data_exchange_in_process = False
                print('Read exception ', ex)

            if self.data_exchange_in_process:
                self.state_machine_state = self.State.WRITE

        elif self.state_machine_state == self.State.WRITE:
            if not self.queue_outcome.empty():
                try:
                    with self.queue_lock:
                        sets = self.queue_outcome.get()
                        self.client.write_registers(1002, sets, count=10, unit=self.slave_id)
                    self.data_exchange_in_process = True
                except Exception as ex:
                    self.data_exchange_in_process = False
                    print('Write exception ', ex)

            self.state_machine_state = self.State.READ

        elif self.state_machine_state == self.State.CONN_DEMOLISH:
            self.disconnect()
            self.state_machine_state = self.State.IDLE
            self.data_exchange_in_process = False

        else:
            pass

        time.sleep(0.05)

    def run(self):
        while not self.stopped:
            self.modbus_execution()
        print('Serial Task: destroyed')
