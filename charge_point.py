import asyncio
import websockets
from datetime import datetime

from ocpp_d.routing import on
from ocpp_d.v16 import call, ChargePoint as cp, call_result
from ocpp_d.v16.enums import RegistrationStatus, ChargePointStatus, ChargePointErrorCode, Action, ResetStatus


class TestChargePoint(cp):
    async def send_boot_notification(self):
        print("Boot-Notification")
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
        response = await self.call(request)
        print(response)

    async def send_heartbeats(self):
        while True:
            await asyncio.sleep(10)
            request = call.HeartbeatPayload()
            response = await self.call(request)
            print(response.current_time)

    async def send_authorize(self):
        request = call.AuthorizePayload(
            id_tag="0123456789ABCDEF1234"
            #id_tag="0000AAAA0000AAAA"
        )
        response = await self.call(request)
        print('Tried to authorize, got: {0}'.format(response.id_tag_info['status']))
        #print('Tried to authorize, got: {0}'.format(response.id_tag_info["status"]))

    async def start_transaction(self):
        request = call.StartTransactionPayload(
            connector_id=1,
            id_tag="1",
            meter_start=0,
            timestamp=str(datetime.utcnow())
        )
        response = await self.call(request)
        print('Start TransactionId {0} Status: {1}'.format(response.transaction_id, response.id_tag_info["status"]))

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
        await self.send_meter_value()
        await asyncio.sleep(1)
        await self.stop_transaction()

    """
    @on(Action.ChangeAvailability)
    async def change_availability(self, connector_id, availability_type):
        print("Change availability for connector {0}, to {1}".format(connector_id, availability_type))
        return 0

    """
    @on(Action.Reset)
    async def change_availability(self, type):
        print("Reset!!! Typ: {0}".format(type))
        response = call_result.ResetPayload(status=ResetStatus.accepted)
        print(response)
        return response
    #"""

async def main():
    async with websockets.connect(
        'ws://localhost:8000/CP_1/',
         subprotocols=['ocpp1.6']
    ) as ws:

        cp = TestChargePoint('10002', ws)

        await asyncio.gather(cp.start(),
                             cp.send_boot_notification(),
                             #cp.send_heartbeats(),
                             cp.send_authorize())

if __name__ == '__main__':
    asyncio.run(main())

"""
    #async with websockets.connect(
    #    'ws://ec2-18-202-56-229.eu-west-1.compute.amazonaws.com:8000/CP_1',
    #     subprotocols=['ocpp1.6']
    #) as ws:
"""

"""
                     cp.send_status_notification(),
                     cp.send_heartbeats(),
                     cp.do_transaction())
"""
