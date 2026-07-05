from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from backend_api.manager import websocket_manager

router = APIRouter()

@router.websocket("/ws/vehicles")
async def websocket_endpoint(websocket: WebSocket):
    await websocket_manager.connect(websocket)
    print("[ROUTE] User connected")

    try:
        repository = websocket.app.state.repository
        latest_data = await repository.get_view_realtime_vehicles()

        print("[ROUTE] Sending snapshot")
        await websocket.send_json({"type": "snapshot", "vehicles": latest_data})

        while True:
            await websocket.receive_text()
    
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)

    except Exception as e:
        print(e)
        websocket_manager.disconnect(websocket)