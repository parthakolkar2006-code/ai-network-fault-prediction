"""WebSocket route endpoint."""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from .connection_manager import manager

ws_router = APIRouter()

@ws_router.websocket("/ws/live")
async def websocket_live_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    from ..main import global_state
    # Send immediate latest snapshot upon connection
    if global_state.get("latest_telemetry"):
        await websocket.send_json({
            "type": "SNAPSHOT",
            "telemetry": global_state.get("latest_telemetry"),
            "prediction": global_state.get("latest_prediction"),
            "alerts": global_state.get("latest_alerts", [])
        })
    try:
        while True:
            # Keep connection open and receive any client pings
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception:
        manager.disconnect(websocket)
