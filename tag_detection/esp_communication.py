import asyncio
import websockets

esp32_ip = "ws://192.168.4.1/CarInput"  # Replace with your ESP32's IP address

async def send_two_values(key, value1, value2):
    async with websockets.connect(esp32_ip) as websocket:
        message = f"{key},{value1},{value2}"
        await websocket.send(message)
        print(f"Sent: {message}")
        await asyncio.sleep(0.001)

if __name__ == "__main__":
    asyncio.run(send_two_values("MoveCar", 1, 0))
