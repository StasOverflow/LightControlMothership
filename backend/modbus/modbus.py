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
        CONN_RECONNECT = 6

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
        self.queue_new_data = queue.Queue()

        self.method = conn_method
        self.port = port
        self.baudrate = baudrate
        self.parity = parity
        self.timeout = timeout
        self.slave_id = slave_id
        self.bytesize = bytesize
        self.stopbits = stopbits

        self.stopped = False
        self._inner_modbus_is_conn = self.Cmd.DISCONNECT
        self.client = None

        self.port_lock = threading.Lock()
        self.queue_lock = threading.Lock()
        self.blink_lock = threading.Lock()
        self.reconnect_lock = threading.Lock()
        self.state_lock = threading.Lock()

        self._rr = None
        self._wr = None

        self.state_machine_state = self.State.IDLE

        self.exception_state = False
        self.data_exchange_in_process = False
        self.connection_cmd_sent = False
        self.state_read = True

        self.cmd_current = None
        self.data_renewed = False
        self.slave_changed = False
        self.reconnect_requested = False

    def _modbus_data_flush(self):
        while not self.queue_outcome.empty():
            self.queue_outcome.get()
        while not self.queue_income.empty():
            self.queue_income.get()

        self.data_renewed = False
        self.app_data.modbus_data = None
        self.app_data.modbus_send_data = None

    @property
    def is_connected(self):
        return self.data_exchange_in_process

    @property
    def connection_cmd(self):
        return self.cmd_current

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
        if self.cmd_current != self.Cmd.CONNECT:
            with self.port_lock:
                self.port = new_com_port
        else:
            print('Error: PORT cant be changed while connected!')

    def slave_id_update(self, new_slave_id):
        self.slave_id = new_slave_id

        self.slave_changed = True
        self._modbus_data_flush()

    def stop(self):
        print('Serial Task: command CLOSE')
        if self.client is not None:
            self.client.close()
        self.stopped = True

    def connect(self):
        try:
            self.client = ModbusClient(method=self.method, port=self.port,
                                       baudrate=self.baudrate, parity=self.parity,
                                       timeout=self.timeout, bytesize=self.bytesize,
                                       stopbits=self.stopbits)
        except Exception as ex:
            print('is connected exception', ex)

    def disconnect(self):
        try:
            if self.client is not None:
                self.client.close()
        except Exception as ex:
            print('is connected exception', ex)

    def exception_state_get(self):
        return self.exception_state

    def modbus_execution(self):
        if self.queue_cmd.qsize():
            self.cmd_current = self.queue_cmd.get()

        machine_state = self.state_machine_state

        if self.cmd_current == self.Cmd.DISCONNECT and machine_state != self.State.IDLE:
            machine_state = self.State.CONN_DEMOLISH

        if machine_state == self.State.IDLE:
            if self.cmd_current == self.Cmd.CONNECT:
                machine_state = self.State.CONN_ESTABLISH
            self.data_exchange_in_process = False

        elif machine_state == self.State.CONN_ESTABLISH:
            self.data_exchange_in_process = False
            self.connect()
            machine_state = self.State.CONN_CONFIRM

        elif machine_state == self.State.CONN_CONFIRM:
            try:
                with self.queue_lock:
                    rr = self.client.read_holding_registers(1000, count=13,
                                                            unit=self.slave_id)
                    if rr.registers:
                        machine_state = self.State.READ
                        self.queue_income.put(rr.registers)
                        self.app_data.modbus_data = rr.registers
                        self.app_data.modbus_send_data = self.app_data.modbus_data[2:12]
                        self.data_renewed = True

            except Exception as ex:
                machine_state = self.State.CONN_RECONNECT
                self.reconnect_requested = True
                self.data_renewed = False
                self.data_exchange_in_process = False
                print('establish exception ', ex)

        elif machine_state == self.State.READ:
            try:
                with self.queue_lock:
                    rr = self.client.read_holding_registers(1000, count=13,
                                                            unit=self.slave_id)
                    self.queue_income.put(rr.registers)
                    self.data_exchange_in_process = True
                    machine_state = self.State.WRITE
            except Exception as ex:
                self.data_exchange_in_process = False
                print('Read exception ', ex)
                machine_state = self.State.CONN_RECONNECT
                self.reconnect_requested = True

        elif machine_state == self.State.WRITE:
            if not self.queue_outcome.empty():
                try:
                    with self.queue_lock:
                        sets = self.queue_outcome.get()
                        self.client.write_registers(1002, sets, count=10, unit=self.slave_id)
                        self.data_exchange_in_process = True
                        machine_state = self.State.READ
                except Exception as ex:
                    self.data_exchange_in_process = False
                    print('Write exception ', ex)
                    machine_state = self.State.CONN_RECONNECT
            else:
                machine_state = self.State.READ

        elif machine_state == self.State.CONN_DEMOLISH:
            self.disconnect()
            self._modbus_data_flush()

            machine_state = self.State.IDLE
            self.data_exchange_in_process = False

        elif machine_state == self.State.CONN_RECONNECT:
            with self.reconnect_lock:
                self.disconnect()
                self._modbus_data_flush()
                machine_state = self.State.IDLE
                self.data_exchange_in_process = False

        if not self.slave_changed:
            self.state_machine_state = machine_state
        else:
            self.slave_changed = False
            self.state_machine_state = self.State.CONN_RECONNECT
            self.reconnect_requested = True

        time.sleep(0.05)

    def run(self):
        while not self.stopped:
            self.modbus_execution()
        print('Serial Task: destroyed')
