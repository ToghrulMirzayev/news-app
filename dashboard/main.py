import redis
import json
import os
import asyncio
import websockets

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
redis_client = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)

connected_clients = set()


async def notify_clients(data):
    if connected_clients:
        await asyncio.gather(*[client.send(json.dumps(data)) for client in connected_clients])


async def websocket_handler(websocket):
    connected_clients.add(websocket)
    try:
        async for _ in websocket:
            print("Received a message from a client")
    finally:
        connected_clients.remove(websocket)
        print("Client disconnected")


def handle_message(message):
    data = json.loads(message["data"])
    if data.get("type") == "NEWS_UPDATE":
        asyncio.run_coroutine_threadsafe(notify_clients(data["data"]), loop)


pubsub = redis_client.pubsub()
pubsub.subscribe(**{"news-updates": handle_message})


async def start_websocket_server():
    print("Starting WebSocket server on ws://0.0.0.0:8765")
    start_server = await websockets.serve(websocket_handler, "0.0.0.0", 8765)
    await start_server.wait_closed()


async def main():
    pubsub.run_in_thread(sleep_time=0.01)

    await start_websocket_server()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
