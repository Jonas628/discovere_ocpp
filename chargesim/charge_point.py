import asyncio
import websockets
from datetime import datetime
from ocpp.v16 import ChargePoint as cp
from ocpp.v16 import call
from ocpp.v16.enums import RegistrationStatus
import time
from base64 import b64encode


class ChargePoint(cp):
    """
    Charge point class which inherits from the OCPP python module's charge
    point. The parent class handles the sending and receiving of messages.
    This class adds some methods for sending messages and executing functions
    when a specific message is received
    """

    def __init__(self, id, connection, response_timeout=30):
        super().__init__(id, connection, response_timeout=response_timeout)
        self.power = float(11)
        self.status = "available"

    async def send_boot_notification(self):
        request = call.BootNotificationPayload(
            charge_point_model="Wallbox",
            charge_point_vendor="Discovere"
        )
        response = await self.call(request)
        if response.status == RegistrationStatus.accepted:
            print("Connected to central system.")

    async def send_heartbeats(self):
        while True:
            request = call.HeartbeatPayload()
            await self.call(request)
            await asyncio.sleep(1)

    async def send_meter_value(self, cid=1, tid=1):
        request = call.MeterValuesPayload(
            connector_id=cid,
            transaction_id=tid,
            meter_value=[{
                "timestamp": str(datetime.utcnow()),
                "sampledValue": [
                    {"measurand": "Power.Active.Import",
                     "phase": "N",
                     "unit": "kW",
                     "value": str(self.power)},
                    {"measurand": "Energy.Active.Import.Register",
                     "phase": "N",
                     "unit": "kWh",
                     "value": "0.00"}]}]
        )
        await self.call(request)

    async def charge(self, car):
        self.status = "charging"
        transaction_start = time.time()
        while car.soc < car.capacity*0.9:
            await asyncio.sleep(0.01)
            elapsed = 0.01 * car.timelapse
            car.soc += elapsed*self.power
            await self.send_meter_value()
        self.status = "available"


def basic_auth_header(charge_point_id):
    basic_credentials = b64encode(charge_point_id.encode()).decode()
    return 'Authorization', f'Basic {basic_credentials}'


async def main(username, password, hostname, port, charge_point_id="CP0001"):
    url = f"ws://{username}:{password}@{hostname}:{port}"
    # open the connection with a websocket
    async with websockets.connect(url, extra_headers=[basic_auth_header(charge_point_id)]) as websocket:
        cp = ChargePoint(charge_point_id, websocket)
        # when the charge point is started it is waiting for messages
        await asyncio.gather(cp.start(), cp.send_boot_notification(), cp.send_heartbeats())


if __name__ == '__main__':
    # specify host and port and run forever, will raise an error if the server is not found
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(hostname="0.0.0.0", port=8000))
    loop.run_forever()
