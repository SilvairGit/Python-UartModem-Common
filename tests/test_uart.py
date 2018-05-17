import unittest

from silvair_uart_common_libs.uart_common_classes import UartAdapter


class TestUartClass(unittest.TestCase):
    invalid_half_frame_bytes_with_data = bytes.fromhex("AA55010122")
    valid_full_frame_bytes_with_data = bytes.fromhex("AA55010122DB88")
    valid_full_frame_payload = bytes.fromhex("010122")
    valid_full_frame_bytes_with_data_with_preamle_and_crc = bytes.fromhex("AA55010122DB88")
    valid_full_frame_dict_with_data = {"len": "01", "cmd": "01", "data": "22"}

    def test_one_and_half_frame_is_parsed(self):
        self.assertEqual(UartAdapter.extract_frames(self.valid_full_frame_bytes_with_data + self.invalid_half_frame_bytes_with_data),
                         ([self.valid_full_frame_payload], self.invalid_half_frame_bytes_with_data))

    def test_two_frames_from_buffer_are_processed(self):
        self.assertEqual(UartAdapter.extract_frames(self.valid_full_frame_bytes_with_data + self.valid_full_frame_bytes_with_data),
                         ([self.valid_full_frame_payload, self.valid_full_frame_payload], bytearray()))

    def test_empty_buffer_is_processed(self):
        self.assertEqual(UartAdapter.extract_frames(bytearray()),
                         ([], bytearray()))