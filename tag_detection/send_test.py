import asyncio
import websockets

# Replace with the actual IP address of your ESP32
esp32_ip = "ws://192.168.4.1/CarInput"  # Replace with your ESP32's IP address

async def send_variable():
    async with websockets.connect(esp32_ip) as websocket:
        while True:
            # Example to control LED
            key = "MoveCar"
            value = 1 # Send 1 to turn the LED on, or 0 to turn it off
            value2 = "0"

            # Create the message in the format "Key,Value"
            message = f"{key},{value}"

            # Send the message to the ESP32
            await websocket.send(message)
            print(f"Sent: {message}")

            # Wait for 1 second before sending the next message
            await asyncio.sleep(1)

asyncio.run(send_variable())