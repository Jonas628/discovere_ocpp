from asgiref.sync import sync_to_async
from datetime import datetime

from ocpp_d.v16 import call_result
from ocpp_d.v16.enums import RegistrationStatus

from cp_handler.models.models import ChargingStation, ChargePoint
from cp_handler.operation_handlers.auxiliaries import save_object
from enums.enums import PhaseRotation, BackendProtocol


async def handle_boot_notification(cp_id, charge_point_vendor, charge_point_model, **kwargs):
    """
    If charge point is accepted by central system
    """
    # status Accepted

    # status Pending
    # set configuration to chargepoint or send trigger message to invoce charge point

    # status Rejected

    """
    If charge point is not registered, register it in database
    Else set status to registered 
    """
    _charge_point = await get_charge_point(1)
    if _charge_point is None:
        charging_station = ChargingStation(
            id=2,
            name="choseName",
            phase_rotation=PhaseRotation.RST,
            installation_date=datetime.utcnow().isoformat(),
            max_current=16.0)
        await save_object(charging_station)
        charge_point = ChargePoint(
            charging_station=charging_station,
            id=str(cp_id),
            name=cp_id,
            slug=cp_id,
            max_power=11000,
            protocol=BackendProtocol.OCPP16_J,
            charge_point_model=charge_point_model,
            charge_point_vendor=charge_point_vendor)
        await save_object(charge_point)
    else:
        # change registration status to registered
        print("chargepoint already registered!!!")

    payload = call_result.BootNotificationPayload(
        current_time=datetime.utcnow().isoformat(),
        interval=10,
        status=RegistrationStatus.accepted)

    return payload

@sync_to_async
def get_charge_point(cp_id):
    return ChargePoint.objects.filter(pk=cp_id).first()


