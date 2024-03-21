import network

class WiFiConnect:
    def __init__(self):
        pass

    def start(self, ssid, password):
        sta_if = network.WLAN(network.STA_IF)
        if not sta_if.isconnected():
            print('Connecting to network...')
            sta_if.active(True)
            sta_if.connect(ssid, password)
            while not sta_if.isconnected(): pass

        print('Network Configured!')

    def config(self, value):
        return network.WLAN(network.STA_IF).config(value)

    def ifconfig(self):
        return network.WLAN(network.STA_IF).ifconfig()
