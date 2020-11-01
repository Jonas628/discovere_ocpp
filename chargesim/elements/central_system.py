import asyncio
import websockets
import json
from pathlib import Path
from clock import timestamp
from ocpp.routing import on
from ocpp.v16 import ChargePoint as cp
from ocpp.v16.enums import Action, RegistrationStatus
from ocpp.v16 import call_result

DATADIR = Path("/home/ole/projects/charging_management/data/")


class MyChargePoint(cp):
    """
    Make an instance of this everytime a charge_point is connected.
    """
    @on(Action.BootNotification)
    def on_boot_notitication(self, charge_point_vendor,
                             charge_point_model, **kwargs):
        print("ChargePoint Connected!")
        return call_result.BootNotificationPayload(
            current_time=datetime.utcnow().isoformat(),
            interval=10,
            status=RegistrationStatus.accepted)

    @on(Action.Heartbeat)
    async def on_heartbeat(self):
        timestamp = datetime.utcnow()
        print(f"received Heartbeat at {timestamp.hour}:{timestamp.minute}:{timestamp.second}")
        return call_result.HeartbeatPayload(current_time=str(timestamp))

    @on(Action.MeterValues)
    async def on_meter_value(self, connector_id, meter_value):
        print(meter_value)
        fname = meter_value[0]['timestamp']
        with open(DATADIR/fname, 'w') as outfile:
            json.dump(meter_value[0], outfile)
        return call_result.MeterValuesPayload()


class CentralSystem(object):

    def __init__(self):
        self.clients = []  # all currently connected charging_points

    async def register(self, websocket):
        charge_point_id = "CP01"
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
    start_server = websockets.serve(server.ws_handler, "localhost", 3000, subprotocols=['ocpp1.6'])
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_server)
    loop.run_forever()
