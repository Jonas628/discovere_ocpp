import asyncio
import websockets
import logging
from pathlib import Path
from datetime import datetime
from ocpp.routing import on
from ocpp.v16 import ChargePoint as cp
from ocpp.v16.enums import Action, RegistrationStatus, AuthorizationStatus, AvailabilityType
from ocpp.v16 import call_result, call

# import all sub-modules

p = Path().resolve()
logging.basicConfig(filename=str(p/'log'/'debug.log'), level=logging.INFO,
                    format='# %(levelname)s # %(asctime)s: %(message)s')

transaction_id = 0

id_tags = {"0123456789ABCDEF1234":
               {"expiry_date": datetime(2021, 4, 15, 23, 59, 59, 999999),
                "parent_id_tag": "AABBCCDDEEFF12345678",
                "status": AuthorizationStatus.accepted},
           "1123456789ABCDEF1234":
               {"expiry_date": datetime(2021, 4, 20, 23, 59, 59, 999999),
                "parent_id_tag": "AABBCCDDEEFF12345678",
                "status": AuthorizationStatus.accepted},
           }


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

    def post_id_tag(self, id_tag, id_tag_info):
        id_tags [id_tag] = id_tag_info

    @on(Action.Authorize)
    async def on_authorize(self, id_tag):
        # ToDo: implement DB-connection for id_tags, id_tag_info
        # better using a dictionary or a list of objects?
        # primary-key = idTag; attributes : expiryDate, parentIdTag, status


        print(id_tag)
        _id_tag_info = {"expiry_date": str(datetime(2021, 4, 15, 23, 59, 59, 999999)),
                        "parent_id_tag": "AABBCCDDEEFF12345678",
                        "status": AuthorizationStatus.expired}

        # invalid: Identifier is unknown. Not allowed for charging.
        authorization_status = AuthorizationStatus.invalid

        if id_tag in id_tags:
            _id_tag_info = id_tags[id_tag]

            # blocked: Identifier has been blocked. Not allowed for charging.
            if _id_tag_info["status"] == AuthorizationStatus.blocked:
                authorization_status = AuthorizationStatus.blocked

            # concurrent_tx: Identifier is already involved in another transaction and multiple transactions
            # are not allowed. (Only relevant for a StartTransaction.req.)
            elif _id_tag_info["status"] == AuthorizationStatus.concurrent_tx:
                authorization_status = AuthorizationStatus.concurrent_tx

            else:
                # accepted: Identifier is allowed for charging.
                if _id_tag_info["expiry_date"] > datetime.utcnow():
                    authorization_status = AuthorizationStatus.accepted

                # expired: Identifier has expired. Not allowed for charging.
                else:
                    authorization_status = AuthorizationStatus.expired

        _id_tag_info["status"] = authorization_status
        _id_tag_info["expiry_date"] = str(_id_tag_info["expiry_date"])
        return call_result.AuthorizePayload(id_tag_info=_id_tag_info)


    # @on(Action.ChangeAvailability)
    async def change_availability(self, connector_id, availability_type):
        # ToDo for ConnectorId = 0 the change applies to all connectors --> implement structur
        cps = {"CP01":
                    {"1": AvailabilityType.operative},
               "CP02":
                    {"1": AvailabilityType.inoperative}}

        # comparing availability_type with current availability_type
        if cps[self.id][connector_id].value != availability_type:
            call.ChangeAvailabilityPayload(connector_id=connector_id, type=availability_type)
            # async await

            # Inoperative: Charge point is not available for charging.

            # Operative: Charge point is available for charging.


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
