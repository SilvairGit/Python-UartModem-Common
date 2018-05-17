import unittest

from silvair_uart_common_libs import message_factory
from silvair_uart_common_libs.messages import UartCommand, PingRequestMessage, PongResponseMessage


class PingRequestMessageFactoryTests(unittest.TestCase):
    def test_ping_request_deserialize_valid(self):
        bytes = b"\x01\x01\xAA"

        msg = message_factory.deserialize_message(bytes)

        self.assertEquals(msg.type, UartCommand.PingRequest)
        self.assertEquals(msg.data, b'\xAA')

    def test_ping_request_serialize_valid(self):
        msg = PingRequestMessage()
        msg.data = b'\xBB'
        expected_output = b"\x01\x01\xBB"

        bytes = message_factory.serialize_message(msg)

        self.assertEquals(expected_output, bytes)


class PongResponseMessageFactoryTests(unittest.TestCase):
    def test_ping_request_deserialize_valid(self):
        bytes = b"\x01\x02\xAA"

        msg = message_factory.deserialize_message(bytes)

        self.assertEquals(msg.type, UartCommand.PongResponse)
        self.assertEquals(msg.data, b'\xAA')

    def test_ping_request_serialize_valid(self):
        msg = PongResponseMessage()
        msg.data = b'\xBB'
        expected_output = b"\x01\x02\xBB"

        bytes = message_factory.serialize_message(msg)

        self.assertEquals(expected_output, bytes)