import asyncio
import json
from asyncio import sleep

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.generic.websocket import AsyncJsonWebsocketConsumer

import logging
from datetime import datetime
from ocpp_d.routing import on
from ocpp_d.v16 import ChargePoint as cp
from ocpp_d.v16.enums import Action, RegistrationStatus, AuthorizationStatus, AvailabilityType, ResetType
from ocpp_d.v16 import call_result, call

from cp_handler.models.models import IdTagInfo, ChargePoint, IdTag, ChargingStation
from cp_handler.models.serializers import IdTagInfoSerializer
from cp_handler.operation_handlers.authorize import handle_authorize
from cp_handler.operation_handlers.boot_notification import handle_boot_notification
from cp_handler.operation_handlers.status_notification import handle_status_notification
from enums import enums
from enums.enums import PhaseRotation

transaction_id = 0


class ConsumerMap():
    def __init__(self):
        self.map = {}

    def add_consumer(self, consumer):
        self.map[consumer.get_cp_id()] = consumer
        print("Added new consumer to map with ID: {0}".format(consumer.get_cp_id()))

    def remove_consumer(self, cp_id, consumer=None):
        del self.map[cp_id]

    def get_consumer(self, cp_id):
        print("Get Consumer with CP-ID {0}".format(self.map[cp_id]._charge_point.id))
        return self.map[cp_id]

    def get_cp_id(self, consumer):
        return {v == consumer for (k, v) in self.map.items()}


consumer_map = ConsumerMap()


class CPConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ToDo implement charge_point_id dynamically (used for logging in OCPP)
        self._cp_id="CP_1"
        self._charge_point = ChargePointClass(charge_point_id="CP_1", consumer=self)

    def get_cp_id(self):
        return self._cp_id

    """ For every new charge point that connects, create a ChargePoint instance
        and start listening for messages. """
    async def connect(self):
        # scope provides meta data
        path = self.scope["path"]
        charge_point_id = path.strip('/')
        print("CP-ID: {0}".format(charge_point_id))
        self._charge_point.set_cp_id(charge_point_id)
        self._cp_id=charge_point_id
        consumer_map.add_consumer(self)

        subprotocols = self.scope["subprotocols"]
        print("sub-protocol: {0}".format(subprotocols[0]))
        print("headers: {0}".format(self.scope["headers"]))
        #print("headers: {0}".format(self.scope["method"]))

        print("new chargepoint created")
        await self.accept(subprotocols[0])
        print("WS-connection accepted with subprotocol {0}".format(subprotocols))

    async def disconnect(self, close_code):
        print("-----------disconnect-------------")

    async def receive(self, text_data=None, bytes_data=None):
        print("")
        print("text_data: {0}".format(text_data))
        await self._charge_point.route_message(text_data)

        """
        await sleep(2)
        print("send message to CP")
        #payload = call.ChangeAvailabilityPayload(connector_id=1, type=AvailabilityType.operative)
        payload = call.ResetPayload(type=ResetType.soft)
        print(payload)
        response = await self._charge_point.call(payload)
        print(response)
        """

    # ToDo: re-implement send-method from consumer with logging (similar as OCPP)
    # async def send(self, text_data=None, bytes_data=None, close=False):
    #    pass


# digital twin
class ChargePointClass (cp):
    def __init__(self, charge_point_id, consumer):
        super().__init__(id=charge_point_id, connection=consumer, response_timeout=30)
        # super().__init__(id=charge_point_id, connection=0, response_timeout=30)
        # self._consumer = consumer

    def set_cp_id(self, cp_id):
        self.id = cp_id

    async def send(self, message):
        # ToDo: check data format (JSON?)
        # await self._consumer.send(text_data=message)
        await self._connection.send(message)

    """
    CALL_RESULT
    """
    @on(Action.Authorize)
    async def on_authorize(self, id_tag):
        # ToDo: implement DB-connection for id_tags, id_tag_info
        # primary-key = idTag; attributes : expiryDate, parentIdTag, status

        print("Authorize-request, id-Tag: {0}".format(id_tag))

        # ToDo check format of CP-ID: should it be a number or a string? Is there a prefix?
        cp_id = self.id[3:]
        print("ChargePoint ID: {0}".format(cp_id))

        return await handle_authorize(id_tag, cp_id)

    @on(Action.BootNotification)
    async def on_boot_notification(self, charge_point_vendor, charge_point_model, **kwargs):
        logging.info(f"Boot notification from charge point model {charge_point_model} "
                     f"from vendor {charge_point_vendor}.")

        return await handle_boot_notification(self.id, charge_point_vendor, charge_point_model, **kwargs)

    @on(Action.Heartbeat)
    async def on_heartbeat(self):
        current_time = str(datetime.utcnow())
        logging.info(f"received heartbeat at {current_time}")
        return call_result.HeartbeatPayload(current_time=current_time)

    @on(Action.MeterValues)
    async def on_meter_value(self, connector_id, transaction_id, meter_value):
        logging.info(meter_value)
        return call_result.MeterValuesPayload()

    @on(Action.StartTransaction)
    async def on_start_transaction(self, connector_id, id_tag, meter_start, timestamp):
        global transaction_id
        logging.info(f"received start transaction request at {timestamp}. \n"
                     f"connector_id: {connector_id} \n"
                     f"id_tag: {id_tag} \n"
                     f"meter_start: {meter_start}")
        transaction_id += 1  # count all transactions
        return call_result.StartTransactionPayload(transaction_id=transaction_id, id_tag_info={"status": "Accepted"})

    @on(Action.StatusNotification)
    async def on_status_notification(self, connector_id, error_code, status, **kwargs):
        logging.info("received status notification. \n"
                     f"connector_id: {connector_id} \n"
                     f"error_code: {error_code} \n"
                     f"status: {status}")

        return await handle_status_notification(connector_id, error_code, status, **kwargs)

    @on(Action.StopTransaction)
    async def on_stop_transaction(self, meter_stop, timestamp, transaction_id):
        logging.info(f"received stop transaction request at {timestamp}. \n"
                     f"transaction_id: {transaction_id} \n"
                     f"meter_stop: {meter_stop}")
        return call_result.StopTransactionPayload()

    """
    CALL
    """

    @on(Action.ChangeAvailability)
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
