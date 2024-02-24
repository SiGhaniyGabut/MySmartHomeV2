import time, asyncio
from localtime import LocalTime

async def iteration():
    a = 0
    while True:
        await asyncio.sleep(1)

        a += 1

        print(a)

async def say_it_louder():
    while True:
        await asyncio.sleep(0.3)
        print("My Smart Home is running...")

class MySmartHome:
    def __init__(self, config):
        self.config = config
        self.localtime = LocalTime(self.config['timezone_offset'])
    
    def run(self):
        # Set NTP Time
        self.__set_local_ntp_time()
        # Start Modules
        asyncio.run(self.__start_modules())

    def __set_local_ntp_time(self):     
        try:
            self.localtime.set_time()
        except:
            print("NTP Server not connected...")
            time.sleep(2)

            # Retry to set NTP Time using recursive function.
            self.__set_local_ntp_time()

    async def __start_modules(self):
        asyncio.create_task(iteration())
        asyncio.create_task(say_it_louder())

        while True: await asyncio.sleep(0.01)