import binascii, json, asyncio
from collections import namedtuple
from wifi_connect import WiFiConnect
from async_websocket_client import AsyncWebsocketClient

class Message:
    MessageData = namedtuple('MessageData', ['event', 'topic', 'subject', 'payload'])

    @staticmethod
    def response(message: str | None) -> MessageData | None:
        try: return Message.MessageData(**json.loads(message))
        except: pass

    @staticmethod
    def request(event: str, topic: str, subject: str, payload: dict) -> str:
        if not isinstance(payload, dict): payload = {}
        return json.dumps({ 'event': event, 'topic': topic, 'subject': subject, 'payload': payload })

    @staticmethod
    def auth_payload(api_key: str, mac: str) -> dict:
        return { 'api_key': api_key, 'mac': mac }

class DeviceHandler(Message):
    def __init__(self, url: str, api_key: str) -> None:
        self.url = url
        self.api_key = api_key
        self.mac = self.__mac_parser(WiFiConnect().config('mac'))
        self.websocket = AsyncWebsocketClient()
        self.authenticated = False

    async def connect(self, reconnect_in: int = 5, max_retries: int = 720, auth_wait_cycles: int = 10, auth_cycle_duration: int = 1) -> None:
        retries = max_retries            

        while retries > 0:
            try:
                await self.websocket.handshake(self.url)

                while not await self.websocket.open():
                    if retries == 0: break

                    print(f'Connection failed. Retrying in {reconnect_in} seconds...')
                    await self.websocket.close()

                    # Wait for the next retry...
                    await asyncio.sleep(reconnect_in)
                    await self.websocket.handshake(self.url)

                    retries -= 1
                else:
                    print(f'Connected to {self.url}. Authenticating...')
                    await self.__authenticate(auth_wait_cycles, auth_cycle_duration)
                    break # outer loop if connection and authentication are successful
            except Exception as e:
                print(f'Internet connection failed. Reconnecting in {reconnect_in} seconds...')
                await asyncio.sleep(reconnect_in)
                retries -= 1
        else:
            print(f'Failed to connect to WebSocket server after {max_retries} retries.')

    async def publish(self, event: str, topic: str, subject: str, payload: dict = {}) -> None:
        await self.websocket.send(self.__request(event, topic, subject, payload))

    async def subscribe(self, callback) -> None:
        if not self.authenticated: return

        while await self.websocket.open():
            try: await callback(self.__response(await self.websocket.recv()))
            except Exception as e:
                print('Error receiving message from the server. Connection closed...', e)
                await self.websocket.close()
                break

    async def run_forever(self, callback, reconnect_on_fail: bool = True, *args, **kwargs) -> None:
        while reconnect_on_fail:
            if self.authenticated: self.authenticated = False # Reset the authentication status
            if not await self.websocket.open(): await self.connect(*args, **kwargs)

            # Abort the loop if the device is not authenticated
            if not self.authenticated: break

            await self.subscribe(callback)

    async def __authenticate(self, wait_cycles: int, cycle_duration: int) -> None:
        if self.authenticated: return
        await self.publish('join', f"devices:{self.mac}", "join")

        while not self.authenticated:
            # If the device is not authenticated after several cycles, force close the connection
            if wait_cycles == 0:
                print('Authentication cycle ended. Closing connection...')
                await self.websocket.close()
                break
            
            # Check closed connection for not authenticated device by several cycles
            if not await self.websocket.open():
                print('Server closed the connection due to authentication failure...')
                await self.websocket.close()
                break

            auth_response = self.__response(await self.websocket.recv())
            if auth_response and auth_response.subject == 'joined':
                self.authenticated = True
                print(auth_response.payload['message'])
                break

            # Wait for the next cycle...
            await asyncio.sleep(cycle_duration)
            wait_cycles -= 1
    
    def __mac_parser(self, mac: bytes) -> str:
        return binascii.hexlify(mac, "-").decode().upper()
    
    def __request(self, event: str, topic: str, subject: str, payload: dict) -> str:
        payload.update(DeviceHandler.auth_payload(self.api_key, self.mac))
        return DeviceHandler.request(event, topic, subject, payload)

    def __response(self, message: str | None) -> Message.MessageData | None:
        return DeviceHandler.response(message)
