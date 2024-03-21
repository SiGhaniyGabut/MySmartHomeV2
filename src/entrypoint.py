import time, asyncio, gc, machine
from localtime import LocalTime
from device_handler import DeviceHandler

class MessageHandler:
    def __init__(self):
        gc.collect()
        self.pins = {}

    async def listener(self, message):
        if not message: return

        for subject, handler in self.__subject_handlers().items():
            if message.subject == subject: handler(message.payload)

        await asyncio.sleep_ms(50)

    def __on_setup(self, payload):
        # Payload example:
        # {'switches': [{'pin': 2, 'pin_alias': 'D2', 'mode': 'OUT', 'state': 1, 'id': 1, 'active': True}]}
        for pin in payload['switches']:
            self.pins[pin['pin_alias']] = machine.Pin(pin['pin'], getattr(machine.Pin, pin['mode']), value=pin['state'])

    def __on_command(self, payload):
        # Payload example:
        # {'pin': 2, 'pin_alias': 'D2', 'mode': 'OUT', 'state': 1, 'id': 1, 'active': True}
        self.pins[payload['pin_alias']].value(payload['state'])

    def __on_restart(self, payload):
        # Payload example:
        # { 'status': 'success', 'message': 'Restart message has been sent to your device.' }
        print(payload['message'])
        machine.lightsleep(2000)
        machine.reset()

    def __subject_handlers(self):
        return { "setup": self.__on_setup, "command": self.__on_command, "restart": self.__on_restart }

class EntryPoint(MessageHandler):
    def __init__(self, config: dict):
        super().__init__()
        self.localtime = LocalTime(config['timezone_offset'])
        self.device_handler = DeviceHandler(config['device']['wss_url'], config['device']['api_key'])
        self.device_handler.
    
    def run(self):
        # Set NTP Time
        self.__set_local_ntp_time()
        # Start the device handler
        asyncio.run(self.device_handler.run_forever(self.listener))

    def __set_local_ntp_time(self):     
        try:
            self.localtime.set_time()
            print("NTP Server connected...")
            print("Local Time set to: ", self.localtime.strf_current_datetime())
        except:
            print("NTP Server not connected...")
            print("Retry to set NTP Time in 2 seconds...")
            time.sleep(2)

            # Retry to set NTP Time using recursive function.
            self.__set_local_ntp_time()
