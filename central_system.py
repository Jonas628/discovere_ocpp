import asyncio
import websockets
from datetime import datetime
from ocpp.routing import on
from ocpp.v16 import ChargePoint as cp
from ocpp.v16.enums import Action, RegistrationStatus
from ocpp.v16 import call_result


class MyChargePoint(cp):
    @on(Action.BootNotification)
    def on_boot_notitication(self, charge_point_vendor, charge_point_model, **kwargs):
        print("ChargePoint Connected!")
        return call_result.BootNotificationPayload(
            current_time=datetime.utcnow().isoformat(),
            interval=10,
            status=RegistrationStatus.accepted
        )


async def on_connect(websocket, path):
    """
    For every new charge point that connects, create a ChargePoint instance
    and start listening for messages.
    """
    charge_point_id = path.strip('/')
    cp = MyChargePoint(charge_point_id, websocket)

    await cp.start()


# async def on_connect(websocket, path):
#    await websocket.send()
#    print(f'Charge point {path} connected')


async def main():
    # on_connect() is executed on every new connection, it takes two arguments:
    # an instance of websockets.server.WebSocketServerProtocol and the request
    # URI which identifies the charge point
    server = await websockets.serve(on_connect, '0.0.0.0', 9000, subprotocols=['ocpp1.6'])
    await server.wait_closed()


if __name__ == '__main__':
    asyncio.run(main())
