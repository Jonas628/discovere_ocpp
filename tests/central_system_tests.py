from chargesim.central_system import CentralSystem
from chargesim.charge_point import main
import threading
import websockets
import asyncio
server = CentralSystem()


def run_central_system(loop, host="0.0.0.0", port=2234):
    global server
    asyncio.set_event_loop(loop)
    start_server = websockets.serve(server.ws_handler, host, port)
    loop.run_until_complete(start_server)
    loop.run_forever()


def run_charge_point(loop, charge_point_id, host="0.0.0.0", port=2234):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main(hostname=host, port=port, charge_point_id=charge_point_id))
    loop.run_forever()


def test_charge_point_registration():
    """
    Every charge point should register in the clients attribute of the central system.
    For a successful registration, the charge point must provide a username & password which must be validated by
    the central system. If a charge point is stopped it should unregister. IDs should be unique, so registering
    two charge points with the same ID should yield an error.
    """
    host = "0.0.0.0"
    port = 2345
    central_system_loop = asyncio.new_event_loop()
    # run the central system in a thread
    central_system_thread = threading.Thread(target=run_central_system, args=(central_system_loop, host, port,))
    central_system_thread.start()
    # create charging stations, run them in threads and connect to the central system:
    charge_point_ids = ["CP001", "CP002", "CP003"]
    charge_point_loops, charge_point_threads = [], []
    for charge_point_id in charge_point_ids:
        charge_point_loops.append(asyncio.new_event_loop()) # make a new event loop
        charge_point_threads.append(  # run charge point with loop in a thread
            threading.Thread(target=run_charge_point, args=(charge_point_loops[-1], charge_point_id, host, port)))
        charge_point_threads[-1].start()
    # now check if all charge_point_ids are registered as clients on the server:
    client_ids = [client.id for client in server.clients]
    assert client_ids == charge_point_ids
