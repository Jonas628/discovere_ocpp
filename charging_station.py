import asyncio
import websockets
import sys
import os
from datetime import datetime
from ocpp.v16 import ChargePoint as cp
from ocpp.v16 import call
from ocpp.v16.enums import RegistrationStatus
sys.path.append("/home/bialas/projects/charging_management")
from electric_vehicle import ElectricVehicle

try:
    TIMELAPSE = int(os.environ["TIMELAPSE"])
except KeyError:
    TIMELAPSE = 1

# for management:
# ChangeAvailability
# SetChargingProfile / GetCompositeSchedule--> start, stop time
# ChangeConfiguration / GetConfiguration --> how long is this viable, what can we set?

# SetChargingProfile seems like the appropriate thing
# RemoteStart/RemoteStart --> interrupt charging


class ChargePoint(cp):
    """
    Charge point class which inherits from the OCPP python module's charge
    point. The parent class handles the sending and receiving of messages.
    This class adds some methods for sending messages and executing functions
    when a specific message is received
    """

    def __init__(self, id, connection, response_timeout=30):
        super().__init__(id, connection, response_timeout=response_timeout)
        self.maxpower = float(11)

    async def send_boot_notification(self):
        request = call.BootNotificationPayload(
            charge_point_model="Weeyu",
            charge_point_vendor="Discovere"
        )
        response = await self.call(request)
        if response.status == RegistrationStatus.accepted:
            print("Connected to central system.")

    async def send_heartbeats(self):
        while True:
            request = call.HeartbeatPayload()
            await self.call(request)
            await asyncio.sleep(10)

    async def send_meter_value(self):
        request = call.MeterValuesPayload(
            connector_id=1,
            meter_value=[{
                "timestamp": datetime.utcnow().isoformat(),
                "sampledValue": [{
                    "measurand": "Power.Active.Export",
                    "phase": "N",
                    "unit": "kW",
                    "value": f"{self.maxpower}"}]
            }]
        )
        await self.call(request)

    async def charge(self, car):
        while car.soc < car.capacity*0.9:
            car.soc += 10*self.maxpower
            await self.send_meter_value()
            await asyncio.sleep(10/TIMELAPSE)


async def main(hostname: str, port: int) -> None:
    websocket_resource_url = f"ws://{hostname}:{port}"
    # open the connection with a websocket
    async with websockets.connect(websocket_resource_url, subprotocols=['ocpp1.6']) as websocket:
        cp = ChargePoint('CP_1', websocket)
        ev = ElectricVehicle(cp)
        # when the charge point is started it is waiting for messages
        await asyncio.gather(cp.start(), cp.send_boot_notification(), cp.send_heartbeats(), ev.run())


if __name__ == '__main__':
    # specify host and port and run forever, will raise an error if the
    # server is not found
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(hostname='localhost', port=3000))
    loop.run_forever()
