Simple tutorial on websockets, taken from:
https://medium.com/better-programming/how-to-create-a-websocket-in-python-b68d65dbd549

server.py starts a websocket server that waits for clients to connect.
The server waits for messages and distributes them to all listening clients

consumer.py starts a client that is listening for messages

producer.py starts a client and send a single message to the server
