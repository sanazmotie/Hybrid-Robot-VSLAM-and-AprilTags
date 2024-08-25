import asyncio
import websockets

async def send_two_values(key, value1, value2):
    esp32_ip = "ws://192.168.4.1/CarInput"  # Replace with your ESP32's IP address
    async with websockets.connect(esp32_ip) as websocket:
        message = f"{key},{value1},{value2}"
        await websocket.send(message)
        print(f"Sent: {message}")

# If you want to run this file directly, you can add this:
if __name__ == "__main__":
    asyncio.run(send_two_values("LED", 1, 0))
