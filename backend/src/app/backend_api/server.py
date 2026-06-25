import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager

import at_api.client
import transformers.transformer
import database.client
import database.repository

from backend_api.manager import websocket_manager
from backend_api.routes import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.at_client = at_api.client.ATClient()

    supabase_client = await database.client.create_supabase_client()
    app.state.repository = database.repository.ATRepository(supabase_client)

    polling_task = asyncio.create_task(vehicle_polling(app))

    yield

    polling_task.cancel()
    await app.state.at_client.close()

app = FastAPI(lifespan=lifespan)

app.include_router(router)

async def vehicle_polling(app: FastAPI):
    while True:
        try:
            print("[POLLER] Making AT request")
            raw_data = await app.state.at_client.get_vehicle_locations()
            transformed_data = transformers.transformer.parse_vehicle_location_data(raw_data)

            print("[POLLER] Upsert to database")
            await app.state.repository.upsert_vehicle_locations(transformed_data)

            print("[POLLER] Sending data to users")
            payload = {"type": "live_update", "buses": transformed_data}
            await websocket_manager.broadcast_to_all(payload)
        except asyncio.CancelledError:
            break  
        except Exception as e:
            print("[POLLER] Exception: " + e)

        await asyncio.sleep(30)