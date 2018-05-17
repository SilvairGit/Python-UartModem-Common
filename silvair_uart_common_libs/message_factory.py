import io

from silvair_uart_common_libs.messages import UartCommand, PingRequestMessage, PongResponseMessage, \
    InitDeviceEventMessage, \
    CreateInstancesRequestMessage, CreateInstancesResponseMessage, InitNodeEventMessage, MeshMessageRequestMessage, \
    StartNodeRequestMessage, StartNodeResponseMessage, FactoryResetRequestMessage, FactoryResetResponseMessage, \
    FactoryResetEventMessage, MeshMessageResponseMessage, CurrentStateRequestMessage, CurrentStateResponseMessage, \
    ErrorMessage, FirmwareVersionRequestMessage, FirmwareVersionResponseMessage, SensorUpdateRequestMessage, \
    AttentionEventMessage, SoftResetRequestMessage, SoftResetResponseMessage, SensorUpdateResponseMessage, \
    DeviceUUIDRequestMessage, DeviceUUIDResponseMessage, GenericMessage, DfuInitRequestMessage, DfuInitResponseMessage, \
    DfuStatusRequestMessage, DfuStatusResponseMessage, DfuPageCreateRequestMessage, DfuPageCreateResponseMessage, \
    DfuWriteDataEventMessage, DfuPageStoreRequestMessage, DfuPageStoreResponseMessage, InvalidOpcode, InvalidLen, \
    DfuStateRequestMessage, DfuStateResponseMessage, DfuCancelRequestMessage, \
    DfuCancelResponseMessage, StartTestRequest, StartTestResponse

UART_CLASSES = {
    UartCommand.PingRequest: PingRequestMessage,
    UartCommand.PongResponse: PongResponseMessage,
    UartCommand.InitDeviceEvent: InitDeviceEventMessage,
    UartCommand.CreateInstancesRequest: CreateInstancesRequestMessage,
    UartCommand.CreateInstancesResponse: CreateInstancesResponseMessage,
    UartCommand.InitNodeEvent: InitNodeEventMessage,
    UartCommand.MeshMessageRequest: MeshMessageRequestMessage,
    UartCommand.StartNodeRequest: StartNodeRequestMessage,
    UartCommand.StartNodeResponse: StartNodeResponseMessage,
    UartCommand.FactoryResetRequest: FactoryResetRequestMessage,
    UartCommand.FactoryResetResponse: FactoryResetResponseMessage,
    UartCommand.FactoryResetEvent: FactoryResetEventMessage,
    UartCommand.MeshMessageResponse: MeshMessageResponseMessage,
    UartCommand.CurrentStateRequest: CurrentStateRequestMessage,
    UartCommand.CurrentStateResponse: CurrentStateResponseMessage,
    UartCommand.Error: ErrorMessage,
    UartCommand.FirmwareVersionRequest: FirmwareVersionRequestMessage,
    UartCommand.FirmwareVersionResponse: FirmwareVersionResponseMessage,
    UartCommand.SensorUpdateRequest: SensorUpdateRequestMessage,
    UartCommand.AttentionEvent: AttentionEventMessage,
    UartCommand.SoftResetRequest: SoftResetRequestMessage,
    UartCommand.SoftResetResponse: SoftResetResponseMessage,
    UartCommand.SensorUpdateResponse: SensorUpdateResponseMessage,
    UartCommand.DeviceUUIDRequest: DeviceUUIDRequestMessage,
    UartCommand.DeviceUUIDResponse: DeviceUUIDResponseMessage,
    UartCommand.StartTestRequest: StartTestRequest,
    UartCommand.StartTestResponse: StartTestResponse,
    UartCommand.Generic: GenericMessage,
    UartCommand.DfuInitRequest: DfuInitRequestMessage,
    UartCommand.DfuInitResponse: DfuInitResponseMessage,
    UartCommand.DfuStatusRequest: DfuStatusRequestMessage,
    UartCommand.DfuStatusResponse: DfuStatusResponseMessage,
    UartCommand.DfuPageCreateRequest: DfuPageCreateRequestMessage,
    UartCommand.DfuPageCreateResponse: DfuPageCreateResponseMessage,
    UartCommand.DfuWriteDataEvent: DfuWriteDataEventMessage,
    UartCommand.DfuPageStoreRequest: DfuPageStoreRequestMessage,
    UartCommand.DfuPageStoreResponse: DfuPageStoreResponseMessage,
    UartCommand.DfuStateRequest: DfuStateRequestMessage,
    UartCommand.DfuStateResponse: DfuStateResponseMessage,
    UartCommand.DfuCancelRequest: DfuCancelRequestMessage,
    UartCommand.DfuCancelResponse: DfuCancelResponseMessage
}

def serialize_message(msg):
    """
    Serialize GenericMessage into bytes

    :param msg:     GenericMessage or derivative, message to be serialized
    :return:        bytes, serialized message
    """
    stream = io.BytesIO()
    msg.serialize(stream)
    return stream.getvalue()


def deserialize_message(data):
    """
    Deserialize bytes into derivative of GenericMessage

    :param data:    Data to be deserialized
    :return:        GenericMessage or derivative, deserialized message
    """
    try:
        cmd = data[1]
    except IndexError:
        raise InvalidLen

    stream = io.BytesIO(data)

    try:
        msg_class = UART_CLASSES[cmd]
        msg = msg_class()
        msg.deserialize(stream)
        return msg
    except KeyError:
        raise InvalidOpcode
