# optional websocket client placeholder
import asyncio
import websockets

async def send_frame(uri, frame_bytes):
    async with websockets.connect(uri) as ws:
        await ws.send('frame')
