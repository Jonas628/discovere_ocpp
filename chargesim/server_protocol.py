import websockets
import http
from websockets.headers import build_authorization_basic

USERNAME = 'foo'
PASSWORD = 'bar'
AUTHORIZATION = build_authorization_basic(USERNAME, PASSWORD)

class BasicAuthServerProtocol(websockets.WebSocketServerProtocol):

    async def process_request(self, path, request_headers):
        print("HTTP connection")
        try:
            authorization = request_headers['Authorization']
        except KeyError:
            return http.HTTPStatus.UNAUTHORIZED, [], b'Missing credentials\n'
        if authorization != AUTHORIZATION:
            return http.HTTPStatus.FORBIDDEN, [], b'Incorrect credentials\n'
