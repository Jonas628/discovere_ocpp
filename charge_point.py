import asyncio
import websockets
from datetime import datetime
from ocpp.v16 import call, ChargePoint as cp
from ocpp.v16.enums import RegistrationStatus, ChargePointStatus, ChargePointErrorCode


class ChargePoint(cp):
    async def send_boot_notification(self):
        request = call.BootNotificationPayload(
            charge_point_model="Optimus",
            charge_point_vendor="The Mobility House"
        )
        response = await self.call(request)
        if response.status == RegistrationStatus.accepted:
            print("Connected to central system.")

    async def send_status_notification(self):
        await asyncio.sleep(2)  # wait so status comes after boot notification
        request = call.StatusNotificationPayload(
            connector_id=1,
            error_code=ChargePointErrorCode.no_error,
            status=ChargePointStatus.available
        )
        await self.call(request)

    async def send_heartbeats(self):
        await asyncio.sleep(10)
        while True:
            await asyncio.sleep(10)
            request = call.HeartbeatPayload()
            await self.call(request)

    async def start_transaction(self):
        request = call.StartTransactionPayload(
            connector_id=1,
            id_tag="1",
            meter_start=0,
            timestamp=str(datetime.utcnow())
        )
        await self.call(request)

    async def stop_transaction(self):
        request = call.StopTransactionPayload(
            meter_stop=20,
            timestamp=str(datetime.utcnow()),
            transaction_id=1,  # is this the same as `id_tag` in `start_transaction()`?
        )
        await self.call(request)

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
                     "value": "11"},
                    {"measurand": "Energy.Active.Import.Register",
                     "phase": "N",
                     "unit": "kWh",
                     "value": "0.00"}]}]
        )
        await self.call(request)

    async def do_transaction(self):
        """
        send a start transaction, two meter values and a stop transaction
        """
        await asyncio.sleep(5)
        await self.start_transaction()
        await asyncio.sleep(1)
        # await self.send_meter_value()
        await asyncio.sleep(1)
        await self.stop_transaction()

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

        await asyncio.gather(cp.start(),
                             cp.send_boot_notification(),
                             cp.send_status_notification(),
                             cp.send_heartbeats(),
                             cp.do_transaction())


if __name__ == '__main__':
    asyncio.run(main())