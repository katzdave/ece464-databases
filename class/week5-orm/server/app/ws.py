from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()

# room_code -> set of connected websockets
_connections: dict[str, set[WebSocket]] = {}


async def broadcast(room_code: str, message: dict):
    dead: list[WebSocket] = []
    for ws in _connections.get(room_code, set()):
        try:
            await ws.send_json(message)
        except Exception:
            dead.append(ws)
    for ws in dead:
        _connections[room_code].discard(ws)
    if room_code in _connections and not _connections[room_code]:
        del _connections[room_code]


@router.websocket("/ws/{room_code}")
async def room_websocket(websocket: WebSocket, room_code: str):
    await websocket.accept()
    _connections.setdefault(room_code, set()).add(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            # Echo to all clients in the room
            await broadcast(room_code, data)
    except WebSocketDisconnect:
        _connections[room_code].discard(websocket)
        if not _connections[room_code]:
            del _connections[room_code]
