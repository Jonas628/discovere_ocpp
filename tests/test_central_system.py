import asyncio
import websockets
from datetime import datetime
from ocpp.v16 import call, ChargePoint as cp
from ocpp.v16.enums import RegistrationStatus, ChargePointStatus, ChargePointErrorCode


### This script provides tests to proof the Central System (CS)
### Therefore this script simulates a charge point


def test_send_authorization(self):
    request = call.AuthorizePayload("1")
    x = self.call(request)
    print(x)


async def main():
    #async with websockets.connect(
    #    'ws://ec2-18-202-56-229.eu-west-1.compute.amazonaws.com:8000/CP_1',
    #     subprotocols=['ocpp1.6']
    #) as ws:

    async with websockets.connect(
        'ws://localhost:8000/CP_1',
         subprotocols=['ocpp1.6']
    ) as ws:

        cp = ChargePoint('CP_1', ws)

        print("chargePoint started")
        #await asyncio.cp.start()

        test_send_authorization(cp)


if __name__ == '__main__':
    asyncio.run(main())
