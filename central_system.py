import asyncio
import websockets
from datetime import datetime
from ocpp.routing import on
from ocpp.v16 import ChargePoint as cp
from ocpp.v16.enums import Action, RegistrationStatus
from ocpp.v16 import call_result


class ChargePoint(cp):
    @on(Action.BootNotification)
    def on_boot_notification(self, charge_point_vendor, charge_point_model, **kwargs):
        print(f"Boot notification from charge point model {charge_point_model} "
              f"from vendor {charge_point_vendor}.")
        return call_result.BootNotificationPayload(
            current_time=datetime.utcnow().isoformat(),
            interval=10,
            status=RegistrationStatus.accepted
        )

    @on(Action.Heartbeat)
    async def on_heartbeat(self):
        current_time = str(datetime.utcnow())
        print(f"received heartbeat at {current_time}")
        return call_result.HeartbeatPayload(current_time=current_time)

    @on(Action.MeterValues)
    async def on_meter_value(self, connector_id, transaction_id, meter_value):
        print(meter_value)
        return call_result.MeterValuesPayload()


async def on_connect(websocket, path):
    """ For every new charge point that connects, create a ChargePoint instance
    and start listening for messages. """
    charge_point_id = path.strip('/')
    cp = ChargePoint(charge_point_id, websocket)
    print(f"new websocket connection: {websocket}")
    print(f"charge point {charge_point_id} connected! \n")

    await cp.start()


async def main():
    server = await websockets.serve(
        on_connect,
        '0.0.0.0',
        8000,
        subprotocols=['ocpp1.6']
    )

    await server.wait_closed()


if __name__ == '__main__':
    asyncio.run(main())