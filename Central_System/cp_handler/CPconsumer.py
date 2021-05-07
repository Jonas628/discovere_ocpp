#import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer

import logging
from pathlib import Path
from datetime import datetime
from ocpp.routing import on
from ocpp.v16 import ChargePoint as cp
from ocpp.v16.enums import Action, RegistrationStatus, AuthorizationStatus, AvailabilityType
from ocpp.v16 import call_result, call
#import websockets

import json
from time import sleep
#from datetime import datetime


class ChargePoint(cp):  # digital twin
    def __init__(self, consumer):
        self.cp_consumer = consumer

    async def start(self):
        while True:
            message = await self.cp_consumer.receive()
            #LOGGER.info('%s: receive message %s', self.id, message)
            if(message!=None):
                print("message")
                print(message)
            #await sleep(10)
            #await self.route_message(message)

    # send überschreiben
    async def send(self, message):
        self.cp_consumer.send(text_data=message)

    @on(Action.BootNotification)
    async def on_boot_notification(self, charge_point_vendor, charge_point_model, **kwargs):
        logging.info(f"Boot notification from charge point model {charge_point_model} "
                     f"from vendor {charge_point_vendor}.")
        return call_result.BootNotificationPayload(
            current_time=datetime.utcnow().isoformat(),
            interval=10,
            status=RegistrationStatus.accepted
        )


class CPConsumer(AsyncWebsocketConsumer):

    """ For every new charge point that connects, create a ChargePoint instance
        and start listening for messages. """
    async def connect(self):
        # just for test reasons
        path = self.scope["path"]
        charge_point_id = path.strip('/')
        print("path: {0}", charge_point_id)

        _cp = ChargePoint(consumer=self)
        print("new chargepoint created")

        await self.accept()
        print("new chargepoint started")

        await _cp.start()
        #self.send(json.dumps({'message': 'connected - wait for ocpp message'}))

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        return message

    # use send-method from base class:
    # async def send(self, text_data=None, bytes_data=None, close=False):


#if __name__ == '__main__':
#    main()
