import asyncio
import websockets
from datetime import datetime
from pathlib import Path
from ocpp.routing import on
from ocpp.v16 import ChargePoint as Cp
from ocpp.v16.enums import Action, RegistrationStatus
from ocpp.v16 import call_result

DATADIR = Path("/home/ole/projects/charging_management/data/")


class MyChargePoint(Cp):
    """
    Make an instance of this everytime a charge_point is connected.
    """
    @on(Action.BootNotification)
    def on_boot_notification(self, charge_point_vendor, charge_point_model, **kwargs):
        print("ChargePoint Connected!")
        return call_result.BootNotificationPayload(
            current_time=str(datetime.utcnow()),
            interval=10,
            status=RegistrationStatus.accepted)

    @on(Action.Heartbeat)
    async def on_heartbeat(self):
        print(f"received Heartbeat at: {datetime.utcnow()}")
        return call_result.HeartbeatPayload(current_time=str(datetime.utcnow()))

    @on(Action.MeterValues)
    async def on_meter_value(self, connector_id, transaction_id, meter_value):
        print(meter_value)
        # svc.write_meter_value(meter_value[0])
        return call_result.MeterValuesPayload()


class CentralSystem(object):

    def __init__(self):
        self.clients = []  # all currently connected charging_points

    async def register(self, websocket):
        charge_point_id = "CP01"
        print(f"New charge point {charge_point_id} registered!")
        self.clients.append(MyChargePoint(charge_point_id, websocket))
        await asyncio.gather(self.clients[-1].start())

    async def ws_handler(self, websocket, uri):
        await self.register(websocket)  # add the client to the list of clients


if __name__ == '__main__':
    server = CentralSystem()
    # Whenever a client connects, the server accepts the connection,
    # creates a WebSocketServerProtocol, performs the opening handshake,
    # and delegates to the connection handler defined by ws_handler.
    # Once the handler completes, either normally or with an exception,
    # the server performs the closing handshake and closes the connection
    start_server = websockets.serve(server.ws_handler, "0.0.0.0", 8000)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_server)
    loop.run_forever()
