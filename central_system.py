import asyncio
import websockets
import logging
from pathlib import Path
from datetime import datetime
from ocpp.routing import on
from ocpp.v16 import ChargePoint as cp
from ocpp.v16.enums import Action, RegistrationStatus
from ocpp.v16 import call_result

p = Path().resolve()
logging.basicConfig(filename=str(p/'log'/'debug.log'), level=logging.INFO,
                    format='# %(levelname)s # %(asctime)s: %(message)s')

transaction_id = 0


class ChargePoint(cp):  # digital twin
    @on(Action.BootNotification)
    async def on_boot_notification(self, charge_point_vendor, charge_point_model, **kwargs):
        logging.info(f"Boot notification from charge point model {charge_point_model} "
                     f"from vendor {charge_point_vendor}.")
        return call_result.BootNotificationPayload(
            current_time=datetime.utcnow().isoformat(),
            interval=10,
            status=RegistrationStatus.accepted
        )

    @on(Action.StatusNotification)
    async def on_status_notification(self, connector_id, error_code, status, **kwargs):
        logging.info("received status notification. \n"
                     f"connector_id: {connector_id} \n"
                     f"error_code: {error_code} \n"
                     f"status: {status}")
        return call_result.StatusNotificationPayload()

    @on(Action.Heartbeat)
    async def on_heartbeat(self):
        current_time = str(datetime.utcnow())
        logging.info(f"received heartbeat at {current_time}")
        return call_result.HeartbeatPayload(current_time=current_time)

    @on(Action.StartTransaction)
    async def on_start_transaction(self, connector_id, id_tag, meter_start, timestamp):
        global transaction_id
        logging.info(f"received start transaction request at {timestamp}. \n"
                     f"connector_id: {connector_id} \n"
                     f"id_tag: {id_tag} \n"
                     f"meter_start: {meter_start}")
        transaction_id += 1  # count all transactions
        return call_result.StartTransactionPayload(transaction_id=transaction_id, id_tag_info={"status": "Accepted"})

    @on(Action.StopTransaction)
    async def on_stop_transaction(self, meter_stop, timestamp, transaction_id):
        logging.info(f"received stop transaction request at {timestamp}. \n"
                     f"transaction_id: {transaction_id} \n"
                     f"meter_stop: {meter_stop}")
        return call_result.StopTransactionPayload()

    @on(Action.MeterValues)
    async def on_meter_value(self, connector_id, transaction_id, meter_value):
        logging.info(meter_value)
        return call_result.MeterValuesPayload()


async def on_connect(websocket, path):
    """ For every new charge point that connects, create a ChargePoint instance
    and start listening for messages. """
    charge_point_id = path.strip('/')
    cp = ChargePoint(charge_point_id, websocket)
    logging.info(f"new websocket connection: {websocket}")
    logging.info(f"charge point {charge_point_id} connected! \n")

    await cp.start()


async def main():
    server = await websockets.serve(
        on_connect,
        '0.0.0.0',
        8000,
        subprotocols=['ocpp1.6']
    )

    await server.wait_closed()


if __name__ == '__main__':
    asyncio.run(main())
