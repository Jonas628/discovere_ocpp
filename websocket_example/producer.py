import asyncio
import websockets


async def produce(message: str, host: str, port: int) -> None:
    # connect to the websocket
    async with websockets.connect(f"ws://{host}:{port}") as websocket:
        await websocket.send(message)  # send the message to the server
        await websocket.recv()  # wait for response to be sure it was delivered


if __name__ == '__main__':
    # to produce a single message, run just once
    asyncio.run(produce(message="Hello", host="localhost", port=3000))
