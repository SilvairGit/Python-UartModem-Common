import logging
import queue
import threading
import time
import crcmod
import serial

LOGGER = logging.getLogger(__name__)


class UartConnectionThread(threading.Thread):
    """
    Class responsible for handling UART connection (sending and receiving data).
    """

    def __init__(self, _serial, in_queue, out_queue):
        """
        Initializes UART connection thread class.

        :param _serial: serial.Serial, class allowing for serial port access.
        :param in_queue: queue.Queue, queue to which will be put received bytes.
        :param out_queue: queue.Queue, queue with bytes that will be sent.
        """
        super().__init__()
        self.daemon = True

        self._serial = _serial
        self._serial_busy = threading.Event()

        self._in_queue = in_queue
        self._out_queue = out_queue

    def set_baudrate(self, baudrate):
        """
        Sets UART baudrate.

        :param baudrate: int, UART baudrate
        """
        settings = self._serial.get_settings()
        settings["baudrate"] = baudrate

        self._serial.apply_settings(settings)

    def stop(self):
        """
        Stops UART connection thread.
        """
        try:
            self._serial_busy.clear()
            self.join()
        except RuntimeError as e:
            LOGGER.info("Tried to stop UartConnectionThread before it is started. An error occurred: %s", e)

    def run(self):
        """
        A run method that sending and receiving data over the UART.
        """
        self._serial_busy.set()

        self._serial.reset_input_buffer()
        self._serial.reset_output_buffer()

        data_to_be_sent = bytearray()

        while self._serial_busy.is_set():
            if not data_to_be_sent and not self._out_queue.empty():
                data_to_be_sent = self._out_queue.get_nowait()

            if data_to_be_sent:
                sent_bytes_n = self._serial.write(data_to_be_sent)
                data_to_be_sent = data_to_be_sent[sent_bytes_n:]

            self._in_queue.put(self._serial.read_all())

            time.sleep(0.001)  # Needed on Linux. Otherwise CPU utilization 100% is observed.


def create_uart_connection_thread(in_queue, out_queue, port, baudrate=56700, timeout_s=0, write_timeout_s=0):
    """
    Function creates UartConnectionThread object.

    :param in_queue: queue.Queue, queue to which will be put received bytes.
    :param out_queue: queue.Queue, queue with bytes that will be sent.
    :param port: str, UART com port name
    :param baudrate: int, UART baudrate
    :param timeout_s: int, timeout for receiving data from UART
    :param write_timeout_s: int, timeout for sendin data over UART
    :return: UartConnectionThread object
    """
    _serial = serial.Serial(
        port,
        baudrate,
        timeout=timeout_s,
        write_timeout=write_timeout_s
    )

    return UartConnectionThread(_serial, in_queue, out_queue)


class UartAdapterObserver:
    """
    Abstract class responsible for receiving notifications from UartAdapter.
    Inherit this class to make registering of your class possible.
    """

    def new_frame_notification(self, frame):
        """
        Called when new frame is received. Should be overloaded in derived class.

        :param frame:   bytes, received frame, consist of len, cmd and payload (without preamble and crc)
        :return:        None
        """
        pass


class UartAdapter(threading.Thread):
    """
    Class responsible for communicating with firmware over uart protocol in new thread. In order to start execution of
    thread start() method has to be called on
    instance of UartAdapter class.
    Provides methods for sending or writing from serial buffer using Queue.
    This class expects that registered object is of MeshNodeUart type which will have received_frames queue populated
    with every parsed frame.
    """

    UART_PREAMBLE = bytes.fromhex("AA55")

    def __init__(self, port, baud_rate=56700, timeout_s=0, write_timeout_s=0):
        """
        Initializes UartAdapter class.

        :param port:            COM port to be used
        :param baud_rate:       UART baudrate
        :param timeout_s:       UART connection timeout
        :param write_timeout_s: UART connection write timeout
        """
        super().__init__()
        self.daemon = True

        self._in_queue = queue.Queue()
        self._out_queue = queue.Queue()

        self._uart_conn = create_uart_connection_thread(
            self._in_queue,
            self._out_queue,
            port=port,
            baudrate=baud_rate,
            timeout_s=timeout_s,
            write_timeout_s=write_timeout_s
        )
        self._uart_conn.start()

        self.observers = []

        self._processing_frames = threading.Event()

        LOGGER.info("UART adapter initialized")

    def change_baudrate(self, baud_rate):
        """
        Sets serial port baudrate. This method is thread safe

        :param baud_rate: int, new baudrate value
        """
        self._uart_conn.set_baudrate(baud_rate)

    def register_observer(self, observer_obj):
        """
        Register objects for notification (updating queue). Registered object has to be of UartAdapterObserver class.

        :param observer_obj: instance of object
        """
        assert isinstance(observer_obj,
                          UartAdapterObserver), "[UART ADAPTER] Invalid class instance. Expected 'UartAdapterObserver'"
        if observer_obj not in self.observers:
            self.observers.append(observer_obj)

    def unregister_observer(self, observer_obj):
        """
        Unregister objects for notification. Unregistered object has to be of UartAdapterObserver class.

        :param observer_obj: instance of object
        """
        assert isinstance(observer_obj,
                          UartAdapterObserver), "[UART ADAPTER] Invalid class instance. Expected 'UartAdapterObserver'"
        self.observers.remove(observer_obj)

    def _insert_parsed_frame(self, frame):
        """
        Populates queues for all registered objects with parsed frame.

        :param frame_dict: dict representing parsed uart frame
        """
        for observer in self.observers:
            observer.new_frame_notification(frame)

    def write_uart_frame(self, uart_frame, send_raw=False):
        """
        Writes uart_frame directly to serial buffer

        :param uart_frame: bytes with raw data (without preamble and crc)
        :param send_raw: bool, if set to True will send raw bytes else will append preamble and crc
        """
        assert type(uart_frame) in [bytes], "Given data type for creating uart frame: '{}' is invalid. " \
                                            "Expected bytes.".format(type(uart_frame))

        if send_raw:
            frame_to_send = uart_frame
        else:
            crc = UartAdapter.calculate_crc_bytes(uart_frame)
            frame_to_send = UartAdapter.UART_PREAMBLE + uart_frame + crc
        self._out_queue.put(frame_to_send)

    def stop(self):
        """
        Stops execution of thread.
        """
        self._uart_conn.stop()

        try:
            self._processing_frames.clear()
            self.join()
        except RuntimeError as e:
            LOGGER.info("Tried to stop UartAdapter thread before it is started. An error occurred: %s", e)

    def run(self):
        """
        Main UartAdapter loop. Responsible for receiving data from UART

        :return:    None
        """
        LOGGER.info("uart adapter run")
        self._processing_frames.set()

        not_processed_buffer_data = bytearray()

        while self._processing_frames.is_set():
            try:
                not_processed_buffer_data += self._in_queue.get(timeout=0.1)

                frames, not_processed_buffer_data = UartAdapter.extract_frames(not_processed_buffer_data)
                for frame in frames:
                    self._insert_parsed_frame(frame)

            except queue.Empty:
                pass

    @staticmethod
    def extract_frames(raw_uart_data):
        """
        Extract single-message-frames (without preamble and crc) from raw uart data.

        :param raw_uart_data:   bytes, bytearray    Raw uart data
        :return:                tuple:  list of extracted uart frames, bytes remaining data
        """
        uart_frames = list()
        raw_uart_data = UartAdapter.eat_bytes_until_preamble(raw_uart_data)

        if len(raw_uart_data) < 6:
            return uart_frames, raw_uart_data

        data_len = int.from_bytes(raw_uart_data[2:3], byteorder='little', signed=False)
        if len(raw_uart_data) < 6 + data_len:
            return uart_frames, raw_uart_data

        uart_frame = raw_uart_data[:4 + data_len + 2]
        remaining_data = raw_uart_data[6 + data_len:]
        expected_crc = UartAdapter.calculate_crc(uart_frame[2:4 + data_len])
        actual_crc = int.from_bytes(uart_frame[len(uart_frame) - 2:], byteorder='little',
                                    signed=False)

        uart_frame_no_preamble_and_crc = uart_frame[2:len(uart_frame) - 2]

        if expected_crc == actual_crc:
            uart_frames.append(uart_frame_no_preamble_and_crc)
            if len(remaining_data) > 0:
                another_frames, remaining_data = UartAdapter.extract_frames(remaining_data)
                uart_frames.extend(another_frames)
            return uart_frames, remaining_data
        else:
            return uart_frames, remaining_data

    @staticmethod
    def calculate_crc(bytes_data):
        """
        Calculates checksum for given series of bytes.
        Parameters for checksum:
        - polynomial = 0x8005
        - init value = 0xFFFF

        :param bytes_data:  bytes type data for calculating checksum
        :return:            int, checksum
        """
        _checksum_function = crcmod.mkCrcFun(0x18005, rev=False, initCrc=0xFFFF, xorOut=0x0000)
        assert type(bytes_data) == bytes or type(
            bytes_data) == bytearray, "Given invalid data type '{}', expected 'bytes'".format(type(bytes_data))
        checksum = _checksum_function(bytes_data)
        return checksum

    @staticmethod
    def calculate_crc_bytes(bytes_data):
        """
        Calculates checksum for given series of bytes

        :param bytes_data: bytes type data for calculating checksum
        :return: bytes, checksum
        """
        return UartAdapter.calculate_crc(bytes_data).to_bytes(2, byteorder='little', signed=False)

    @staticmethod
    def eat_bytes_until_preamble(buffer_data):
        """
        Removes bytes from received data until preamble indicating a new frame is found.

        :param buffer_data: bytearray with raw data obtained from the serial port buffer
        :return: bytearray with raw data, with preamble on first bytes (or all raw data, if there was no preamble in
        the buffer).
        """
        orphaned_bytes = bytearray()
        while len(buffer_data) > 0 and buffer_data[:2] != bytearray(UartAdapter.UART_PREAMBLE):
            orphaned_bytes.append(buffer_data.pop(0))
        if len(orphaned_bytes) > 0:
            if len(buffer_data) == 0:
                return orphaned_bytes
            print("Removed orphaned bytes: {}".format(orphaned_bytes))
        return buffer_data
