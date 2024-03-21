from uwebsockets import client

class WSClient:
    def __init__(self, url):
        self.url = url
        self.websocket = client.connect(url)
        self.is_connected = self.websocket.open

    def send(self, message):
        self.websocket.send(message)

    def receive(self):
        try:
            return self.websocket.recv()
        except:
            print('Error receiving message from the server. Connection closed...')
            self.is_connected = False
            self.close()

    def receive_forever(self, reconnect_on_fail=False, callback=None):
        while self.is_connected:
            message = self.receive()
            if message and callback: callback(message)
        else:
            if reconnect_on_fail:
                # Loop until reconnected
                while not self.is_connected:
                    self.close()
                    self.websocket = client.connect(self.url)
                    self.is_connected = self.websocket.open
                else:
                    self.receive_forever(reconnect_on_fail, callback)

    def close(self):
        self.websocket.close()
