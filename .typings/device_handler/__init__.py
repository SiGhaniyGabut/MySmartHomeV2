from collections import namedtuple
from wifi_connect import WiFiConnect
from async_websocket_client import AsyncWebsocketClient

class Message:
    """
    Message class for creating and parsing messages, used by Device Handler.

    Incoming or outgoing messages are parsed and created using this class.
    """

    MessageData = namedtuple('MessageData', ['event', 'topic', 'subject', 'payload'])
    """
    MessageData is a named tuple that contains the following fields:
    - event: str
    - topic: str
    - subject: str
    - payload: dict

    Used to wrap incoming parsed messages from the server.
    """

    @staticmethod
    def response(message: str) -> MessageData | None:
        """
        Parse incoming message from the server.
        """
        ...

    @staticmethod
    def request(event: str, topic: str, subject: str, payload: dict) -> str:
        """
        Create a message to be sent to the server.

        All outgoing payload messages injected with Auth Payload: API Key and MAC Address.
        """
        ...

    @staticmethod
    def auth_payload(api_key: str, mac: str) -> dict:
        """
        Create a payload for authentication.
        """
        ...

class DeviceHandler(Message):
    """
    Device Handler used to handle WebSocket communication with the server.
    """
    def __init__(self, url: str, api_key: str) -> None: ...

    async def connect(self, reconnect_in: int = 5, max_retries: int = 5, auth_wait_cycles: int = 10, auth_cycle_duration: int = 1) -> None:
        """
        Connect to the WebSocket server and authenticate the device.

        Max Retries and Auth Wait Cycles are used to handle connection and authentication retries.
        If the device is not authenticated after several cycles, the connection will be closed.

        Cycle Duration in Seconds.
        """
        ...

    async def publish(self, event: str, topic: str, subject: str, payload: dict = {}) -> None:
        """
        Send a message to the server.

        All outgoing payload messages injected with Auth Payload: API Key and MAC Address.
        """

    async def subscribe(self, callback) -> None:
        """
        Subscribe to the server's messages.

        This method will be called in a loop to receive messages from the server.
        If server closed the connection, the loop will be aborted.

        Callback must be passed as Async function.
        """
        ...

    async def run_forever(self, callback, reconnect_on_fail: bool = True, *args, **kwargs) -> None:
        """
        Run the WebSocket connection in a loop.

        This method will run:
        - Connect to the server
        - Authenticate the device
        - Subscribe to the server's messages

        If any of the steps failed, the loop will be aborted. Async Callback must be passed as handler of
        the incoming messages from the server.

        Args and Kwargs are Connect Function's arguments.
        """
        ...

    async def __authenticate(self, wait_cycles: int, cycle_duration: int) -> None:
        """
        Authenticate the device with the server.

        If the device is not authenticated after several cycles, the connection will be closed.

        Steps to authenticate the device:
        - Send a join message to the server
        - Wait for the server's response
        - If the device is authenticated, the loop will be aborted, `authenticated` props will be set to True.
        - If the device is not authenticated after several cycles, the connection will be closed.
        
        Cycle Duration in Seconds.
        """
        ...
    
    def __mac_parser(self, mac: bytes) -> str:
        """
        Parse the MAC Address from bytes (get from WiFiConnect.config('mac')).
        and return it as a string with format: "XX-XX-XX-XX-XX-XX"
        """
        ...
    
    def __request(self, event: str, topic: str, subject: str, payload: dict) -> str:
        """
        Wrap the message, inject the Auth Payload, and return it as a JSON string.
        """
        ...

    def __response(self, message: str | None) -> Message.MessageData | None:
        """
        Parse the incoming message from the server, and return it as a named tuple.
        """
        ...
