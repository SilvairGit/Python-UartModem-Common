from enum import IntEnum


class Serializable:
    """
    Abstract class describing serializable class
    """

    def serialize(self, stream):
        """
        Serialize message into stream. Overload this in derivative class

        :param stream:  io.BytesIO stream, destination
        :return:        None
        """
        assert False, "Not implemented method cannot be used"

    def deserialize(self, stream):
        """
        Deserialize message, fill fields consuming stream

        :param stream:  io.BytesIO stream, source stream to read from
        :return:        None
        """
        assert False, "Not implemented method cannot be used"


UART_MODEL_ID_LEN = 2
UART_SENSOR_SETUP_SERVER_CONFIG_LEN = 10


class ModelID(IntEnum):
    """
    Enumerator mapping Mesh Model ID to its name.
    Consist only of supported by UART Modem.
    """
    GenOnOffClientID = 0x1001,
    GenLevelClientID = 0x1003,
    GenPowerOnOffClientID = 0x1008,
    LightLightnessClientID = 0x1302,
    LightLCClientID = 0x1311,
    SensorServerID = 0x1100,
    SensorSetupServerID = 0x1101,
    LightLightnessServerID = 0x1300,
    LightLCServerID = 0x130F,
    SensorClientID = 0x1102,
    HealthServerID = 0x0002,
    HealthClientID = 0x0003


class FactoryResetSource(IntEnum):
    """
    Enumerator mapping Factory Reset source to its name.
    """
    Mesh = 0x00,
    Pin = 0x01,
    RFU = 0x02


class ModemState(IntEnum):
    """
    Enumerator mapping Modem State to its name.
    """
    InitDevice = 0x00,
    Device = 0x01,
    InitNode = 0x02,
    Node = 0x03,
    Unknown = 0xFF


class Error(IntEnum):
    """
    Enumerator mapping Error Code to its name.
    """
    InvalidCRC = 0x00,
    InvalidCMD = 0x01,
    InvalidLen = 0x02,
    InvalidState = 0x03,
    InvalidParam = 0x04,
    Timeout = 0x05,
    NoLicenseForModelRegistration = 0x06,
    NoResourcesForModelRegistration = 0x07,
    MeshMessageRequestProcessError = 0x08


class DFUStatus(IntEnum):
    """
    Enumerator mapping DFU Status to its name.
    """
    DFU_INVALID_CODE = 0x00,
    DFU_SUCCESS = 0x01,
    DFU_OPCODE_NOT_SUPPORTED = 0x02,
    DFU_INVALID_PARAMETER = 0x03,
    DFU_INSUFFICIENT_RESOURCES = 0x04,
    DFU_INVALID_OBJECT = 0x05,
    DFU_UNSUPPORTED_TYPE = 0x07,
    DFU_OPERATION_NOT_PERMITTED = 0x08,
    DFU_OPERATION_FAILED = 0x0A,
    DFU_FIRMWARE_SUCCESSFULLY_UPDATED = 0xFF,


class AttentionEvent(IntEnum):
    """
    Enumerator mapping Attention Event to its name.
    """
    Off = 0x00,
    On = 0x01


class DfuStatus(IntEnum):
    """
    Enumerator mapping Attention Event to its name.
    """
    InProgress = 0x01,
    NotInProgress = 0x00


class ModelDesc(Serializable):
    """
    Class representing Mesh Model Description
    Class fields are:
        self.model_id - Mesh Model ID opcode
        self.config   - optional model configuration
    """

    def __init__(self, model_id: ModelID = None):
        """
        Initialize class and all its fields
        """
        super().__init__()
        self.model_id = model_id
        self.config = bytes()

    def __eq__(self, other):
        """
        Compare two models. Returns true if all fields are identical.

        :param other:     ModelDesc, other model to be compared with self
        :return:          True if identical, False otherwise
        """
        return self.model_id == other.model_id and self.config == other.config

    def get_length(self):
        """
        Get serialized model id len. This should be used ONLY when all fields are filled

        :param config:  If True configuration length is added
        :return:        int, serialized model id length
        """
        return UART_MODEL_ID_LEN + len(self.config)

    def serialize(self, stream):
        """
        Serialize model id into bytes

        :param stream:  io.BytesIO stream, destination
        :param config:  If True configuration is added
        :return:        None
        """
        stream.write(self.model_id.to_bytes(UART_MODEL_ID_LEN, byteorder='little', signed=False))

        if self.model_id == ModelID.SensorSetupServerID:
            stream.write(self.config)

    def deserialize(self, stream):
        """
        Deserialize model id, fill fields consuming stream

        :param stream:  io.BytesIO stream, source stream to read from
        :param config:  If True configuration is expected
        :return:        None
        """
        b = stream.read(UART_MODEL_ID_LEN)
        self.model_id = ModelID.from_bytes(b, byteorder='little')

        if self.model_id == ModelID.SensorSetupServerID:
            self.config = stream.read(UART_SENSOR_SETUP_SERVER_CONFIG_LEN)
