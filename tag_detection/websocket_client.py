import asyncio
import websockets

class WebSocketClient:
    def __init__(self, esp32_ip):
        self.esp32_ip = esp32_ip
        self.websocket = None

    async def connect(self):
        self.websocket = await websockets.connect(self.esp32_ip)
        print("Connected to WebSocket")

    async def disconnect(self):
        if self.websocket:
            await self.websocket.close()
            print("Disconnected from WebSocket")

    async def send_two_values(self, key, value1, value2):
        if self.websocket is None:
            raise Exception("WebSocket is not connected")
        message = f"{key},{value1},{value2}"
        await self.websocket.send(message)
        print(f"Sent: {message}")
        await asyncio.sleep(0.001)
    
    async def send_values(self, key, values):
        if self.websocket is None:
            raise Exception("WebSocket is not connected")
        message = f"{key}"
        for val in values:
            message+= f",{val}"
        await self.websocket.send(message)
        print(f"Sent: {message}")
        try:
            response = await asyncio.wait_for(self.websocket.recv(), timeout=0.1)
            print("Response: ", response)
            return response
        except:
            print("No response!")
            return None
        # await asyncio.sleep(0.1)



