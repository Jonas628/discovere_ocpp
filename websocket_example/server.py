import asyncio
import logging
import websockets
from websockets import WebSocketServerProtocol
logging.basicConfig(level=logging.INFO)


class Server:
    """distribute the messages sent by a producer to all listening consumers """
    clients = set()

    async def register(self, websocket: WebSocketServerProtocol) -> None:
        self.clients.add(websocket)
        logging.info(f'Websocket on remote address {websocket.remote_address} is connected.')

    async def unregister(self, websocket: WebSocketServerProtocol) -> None:
        self.clients.remove(websocket)
        logging.info(f'Websocket on remote address {websocket.remote_address} is disconnected.')

    async def send_message_to_every_client(self, message_body: str) -> None:
        if self.clients:
            # asyncio.wait makes sure we only continue after every client has been sent the message
            await asyncio.wait([client.send(message_body) for client in self.clients])

    async def ws_handler(self, websocket: WebSocketServerProtocol, uri: str) -> None:
        """accept connecting clients and delegate the connection.
        this is called everytime the producer produces something.
        The consumer will stay connected, while the producer, on the other hand,
        unregisters himself after the message is sent
        """

        await self.register(websocket)  # add the client to the list of clients
        try:
            await self.send_message_out(websocket)  # send message to every client in list
        finally:
            await self.unregister(websocket)  # close the connection

    async def send_message_out(self, websocket: WebSocketServerProtocol) -> None:
        async for message_body in websocket:
            await self.send_message_to_every_client(message_body)


if __name__ == '__main__':
    server = Server()
    # The WebSocket’s serve function is a wrapper around the event loop’s
    # create_server() method. It creates and starts a server
    start_server = websockets.serve(server.ws_handler, "localhost", 3000)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_server)
    loop.run_forever()
