import asyncio
import websockets
from ocpp.v16 import ChargePoint as cp
from ocpp.v16 import call
from ocpp.v16.enums import RegistrationStatus


class ChargePoint(cp):
    """
    Charge point class which inherits from the OCPP python module's charge
    point. The parent class handles the sending and receiving of messages.
    This class adds some methods for sending messages and executing functions
    when a specific message is received
    """

    def __init__(self, id, connection, response_timeout=30):
        super().__init__(id, connection, response_timeout=response_timeout)

    async def send_boot_notification(self):
        request = call.BootNotificationPayload(
            charge_point_model="Optimus",
            charge_point_vendor="Orientsoftware"
        )
        response = await self.call(request)
        if response.status == RegistrationStatus.accepted:
            print("Connected to central system.")


async def main():
    async with websockets.connect('ws://localhost:9000/CP_1', subprotocols=['ocpp1.6']) as ws:
        cp = ChargePoint('CP_1', ws)
        # when the charge point is started it is waiting for messages
        await asyncio.gather(cp.start(), cp.send_boot_notification())


if __name__ == '__main__':
    while True:
        asyncio.run(main())
