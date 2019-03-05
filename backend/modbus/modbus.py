from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import threading
import queue
import time
import settings


class ModbusThread(threading.Thread):
    def __init__(
            self, queue_income, queue_outcome,
            method='rtu',
            port='COM2',
            baudrate=19200,
            parity='E',
            timeout=1,
            slave_id=32,
            *args,
            **kwargs,
    ):
        self.app_state = settings.ApplicationState()

        super().__init__(*args, **kwargs)
        self.daemon = True

        self.stopped = False
        self.is_connected = False
        self.client = None

        self.queue_income = queue_income
        self.queue_outcome = queue_outcome

        self.method = method
        self.port = port
        self.baudrate = baudrate
        self.parity = parity
        self.timeout = timeout
        self.slave_id = slave_id

    def com_port_update(self, new_com_port):
        if not self.is_connected:
            lock = threading.Lock()
            with lock:
                self.port = new_com_port
        else:
            print('Error: PORT cant be changed, still connected!')

    def slave_id_update(self, new_slave_id):
        if not self.is_connected:
            lock = threading.Lock()
            with lock:
                self.slave_id = new_slave_id
        else:
            print('Error: Device ID cant be changed, still connected!')

    def stop(self):
        print('Serial Task: command CLOSE')
        self.is_connected = False
        if self.client is not None:
            self.client.close()
        self.stopped = True

    def connect(self):
        self.is_connected = True
        self.client = ModbusClient(method=self.method, port=self.port, baudrate=self.baudrate,
                                   parity=self.parity, timeout=self.timeout)

    def disconnect(self):
        self.is_connected = False
        try:
            self.is_connected = False
            if self.client is not None:
                self.client.close()
        except Exception as ex:
            print(ex)

    def run(self):
        while not self.stopped:

            if self.is_connected:
                if self.queue_outcome.qsize():
                    try:
                        sets = self.queue_outcome.get()
                        self.client.write_registers(1013, sets, count=4, unit=self.slave_id)
                    except queue.Empty:
                        pass
                else:
                    try:
                        rr = self.client.read_holding_registers(1000, count=18, unit=self.slave_id)
                        self.queue_income.put(rr.registers)
                    except Exception as ex:
                        print(ex)
            time.sleep(0.1)
        print('Serial Task: destroyed')
