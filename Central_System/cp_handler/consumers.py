from channels.generic.websocket import WebsocketConsumer

import json
from random import randint
from time import sleep


class WSConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

        for i in range(10):
            self.send(json.dumps({'message': randint(1, 100)}))
            sleep(1)

    class CPConsumer(WebsocketConsumer):
        def connect(self):
            # add condition statements before accepting
            self.accept()

            # self.send(json.dumps({'message': 'connected - wait for ocpp message'}))
            sleep(1)

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        return message

    # already implemented
    # def send(message)
    #
