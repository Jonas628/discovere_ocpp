import asyncio
import logging

import websockets
from websockets.client import WebSocketClientProtocol

logging.basicConfig(level=logging.INFO)


async def consumer_handler(websocket: WebSocketClientProtocol) -> None:
    # iterate over asynchronous iterator, websocket "generates" the messages
    async for message in websocket:
        log_message(message)


async def consume(hostname: str, port: int) -> None:
    websocket_resource_url = f"ws://{hostname}:{port}"
    # open the connection with a websocket
    async with websockets.connect(websocket_resource_url) as websocket:
        # awaiting connect yields a WebSocketClientProtocol which can be
        # used to send and receive messages
        await consumer_handler(websocket)


def log_message(message: str) -> None:
    logging.info(f"> {message}")


if __name__ == '__main__':
    # specify host and port and run forever, will raise an error if the
    # server is not found
    loop = asyncio.get_event_loop()
    loop.run_until_complete(consume(hostname='localhost', port=3000))
    loop.run_forever()
