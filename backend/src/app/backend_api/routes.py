from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from backend_api.manager import websocket_manager

router = APIRouter()

@router.websocket("/ws/vehicles")
async def websocket_endpoint(websocket: WebSocket):
    await websocket_manager.connect(websocket)
    print("[ROUTE] User connected")

    try:
        repository = websocket.app.state.repository
        latest_vehicle_data = await repository.get_view_realtime_vehicles()
        latest_stop_data = await repository.get_view_static_stops()

        print("[ROUTE] Sending snapshot")
        await websocket.send_json({"type": "snapshot", "vehicles": latest_vehicle_data})
        await websocket.send_json({"type": "snapshot", "stops": latest_stop_data})

        while True:
            data = await websocket.receive_json()
            latest_trip_data = await repository.get_function_upcoming_trips(data["stop_id"])
            print(latest_trip_data)
    
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)

    except Exception as e:
        print(e)
        websocket_manager.disconnect(websocket)