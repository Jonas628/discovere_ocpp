import asyncio
import websockets
from datetime import datetime
from ocpp.v16 import ChargePoint as cp
from ocpp.v16 import call
from ocpp.v16.enums import RegistrationStatus
import time

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
            tic = time.time()
            request = call.HeartbeatPayload()
            await self.call(request)
            await asyncio.sleep(1)
            print(f"ping: {time.time() - tic}")

    async def send_meter_value(self, power, cid=1, tid=1):
        request = call.MeterValuesPayload(
            connector_id=cid,
            transaction_id=tid,
            meter_value=[{
                "timestamp": str(datetime.utcnow()),
                "sampledValue": [
                    {"measurand": "Power.Active.Import",
                     "phase": "N",
                     "unit": "kW",
                     "value": str(power)},
                    {"measurand": "Energy.Active.Import.Register",
                     "phase": "N",
                     "unit": "kWh",
                     "value": "0.00"}]}]
        )
        await self.call(request)


async def main(hostname: str, port: int) -> None:
    websocket_resource_url = f"ws://{hostname}:{port}"
    # open the connection with a websocket
    async with websockets.connect(websocket_resource_url) as websocket:
        cp = ChargePoint('CP_1', websocket)
        # when the charge point is started it is waiting for messages
        await asyncio.gather(cp.start(), cp.send_boot_notification(), cp.send_heartbeats())


if __name__ == '__main__':
    # specify host and port and run forever, will raise an error if the
    # server is not found
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(hostname="ec2-18-192-214-51.eu-central-1.compute.amazonaws.com", port=8000))
    loop.run_forever()
