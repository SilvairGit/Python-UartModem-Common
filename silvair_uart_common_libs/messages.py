from enum import IntEnum

from .message_types import Serializable, ModelDesc, UART_MODEL_ID_LEN, Error, FactoryResetSource, ModemState, \
    AttentionEvent, DFUStatus, DfuStatus, ModelID

UART_CMD_LEN = 1
UART_LENGTH_LEN = 1
UART_PING_DATA_LEN = 1
UART_INSTANCE_INDEX_LEN = 1
UART_SUB_INDEX_LEN = 1
UART_MESH_OPCODE_LEN = 2
UART_FACTORY_RESET_SOURCE_LEN = 1
UART_MODEM_STATE_LEN = 1
UART_ERROR_ID_LEN = 1
UART_PROPERTY_ID_LEN = 2
UART_ATTENTION_EVENT_LEN = 1
UART_UUID_LEN = 16
UART_DFU_FIRMWARE_SIZE_LEN = 4
UART_DFU_FIRMWARE_CRC_LEN = 4
UART_DFU_APP_DATA_LENGTH_LEN = 1
UART_DFU_STATUS_LEN = 1
UART_DFU_SUPPORTED_PAGE_SIZE_LEN = 4
UART_DFU_FIRMWARE_OFFSET_LEN = 4
UART_REQUESTED_PAGE_SIZE_LEN = 4
UART_DFU_DATA_LENGTH_LEN = 1
UART_DFU_FIRMWARE_SHA256_LEN = 32
UART_DFU_PRE_VALIDATION_STATUS_LEN = 1
UART_COMPANY_ID_LEN = 2
UART_TEST_ID_LEN = 1


class UartCommand(IntEnum):
    """
    Enumerator mapping UART command opcode to its name.
    """
    PingRequest = 0x01
    PongResponse = 0x02
    InitDeviceEvent = 0x03
    CreateInstancesRequest = 0x04
    CreateInstancesResponse = 0x05
    InitNodeEvent = 0x06
    MeshMessageRequest = 0x07
    OpcodeError = 0x08
    StartNodeRequest = 0x09
    StartNodeResponse = 0x0B
    FactoryResetRequest = 0x0C
    FactoryResetResponse = 0x0D
    FactoryResetEvent = 0x0E
    MeshMessageResponse = 0x0F
    CurrentStateRequest = 0x10
    CurrentStateResponse = 0x11
    Error = 0x12
    FirmwareVersionRequest = 0x13
    FirmwareVersionResponse = 0x14
    SensorUpdateRequest = 0x15
    AttentionEvent = 0x16
    SoftResetRequest = 0x17
    SoftResetResponse = 0x18
    SensorUpdateResponse = 0x19
    DeviceUUIDRequest = 0x1A
    DeviceUUIDResponse = 0x1B
    StartTestRequest = 0x20
    StartTestResponse = 0x21
    DfuInitRequest = 0x80
    DfuInitResponse = 0x81
    DfuStatusRequest = 0x82
    DfuStatusResponse = 0x83
    DfuPageCreateRequest = 0x84
    DfuPageCreateResponse = 0x85
    DfuWriteDataEvent = 0x86
    DfuPageStoreRequest = 0x87
    DfuPageStoreResponse = 0x88
    DfuStateRequest = 0x89
    DfuStateResponse = 0x8A
    DfuCancelRequest = 0x8B
    DfuCancelResponse = 0x8C
    Generic = 0xFF


class InvalidOpcode(Exception):
    """
    Invalid opcode exception
    """
    pass


class InvalidLen(Exception):
    """
    Invalid len exception
    """
    pass


class GenericMessage(Serializable):
    """
    Class representing Generic uart message.
    Class fields are adequate to message parameters, described in UART specification.
    """

    def __init__(self):
        """
        Initialize message and all its fields
        """
        self.type = UartCommand.Generic

    def __str__(self):
        """
        Generate string representing message
        """
        return self.type.name

    def __eq__(self, other):
        """
        Compare two messages. Returns true if all fields are identical.

        :param other:     GenericMessage or derivative, other message to be compared with self
        :return:          True if identical, False otherwise
        """
        return self.type == other.type

    def get_length(self):
        """
        Get serialized message len. This should be used ONLY when all fields are filled

        :return:    int, serialized message length
        """
        return 0

    def serialize_common_part(self, stream):
        """
        Serialize common message part into bytes

        :param stream:  io.BytesIO stream, destination
        :return:        None
        """
        length = self.get_length()

        stream.write(length.to_bytes(UART_LENGTH_LEN, byteorder='little', signed=False))
        stream.write(self.type.to_bytes(UART_CMD_LEN, byteorder='little', signed=False))

    def deserialize_common_part(self, stream):
        """
        Deserialize message, fill fields consuming stream

        :param stream:  io.BytesIO stream, source stream to read from
        :return:        int, message length
        """
        length = int.from_bytes(stream.read(UART_LENGTH_LEN), byteorder='little')
        opcode = int.from_bytes(stream.read(UART_CMD_LEN), byteorder='little')

        if opcode != self.type:
            raise InvalidOpcode

        return length

    def serialize(self, stream):
        """
        Serialize message into bytes. Overload this in derivative class

        :param stream:  io.BytesIO stream, destination
        :return:        None
        """
        assert False, "Not implemented method cannot be used"

    def deserialize(self, stream):
        """
        Deserialize message, fill fields consuming stream. Overload this in derivative class

        :param stream:  io.BytesIO stream, source stream to read from
        :return:        None
        """
        assert False, "Not implemented method cannot be used"


class PingRequestMessage(GenericMessage):
    """
    Class representing PingRequest uart message.
    Class fields are adequate to message parameters, described in UART specification.
    """

    def __init__(self):
        """
        Initialize message and all its fields
        """
        super().__init__()
        self.type = UartCommand.PingRequest
        self.data = bytes()

    def __eq__(self, other):
        """
        Compare two messages. Returns true if all fields are identical.

        :param other:     GenericMessage or derivative, other message to be compared with self
        :return:          True if identical, False otherwise
        """
        return super().__eq__(other) and self.data == other.data

    def __str__(self):
        """
        Generate string representing message
        """
        return super().__str__() + ", data= " + self.data.hex()

    def get_length(self):
        """
        Get serialized message len. This should be used ONLY when all fields are filled

        :return:    int, serialized message length
        """
        return len(self.data)

    def serialize(self, stream):
        """
        Serialize message into bytes

        :param stream:  io.BytesIO stream, destination
        :return:        None
        """
        self.serialize_common_part(stream)
        stream.write(self.data)

    def deserialize(self, stream):
        """
        Deserialize message, fill fields consuming stream

        :param stream:  io.BytesIO stream, source stream to read from
        :return:        None
        """
        length = self.deserialize_common_part(stream)
        self.data = stream.read(length)

        if length != len(self.data):
            raise InvalidLen


class PongResponseMessage(GenericMessage):
    """
    Class representing PongResponse uart message.
    Class fields are adequate to message parameters, described in UART specification.
    """

    def __init__(self):
        """
        Initialize message and all its fields
        """
        super().__init__()
        self.type = UartCommand.PongResponse
        self.data = bytes()

    def __eq__(self, other):
        """
        Compare two messages. Returns true if all fields are identical.

        :param other:     GenericMessage or derivative, other message to be compared with self
        :return:          True if identical, False otherwise
        """
        return super().__eq__(other) and self.data == other.data

    def __str__(self):
        """
        Generate string representing message
        """
        return super().__str__() + ", data= " + self.data.hex()

    def get_length(self):
        """
        Get serialized message len. This should be used ONLY when all fields are filled

        :return:    int, serialized message length
        """
        return len(self.data)

    def serialize(self, stream):
        """
        Serialize message into bytes

        :param stream:  io.BytesIO stream, destination
        :return:        None
        """
        self.serialize_common_part(stream)
        stream.write(self.data)

    def deserialize(self, stream):
        """
        Deserialize message, fill fields consuming stream

        :param stream:  io.BytesIO stream, source stream to read from
        :return:        None
        """
        length = self.deserialize_common_part(stream)
        self.data = stream.read(length)

        if length != len(self.data):
            raise InvalidLen


class InitDeviceEventMessage(GenericMessage):
    """
    Class representing InitDeviceEvent uart message.
    Class fields are adequate to message parameters, described in UART specification.
    """

    def __init__(self):
        """
        Initialize message and all its fields
        """
        super().__init__()
        self.type = UartCommand.InitDeviceEvent
        self.model_ids = list()

    def __eq__(self, other):
        """
        Compare two messages. Returns true if all fields are identical.

        :param other:     GenericMessage or derivative, other message to be compared with self
        :return:          True if identical, False otherwise
        """
        return super().__eq__(other) and self.model_ids == other.model_ids

    def __str__(self):
        """
        Generate string representing message
        """
        output = super().__str__() + ", model_ids= "
        for model_id in self.model_ids:
            output += "0x{:04x} {:s}, ".format(model_id, model_id.name)

        return output

    def get_length(self):
        """
        Get serialized message len. This should be used ONLY when all fields are filled

        :return:    int, serialized message length
        """
        length = UART_MODEL_ID_LEN * len(self.model_ids)
        return length

    def serialize(self, stream):
        """
        Serialize message into bytes

        :param stream:  io.BytesIO stream, destination
        :return:        None
        """
        self.serialize_common_part(stream)
        for model_id in self.model_ids:
            stream.write(model_id.to_bytes(UART_MODEL_ID_LEN, byteorder='little', signed=False))

    def deserialize(self, stream):
        """
        Deserialize message, fill fields consuming stream

        :param stream:  io.BytesIO stream, source stream to read from
        :return:        None
        """
        length = self.deserialize_common_part(stream)
        while length >= UART_MODEL_ID_LEN:
            model_id = ModelID.from_bytes(stream.read(UART_MODEL_ID_LEN), byteorder='little')
            length -= UART_MODEL_ID_LEN
            self.model_ids.append(model_id)

        if length != 0:
            raise InvalidLen


class CreateInstancesRequestMessage(GenericMessage):
    """
    Class representing CreateInstancesRequest uart message.
    Class fields are adequate to message parameters, described in UART specification.
    """

    def __init__(self):
        """
        Initialize message and all its fields
        """
        super().__init__()
        self.type = UartCommand.CreateInstancesRequest
        self.model_descs = list()

    def __eq__(self, other):
        """
        Compare two messages. Returns true if all fields are identical.

        :param other:     GenericMessage or derivative, other message to be compared with self
        :return:          True if identical, False otherwise
        """
        return super().__eq__(other) and self.model_descs == other.model_descs

    def __str__(self):
        """
        Generate string representing message
        """
        output = super().__str__() + ", model_ids= "
        for model_desc in self.model_descs:
            output += "0x{:04x} {:s}, ".format(model_desc.model_id, model_desc.model_id.name)

        return output

    def get_length(self):
        """
        Get serialized message len. This should be used ONLY when all fields are filled

        :return:    int, serialized message length
        """
        length = 0
        for model_desc in self.model_descs:
            length += model_desc.get_length()
        return length

    def serialize(self, stream):
        """
        Serialize message into bytes

        :param stream:  io.BytesIO stream, destination
        :return:        None
        """
        self.serialize_common_part(stream)
        for model_desc in self.model_descs:
            model_desc.serialize(stream)

    def deserialize(self, stream):
        """
        Deserialize message, fill fields consuming stream

        :param stream:  io.BytesIO stream, source stream to read from
        :return:        None
        """
        length = self.deserialize_common_part(stream)
        while length >= UART_MODEL_ID_LEN:
            model_desc = ModelDesc()
            model_desc.deserialize(stream)
            length -= model_desc.get_length()
            self.model_descs.append(model_desc)

        if length != 0:
            raise InvalidLen


class CreateInstancesResponseMessage(GenericMessage):
    """
    Class representing CreateInstancesResponse uart message.
    Class fields are adequate to message parameters, described in UART specification.
    """

    def __init__(self):
        """
        Initialize message and all its fields
        """
        super().__init__()
        self.type = UartCommand.CreateInstancesResponse
        self.model_ids = list()

    def __eq__(self, other):
        """
        Compare two messages. Returns true if all fields are identical.

        :param other:     GenericMessage or derivative, other message to be compared with self
        :return:          True if identical, False otherwise
        """
        return super().__eq__(other) and self.model_ids == other.model_ids

    def __str__(self):
        """
        Generate string representing message
        """
        output = super().__str__() + ", model_ids= "
        for model_id in self.model_ids:
            output += "0x{:04x} {:s}, ".format(model_id, model_id.name)

        return output

    def get_length(self):
        """
        Get serialized message len. This should be used ONLY when all fields are filled

        :return:    int, serialized message length
        """
        length = UART_MODEL_ID_LEN * len(self.model_ids)
        return length

    def serialize(self, stream):
        """
        Serialize message into bytes

        :param stream:  io.BytesIO stream, destination
        :return:        None
        """
        self.serialize_common_part(stream)
        for model_id in self.model_ids:
            stream.write(model_id.to_bytes(UART_MODEL_ID_LEN, byteorder='little', signed=False))

    def deserialize(self, stream):
        """
        Deserialize message, fill fields consuming stream

        :param stream:  io.BytesIO stream, source stream to read from
        :return:        None
        """
        length = self.deserialize_common_part(stream)
        while length >= UART_MODEL_ID_LEN:
            model_id = ModelID.from_bytes(stream.read(UART_MODEL_ID_LEN), byteorder='little')
            length -= UART_MODEL_ID_LEN
            self.model_ids.append(model_id)

        if length != 0:
            raise InvalidLen


class InitNodeEventMessage(GenericMessage):
    """
    Class representing InitNodeEvent uart message.
    Class fields are adequate to message parameters, described in UART specification.
    """

    def __init__(self):
        """
        Initialize message and all its fields
        """
        super().__init__()
        self.type = UartCommand.InitNodeEvent
        self.model_ids = list()

    def __eq__(self, other):
        """
        Compare two messages. Returns true if all fields are identical.

        :param other:     GenericMessage or derivative, other message to be compared with self
        :return:          True if identical, False otherwise
        """
        return super().__eq__(other) and self.model_ids == other.model_ids

    def __str__(self):
        """
        Generate string representing message
        """
        output = super().__str__() + ", model_ids= "
        for model_id in self.model_ids:
            output += "0x{:04x} {:s}, ".format(model_id, model_id.name)

        return output

    def get_length(self):
        """
        Get serialized message len. This should be used ONLY when all fields are filled

        :return:    int, serialized message length
        """
        length = UART_MODEL_ID_LEN * len(self.model_ids)
        return length

    def serialize(self, stream):
        """
        Serialize message into bytes

        :param stream:  io.BytesIO stream, destination
        :return:        None
        """
        self.serialize_common_part(stream)
        for model_id in self.model_ids:
            stream.write(model_id.to_bytes(UART_MODEL_ID_LEN, byteorder='little', signed=False))

    def deserialize(self, stream):
        """
        Deserialize message, fill fields consuming stream

        :param stream:  io.BytesIO stream, source stream to read from
        :return:        None
        """
        length = self.deserialize_common_part(stream)
        while length >= UART_MODEL_ID_LEN:
            model_id = ModelID.from_bytes(stream.read(UART_MODEL_ID_LEN), byteorder='little')
            length -= UART_MODEL_ID_LEN
            self.model_ids.append(model_id)

        if length != 0:
            raise InvalidLen


class MeshMessageRequestMessage(GenericMessage):
    """
    Class representing MeshMessageRequest uart message.
    Class fields are adequate to message parameters, described in UART specification.
    """

    def __init__(self):
        """
        Initialize message and all its fields
        """
        super().__init__()
        self.type = UartCommand.MeshMessageRequest
        self.instance_index = 0
        self.sub_index = 0
        self.mesh_opcode = 0
        self.mesh_command = bytes()

    def __eq__(self, other):
        """
        Compare two messages. Returns true if all fields are identical.

        :param other:     GenericMessage or derivative, other message to be compared with self
        :return:          True if identical, False otherwise
        """
        return super().__eq__(other) and \
               self.instance_index == other.instance_index and \
               self.sub_index == other.sub_index and \
               self.mesh_opcode == other.mesh_opcode and \
               self.mesh_command == other.mesh_command

    def __str__(self):
        """
        Generate string representing message
        """
        return super().__str__() + ", instance_index=" + str(self.instance_index) \
               + ", sub_index=" + str(self.sub_index) \
               + ", mesh_opcode=" + str(self.mesh_opcode) \
               + ", mesh_command=" + self.mesh_command.hex()

    def get_length(self):
        """
        Get serialized message len. This should be used ONLY when all fields are filled

        :return:    int, serialized message length
        """
        return UART_INSTANCE_INDEX_LEN + \
               UART_SUB_INDEX_LEN + \
               UART_MESH_OPCODE_LEN + \
               len(self.mesh_command)

    def serialize(self, stream):
        """
        Serialize message into bytes

        :param stream:  io.BytesIO stream, destination
        :return:        None
        """
        self.serialize_common_part(stream)
        stream.write(self.instance_index.to_bytes(UART_INSTANCE_INDEX_LEN, byteorder='little', signed=False))
        stream.write(self.sub_index.to_bytes(UART_SUB_INDEX_LEN, byteorder='little', signed=False))
        stream.write(self.mesh_opcode.to_bytes(UART_MESH_OPCODE_LEN, byteorder='little', signed=False))
        stream.write(self.mesh_command)

    def deserialize(self, stream):
        """
        Deserialize message, fill fields consuming stream

        :param stream:  io.BytesIO stream, source stream to read from
        :return:        None
        """
        length = self.deserialize_common_part(stream)
        self.instance_index = int.from_bytes(stream.read(UART_INSTANCE_INDEX_LEN), byteorder='little')
        self.sub_index = int.from_bytes(stream.read(UART_SUB_INDEX_LEN), byteorder='little')
        self.mesh_opcode = int.from_bytes(stream.read(UART_MESH_OPCODE_LEN), byteorder='little')

        length -= UART_INSTANCE_INDEX_LEN + UART_SUB_INDEX_LEN + UART_MESH_OPCODE_LEN

        self.mesh_command = stream.read(length)

        if length != len(self.mesh_command):
            raise InvalidLen


class StartNodeRequestMessage(GenericMessage):
    """
    Class representing StartNodeRequest uart message.
    Class fields are adequate to message parameters, described in UART specification.
    """

    def __init__(self):
        """
        Initialize message and all its fields
        """
        super().__init__()
        self.type = UartCommand.StartNodeRequest

    def serialize(self, stream):
        """
        Serialize message into bytes

        :param stream:  io.BytesIO stream, destination
        :return:        None
        """
        self.serialize_common_part(stream)

    def deserialize(self, stream):
        """
        Deserialize message, fill fields consuming stream

        :param stream:  io.BytesIO stream, source stream to read from
        :return:        None
        """
        length = self.deserialize_common_part(stream)

        if length != 0:
            raise InvalidLen


class StartNodeResponseMessage(GenericMessage):
    """
    Class representing StartNodeResponse uart message.
    Class fields are adequate to message parameters, described in UART specification.
    """

    def __init__(self):
        """
        Initialize message and all its fields
        """
        super().__init__()
        self.type = UartCommand.StartNodeResponse

    def serialize(self, stream):
        """
        Serialize message into bytes

        :param stream:  io.BytesIO stream, destination
        :return:        None
        """
        self.serialize_common_part(stream)

    def deserialize(self, stream):
        """
        Deserialize message, fill fields consuming stream

        :param stream:  io.BytesIO stream, source stream to read from
        :return:        None
        """
        length = self.deserialize_common_part(stream)

        if length != 0:
            raise InvalidLen


class FactoryResetRequestMessage(GenericMessage):
    """
    Class representing FactoryResetRequest uart message.
    Class fields are adequate to message parameters, described in UART specification.
    """

    def __init__(self):
        """
        Initialize message and all its fields
        """
        super().__init__()
        self.type = UartCommand.FactoryResetRequest

    def serialize(self, stream):
        """
        Serialize message into bytes

        :param stream:  io.BytesIO stream, destination
        :return:        None
        """
        self.serialize_common_part(stream)

    def deserialize(self, stream):
        """
        Deserialize message, fill fields consuming stream

        :param stream:  io.BytesIO stream, source stream to read from
        :return:        None
        """
        length = self.deserialize_common_part(stream)

        if length != 0:
            raise InvalidLen


class FactoryResetResponseMessage(GenericMessage):
    """
    Class representing FactoryResetResponse uart message.
    Class fields are adequate to message parameters, described in UART specification.
    """

    def __init__(self):
        """
        Initialize message and all its fields
        """
        super().__init__()
        self.type = UartCommand.FactoryResetResponse

    def serialize(self, stream):
        """
        Serialize message into bytes

        :param stream:  io.BytesIO stream, destination
        :return:        None
        """
        self.serialize_common_part(stream)

    def deserialize(self, stream):
        """
        Deserialize message, fill fields consuming stream

        :param stream:  io.BytesIO stream, source stream to read from
        :return:        None
        """
        length = self.deserialize_common_part(stream)

        if length != 0:
            raise InvalidLen


class FactoryResetEventMessage(GenericMessage):
    """
    Class representing FactoryResetEvent uart message.
    Class fields are adequate to message parameters, described in UART specification.
    """

    def __init__(self):
        """
        Initialize message and all its fields
        """
        super().__init__()
        self.type = UartCommand.FactoryResetEvent

    def serialize(self, stream):
        """
        Serialize message into bytes

        :param stream:  io.BytesIO stream, destination
        :return:        None
        """
        self.serialize_common_part(stream)

    def deserialize(self, stream):
        """
        Deserialize message, fill fields consuming stream

        :param stream:  io.BytesIO stream, source stream to read from
        :return:        None
        """
        length = self.deserialize_common_part(stream)

        if length != 0:
            raise InvalidLen


class MeshMessageResponseMessage(GenericMessage):
    """
    Class representing MeshMessageResponse uart message.
    Class fields are adequate to message parameters, described in UART specification.
    """

    def __init__(self):
        """
        Initialize message and all its fields
        """
        super().__init__()
        self.type = UartCommand.MeshMessageResponse
        self.instance_index = int()
        self.sub_index = int()

    def __eq__(self, other):
        """
        Compare two messages. Returns true if all fields are identical.

        :param other:     GenericMessage or derivative, other message to be compared with self
        :return:          True if identical, False otherwise
        """
        return super().__eq__(other) and \
               self.instance_index == other.instance_index and \
               self.sub_index == other.sub_index

    def __str__(self):
        """
        Generate string representing message
        """
        return super().__str__() + ", instance_index=" + str(self.instance_index) \
               + ", sub_index=" + str(self.sub_index)

    def get_length(self):
        """
        Get serialized message len. This should be used ONLY when all fields are filled

        :return:    int, serialized message length
        """
        return UART_INSTANCE_INDEX_LEN + UART_SUB_INDEX_LEN

    def serialize(self, stream):
        """
        Serialize message into bytes

        :param stream:  io.BytesIO stream, destination
        :return:        None
        """
        self.serialize_common_part(stream)
        stream.write(self.instance_index.to_bytes(UART_INSTANCE_INDEX_LEN, byteorder='little', signed=False))
        stream.write(self.sub_index.to_bytes(UART_SUB_INDEX_LEN, byteorder='little', signed=False))

    def deserialize(self, stream):
        """
        Deserialize message, fill fields consuming stream

        :param stream:  io.BytesIO stream, source stream to read from
        :return:        None
        """
        length = self.deserialize_common_part(stream)
        self.instance_index = int.from_bytes(stream.read(UART_INSTANCE_INDEX_LEN), byteorder='little')
        self.sub_index = int.from_bytes(stream.read(UART_SUB_INDEX_LEN), byteorder='little')

        if length - UART_INSTANCE_INDEX_LEN - UART_SUB_INDEX_LEN != 0:
            raise InvalidLen


class CurrentStateRequestMessage(GenericMessage):
    """
    Class representing CurrentStateRequest uart message.
    Class fields are adequate to message parameters, described in UART specification.
    """

    def __init__(self):
        """
        Initialize message and all its fields
        """
        super().__init__()
        self.type = UartCommand.CurrentStateRequest

    def serialize(self, stream):
        """
        Serialize message into bytes

        :param stream:  io.BytesIO stream, destination
        :return:        None
        """
        self.serialize_common_part(stream)

    def deserialize(self, stream):
        """
        Deserialize message, fill fields consuming stream

        :param stream:  io.BytesIO stream, source stream to read from
        :return:        None
        """
        length = self.deserialize_common_part(stream)

        if length != 0:
            raise InvalidLen


class CurrentStateResponseMessage(GenericMessage):
    """
    Class representing CurrentStateResponse uart message.
    Class fields are adequate to message parameters, described in UART specification.
    """

    def __init__(self):
        """
        Initialize message and all its fields
        """
        super().__init__()
        self.type = UartCommand.CurrentStateResponse
        self.state = ModemState(ModemState.Unknown)

    def __eq__(self, other):
        """
        Compare two messages. Returns true if all fields are identical.

        :param other:     GenericMessage or derivative, other message to be compared with self
        :return:          True if identical, False otherwise
        """
        return super().__eq__(other) and self.state == other.state

    def __str__(self):
        """
        Generate string representing message
        """
        return super().__str__() + ", state=" + self.state.name

    def get_length(self):
        """
        Get serialized message len. This should be used ONLY when all fields are filled

        :return:    int, serialized message length
        """
        return UART_MODEM_STATE_LEN

    def serialize(self, stream):
        """
        Serialize message into bytes

        :param stream:  io.BytesIO stream, destination
        :return:        None
        """
        self.serialize_common_part(stream)
        stream.write(self.state.to_bytes(UART_MODEM_STATE_LEN, byteorder='little', signed=False))

    def deserialize(self, stream):
        """
        Deserialize message, fill fields consuming stream

        :param stream:  io.BytesIO stream, source stream to read from
        :return:        None
        """
        length = self.deserialize_common_part(stream)
        self.state = ModemState.from_bytes(stream.read(UART_MODEM_STATE_LEN), byteorder='little')

        if length - UART_MODEM_STATE_LEN != 0:
            raise InvalidLen


class ErrorMessage(GenericMessage):
    """
    Class representing Error uart message.
    Class fields are adequate to message parameters, described in UART specification.
    """

    def __init__(self):
        """
        Initialize message and all its fields
        """
        super().__init__()
        self.type = UartCommand.Error
        self.error = Error(Error.InvalidCRC)

    def __eq__(self, other):
        """
        Compare two messages. Returns true if all fields are identical.

        :param other:     GenericMessage or derivative, other message to be compared with self
        :return:          True if identical, False otherwise
        """
        return super().__eq__(other) and self.error == other.error

    def __str__(self):
        """
        Generate string representing message
        """
        return super().__str__() + ", error=" + self.error.name

    def get_length(self):
        """
        Get serialized message len. This should be used ONLY when all fields are filled

        :return:    int, serialized message length
        """
        return UART_ERROR_ID_LEN

    def serialize(self, stream):
        """
        Serialize message into bytes

        :param stream:  io.BytesIO stream, destination
        :return:        None
        """
        self.serialize_common_part(stream)
        stream.write(self.error.to_bytes(UART_ERROR_ID_LEN, byteorder='little', signed=False))

    def deserialize(self, stream):
        """
        Deserialize message, fill fields consuming stream

        :param stream:  io.BytesIO stream, source stream to read from
        :return:        None
        """
        length = self.deserialize_common_part(stream)
        self.error = Error.from_bytes(stream.read(UART_ERROR_ID_LEN), byteorder='little')

        if length - UART_ERROR_ID_LEN != 0:
            raise InvalidLen


class FirmwareVersionRequestMessage(GenericMessage):
    """
    Class representing FirmwareVersionRequest uart message.
    Class fields are adequate to message parameters, described in UART specification.
    """

    def __init__(self):
        """
        Initialize message and all its fields
        """
        super().__init__()
        self.type = UartCommand.FirmwareVersionRequest

    def serialize(self, stream):
        """
        Serialize message into bytes

        :param stream:  io.BytesIO stream, destination
        :return:        None
        """
        self.serialize_common_part(stream)

    def deserialize(self, stream):
        """
        Deserialize message, fill fields consuming stream

        :param stream:  io.BytesIO stream, source stream to read from
        :return:        None
        """
        length = self.deserialize_common_part(stream)

        if length != 0:
            raise InvalidLen


class FirmwareVersionResponseMessage(GenericMessage):
    """
    Class representing FirmwareVersionResponse uart message.
    Class fields are adequate to message parameters, described in UART specification.
    """

    def __init__(self):
        """
        Initialize message and all its fields
        """
        super().__init__()
        self.type = UartCommand.FirmwareVersionResponse
        self.firmware_version = bytes()

    def __eq__(self, other):
        """
        Compare two messages. Returns true if all fields are identical.

        :param other:     GenericMessage or derivative, other message to be compared with self
        :return:          True if identical, False otherwise
        """
        return super().__eq__(other) and self.firmware_version == other.firmware_version

    def __str__(self):
        """
        Generate string representing message
        """
        return super().__str__() + ", firmware_version=" + self.firmware_version.hex()

    def get_length(self):
        """
        Get serialized message len. This should be used ONLY when all fields are filled

        :return:    int, serialized message length
        """
        return len(self.firmware_version)

    def serialize(self, stream):
        """
        Serialize message into bytes

        :param stream:  io.BytesIO stream, destination
        :return:        None
        """
        self.serialize_common_part(stream)
        stream.write(self.firmware_version)

    def deserialize(self, stream):
        """
        Deserialize message, fill fields consuming stream

        :param stream:  io.BytesIO stream, source stream to read from
        :return:        None
        """
        length = self.deserialize_common_part(stream)

        if length == 0:
            raise InvalidLen

        self.firmware_version = stream.read(length)


class SensorUpdateRequestMessage(GenericMessage):
    """
    Class representing SensorUpdateRequest uart message.
    Class fields are adequate to message parameters, described in UART specification.
    """

    def __init__(self):
        """
        Initialize message and all its fields
        """
        super().__init__()
        self.type = UartCommand.SensorUpdateRequest
        self.instance_index = int()
        self.property_id = int()
        self.data = bytes()

    def __eq__(self, other):
        """
        Compare two messages. Returns true if all fields are identical.

        :param other:     GenericMessage or derivative, other message to be compared with self
        :return:          True if identical, False otherwise
        """
        return super().__eq__(other) and \
               self.instance_index == other.instance_index and \
               self.property_id == other.property_id and \
               self.data == other.data

    def __str__(self):
        """
        Generate string representing message
        """
        return super().__str__() + ", instance_index=" + str(self.instance_index) \
               + ", property_id=" + str(self.property_id) \
               + ", data=" + self.data.hex()

    def get_length(self):
        """
        Get serialized message len. This should be used ONLY when all fields are filled

        :return:    int, serialized message length
        """
        return UART_INSTANCE_INDEX_LEN + UART_PROPERTY_ID_LEN + len(self.data)

    def serialize(self, stream):
        """
        Serialize message into bytes

        :param stream:  io.BytesIO stream, destination
        :return:        None
        """
        self.serialize_common_part(stream)
        stream.write(self.instance_index.to_bytes(UART_INSTANCE_INDEX_LEN, byteorder='little', signed=False))
        stream.write(self.property_id.to_bytes(UART_PROPERTY_ID_LEN, byteorder='little', signed=False))
        stream.write(self.data)

    def deserialize(self, stream):
        """
        Deserialize message, fill fields consuming stream

        :param stream:  io.BytesIO stream, source stream to read from
        :return:        None
        """
        length = self.deserialize_common_part(stream)
        self.instance_index = int.from_bytes(stream.read(UART_INSTANCE_INDEX_LEN), byteorder='little')
        self.property_id = int.from_bytes(stream.read(UART_PROPERTY_ID_LEN), byteorder='little')

        length -= UART_INSTANCE_INDEX_LEN + UART_PROPERTY_ID_LEN

        self.data = stream.read(length)

        if length != len(self.data):
            raise InvalidLen


class AttentionEventMessage(GenericMessage):
    """
    Class representing AttentionEvent uart message.
    Class fields are adequate to message parameters, described in UART specification.
    """

    def __init__(self):
        """
        Initialize message and all its fields
        """
        super().__init__()
        self.type = UartCommand.AttentionEvent
        self.attention = AttentionEvent(AttentionEvent.Off)

    def __eq__(self, other):
        """
        Compare two messages. Returns true if all fields are identical.

        :param other:     GenericMessage or derivative, other message to be compared with self
        :return:          True if identical, False otherwise
        """
        return super().__eq__(other) and self.attention == other.attention

    def __str__(self):
        """
        Generate string representing message
        """
        return super().__str__() + ", attention=" + self.attention.name

    def get_length(self):
        """
        Get serialized message len. This should be used ONLY when all fields are filled

        :return:    int, serialized message length
        """
        return UART_ATTENTION_EVENT_LEN

    def serialize(self, stream):
        """
        Serialize message into bytes

        :param stream:  io.BytesIO stream, destination
        :return:        None
        """
        self.serialize_common_part(stream)
        stream.write(self.attention.to_bytes(UART_ATTENTION_EVENT_LEN, byteorder='little', signed=False))

    def deserialize(self, stream):
        """
        Deserialize message, fill fields consuming stream

        :param stream:  io.BytesIO stream, source stream to read from
        :return:        None
        """
        length = self.deserialize_common_part(stream)
        self.attention = AttentionEvent.from_bytes(stream.read(UART_ATTENTION_EVENT_LEN), byteorder='little')

        if length - UART_ATTENTION_EVENT_LEN != 0:
            raise InvalidLen


class SoftResetRequestMessage(GenericMessage):
    """
    Class representing SoftResetRequest uart message.
    Class fields are adequate to message parameters, described in UART specification.
    """

    def __init__(self):
        """
        Initialize message and all its fields
        """
        super().__init__()
        self.type = UartCommand.SoftResetRequest

    def serialize(self, stream):
        """
        Serialize message into bytes

        :param stream:  io.BytesIO stream, destination
        :return:        None
        """
        self.serialize_common_part(stream)

    def deserialize(self, stream):
        """
        Deserialize message, fill fields consuming stream

        :param stream:  io.BytesIO stream, source stream to read from
        :return:        None
        """
        length = self.deserialize_common_part(stream)

        if length != 0:
            raise InvalidLen


class SoftResetResponseMessage(GenericMessage):
    """
    Class representing SoftResetResponse uart message.
    Class fields are adequate to message parameters, described in UART specification.
    """

    def __init__(self):
        """
        Initialize message and all its fields
        """
        super().__init__()
        self.type = UartCommand.SoftResetResponse

    def serialize(self, stream):
        """
        Serialize message into bytes

        :param stream:  io.BytesIO stream, destination
        :return:        None
        """
        self.serialize_common_part(stream)

    def deserialize(self, stream):
        """
        Deserialize message, fill fields consuming stream

        :param stream:  io.BytesIO stream, source stream to read from
        :return:        None
        """
        length = self.deserialize_common_part(stream)

        if length != 0:
            raise InvalidLen


class SensorUpdateResponseMessage(GenericMessage):
    """
    Class representing SensorUpdateResponse uart message.
    Class fields are adequate to message parameters, described in UART specification.
    """

    def __init__(self):
        """
        Initialize message and all its fields
        """
        super().__init__()
        self.type = UartCommand.SensorUpdateResponse

    def serialize(self, stream):
        """
        Serialize message into bytes

        :param stream:  io.BytesIO stream, destination
        :return:        None
        """
        self.serialize_common_part(stream)

    def deserialize(self, stream):
        """
        Deserialize message, fill fields consuming stream

        :param stream:  io.BytesIO stream, source stream to read from
        :return:        None
        """
        length = self.deserialize_common_part(stream)

        if length != 0:
            raise InvalidLen


class DeviceUUIDRequestMessage(GenericMessage):
    """
    Class representing DeviceUUIDRequest uart message.
    Class fields are adequate to message parameters, described in UART specification.
    """

    def __init__(self):
        """
        Initialize message and all its fields
        """
        super().__init__()
        self.type = UartCommand.DeviceUUIDRequest

    def serialize(self, stream):
        """
        Serialize message into bytes

        :param stream:  io.BytesIO stream, destination
        :return:        None
        """
        self.serialize_common_part(stream)

    def deserialize(self, stream):
        """
        Deserialize message, fill fields consuming stream

        :param stream:  io.BytesIO stream, source stream to read from
        :return:        None
        """
        length = self.deserialize_common_part(stream)

        if length != 0:
            raise InvalidLen


class DeviceUUIDResponseMessage(GenericMessage):
    """
    Class representing DeviceUUIDResponse uart message.
    Class fields are adequate to message parameters, described in UART specification.
    """

    def __init__(self):
        """
        Initialize message and all its fields
        """
        super().__init__()
        self.type = UartCommand.DeviceUUIDResponse
        self.uuid = bytes(UART_UUID_LEN)

    def __eq__(self, other):
        """
        Compare two messages. Returns true if all fields are identical.

        :param other:     GenericMessage or derivative, other message to be compared with self
        :return:          True if identical, False otherwise
        """
        return super().__eq__(other) and self.uuid == other.uuid

    def __str__(self):
        """
        Generate string representing message
        """
        return super().__str__() + ", uuid=" + self.uuid.hex()

    def get_length(self):
        """
        Get serialized message len. This should be used ONLY when all fields are filled

        :return:    int, serialized message length
        """
        return UART_UUID_LEN

    def serialize(self, stream):
        """
        Serialize message into bytes

        :param stream:  io.BytesIO stream, destination
        :return:        None
        """
        self.serialize_common_part(stream)
        stream.write(self.uuid)

    def deserialize(self, stream):
        """
        Deserialize message, fill fields consuming stream

        :param stream:  io.BytesIO stream, source stream to read from
        :return:        None
        """
        length = self.deserialize_common_part(stream)
        self.uuid = stream.read(UART_UUID_LEN)

        if length - UART_UUID_LEN != 0:
            raise InvalidLen

        if len(self.uuid) - UART_UUID_LEN != 0:
            raise InvalidLen


class DfuInitRequestMessage(GenericMessage):
    """
    Class representing DfuInitRequest uart message.
    Class fields are adequate to message parameters, described in UART specification.
    """

    def __init__(self):
        """
        Initialize message and all its fields
        """
        super().__init__()
        self.type = UartCommand.DfuInitRequest
        self.firmware_size = int()
        self.firmware_sha256 = bytes(UART_DFU_FIRMWARE_SHA256_LEN)
        self.app_data_length = int()
        self.app_data = bytes()

    def __eq__(self, other):
        """
        Compare two messages. Returns true if all fields are identical.

        :param other:     GenericMessage or derivative, other message to be compared with self
        :return:          True if identical, False otherwise
        """
        return super().__eq__(other) and \
               self.firmware_size == other.firmware_size and \
               self.firmware_sha256 == other.firmware_sha256 and \
               self.app_data_length == other.app_data_length and \
               self.app_data == other.app_data

    def __str__(self):
        """
        Generate string representing message
        """
        return super().__str__() + ", firmware_size=" + str(self.firmware_size) \
               + ", firmware_sha256=" + self.firmware_sha256.hex() \
               + ", app_data_length=" + str(self.app_data_length) \
               + ", app_data=" + self.app_data.hex()

    def get_length(self):
        """
        Get serialized message len. This should be used ONLY when all fields are filled

        :return:    int, serialized message length
        """
        return UART_DFU_FIRMWARE_SIZE_LEN + \
               UART_DFU_FIRMWARE_SHA256_LEN + \
               UART_DFU_APP_DATA_LENGTH_LEN + \
               len(self.app_data)

    def serialize(self, stream):
        """
        Serialize message into bytes

        :param stream:  io.BytesIO stream, destination
        :return:        None
        """
        self.serialize_common_part(stream)
        stream.write(self.firmware_size.to_bytes(UART_DFU_FIRMWARE_SIZE_LEN, byteorder='little', signed=False))
        stream.write(self.firmware_sha256)
        stream.write(self.app_data_length.to_bytes(UART_DFU_APP_DATA_LENGTH_LEN, byteorder='little', signed=False))
        stream.write(self.app_data)

    def deserialize(self, stream):
        """
        Deserialize message, fill fields consuming stream

        :param stream:  io.BytesIO stream, source stream to read from
        :return:        None
        """
        length = self.deserialize_common_part(stream)
        self.firmware_size = int.from_bytes(stream.read(UART_DFU_FIRMWARE_SIZE_LEN), byteorder='little')
        self.firmware_sha256 = stream.read(UART_DFU_FIRMWARE_SHA256_LEN)
        self.app_data_length = int.from_bytes(stream.read(UART_DFU_APP_DATA_LENGTH_LEN), byteorder='little')

        length -= UART_DFU_FIRMWARE_SIZE_LEN + UART_DFU_FIRMWARE_SHA256_LEN + UART_DFU_APP_DATA_LENGTH_LEN

        if length != self.app_data_length:
            raise InvalidLen

        self.app_data = stream.read(length)

        if self.app_data_length != len(self.app_data):
            raise InvalidLen


class DfuInitResponseMessage(GenericMessage):
    """
    Class representing DfuInitResponse uart message.
    Class fields are adequate to message parameters, described in UART specification.
    """

    def __init__(self):
        """
        Initialize message and all its fields
        """
        super().__init__()
        self.type = UartCommand.DfuInitResponse
        self.status = DFUStatus(DFUStatus.DFU_INVALID_CODE)

    def __eq__(self, other):
        """
        Compare two messages. Returns true if all fields are identical.

        :param other:     GenericMessage or derivative, other message to be compared with self
        :return:          True if identical, False otherwise
        """
        return super().__eq__(other) and self.status == other.status

    def __str__(self):
        """
        Generate string representing message
        """
        return super().__str__() + ", status=" + self.status.name

    def get_length(self):
        """
        Get serialized message len. This should be used ONLY when all fields are filled

        :return:    int, serialized message length
        """
        return UART_DFU_STATUS_LEN

    def serialize(self, stream):
        """
        Serialize message into bytes

        :param stream:  io.BytesIO stream, destination
        :return:        None
        """
        self.serialize_common_part(stream)
        stream.write(self.status.to_bytes(UART_DFU_STATUS_LEN, byteorder='little', signed=False))

    def deserialize(self, stream):
        """
        Deserialize message, fill fields consuming stream

        :param stream:  io.BytesIO stream, source stream to read from
        :return:        None
        """
        length = self.deserialize_common_part(stream)
        self.status = DFUStatus.from_bytes(stream.read(UART_DFU_STATUS_LEN), byteorder='little')

        if length - UART_DFU_STATUS_LEN != 0:
            raise InvalidLen


class DfuStatusRequestMessage(GenericMessage):
    """
    Class representing DfuStatusRequest uart message.
    Class fields are adequate to message parameters, described in UART specification.
    """

    def __init__(self):
        """
        Initialize message and all its fields
        """
        super().__init__()
        self.type = UartCommand.DfuStatusRequest

    def serialize(self, stream):
        """
        Serialize message into bytes

        :param stream:  io.BytesIO stream, destination
        :return:        None
        """
        self.serialize_common_part(stream)

    def deserialize(self, stream):
        """
        Deserialize message, fill fields consuming stream

        :param stream:  io.BytesIO stream, source stream to read from
        :return:        None
        """
        length = self.deserialize_common_part(stream)

        if length != 0:
            raise InvalidLen


class DfuStatusResponseMessage(GenericMessage):
    """
    Class representing DfuStatusResponse uart message.
    Class fields are adequate to message parameters, described in UART specification.
    """

    def __init__(self):
        """
        Initialize message and all its fields
        """
        super().__init__()
        self.type = UartCommand.DfuStatusResponse
        self.status = DFUStatus(DFUStatus.DFU_INVALID_CODE)
        self.supported_page_size = int()
        self.firmware_offset = int()
        self.firmware_crc = int()

    def __eq__(self, other):
        """
        Compare two messages. Returns true if all fields are identical.

        :param other:     GenericMessage or derivative, other message to be compared with self
        :return:          True if identical, False otherwise
        """
        return super().__eq__(other) and \
               self.status == other.status and \
               self.supported_page_size == other.supported_page_size and \
               self.firmware_offset == other.firmware_offset and \
               self.firmware_crc == other.firmware_crc

    def __str__(self):
        """
        Generate string representing message
        """
        return super().__str__() + ", status=" + self.status.name \
               + ", supported_page_size=" + str(self.supported_page_size) \
               + ", firmware_offset=" + hex(self.firmware_offset) \
               + ", firmware_crc=" + hex(self.firmware_crc)

    def get_length(self):
        """
        Get serialized message len. This should be used ONLY when all fields are filled

        :return:    int, serialized message length
        """
        return UART_DFU_STATUS_LEN + \
               UART_DFU_SUPPORTED_PAGE_SIZE_LEN + \
               UART_DFU_FIRMWARE_OFFSET_LEN + \
               UART_DFU_FIRMWARE_CRC_LEN

    def serialize(self, stream):
        """
        Serialize message into bytes

        :param stream:  io.BytesIO stream, destination
        :return:        None
        """
        self.serialize_common_part(stream)
        stream.write(self.status.to_bytes(UART_DFU_STATUS_LEN, byteorder='little', signed=False))
        stream.write(
            self.supported_page_size.to_bytes(UART_DFU_SUPPORTED_PAGE_SIZE_LEN, byteorder='little', signed=False))
        stream.write(self.firmware_offset.to_bytes(UART_DFU_FIRMWARE_OFFSET_LEN, byteorder='little', signed=False))
        stream.write(self.firmware_crc.to_bytes(UART_DFU_FIRMWARE_CRC_LEN, byteorder='little', signed=False))

    def deserialize(self, stream):
        """
        Deserialize message, fill fields consuming stream

        :param stream:  io.BytesIO stream, source stream to read from
        :return:        None
        """
        length = self.deserialize_common_part(stream)
        self.status = DFUStatus.from_bytes(stream.read(UART_DFU_STATUS_LEN), byteorder='little')
        self.supported_page_size = int.from_bytes(stream.read(UART_DFU_SUPPORTED_PAGE_SIZE_LEN), byteorder='little')
        self.firmware_offset = int.from_bytes(stream.read(UART_DFU_FIRMWARE_OFFSET_LEN), byteorder='little')
        self.firmware_crc = int.from_bytes(stream.read(UART_DFU_FIRMWARE_CRC_LEN), byteorder='little')

        if length - \
           UART_DFU_STATUS_LEN - \
           UART_DFU_SUPPORTED_PAGE_SIZE_LEN - \
           UART_DFU_FIRMWARE_OFFSET_LEN - \
           UART_DFU_FIRMWARE_CRC_LEN != 0:
            raise InvalidLen


class DfuPageCreateRequestMessage(GenericMessage):
    """
    Class representing DfuPageCreateRequest uart message.
    Class fields are adequate to message parameters, described in UART specification.
    """

    def __init__(self):
        """
        Initialize message and all its fields
        """
        super().__init__()
        self.type = UartCommand.DfuPageCreateRequest
        self.requested_page_size = int()

    def __eq__(self, other):
        """
        Compare two messages. Returns true if all fields are identical.

        :param other:     GenericMessage or derivative, other message to be compared with self
        :return:          True if identical, False otherwise
        """
        return super().__eq__(other) and self.requested_page_size == other.requested_page_size

    def __str__(self):
        """
        Generate string representing message
        """
        return super().__str__() + ", requested_page_size=" + str(self.requested_page_size)

    def get_length(self):
        """
        Get serialized message len. This should be used ONLY when all fields are filled

        :return:    int, serialized message length
        """
        return UART_REQUESTED_PAGE_SIZE_LEN

    def serialize(self, stream):
        """
        Serialize message into bytes

        :param stream:  io.BytesIO stream, destination
        :return:        None
        """
        self.serialize_common_part(stream)
        stream.write(self.requested_page_size.to_bytes(UART_REQUESTED_PAGE_SIZE_LEN, byteorder='little', signed=False))

    def deserialize(self, stream):
        """
        Deserialize message, fill fields consuming stream

        :param stream:  io.BytesIO stream, source stream to read from
        :return:        None
        """
        length = self.deserialize_common_part(stream)
        self.requested_page_size = int.from_bytes(stream.read(UART_REQUESTED_PAGE_SIZE_LEN), byteorder='little')

        if length - UART_REQUESTED_PAGE_SIZE_LEN != 0:
            raise InvalidLen


class DfuPageCreateResponseMessage(GenericMessage):
    """
    Class representing DfuPageCreateResponse uart message.
    Class fields are adequate to message parameters, described in UART specification.
    """

    def __init__(self):
        """
        Initialize message and all its fields
        """
        super().__init__()
        self.type = UartCommand.DfuPageCreateResponse
        self.status = DFUStatus(DFUStatus.DFU_INVALID_CODE)

    def __eq__(self, other):
        """
        Compare two messages. Returns true if all fields are identical.

        :param other:     GenericMessage or derivative, other message to be compared with self
        :return:          True if identical, False otherwise
        """
        return super().__eq__(other) and self.status == other.status

    def __str__(self):
        """
        Generate string representing message
        """
        return super().__str__() + ", status=" + self.status.name

    def get_length(self):
        """
        Get serialized message len. This should be used ONLY when all fields are filled

        :return:    int, serialized message length
        """
        return UART_DFU_STATUS_LEN

    def serialize(self, stream):
        """
        Serialize message into bytes

        :param stream:  io.BytesIO stream, destination
        :return:        None
        """
        self.serialize_common_part(stream)
        stream.write(self.status.to_bytes(UART_DFU_STATUS_LEN, byteorder='little', signed=False))

    def deserialize(self, stream):
        """
        Deserialize message, fill fields consuming stream

        :param stream:  io.BytesIO stream, source stream to read from
        :return:        None
        """
        length = self.deserialize_common_part(stream)
        self.status = DFUStatus.from_bytes(stream.read(UART_DFU_STATUS_LEN), byteorder='little')

        if length - UART_DFU_STATUS_LEN != 0:
            raise InvalidLen


class DfuWriteDataEventMessage(GenericMessage):
    """
    Class representing DfuWriteDataEvent uart message.
    Class fields are adequate to message parameters, described in UART specification.
    """

    def __init__(self):
        """
        Initialize message and all its fields
        """
        super().__init__()
        self.type = UartCommand.DfuWriteDataEvent
        self.data_len = int()
        self.data = bytes()

    def __eq__(self, other):
        """
        Compare two messages. Returns true if all fields are identical.

        :param other:     GenericMessage or derivative, other message to be compared with self
        :return:          True if identical, False otherwise
        """
        return super().__eq__(other) and \
               self.data_len == other.data_len and \
               self.data == other.data

    def __str__(self):
        """
        Generate string representing message
        """
        return super().__str__() + ", data_len=" + str(self.data_len) \
               + ", data=" + self.data.hex()

    def get_length(self):
        """
        Get serialized message len. This should be used ONLY when all fields are filled

        :return:    int, serialized message length
        """
        return UART_DFU_DATA_LENGTH_LEN + len(self.data)

    def serialize(self, stream):
        """
        Serialize message into bytes

        :param stream:  io.BytesIO stream, destination
        :return:        None
        """
        self.serialize_common_part(stream)
        stream.write(self.data_len.to_bytes(UART_DFU_DATA_LENGTH_LEN, byteorder='little', signed=False))
        stream.write(self.data)

    def deserialize(self, stream):
        """
        Deserialize message, fill fields consuming stream

        :param stream:  io.BytesIO stream, source stream to read from
        :return:        None
        """
        length = self.deserialize_common_part(stream)
        self.data_len = int.from_bytes(stream.read(UART_DFU_DATA_LENGTH_LEN), byteorder='little')

        length -= UART_DFU_DATA_LENGTH_LEN

        if length != self.data_len:
            raise InvalidLen

        self.data = stream.read(length)

        if self.data_len != len(self.data):
            raise InvalidLen


class DfuPageStoreRequestMessage(GenericMessage):
    """
    Class representing DfuPageStoreRequest uart message.
    Class fields are adequate to message parameters, described in UART specification.
    """

    def __init__(self):
        """
        Initialize message and all its fields
        """
        super().__init__()
        self.type = UartCommand.DfuPageStoreRequest

    def serialize(self, stream):
        """
        Serialize message into bytes

        :param stream:  io.BytesIO stream, destination
        :return:        None
        """
        self.serialize_common_part(stream)

    def deserialize(self, stream):
        """
        Deserialize message, fill fields consuming stream

        :param stream:  io.BytesIO stream, source stream to read from
        :return:        None
        """
        length = self.deserialize_common_part(stream)

        if length != 0:
            raise InvalidLen


class DfuPageStoreResponseMessage(GenericMessage):
    """
    Class representing DfuPageStoreResponse uart message.
    Class fields are adequate to message parameters, described in UART specification.
    """

    def __init__(self):
        """
        Initialize message and all its fields
        """
        super().__init__()
        self.type = UartCommand.DfuPageStoreResponse
        self.status = DFUStatus(DFUStatus.DFU_INVALID_CODE)

    def __eq__(self, other):
        """
        Compare two messages. Returns true if all fields are identical.

        :param other:     GenericMessage or derivative, other message to be compared with self
        :return:          True if identical, False otherwise
        """
        return super().__eq__(other) and self.status == other.status

    def __str__(self):
        """
        Generate string representing message
        """
        return super().__str__() + ", status=" + self.status.name

    def get_length(self):
        """
        Get serialized message len. This should be used ONLY when all fields are filled

        :return:    int, serialized message length
        """
        return UART_DFU_STATUS_LEN

    def serialize(self, stream):
        """
        Serialize message into bytes

        :param stream:  io.BytesIO stream, destination
        :return:        None
        """
        self.serialize_common_part(stream)
        stream.write(self.status.to_bytes(UART_DFU_STATUS_LEN, byteorder='little', signed=False))

    def deserialize(self, stream):
        """
        Deserialize message, fill fields consuming stream

        :param stream:  io.BytesIO stream, source stream to read from
        :return:        None
        """
        length = self.deserialize_common_part(stream)
        self.status = DFUStatus.from_bytes(stream.read(UART_DFU_STATUS_LEN), byteorder='little')

        if length - UART_DFU_STATUS_LEN != 0:
            raise InvalidLen


class DfuStateRequestMessage(GenericMessage):
    """
    Class representing DfuStateRequest uart message.
    Class fields are adequate to message parameters, described in UART specification.
    """

    def __init__(self):
        """
        Initialize message and all its fields
        """
        super().__init__()
        self.type = UartCommand.DfuStateRequest

    def serialize(self, stream):
        """
        Serialize message into bytes

        :param stream:  io.BytesIO stream, destination
        :return:        None
        """
        self.serialize_common_part(stream)

    def deserialize(self, stream):
        """
        Deserialize message, fill fields consuming stream

        :param stream:  io.BytesIO stream, source stream to read from
        :return:        None
        """
        length = self.deserialize_common_part(stream)

        if length != 0:
            raise InvalidLen


class DfuStateResponseMessage(GenericMessage):
    """
    Class representing DfuStateResponse uart message.
    Class fields are adequate to message parameters, described in UART specification.
    """

    def __init__(self):
        """
        Initialize message and all its fields
        """
        super().__init__()
        self.type = UartCommand.DfuStateResponse
        self.status = DfuStatus(DfuStatus.NotInProgress)

    def __str__(self):
        """
        Generate string representing message
        """
        return super().__str__() + ", status=" + self.status.name

    def __eq__(self, other):
        """
        Compare two messages. Returns true if all fields are identical.

        :param other:     GenericMessage or derivative, other message to be compared with self
        :return:          True if identical, False otherwise
        """
        return super().__eq__(other) and self.status == other.status

    def get_length(self):
        """
        Get serialized message len. This should be used ONLY when all fields are filled

        :return:    int, serialized message length
        """
        return UART_DFU_PRE_VALIDATION_STATUS_LEN

    def serialize(self, stream):
        """
        Serialize message into bytes

        :param stream:  io.BytesIO stream, destination
        :return:        None
        """
        self.serialize_common_part(stream)
        stream.write(self.status.to_bytes(UART_DFU_PRE_VALIDATION_STATUS_LEN, byteorder='little', signed=False))

    def deserialize(self, stream):
        """
        Deserialize message, fill fields consuming stream

        :param stream:  io.BytesIO stream, source stream to read from
        :return:        None
        """
        length = self.deserialize_common_part(stream)
        self.status = DfuStatus.from_bytes(stream.read(UART_DFU_PRE_VALIDATION_STATUS_LEN),
                                           byteorder='little')

        if length - UART_DFU_PRE_VALIDATION_STATUS_LEN != 0:
            raise InvalidLen


class DfuCancelRequestMessage(GenericMessage):
    """
    Class representing DfuCancelRequest uart message.
    Class fields are adequate to message parameters, described in UART specification.
    """

    def __init__(self):
        """
        Initialize message and all its fields
        """
        super().__init__()
        self.type = UartCommand.DfuCancelRequest

    def serialize(self, stream):
        """
        Serialize message into bytes

        :param stream:  io.BytesIO stream, destination
        :return:        None
        """
        self.serialize_common_part(stream)

    def deserialize(self, stream):
        """
        Deserialize message, fill fields consuming stream

        :param stream:  io.BytesIO stream, source stream to read from
        :return:        None
        """
        length = self.deserialize_common_part(stream)

        if length != 0:
            raise InvalidLen


class DfuCancelResponseMessage(GenericMessage):
    """
    Class representing DfuCancelResponse uart message.
    Class fields are adequate to message parameters, described in UART specification.
    """

    def __init__(self):
        """
        Initialize message and all its fields
        """
        super().__init__()
        self.type = UartCommand.DfuCancelResponse

    def serialize(self, stream):
        """
        Serialize message into bytes

        :param stream:  io.BytesIO stream, destination
        :return:        None
        """
        self.serialize_common_part(stream)

    def deserialize(self, stream):
        """
        Deserialize message, fill fields consuming stream

        :param stream:  io.BytesIO stream, source stream to read from
        :return:        None
        """
        length = self.deserialize_common_part(stream)

        if length != 0:
            raise InvalidLen


class StartTestRequest(GenericMessage):
    """
    Class representing StartTestRequest uart message.
    Class fields are adequate to message parameters, described in UART specification.
    """

    def __init__(self):
        """
        Initialize message and all its fields
        """
        super().__init__()
        self.type = UartCommand.StartTestRequest
        self.company_id = 0
        self.test_id = 0
        self.instance_index = 0

    def __eq__(self, other):
        """
        Compare two messages. Returns true if all fields are identical.

        :param other:     GenericMessage or derivative, other message to be compared with self
        :return:          True if identical, False otherwise
        """
        return super().__eq__(other) and \
               self.company_id == other.company_id and \
               self.test_id == other.test_id and \
               self.instance_index == other.instance_index

    def get_length(self):
        """
        Get serialized message len. This should be used ONLY when all fields are filled

        :return:    int, serialized message length
        """
        return UART_COMPANY_ID_LEN + UART_TEST_ID_LEN + UART_INSTANCE_INDEX_LEN

    def serialize(self, stream):
        """
        Serialize message into bytes

        :param stream:  io.BytesIO stream, destination
        :return:        None
        """
        self.serialize_common_part(stream)
        stream.write(self.company_id.to_bytes(UART_COMPANY_ID_LEN, byteorder='little', signed=False))
        stream.write(self.test_id.to_bytes(UART_TEST_ID_LEN, byteorder='little', signed=False))
        stream.write(self.instance_index.to_bytes(UART_INSTANCE_INDEX_LEN, byteorder='little', signed=False))

    def deserialize(self, stream):
        """
        Deserialize message, fill fields consuming stream

        :param stream:  io.BytesIO stream, source stream to read from
        :return:        None
        """
        length = self.deserialize_common_part(stream)
        self.company_id = int.from_bytes(stream.read(UART_COMPANY_ID_LEN), byteorder="little")
        self.test_id = int.from_bytes(stream.read(UART_TEST_ID_LEN), byteorder="little")
        self.instance_index = int.from_bytes(stream.read(UART_INSTANCE_INDEX_LEN), byteorder="little")

        length -= UART_COMPANY_ID_LEN + UART_TEST_ID_LEN + UART_INSTANCE_INDEX_LEN

        if length != 0:
            raise InvalidLen


class StartTestResponse(GenericMessage):
    """
    Class representing StartTestResponse uart message.
    Class fields are adequate to message parameters, described in UART specification.
    """

    def __init__(self):
        """
        Initialize message and all its fields
        """
        super().__init__()
        self.type = UartCommand.StartTestResponse

    def get_length(self):
        """
        Get serialized message len. This should be used ONLY when all fields are filled

        :return:    int, serialized message length
        """
        return 0

    def serialize(self, stream):
        """
        Serialize message into bytes

        :param stream:  io.BytesIO stream, destination
        :return:        None
        """
        self.serialize_common_part(stream)

    def deserialize(self, stream):
        """
        Deserialize message, fill fields consuming stream

        :param stream:  io.BytesIO stream, source stream to read from
        :return:        None
        """
        length = self.deserialize_common_part(stream)

        if length != 0:
            raise InvalidLen
