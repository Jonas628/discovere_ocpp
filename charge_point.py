import asyncio
import websockets
import datetime
import time
from ocpp.v16 import call, ChargePoint as cp
from ocpp.v16.enums import RegistrationStatus


class ChargePoint(cp):
    async def send_boot_notification(self):
        request = call.BootNotificationPayload(
            charge_point_model="Optimus",
            charge_point_vendor="The Mobility House"
        )

        response = await self.call(request)

        if response.status ==  RegistrationStatus.accepted:
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


async def main():
    async with websockets.connect(
        'ws://localhost:8000/CP_1',
         subprotocols=['ocpp1.6']
    ) as ws:

        cp = ChargePoint('CP_1', ws)

        await asyncio.gather(cp.start(),
                             cp.send_boot_notification(),
                             cp.send_heartbeats())


if __name__ == '__main__':
    asyncio.run(main())