import asyncio
import websockets

async def test_websocket():
    uri = "ws://localhost:8000/ws/gpu"
    async with websockets.connect(uri) as websocket:
        while True:
            data = await websocket.recv()
            print("📡 Dados recebidos:", data)

asyncio.run(test_websocket())
