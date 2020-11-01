import asyncio
import websockets
from ocpp.v16 import ChargePoint as cp
from ocpp.v16 import call
from ocpp.v16.enums import RegistrationStatus
from chargesim.electric_vehicle import ElectricVehicle
from chargesim import clock

# for management:
# ChangeAvailability
# SetChargingProfile / GetCompositeSchedule--> start, stop time
# ChangeConfiguration / GetConfiguration --> how long is this viable?
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
                "timestamp": clock.timestamp(),
                "sampledValue": [
                    {"measurand": "Power.Active.Import",
                     "phase": "N",
                     "unit": "kW",
                     "value": str(self.maxpower)},
                    {"measurand": "Energy.Active.Import.Register",
                     "phase": "N",
                     "unit": "kWh",
                     "value": "0.00"}]}])

        await self.call(request)

    async def charge(self, car):
        transaction_start = clock.simtime
        while car.soc < car.capacity*0.9:
            await asyncio.sleep(1)
            elapsed = clock.simtime - transaction_start
            if elapsed < 0:
                elapsed = 1
            car.soc += elapsed*self.maxpower
            await self.send_meter_value()


async def main(hostname: str, port: int) -> None:
    websocket_resource_url = f"ws://{hostname}:{port}"
    # open the connection with a websocket
    async with websockets.connect(websocket_resource_url,
                                  subprotocols=['ocpp1.6']) as websocket:
        cp = ChargePoint('CP_1', websocket)
        ev = ElectricVehicle(cp)
        # when the charge point is started it is waiting for messages
        await asyncio.gather(cp.start(), cp.send_boot_notification(),
                             cp.send_heartbeats(), ev.run())


if __name__ == '__main__':
    # specify host and port and run forever, will raise an error if the
    # server is not found
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(hostname='localhost', port=3000))
    loop.run_forever()
