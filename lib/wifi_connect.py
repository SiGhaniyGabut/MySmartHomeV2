import network

class WiFiConnect:
    def __init__(self):
        self.wlan = network.WLAN(network.STA_IF)

    def start(self, ssid, password):
        if not self.is_connected():
            print('Connecting to network...')
            self.wlan.active(True)
            self.wlan.connect(ssid, password)
            while not self.is_connected(): pass

        print('Network Configured!')

    def config(self, value):
        return self.wlan.config(value)

    def ifconfig(self):
        return self.wlan.ifconfig()

    def is_connected(self):
        return self.wlan.isconnected()
