import asyncio
import websockets
import json

connected_clients = set()
loop = None

async def handler(websocket):
    print("Client terhubung:", websocket.remote_address)
    connected_clients.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        connected_clients.remove(websocket)
        print("Client terputus:", websocket.remote_address)

async def send_notification_to_clients(data):
    if not connected_clients:
        print("Tidak ada client yang terhubung.")
        return

    message = json.dumps({
        "title": "Pelanggaran Deteksi",
        "message": f"Terdeteksi: {data['class_name']}",
        "timestamp": data["timestamp"]
    })

    for ws in connected_clients.copy():
        try:
            await ws.send(message)
        except Exception as e:
            print("Gagal mengirim:", e)

def send_notification(data):
    global loop
    if loop is not None:
        asyncio.run_coroutine_threadsafe(
            send_notification_to_clients(data), loop
        )
    else:
        print("Loop belum tersedia, tidak bisa kirim notifikasi.")

async def start_server_main():
    global loop
    loop = asyncio.get_event_loop()
    server = await websockets.serve(handler, "0.0.0.0", 8080)
    print("WebSocket server berjalan di ws://0.0.0.0:8080")
    await server.wait_closed()
    
def set_loop(event_loop):
    global loop
    loop = event_loop