import io
import unittest

from silvair_uart_common_libs.message_types import ModelDesc, FactoryResetSource, ModemState, Error, AttentionEvent, \
    DFUStatus, ModelID
from silvair_uart_common_libs.messages import PingRequestMessage, UartCommand, InvalidOpcode, InvalidLen, \
    PongResponseMessage, \
    InitDeviceEventMessage, CreateInstancesRequestMessage, CreateInstancesResponseMessage, InitNodeEventMessage, \
    StartNodeRequestMessage, StartNodeResponseMessage, FactoryResetResponseMessage, FactoryResetRequestMessage, \
    FactoryResetEventMessage, MeshMessageRequestMessage, MeshMessageResponseMessage, CurrentStateRequestMessage, \
    CurrentStateResponseMessage, ErrorMessage, FirmwareVersionRequestMessage, FirmwareVersionResponseMessage, \
    SensorUpdateRequestMessage, AttentionEventMessage, SoftResetRequestMessage, SoftResetResponseMessage, \
    SensorUpdateResponseMessage, DeviceUUIDRequestMessage, DeviceUUIDResponseMessage, DfuInitRequestMessage, \
    DfuStatusRequestMessage, DfuInitResponseMessage, DfuPageCreateResponseMessage, DfuPageStoreRequestMessage, \
    DfuPageStoreResponseMessage, DfuStatusResponseMessage, DfuPageCreateRequestMessage, DfuWriteDataEventMessage


class PingRequestMessageTests(unittest.TestCase):
    def test_ping_request_deserialize_valid(self):
        stream = io.BytesIO(b"\x01\x01\xAA")

        msg = PingRequestMessage()
        msg.deserialize(stream)

        self.assertEquals(msg.type, UartCommand.PingRequest)
        self.assertEquals(msg.data, b'\xAA')

    def test_ping_request_deserialize_invalid_opcode(self):
        stream = io.BytesIO(b"\x01\xAB\xAA")
        msg = PingRequestMessage()

        with self.assertRaises(InvalidOpcode) as _:
            msg.deserialize(stream)

    def test_ping_request_deserialize_invalid_too_short(self):
        stream = io.BytesIO(b"\x03\x01\xAA\xBB")
        msg = PingRequestMessage()

        with self.assertRaises(InvalidLen) as _:
            msg.deserialize(stream)

    def test_ping_request_serialize_valid(self):
        msg = PingRequestMessage()
        msg.data = b'\xBB'
        expected_output = b"\x01\x01\xBB"
        stream = io.BytesIO()

        msg.serialize(stream)

        self.assertEquals(expected_output, stream.getvalue())


class PongResponseMessageTests(unittest.TestCase):
    def test_pong_response_deserialize_valid(self):
        stream = io.BytesIO(b"\x01\x02\xAA")

        msg = PongResponseMessage()
        msg.deserialize(stream)

        self.assertEquals(msg.type, UartCommand.PongResponse)
        self.assertEquals(msg.data, b'\xAA')

    def test_pong_response_deserialize_invalid_opcode(self):
        stream = io.BytesIO(b"\x01\xAB\xAA")
        msg = PongResponseMessage()

        with self.assertRaises(InvalidOpcode) as _:
            msg.deserialize(stream)

    def test_pong_response_deserialize_invalid_too_short(self):
        stream = io.BytesIO(b"\x03\x02\xAA\xBB")
        msg = PongResponseMessage()

        with self.assertRaises(InvalidLen) as _:
            msg.deserialize(stream)

    def test_pong_response_serialize_valid(self):
        msg = PongResponseMessage()
        msg.data = b'\xBB'
        expected_output = b"\x01\x02\xBB"
        stream = io.BytesIO()

        msg.serialize(stream)

        self.assertEquals(expected_output, stream.getvalue())


class InitDeviceEventMessageTests(unittest.TestCase):
    def test_init_device_event_deserialize_valid(self):
        stream = io.BytesIO(b"\x06\x03\x01\x10\x03\x10\x08\x10")

        expected_model_id_1 = ModelID(0x1001)
        expected_model_id_2 = ModelID(0x1003)
        expected_model_id_3 = ModelID(0x1008)

        msg = InitDeviceEventMessage()
        msg.deserialize(stream)

        self.assertEquals(msg.type, UartCommand.InitDeviceEvent)
        self.assertEquals(msg.model_ids[0], expected_model_id_1)
        self.assertEquals(msg.model_ids[1], expected_model_id_2)
        self.assertEquals(msg.model_ids[2], expected_model_id_3)

    def test_init_device_event_deserialize_invalid_len(self):
        stream = io.BytesIO(b"\x07\x03\x01\x10\x03\x10\x08\x10")
        msg = InitDeviceEventMessage()

        with self.assertRaises(InvalidLen) as _:
            msg.deserialize(stream)

    def test_init_device_event_deserialize_invalid_len2(self):
        stream = io.BytesIO(b"\x05\x03\x01\x10\x03\x10\x08\x10")
        msg = InitDeviceEventMessage()

        with self.assertRaises(InvalidLen) as _:
            msg.deserialize(stream)

    def test_init_device_event_deserialize_invalid_opcode(self):
        stream = io.BytesIO(b"\x06\x04\x01\x10\x03\x10\x08\x10")
        msg = InitDeviceEventMessage()

        with self.assertRaises(InvalidOpcode) as _:
            msg.deserialize(stream)

    def test_init_device_event_serialize_valid(self):
        input_model_id_1 = ModelID(0x1001)
        input_model_id_2 = ModelID(0x1003)
        input_model_id_3 = ModelID(0x1008)

        stream = io.BytesIO()
        expected_output = b"\x06\x03\x01\x10\x03\x10\x08\x10"

        msg = InitDeviceEventMessage()
        msg.model_ids = [input_model_id_1, input_model_id_2, input_model_id_3]
        msg.serialize(stream)

        self.assertEquals(expected_output, stream.getvalue())

    def test_deserialize_real(self):
        stream = io.BytesIO(b"\x14\x03\x01\x10\x03\x10\x08\x10\x02\x13\x11\x13\x00\x11\x01\x11\x00\x13\x0f\x13\x02\x11")

        input_models = list()
        for i in range(10):
            input_models.append(ModelDesc)

        msg = InitDeviceEventMessage()
        msg.deserialize(stream)

        self.assertEquals(msg.type, UartCommand.InitDeviceEvent)

class CreateInstancesRequestTests(unittest.TestCase):
    def test_create_instances_request_deserialize_valid(self):
        stream = io.BytesIO(b"\x06\x04\x01\x10\x03\x10\x08\x10")

        expected_model_desc_1 = ModelDesc()
        expected_model_desc_2 = ModelDesc()
        expected_model_desc_3 = ModelDesc()

        expected_model_desc_1.model_id = 0x1001
        expected_model_desc_2.model_id = 0x1003
        expected_model_desc_3.model_id = 0x1008

        msg = CreateInstancesRequestMessage()
        msg.deserialize(stream)

        self.assertEquals(msg.type, UartCommand.CreateInstancesRequest)
        self.assertEquals(msg.model_descs[0].model_id, expected_model_desc_1.model_id)
        self.assertEquals(msg.model_descs[1].model_id, expected_model_desc_2.model_id)
        self.assertEquals(msg.model_descs[2].model_id, expected_model_desc_3.model_id)

    def test_create_instances_request_deserialize_valid_with_config(self):
        stream = io.BytesIO(b"\x0E\x04\x01\x11\x00\x00\x11\x22\x22\x33\x33\x44\x44\x55\x11\x13")

        expected_model_desc_1 = ModelDesc()
        expected_model_desc_2 = ModelDesc()

        expected_model_desc_1.model_id = 0x1101
        expected_model_desc_1.config = b"\x00\x00\x11\x22\x22\x33\x33\x44\x44\x55"
        expected_model_desc_2.model_id = 0x1311

        msg = CreateInstancesRequestMessage()
        msg.deserialize(stream)

        self.assertEquals(msg.type, UartCommand.CreateInstancesRequest)
        self.assertEquals(msg.model_descs[0].model_id, expected_model_desc_1.model_id)
        self.assertEquals(msg.model_descs[0].config, expected_model_desc_1.config)
        self.assertEquals(msg.model_descs[1].model_id, expected_model_desc_2.model_id)

    def test_create_instances_request_deserialize_invalid_len(self):
        stream = io.BytesIO(b"\x07\x04\x01\x10\x03\x10\x08\x10")
        msg = CreateInstancesRequestMessage()

        with self.assertRaises(InvalidLen) as _:
            msg.deserialize(stream)

    def test_create_instances_request_deserialize_invalid_len2(self):
        stream = io.BytesIO(b"\x05\x04\x01\x10\x03\x10\x08\x10")
        msg = CreateInstancesRequestMessage()

        with self.assertRaises(InvalidLen) as _:
            msg.deserialize(stream)

    def test_create_instances_request_deserialize_invalid_model_id(self):
        stream = io.BytesIO(b"\x06\x03\x01\x10\x03\x10\x08\x10")
        msg = CreateInstancesRequestMessage()

        with self.assertRaises(InvalidOpcode) as _:
            msg.deserialize(stream)

    def test_create_instances_request_serialize_valid(self):
        input_model_id_1 = ModelDesc()
        input_model_id_2 = ModelDesc()
        input_model_id_3 = ModelDesc()

        input_model_id_1.model_id = 0x1001
        input_model_id_2.model_id = 0x1003
        input_model_id_3.model_id = 0x1008

        stream = io.BytesIO()
        expected_output = b"\x06\x04\x01\x10\x03\x10\x08\x10"

        msg = CreateInstancesRequestMessage()
        msg.model_descs = [input_model_id_1, input_model_id_2, input_model_id_3]
        msg.serialize(stream)

        self.assertEquals(expected_output, stream.getvalue())

    def test_create_instances_request_serialize_valid_with_config(self):
        input_model_id_1 = ModelDesc()
        input_model_id_2 = ModelDesc()

        input_model_id_1.model_id = 0x1101
        input_model_id_1.config = b"\x00\x00\x11\x22\x22\x33\x33\x44\x44\x55"
        input_model_id_2.model_id = 0x1311

        stream = io.BytesIO()
        expected_output = b"\x0E\x04\x01\x11\x00\x00\x11\x22\x22\x33\x33\x44\x44\x55\x11\x13"

        msg = CreateInstancesRequestMessage()
        msg.model_descs = [input_model_id_1, input_model_id_2]
        msg.serialize(stream)

        self.assertEquals(expected_output, stream.getvalue())


class CreateInstancesResponseTests(unittest.TestCase):
    def test_create_instances_response_deserialize_valid(self):
        stream = io.BytesIO(b"\x06\x05\x01\x10\x03\x10\x08\x10")

        expected_model_id_1 = ModelID(0x1001)
        expected_model_id_2 = ModelID(0x1003)
        expected_model_id_3 = ModelID(0x1008)

        msg = CreateInstancesResponseMessage()
        msg.deserialize(stream)

        self.assertEquals(msg.type, UartCommand.CreateInstancesResponse)
        self.assertEquals(msg.model_ids[0], expected_model_id_1)
        self.assertEquals(msg.model_ids[1], expected_model_id_2)
        self.assertEquals(msg.model_ids[2], expected_model_id_3)

    def test_create_instances_response_deserialize_invalid_len(self):
        stream = io.BytesIO(b"\x07\x05\x01\x10\x03\x10\x08\x10")
        msg = CreateInstancesResponseMessage()

        with self.assertRaises(InvalidLen) as _:
            msg.deserialize(stream)

    def test_create_instances_response_deserialize_invalid_len2(self):
        stream = io.BytesIO(b"\x05\x05\x01\x10\x03\x10\x08\x10")
        msg = CreateInstancesResponseMessage()

        with self.assertRaises(InvalidLen) as _:
            msg.deserialize(stream)

    def test_create_instances_response_deserialize_invalid_opcode(self):
        stream = io.BytesIO(b"\x06\x03\x01\x10\x03\x10\x08\x10")
        msg = CreateInstancesResponseMessage()

        with self.assertRaises(InvalidOpcode) as _:
            msg.deserialize(stream)

    def test_create_instances_response_serialize_valid(self):
        input_model_id_1 = ModelID(0x1001)
        input_model_id_2 = ModelID(0x1003)
        input_model_id_3 = ModelID(0x1008)

        stream = io.BytesIO()
        expected_output = b"\x06\x05\x01\x10\x03\x10\x08\x10"

        msg = CreateInstancesResponseMessage()
        msg.model_ids = [input_model_id_1, input_model_id_2, input_model_id_3]
        msg.serialize(stream)

        self.assertEquals(expected_output, stream.getvalue())

    def test_deserialize_real(self):
        stream = io.BytesIO(b"\x14\x05\x01\x10\x03\x10\x08\x10\x02\x13\x11\x13\x00\x11\x01\x11\x00\x13\x0f\x13\x02\x11")

        input_models = list()
        for i in range(10):
            input_models.append(ModelDesc)

        msg = CreateInstancesResponseMessage()
        msg.deserialize(stream)

        self.assertEquals(msg.type, UartCommand.CreateInstancesResponse)


class InitNodeEventMessageTests(unittest.TestCase):
    def test_init_node_event_deserialize_valid(self):
        stream = io.BytesIO(b"\x06\x06\x01\x10\x03\x10\x08\x10")

        expected_model_id_1 = ModelID(0x1001)
        expected_model_id_2 = ModelID(0x1003)
        expected_model_id_3 = ModelID(0x1008)

        msg = InitNodeEventMessage()
        msg.deserialize(stream)

        self.assertEquals(msg.type, UartCommand.InitNodeEvent)
        self.assertEquals(msg.model_ids[0], expected_model_id_1)
        self.assertEquals(msg.model_ids[1], expected_model_id_2)
        self.assertEquals(msg.model_ids[2], expected_model_id_3)

    def test_init_node_event_deserialize_invalid_len(self):
        stream = io.BytesIO(b"\x07\x06\x01\x10\x03\x10\x08\x10")
        msg = InitNodeEventMessage()

        with self.assertRaises(InvalidLen) as _:
            msg.deserialize(stream)

    def test_init_node_event_deserialize_invalid_len2(self):
        stream = io.BytesIO(b"\x05\x06\x01\x10\x03\x10\x08\x10")
        msg = InitNodeEventMessage()

        with self.assertRaises(InvalidLen) as _:
            msg.deserialize(stream)

    def test_init_node_event_deserialize_invalid_opcode(self):
        stream = io.BytesIO(b"\x06\x04\xAA\xAA\xBB\xBB\xCC\xCC")
        msg = InitNodeEventMessage()

        with self.assertRaises(InvalidOpcode) as _:
            msg.deserialize(stream)

    def test_init_node_event_serialize_valid(self):
        input_model_id_1 = ModelID(0x1001)
        input_model_id_2 = ModelID(0x1003)
        input_model_id_3 = ModelID(0x1008)

        stream = io.BytesIO()
        expected_output = b"\x06\x06\x01\x10\x03\x10\x08\x10"

        msg = InitNodeEventMessage()
        msg.model_ids = [input_model_id_1, input_model_id_2, input_model_id_3]
        msg.serialize(stream)

        self.assertEquals(expected_output, stream.getvalue())


class MeshMessageRequestMessageTests(unittest.TestCase):
    def test_mesh_message_request_deserialize_valid(self):
        stream = io.BytesIO(b"\x06\x07\xAA\xBB\xCC\xDD\x12\x34")

        msg = MeshMessageRequestMessage()
        msg.deserialize(stream)

        self.assertEquals(msg.type, UartCommand.MeshMessageRequest)
        self.assertEquals(msg.instance_index, 0xAA)
        self.assertEquals(msg.sub_index, 0xBB)
        self.assertEquals(msg.mesh_opcode, 0xDDCC)
        self.assertEquals(msg.mesh_command, b"\x12\x34")

    def test_mesh_message_request_deserialize_invalid_opcode(self):
        stream = io.BytesIO(b"\x06\x09\xAA\xBB\xCC\xDD\x12\x34")
        msg = MeshMessageRequestMessage()

        with self.assertRaises(InvalidOpcode) as _:
            msg.deserialize(stream)

    def test_mesh_message_request_deserialize_invalid_len(self):
        stream = io.BytesIO(b"\x08\x07\xAA\xBB\xCC\xDD\x12\x34")
        msg = MeshMessageRequestMessage()

        with self.assertRaises(InvalidLen) as _:
            msg.deserialize(stream)

    def test_mesh_message_request_serialize_valid(self):
        msg = MeshMessageRequestMessage()
        msg.instance_index = 0xAA
        msg.sub_index = 0xBB
        msg.mesh_opcode = 0xDDCC
        msg.mesh_command = b"\x12\x34"

        stream = io.BytesIO()
        msg.serialize(stream)

        expected_output = b"\x06\x07\xAA\xBB\xCC\xDD\x12\x34"
        self.assertEquals(expected_output, stream.getvalue())


class StartNodeRequestMessageTests(unittest.TestCase):
    def test_start_node_request_deserialize_valid(self):
        stream = io.BytesIO(b"\x00\x09")

        msg = StartNodeRequestMessage()
        msg.deserialize(stream)

        self.assertEquals(msg.type, UartCommand.StartNodeRequest)

    def test_start_node_request_deserialize_invalid_opcode(self):
        stream = io.BytesIO(b"\x00\xAB")
        msg = StartNodeRequestMessage()

        with self.assertRaises(InvalidOpcode) as _:
            msg.deserialize(stream)

    def test_start_node_request_deserialize_invalid_too_long(self):
        stream = io.BytesIO(b"\x02\x09\xAA\xBB")
        msg = StartNodeRequestMessage()

        with self.assertRaises(InvalidLen) as _:
            msg.deserialize(stream)

    def test_start_node_request_serialize_valid(self):
        msg = StartNodeRequestMessage()
        expected_output = b"\x00\x09"
        stream = io.BytesIO()

        msg.serialize(stream)

        self.assertEquals(expected_output, stream.getvalue())


class StartNodeResponseMessageTests(unittest.TestCase):
    def test_start_node_response_deserialize_valid(self):
        stream = io.BytesIO(b"\x00\x0B")

        msg = StartNodeResponseMessage()
        msg.deserialize(stream)

        self.assertEquals(msg.type, UartCommand.StartNodeResponse)

    def test_start_node_response_deserialize_invalid_opcode(self):
        stream = io.BytesIO(b"\x00\xAB")
        msg = StartNodeResponseMessage()

        with self.assertRaises(InvalidOpcode) as _:
            msg.deserialize(stream)

    def test_start_node_response_deserialize_invalid_too_long(self):
        stream = io.BytesIO(b"\x02\x0B\xAA\xBB")
        msg = StartNodeResponseMessage()

        with self.assertRaises(InvalidLen) as _:
            msg.deserialize(stream)

    def test_start_node_response_serialize_valid(self):
        msg = StartNodeResponseMessage()
        expected_output = b"\x00\x0B"
        stream = io.BytesIO()

        msg.serialize(stream)

        self.assertEquals(expected_output, stream.getvalue())


class FactoryResetRequestMessageTests(unittest.TestCase):
    def test_factory_reset_request_deserialize_valid(self):
        stream = io.BytesIO(b"\x00\x0C")

        msg = FactoryResetRequestMessage()
        msg.deserialize(stream)

        self.assertEquals(msg.type, UartCommand.FactoryResetRequest)

    def test_factory_reset_request_deserialize_invalid_opcode(self):
        stream = io.BytesIO(b"\x00\xAB")
        msg = FactoryResetRequestMessage()

        with self.assertRaises(InvalidOpcode) as _:
            msg.deserialize(stream)

    def test_factory_reset_request_deserialize_invalid_too_long(self):
        stream = io.BytesIO(b"\x02\x0C\xAA\xBB")
        msg = FactoryResetRequestMessage()

        with self.assertRaises(InvalidLen) as _:
            msg.deserialize(stream)

    def test_factory_reset_request_serialize_valid(self):
        msg = FactoryResetRequestMessage()
        expected_output = b"\x00\x0C"
        stream = io.BytesIO()

        msg.serialize(stream)

        self.assertEquals(expected_output, stream.getvalue())


class FactoryResetResponseMessageTests(unittest.TestCase):
    def test_factory_reset_response_deserialize_valid(self):
        stream = io.BytesIO(b"\x00\x0D")

        msg = FactoryResetResponseMessage()
        msg.deserialize(stream)

        self.assertEquals(msg.type, UartCommand.FactoryResetResponse)

    def test_factory_reset_response_deserialize_invalid_opcode(self):
        stream = io.BytesIO(b"\x00\xAB")
        msg = FactoryResetResponseMessage()

        with self.assertRaises(InvalidOpcode) as _:
            msg.deserialize(stream)

    def test_factory_reset_response_deserialize_invalid_too_long(self):
        stream = io.BytesIO(b"\x02\x0D\xAA\xBB")
        msg = FactoryResetResponseMessage()

        with self.assertRaises(InvalidLen) as _:
            msg.deserialize(stream)

    def test_factory_reset_response_serialize_valid(self):
        msg = FactoryResetResponseMessage()
        expected_output = b"\x00\x0D"
        stream = io.BytesIO()

        msg.serialize(stream)

        self.assertEquals(expected_output, stream.getvalue())


class FactoryResetEventMessageTests(unittest.TestCase):
    def test_factory_reset_event_deserialize_valid(self):
        stream = io.BytesIO(b"\x00\x0E")

        msg = FactoryResetEventMessage()
        msg.deserialize(stream)

        self.assertEquals(msg.type, UartCommand.FactoryResetEvent)

    def test_factory_reset_event_deserialize_invalid_opcode(self):
        stream = io.BytesIO(b"\x00\xAB")
        msg = FactoryResetEventMessage()

        with self.assertRaises(InvalidOpcode) as _:
            msg.deserialize(stream)

    def test_factory_reset_event_deserialize_invalid_too_long(self):
        stream = io.BytesIO(b"\x01\x0E\x01")
        msg = FactoryResetEventMessage()

        with self.assertRaises(InvalidLen) as _:
            msg.deserialize(stream)

    def test_factory_reset_event_serialize_valid(self):
        msg = FactoryResetEventMessage()
        expected_output = b"\x00\x0E"
        stream = io.BytesIO()

        msg.serialize(stream)

        self.assertEquals(expected_output, stream.getvalue())


class MeshMessageResponseMessageTests(unittest.TestCase):
    def test_mesh_message_response_deserialize_valid(self):
        stream = io.BytesIO(b"\x02\x0F\x01\x02")

        msg = MeshMessageResponseMessage()
        msg.deserialize(stream)

        self.assertEquals(msg.type, UartCommand.MeshMessageResponse)
        self.assertEquals(msg.instance_index, 0x01)
        self.assertEquals(msg.sub_index, 0x02)

    def test_mesh_message_response_deserialize_invalid_opcode(self):
        stream = io.BytesIO(b"\x02\xAB\x01")
        msg = MeshMessageResponseMessage()

        with self.assertRaises(InvalidOpcode) as _:
            msg.deserialize(stream)

    def test_mesh_message_response_deserialize_invalid_too_long(self):
        stream = io.BytesIO(b"\x03\x0F\xAA\xBB\xCC")
        msg = MeshMessageResponseMessage()

        with self.assertRaises(InvalidLen) as _:
            msg.deserialize(stream)

    def test_mesh_message_response_deserialize_invalid_too_short(self):
        stream = io.BytesIO(b"\x01\x0F\xAA")
        msg = MeshMessageResponseMessage()

        with self.assertRaises(InvalidLen) as _:
            msg.deserialize(stream)

    def test_mesh_message_response_serialize_valid(self):
        msg = MeshMessageResponseMessage()
        msg.instance_index = 0x01
        msg.sub_index = 0x02
        expected_output = b"\x02\x0F\x01\x02"
        stream = io.BytesIO()

        msg.serialize(stream)

        self.assertEquals(expected_output, stream.getvalue())


class CurrentStateRequestMessageTests(unittest.TestCase):
    def test_current_state_request_deserialize_valid(self):
        stream = io.BytesIO(b"\x00\x10")

        msg = CurrentStateRequestMessage()
        msg.deserialize(stream)

        self.assertEquals(msg.type, UartCommand.CurrentStateRequest)

    def test_current_state_request_deserialize_invalid_opcode(self):
        stream = io.BytesIO(b"\x00\xAB")
        msg = CurrentStateRequestMessage()

        with self.assertRaises(InvalidOpcode) as _:
            msg.deserialize(stream)

    def test_current_state_request_deserialize_invalid_too_long(self):
        stream = io.BytesIO(b"\x02\x10\xAA\xBB")
        msg = CurrentStateRequestMessage()

        with self.assertRaises(InvalidLen) as _:
            msg.deserialize(stream)

    def test_current_state_request_serialize_valid(self):
        msg = CurrentStateRequestMessage()
        expected_output = b"\x00\x10"
        stream = io.BytesIO()

        msg.serialize(stream)

        self.assertEquals(expected_output, stream.getvalue())


class CurrentStateResponseMessageTests(unittest.TestCase):
    def test_current_state_response_deserialize_valid(self):
        stream = io.BytesIO(b"\x01\x11\x01")

        msg = CurrentStateResponseMessage()
        msg.deserialize(stream)

        self.assertEquals(msg.type, UartCommand.CurrentStateResponse)
        self.assertEquals(msg.state, ModemState.Device)

    def test_current_state_response_deserialize_invalid_opcode(self):
        stream = io.BytesIO(b"\x01\xAB\x01")
        msg = CurrentStateResponseMessage()

        with self.assertRaises(InvalidOpcode) as _:
            msg.deserialize(stream)

    def test_current_state_response_deserialize_invalid_too_long(self):
        stream = io.BytesIO(b"\x02\x11\x01\xBB")
        msg = CurrentStateResponseMessage()

        with self.assertRaises(InvalidLen) as _:
            msg.deserialize(stream)

    def test_current_state_response_serialize_valid(self):
        msg = CurrentStateResponseMessage()
        msg.state = ModemState.InitNode
        expected_output = b"\x01\x11\x02"
        stream = io.BytesIO()

        msg.serialize(stream)

        self.assertEquals(expected_output, stream.getvalue())


class ErrorMessageTests(unittest.TestCase):
    def test_error_deserialize_valid(self):
        stream = io.BytesIO(b"\x01\x12\x01")

        msg = ErrorMessage()
        msg.deserialize(stream)

        self.assertEquals(msg.type, UartCommand.Error)
        self.assertEquals(msg.error, Error.InvalidCMD)

    def test_error_deserialize_invalid_opcode(self):
        stream = io.BytesIO(b"\x01\xAB\x01")
        msg = ErrorMessage()

        with self.assertRaises(InvalidOpcode) as _:
            msg.deserialize(stream)

    def test_error_deserialize_invalid_too_long(self):
        stream = io.BytesIO(b"\x02\x12\x01\xBB")
        msg = ErrorMessage()

        with self.assertRaises(InvalidLen) as _:
            msg.deserialize(stream)

    def test_error_serialize_valid(self):
        msg = ErrorMessage()
        msg.error = Error.InvalidLen
        expected_output = b"\x01\x12\x02"
        stream = io.BytesIO()

        msg.serialize(stream)

        self.assertEquals(expected_output, stream.getvalue())


class FirmwareVersionRequestMessageTests(unittest.TestCase):
    def test_firmware_version_request_deserialize_valid(self):
        stream = io.BytesIO(b"\x00\x13")

        msg = FirmwareVersionRequestMessage()
        msg.deserialize(stream)

        self.assertEquals(msg.type, UartCommand.FirmwareVersionRequest)

    def test_firmware_version_request_deserialize_invalid_opcode(self):
        stream = io.BytesIO(b"\x00\xAB")
        msg = FirmwareVersionRequestMessage()

        with self.assertRaises(InvalidOpcode) as _:
            msg.deserialize(stream)

    def test_firmware_version_request_deserialize_invalid_too_long(self):
        stream = io.BytesIO(b"\x02\x13\xAA\xBB")
        msg = FirmwareVersionRequestMessage()

        with self.assertRaises(InvalidLen) as _:
            msg.deserialize(stream)

    def test_firmware_version_request_serialize_valid(self):
        msg = FirmwareVersionRequestMessage()
        expected_output = b"\x00\x13"
        stream = io.BytesIO()

        msg.serialize(stream)

        self.assertEquals(expected_output, stream.getvalue())


class FirmwareVersionResponseMessageTests(unittest.TestCase):
    def test_firmware_version_response_deserialize_valid(self):
        stream = io.BytesIO(b"\x05\x14\x01\x02\x03\x04\x05")

        msg = FirmwareVersionResponseMessage()
        msg.deserialize(stream)

        self.assertEquals(msg.type, UartCommand.FirmwareVersionResponse)
        self.assertEquals(msg.firmware_version, b"\x01\x02\x03\x04\x05")

    def test_firmware_version_response_deserialize_invalid_opcode(self):
        stream = io.BytesIO(b"\x05\x10\x01\x02\x03\x04\x05")
        msg = FirmwareVersionResponseMessage()

        with self.assertRaises(InvalidOpcode) as _:
            msg.deserialize(stream)

    def test_firmware_version_response_deserialize_invalid_len(self):
        stream = io.BytesIO(b"\x00\x14")
        msg = FirmwareVersionResponseMessage()

        with self.assertRaises(InvalidLen) as _:
            msg.deserialize(stream)

    def test_firmware_version_response_serialize_valid(self):
        msg = FirmwareVersionResponseMessage()
        msg.firmware_version = b"\x01\x02\x03\x04\x05"
        expected_output = b"\x05\x14\x01\x02\x03\x04\x05"
        stream = io.BytesIO()

        msg.serialize(stream)

        self.assertEquals(expected_output, stream.getvalue())


class SensorUpdateRequestMessageTests(unittest.TestCase):
    def test_sensor_update_request_deserialize_valid(self):
        stream = io.BytesIO(b"\x06\x15\xAA\xBB\xCC\x12\x34\x45")

        msg = SensorUpdateRequestMessage()
        msg.deserialize(stream)

        self.assertEquals(msg.type, UartCommand.SensorUpdateRequest)
        self.assertEquals(msg.instance_index, 0xAA)
        self.assertEquals(msg.property_id, 0xCCBB)
        self.assertEquals(msg.data, b"\x12\x34\x45")

    def test_sensor_update_request_deserialize_invalid_opcode(self):
        stream = io.BytesIO(b"\x06\x16\xAA\xBB\xCC\x12\x34\x45")
        msg = SensorUpdateRequestMessage()

        with self.assertRaises(InvalidOpcode) as _:
            msg.deserialize(stream)

    def test_sensor_update_request_deserialize_invalid_len(self):
        stream = io.BytesIO(b"\x07\x15\xAA\xBB\xCC\x12\x34\x45")
        msg = SensorUpdateRequestMessage()

        with self.assertRaises(InvalidLen) as _:
            msg.deserialize(stream)

    def test_sensor_update_request_serialize_valid(self):
        msg = SensorUpdateRequestMessage()
        msg.instance_index = 0xAA
        msg.property_id = 0xCCBB
        msg.data = b"\x12\x34\x45"

        stream = io.BytesIO()
        msg.serialize(stream)

        expected_output = b"\x06\x15\xAA\xBB\xCC\x12\x34\x45"
        self.assertEquals(expected_output, stream.getvalue())


class AttentionEventMessageTests(unittest.TestCase):
    def test_attention_event_deserialize_valid(self):
        stream = io.BytesIO(b"\x01\x16\x01")

        msg = AttentionEventMessage()
        msg.deserialize(stream)

        self.assertEquals(msg.type, UartCommand.AttentionEvent)
        self.assertEquals(msg.attention, AttentionEvent.On)

    def test_attention_event_deserialize_invalid_opcode(self):
        stream = io.BytesIO(b"\x01\x17\x01")
        msg = AttentionEventMessage()

        with self.assertRaises(InvalidOpcode) as _:
            msg.deserialize(stream)

    def test_attention_event_deserialize_invalid_len_too_short(self):
        stream = io.BytesIO(b"\x00\x16")
        msg = AttentionEventMessage()

        with self.assertRaises(InvalidLen) as _:
            msg.deserialize(stream)

    def test_attention_event_deserialize_invalid_len_too_long(self):
        stream = io.BytesIO(b"\x02\x16\x01\x16")
        msg = AttentionEventMessage()

        with self.assertRaises(InvalidLen) as _:
            msg.deserialize(stream)

    def test_attention_event_serialize_valid(self):
        msg = AttentionEventMessage()
        msg.attention = AttentionEvent.Off
        expected_output = b"\x01\x16\x00"
        stream = io.BytesIO()

        msg.serialize(stream)

        self.assertEquals(expected_output, stream.getvalue())


class SoftResetRequestMessageTests(unittest.TestCase):
    def test_soft_reset_request_deserialize_valid(self):
        stream = io.BytesIO(b"\x00\x17")

        msg = SoftResetRequestMessage()
        msg.deserialize(stream)

        self.assertEquals(msg.type, UartCommand.SoftResetRequest)

    def test_soft_reset_request_deserialize_invalid_opcode(self):
        stream = io.BytesIO(b"\x00\xAB")
        msg = SoftResetRequestMessage()

        with self.assertRaises(InvalidOpcode) as _:
            msg.deserialize(stream)

    def test_soft_reset_request_deserialize_invalid_too_long(self):
        stream = io.BytesIO(b"\x02\x17\xAA\xBB")
        msg = SoftResetRequestMessage()

        with self.assertRaises(InvalidLen) as _:
            msg.deserialize(stream)

    def test_soft_reset_request_serialize_valid(self):
        msg = SoftResetRequestMessage()
        expected_output = b"\x00\x17"
        stream = io.BytesIO()

        msg.serialize(stream)

        self.assertEquals(expected_output, stream.getvalue())


class SoftResetResponseMessageTests(unittest.TestCase):
    def test_soft_reset_response_deserialize_valid(self):
        stream = io.BytesIO(b"\x00\x18")

        msg = SoftResetResponseMessage()
        msg.deserialize(stream)

        self.assertEquals(msg.type, UartCommand.SoftResetResponse)

    def test_soft_reset_response_deserialize_invalid_opcode(self):
        stream = io.BytesIO(b"\x00\xAB")
        msg = SoftResetResponseMessage()

        with self.assertRaises(InvalidOpcode) as _:
            msg.deserialize(stream)

    def test_soft_reset_response_deserialize_invalid_too_long(self):
        stream = io.BytesIO(b"\x02\x18\xAA\xBB")
        msg = SoftResetResponseMessage()

        with self.assertRaises(InvalidLen) as _:
            msg.deserialize(stream)

    def test_soft_reset_response_serialize_valid(self):
        msg = SoftResetResponseMessage()
        expected_output = b"\x00\x18"
        stream = io.BytesIO()

        msg.serialize(stream)

        self.assertEquals(expected_output, stream.getvalue())


class SensorUpdateResponseMessageTests(unittest.TestCase):
    def test_sensor_update_response_deserialize_valid(self):
        stream = io.BytesIO(b"\x00\x19")

        msg = SensorUpdateResponseMessage()
        msg.deserialize(stream)

        self.assertEquals(msg.type, UartCommand.SensorUpdateResponse)

    def test_sensor_update_response_deserialize_invalid_opcode(self):
        stream = io.BytesIO(b"\x00\xAB")
        msg = SensorUpdateResponseMessage()

        with self.assertRaises(InvalidOpcode) as _:
            msg.deserialize(stream)

    def test_sensor_update_response_deserialize_invalid_too_long(self):
        stream = io.BytesIO(b"\x02\x19\xAA\xBB")
        msg = SensorUpdateResponseMessage()

        with self.assertRaises(InvalidLen) as _:
            msg.deserialize(stream)

    def test_sensor_update_response_serialize_valid(self):
        msg = SensorUpdateResponseMessage()
        expected_output = b"\x00\x19"
        stream = io.BytesIO()

        msg.serialize(stream)

        self.assertEquals(expected_output, stream.getvalue())


class DeviceUUIDRequestMessageTests(unittest.TestCase):
    def test_device_uuid_request_deserialize_valid(self):
        stream = io.BytesIO(b"\x00\x1A")

        msg = DeviceUUIDRequestMessage()
        msg.deserialize(stream)

        self.assertEquals(msg.type, UartCommand.DeviceUUIDRequest)

    def test_device_uuid_request_deserialize_invalid_opcode(self):
        stream = io.BytesIO(b"\x00\xAB")
        msg = DeviceUUIDRequestMessage()

        with self.assertRaises(InvalidOpcode) as _:
            msg.deserialize(stream)

    def test_device_uuid_request_deserialize_invalid_too_long(self):
        stream = io.BytesIO(b"\x02\x1A\xAA\xBB")
        msg = DeviceUUIDRequestMessage()

        with self.assertRaises(InvalidLen) as _:
            msg.deserialize(stream)

    def test_device_uuid_request_serialize_valid(self):
        msg = DeviceUUIDRequestMessage()
        expected_output = b"\x00\x1A"
        stream = io.BytesIO()

        msg.serialize(stream)

        self.assertEquals(expected_output, stream.getvalue())


class DeviceUUIDResponseMessageTests(unittest.TestCase):
    def test_device_uuid_response_deserialize_valid(self):
        stream = io.BytesIO(b"\x10\x1B\xAB\xAB\xAB\xAB\xAB\xAB\xAB\xAB\xAB\xAB\xAB\xAB\xAB\xAB\xAB\xAB")

        msg = DeviceUUIDResponseMessage()
        msg.deserialize(stream)

        self.assertEquals(msg.type, UartCommand.DeviceUUIDResponse)
        self.assertEquals(msg.uuid, b"\xAB\xAB\xAB\xAB\xAB\xAB\xAB\xAB\xAB\xAB\xAB\xAB\xAB\xAB\xAB\xAB")

    def test_device_uuid_response_deserialize_invalid_opcode(self):
        stream = io.BytesIO(b"\x10\x1A\xAB\xAB\xAB\xAB\xAB\xAB\xAB\xAB\xAB\xAB\xAB\xAB\xAB\xAB\xAB\xAB")
        msg = DeviceUUIDResponseMessage()

        with self.assertRaises(InvalidOpcode) as _:
            msg.deserialize(stream)

    def test_device_uuid_response_deserialize_invalid_too_short(self):
        stream = io.BytesIO(b"\x02\x1B\xAA\xBB")
        msg = DeviceUUIDResponseMessage()

        with self.assertRaises(InvalidLen) as _:
            msg.deserialize(stream)

    def test_device_uuid_response_deserialize_invalid_len(self):
        stream = io.BytesIO(b"\x10\x1B\xAA\xBB")
        msg = DeviceUUIDResponseMessage()

        with self.assertRaises(InvalidLen) as _:
            msg.deserialize(stream)

    def test_device_uuid_response_deserialize_invalid_too_long(self):
        stream = io.BytesIO(b"\x11\x1B\xAB\xAB\xAB\xAB\xAB\xAB\xAB\xAB\xAB\xAB\xAB\xAB\xAB\xAB\xAB\xAB\xBB")
        msg = DeviceUUIDResponseMessage()

        with self.assertRaises(InvalidLen) as _:
            msg.deserialize(stream)

    def test_device_uuid_response_serialize_valid(self):
        msg = DeviceUUIDResponseMessage()
        msg.uuid = b"\xAB\xAB\xAB\xAB\xAB\xAB\xAB\xAB\xAB\xAB\xAB\xAB\xAB\xAB\xAB\xAB"
        expected_output = b"\x10\x1B\xAB\xAB\xAB\xAB\xAB\xAB\xAB\xAB\xAB\xAB\xAB\xAB\xAB\xAB\xAB\xAB"
        stream = io.BytesIO()

        msg.serialize(stream)

        self.assertEquals(expected_output, stream.getvalue())


class DfuInitRequestMessageTests(unittest.TestCase):
    def test_dfu_init_request_deserialize_valid(self):
        stream = io.BytesIO(b"\x28" + \
                            b"\x80" + \
                            b"\x00\x11\x22\x33" + \
                            b"\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA" + \
                            b"\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA" + \
                            b"\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA" + \
                            b"\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA" + \
                            b"\x03\xAA\xBB\xCC")

        msg = DfuInitRequestMessage()
        msg.deserialize(stream)

        self.assertEquals(msg.type, UartCommand.DfuInitRequest)
        self.assertEquals(msg.firmware_size, 0x33221100)
        self.assertEquals(msg.firmware_sha256,
                          b"\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA" + \
                          b"\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA" + \
                          b"\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA" + \
                          b"\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA")
        self.assertEquals(msg.app_data_length, 0x03)
        self.assertEquals(msg.app_data, b"\xAA\xBB\xCC")

    def test_dfu_init_request_deserialize_invalid_opcode(self):
        stream = io.BytesIO(b"\x0C\x70\x00\x11\x22\x33\x00\x11\x22\x33\x03\xAA\xBB\xCC")
        msg = DfuInitRequestMessage()

        with self.assertRaises(InvalidOpcode) as _:
            msg.deserialize(stream)

    def test_dfu_init_request_deserialize_invalid_len(self):
        stream = io.BytesIO(b"\x0C\x80\x00\x11\x22\x33\x00\x11\x22\x33\x02\xAA\xBB\xCC")
        msg = DfuInitRequestMessage()

        with self.assertRaises(InvalidLen) as _:
            msg.deserialize(stream)

    def test_dfu_init_request_deserialize_invalid_len2(self):
        stream = io.BytesIO(b"\x0B\x80\x00\x11\x22\x33\x00\x11\x22\x33\x03\xAA\xBB\xCC")
        msg = DfuInitRequestMessage()

        with self.assertRaises(InvalidLen) as _:
            msg.deserialize(stream)

    def test_dfu_init_request_serialize_valid(self):
        msg = DfuInitRequestMessage()
        msg.firmware_size = 0x33221100
        msg.firmware_sha256 = b"\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA" + \
                              b"\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA" + \
                              b"\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA" + \
                              b"\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA"
        msg.app_data_length = 0x03
        msg.app_data = b"\xAA\xBB\xCC"

        stream = io.BytesIO()
        msg.serialize(stream)

        expected_output = b"\x28" + \
                          b"\x80" + \
                          b"\x00\x11\x22\x33" + \
                          b"\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA" + \
                          b"\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA" + \
                          b"\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA" + \
                          b"\xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA" + \
                          b"\x03\xAA\xBB\xCC"
        self.assertEquals(expected_output, stream.getvalue())


class DfuInitResponseMessageTests(unittest.TestCase):
    def test_dfu_init_response_deserialize_valid(self):
        stream = io.BytesIO(b"\x01\x81\x01")

        msg = DfuInitResponseMessage()
        msg.deserialize(stream)

        self.assertEquals(msg.type, UartCommand.DfuInitResponse)
        self.assertEquals(msg.status, DFUStatus.DFU_SUCCESS)

    def test_dfu_init_response_deserialize_invalid_opcode(self):
        stream = io.BytesIO(b"\x01\x83\x01")
        msg = DfuInitResponseMessage()

        with self.assertRaises(InvalidOpcode) as _:
            msg.deserialize(stream)

    def test_dfu_init_response_deserialize_invalid_len_too_long(self):
        stream = io.BytesIO(b"\x02\x81\x01\x16")
        msg = DfuInitResponseMessage()

        with self.assertRaises(InvalidLen) as _:
            msg.deserialize(stream)

    def test_dfu_init_response_deserialize_invalid_len_too_short(self):
        stream = io.BytesIO(b"\x00\x81")
        msg = DfuInitResponseMessage()

        with self.assertRaises(InvalidLen) as _:
            msg.deserialize(stream)

    def test_dfu_init_response_serialize_valid(self):
        msg = DfuInitResponseMessage()
        msg.status = DFUStatus.DFU_SUCCESS
        expected_output = b"\x01\x81\x01"
        stream = io.BytesIO()

        msg.serialize(stream)

        self.assertEquals(expected_output, stream.getvalue())


class DfuStateRequestMessageTests(unittest.TestCase):
    def test_dfu_state_request_deserialize_valid(self):
        stream = io.BytesIO(b"\x00\x82")

        msg = DfuStatusRequestMessage()
        msg.deserialize(stream)

        self.assertEquals(msg.type, UartCommand.DfuStatusRequest)

    def test_dfu_state_request_deserialize_invalid_opcode(self):
        stream = io.BytesIO(b"\x00\x17")
        msg = DfuStatusRequestMessage()

        with self.assertRaises(InvalidOpcode) as _:
            msg.deserialize(stream)

    def test_dfu_state_request_deserialize_invalid_len_too_long(self):
        stream = io.BytesIO(b"\x02\x82\x16\x16")
        msg = DfuStatusRequestMessage()

        with self.assertRaises(InvalidLen) as _:
            msg.deserialize(stream)

    def test_dfu_state_request_serialize_valid(self):
        msg = DfuStatusRequestMessage()
        expected_output = b"\x00\x82"
        stream = io.BytesIO()

        msg.serialize(stream)

        self.assertEquals(expected_output, stream.getvalue())


class DfuStateResponseMessageTests(unittest.TestCase):
    def test_dfu_state_response_deserialize_valid(self):
        stream = io.BytesIO(b"\x0D\x83\x01\x12\x34\x56\x78\x12\x34\x56\x78\x12\x34\x56\x78")

        msg = DfuStatusResponseMessage()
        msg.deserialize(stream)

        self.assertEquals(msg.type, UartCommand.DfuStatusResponse)
        self.assertEquals(msg.status, DFUStatus.DFU_SUCCESS)
        self.assertEquals(msg.supported_page_size, 0x78563412)
        self.assertEquals(msg.firmware_offset, 0x78563412)
        self.assertEquals(msg.firmware_crc, 0x78563412)

    def test_dfu_state_response_deserialize_invalid_opcode(self):
        stream = io.BytesIO(b"\x0D\x84\x01\x12\x34\x56\x78\x12\x34\x56\x78\x12\x34\x56\x78")
        msg = DfuStatusResponseMessage()

        with self.assertRaises(InvalidOpcode) as _:
            msg.deserialize(stream)

    def test_dfu_state_response_deserialize_invalid_len_too_long(self):
        stream = io.BytesIO(b"\x0E\x83\x01\x12\x34\x56\x78\x12\x34\x56\x78\x12\x34\x56\x78\x00")
        msg = DfuStatusResponseMessage()

        with self.assertRaises(InvalidLen) as _:
            msg.deserialize(stream)

    def test_dfu_state_response_deserialize_invalid_len_too_short(self):
        stream = io.BytesIO(b"\x0C\x83\x01\x12\x34\x56\x78\x12\x34\x56\x78\x12\x34\x56")
        msg = DfuStatusResponseMessage()

        with self.assertRaises(InvalidLen) as _:
            msg.deserialize(stream)

    def test_dfu_state_response_serialize_valid(self):
        msg = DfuStatusResponseMessage()
        msg.status = DFUStatus.DFU_SUCCESS
        msg.supported_page_size = 0x78563412
        msg.firmware_offset = 0x78563412
        msg.firmware_crc = 0x78563412
        expected_output = b"\x0D\x83\x01\x12\x34\x56\x78\x12\x34\x56\x78\x12\x34\x56\x78"
        stream = io.BytesIO()

        msg.serialize(stream)

        self.assertEquals(expected_output, stream.getvalue())


class DfuPageCreateRequestMessageTests(unittest.TestCase):
    def test_dfu_page_create_request_deserialize_valid(self):
        stream = io.BytesIO(b"\x04\x84\xAA\xBB\xCC\xDD")

        msg = DfuPageCreateRequestMessage()
        msg.deserialize(stream)

        self.assertEquals(msg.type, UartCommand.DfuPageCreateRequest)
        self.assertEquals(msg.requested_page_size, 0xDDCCBBAA)

    def test_dfu_page_create_request_deserialize_invalid_opcode(self):
        stream = io.BytesIO(b"\x04\x85\xAA\xBB\xCC\xDD")
        msg = DfuPageCreateRequestMessage()

        with self.assertRaises(InvalidOpcode) as _:
            msg.deserialize(stream)

    def test_dfu_page_create_request_deserialize_invalid_len_too_long(self):
        stream = io.BytesIO(b"\x05\x84\xAA\xBB\xCC\xDD\xEE")
        msg = DfuPageCreateRequestMessage()

        with self.assertRaises(InvalidLen) as _:
            msg.deserialize(stream)

    def test_dfu_page_create_request_deserialize_invalid_len_too_short(self):
        stream = io.BytesIO(b"\x00\x84")
        msg = DfuPageCreateRequestMessage()

        with self.assertRaises(InvalidLen) as _:
            msg.deserialize(stream)

    def test_dfu_page_create_request_serialize_valid(self):
        msg = DfuPageCreateRequestMessage()
        msg.requested_page_size = 0xDDCCBBAA
        expected_output = b"\x04\x84\xAA\xBB\xCC\xDD"
        stream = io.BytesIO()

        msg.serialize(stream)

        self.assertEquals(expected_output, stream.getvalue())


class DfuPageCreateResponseMessageTests(unittest.TestCase):
    def test_dfu_page_create_response_deserialize_valid(self):
        stream = io.BytesIO(b"\x01\x85\x01")

        msg = DfuPageCreateResponseMessage()
        msg.deserialize(stream)

        self.assertEquals(msg.type, UartCommand.DfuPageCreateResponse)
        self.assertEquals(msg.status, DFUStatus.DFU_SUCCESS)

    def test_dfu_page_create_response_deserialize_invalid_opcode(self):
        stream = io.BytesIO(b"\x01\x83\x01")
        msg = DfuPageCreateResponseMessage()

        with self.assertRaises(InvalidOpcode) as _:
            msg.deserialize(stream)

    def test_dfu_page_create_response_deserialize_invalid_len_too_long(self):
        stream = io.BytesIO(b"\x02\x85\x01\x16")
        msg = DfuPageCreateResponseMessage()

        with self.assertRaises(InvalidLen) as _:
            msg.deserialize(stream)

    def test_dfu_page_create_response_deserialize_invalid_len_too_short(self):
        stream = io.BytesIO(b"\x00\x85")
        msg = DfuPageCreateResponseMessage()

        with self.assertRaises(InvalidLen) as _:
            msg.deserialize(stream)

    def test_dfu_page_create_response_serialize_valid(self):
        msg = DfuPageCreateResponseMessage()
        msg.status = DFUStatus.DFU_SUCCESS
        expected_output = b"\x01\x85\x01"
        stream = io.BytesIO()

        msg.serialize(stream)

        self.assertEquals(expected_output, stream.getvalue())


class DfuWriteDataEventMessageTests(unittest.TestCase):
    def test_dfu_write_data_event_deserialize_valid(self):
        stream = io.BytesIO(b"\x04\x86\x03\xAA\xBB\xCC")

        msg = DfuWriteDataEventMessage()
        msg.deserialize(stream)

        self.assertEquals(msg.type, UartCommand.DfuWriteDataEvent)
        self.assertEquals(msg.data_len, 0x03)
        self.assertEquals(msg.data, b"\xAA\xBB\xCC")

    def test_dfu_write_data_event_deserialize_invalid_opcode(self):
        stream = io.BytesIO(b"\x04\x85\x03\xAA\xBB\xCC")
        msg = DfuWriteDataEventMessage()

        with self.assertRaises(InvalidOpcode) as _:
            msg.deserialize(stream)

    def test_dfu_write_data_event_deserialize_invalid_len(self):
        stream = io.BytesIO(b"\x04\x86\x02\xAA\xBB\xCC")
        msg = DfuWriteDataEventMessage()

        with self.assertRaises(InvalidLen) as _:
            msg.deserialize(stream)

    def test_dfu_write_data_event_deserialize_invalid_len2(self):
        stream = io.BytesIO(b"\x03\x86\x03\xAA\xBB\xCC")
        msg = DfuWriteDataEventMessage()

        with self.assertRaises(InvalidLen) as _:
            msg.deserialize(stream)

    def test_dfu_write_data_event_serialize_valid(self):
        msg = DfuWriteDataEventMessage()
        msg.data_len = 0x03
        msg.data = b"\xAA\xBB\xCC"

        stream = io.BytesIO()
        msg.serialize(stream)

        expected_output = b"\x04\x86\x03\xAA\xBB\xCC"
        self.assertEquals(expected_output, stream.getvalue())


class DfuPageStoreRequestMessageTests(unittest.TestCase):
    def test_dfu_page_store_request_deserialize_valid(self):
        stream = io.BytesIO(b"\x00\x87")

        msg = DfuPageStoreRequestMessage()
        msg.deserialize(stream)

        self.assertEquals(msg.type, UartCommand.DfuPageStoreRequest)

    def test_dfu_page_store_request_deserialize_invalid_opcode(self):
        stream = io.BytesIO(b"\x00\x17")
        msg = DfuPageStoreRequestMessage()

        with self.assertRaises(InvalidOpcode) as _:
            msg.deserialize(stream)

    def test_dfu_page_store_request_deserialize_invalid_len_too_long(self):
        stream = io.BytesIO(b"\x02\x87\x16\x16")
        msg = DfuPageStoreRequestMessage()

        with self.assertRaises(InvalidLen) as _:
            msg.deserialize(stream)

    def test_dfu_page_store_request_serialize_valid(self):
        msg = DfuPageStoreRequestMessage()
        expected_output = b"\x00\x87"
        stream = io.BytesIO()

        msg.serialize(stream)

        self.assertEquals(expected_output, stream.getvalue())


class DfuPageStoreResponseMessageTests(unittest.TestCase):
    def test_dfu_page_store_response_deserialize_valid(self):
        stream = io.BytesIO(b"\x01\x88\x01")

        msg = DfuPageStoreResponseMessage()
        msg.deserialize(stream)

        self.assertEquals(msg.type, UartCommand.DfuPageStoreResponse)
        self.assertEquals(msg.status, DFUStatus.DFU_SUCCESS)

    def test_dfu_page_store_response_deserialize_invalid_opcode(self):
        stream = io.BytesIO(b"\x01\x83\x01")
        msg = DfuPageStoreResponseMessage()

        with self.assertRaises(InvalidOpcode) as _:
            msg.deserialize(stream)

    def test_dfu_page_store_response_deserialize_invalid_len_too_long(self):
        stream = io.BytesIO(b"\x02\x88\x01\x16")
        msg = DfuPageStoreResponseMessage()

        with self.assertRaises(InvalidLen) as _:
            msg.deserialize(stream)

    def test_dfu_page_store_response_deserialize_invalid_len_too_short(self):
        stream = io.BytesIO(b"\x00\x88")
        msg = DfuPageStoreResponseMessage()

        with self.assertRaises(InvalidLen) as _:
            msg.deserialize(stream)

    def test_dfu_page_store_response_serialize_valid(self):
        msg = DfuPageStoreResponseMessage()
        msg.status = DFUStatus.DFU_SUCCESS
        expected_output = b"\x01\x88\x01"
        stream = io.BytesIO()

        msg.serialize(stream)

        self.assertEquals(expected_output, stream.getvalue())
