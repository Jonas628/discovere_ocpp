import websockets
import http
from websockets.headers import build_authorization_basic
from python_backend import DIR
import numpy as np

AUTHORIZATIONS = np.loadtxt(DIR/"protocol"/"authorizations.txt", dtype=str, delimiter=";")


class BasicAuthServerProtocol(websockets.WebSocketServerProtocol):

    async def process_request(self, path, request_headers):
        print("HTTP connection")
        try:
            authorization = request_headers['Authorization']
        except KeyError:
            return http.HTTPStatus.UNAUTHORIZED, [], b'Missing credentials\n'
        if not authorization in AUTHORIZATIONS:
            return http.HTTPStatus.FORBIDDEN, [], b'Incorrect credentials\n'


def build_authorizations():
    registered_charge_points = np.loadtxt(DIR/"protocol"/"registered_charge_points.txt", dtype=str, delimiter=" ")
    authorizations = []
    for cp in registered_charge_points:
        name = cp[0]
        password = cp[1]
        authorizations.append(build_authorization_basic(name, password))
    np.savetxt(DIR/"protocol"/"authorizations.txt", authorizations, fmt="%s")


def add_charge_point(name, password):
    registered_charge_points = np.loadtxt(DIR/"protocol"/"registered_charge_points.txt", dtype=str, delimiter=" ")
    new_charge_point = np.array([name, password], dtype=str)
    registered_charge_points = np.concatenate([registered_charge_points, new_charge_point])
    np.savetxt(DIR/"protocol"/"registered_charge_points.txt", registered_charge_points)
    build_authorizations()