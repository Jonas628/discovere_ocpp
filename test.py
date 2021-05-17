from time import sleep


# Websocket consumer


class Connection:
    def __init__(self):
        self._handler = Handler(self)

    def receive(self, message):
        print("")
        print("received: {0}".format(message))
        self._handler.route(message)

    def send(self, message):
        print("Empfangene Message: {0}".format(message))


# ChargePoint_Base
class BaseHandler:
#    def __init__(self, connection):
#        self._connection = connection

    def route(self, message):
        if "x" in message:
            message = "No answer"
            self.send(message)
        else:
            message = message + "!!!"
            self.send(message)

    def send(self, message):
        print("Base-Message: {0}".format(message))


# ChargePoint
class Handler(BaseHandler):
    def __init__(self, connection):
        self._connection = connection

    def send(self, message):
        self._connection.send(message)


"""
    def route(self, message):
        if "x" in message:
            message = "No answer"
            self._connection.send(message)
        else:
            message = message + "!!!"
            self._connection.send(message)
"""

def main():
    object = [{"model": "cp_handler.idtaginfo", "pk": 1, "fields": {
	            "expiry_date": "2021-06-28T22:21:36Z",
	            "parent_id_tag": "AAAAAAAAAAAAAAAA",
	            "status": "AuthorizationStatus.accepted"}}]
    print(object)


    connection = Connection()
    connection.receive("test")
    sleep(2)
    connection.receive("xts")
    sleep(2)
    connection.receive("test")
    sleep(2)


if __name__ == '__main__':
    main()
