import network

class WiFiConnect:
    def __init__(self, ssid, password):
        self.ssid = ssid
        self.password = password

    def start(self):
        sta_if = network.WLAN(network.STA_IF)
        if not sta_if.isconnected():
            print('Connecting to network...')
            sta_if.active(True)
            sta_if.connect(self.ssid, self.password)
            while not sta_if.isconnected(): pass

        print('Network Configurations:', sta_if.ifconfig())