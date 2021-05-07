import websockets
# from channels.generic.websocket import WebsocketConsumer


class WebsocketAdapter(websockets):
   # WebsocketConsumer:
   #__socket = None
    def __init__(self, socket):
        self.__socket = socket

    def send(self, message):
        self.__socket.send(message)

    def recv(self):
        self.__socket.receive()
