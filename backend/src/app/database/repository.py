from supabase import AsyncClient
import asyncio
from datetime import datetime, timedelta, timezone

class ATRepository:
    def __init__(self, supabase_client: AsyncClient):
        self.database = supabase_client

    async def _upsert_realtime_trips(self, data: list):
        response = await (self.database.table("realtime_trips")
                    .upsert(data).execute())
    
    async def _upsert_realtime_vehicles(self, data: list):
        response = await (self.database.table("realtime_vehicles")
                    .upsert(data).execute())

    async def _upsert_realtime_alerts(self, data: list):
        response = await (self.database.table("realtime_alerts")
                    .upsert(data).execute())
        
    async def _clean_realtime_trips(self, cutoff_iso):
        response = await (self.database.table("realtime_trips")
                    .delete().lt("updated_at", cutoff_iso).execute())
        
    async def _clean_realtime_vehicles(self, cutoff_iso):
        response = await (self.database.table("realtime_vehicles")
                    .delete().lt("updated_at", cutoff_iso).execute())
    
    async def _clean_realtime_alerts(self, cutoff_iso):
        response = await (self.database.table("realtime_alerts")
                    .delete().lt("updated_at", cutoff_iso).execute())
    
    async def upsert_realtime_data(self, data: list):
        await asyncio.gather(
            self._upsert_realtime_trips(data[0]),
            self._upsert_realtime_vehicles(data[1]),
            self._upsert_realtime_alerts(data[2])
        )

    async def clean_realtime_data(self):
        cutoff = datetime.now(timezone.utc) - timedelta(minutes=1)
        cutoff_iso = cutoff.isoformat()

        await asyncio.gather(
            self._clean_realtime_trips(cutoff_iso),
            self._clean_realtime_vehicles(cutoff_iso),
            self._clean_realtime_alerts(cutoff_iso)
        )

    async def get_view_realtime_vehicles(self):
        response = await (self.database.table("view_realtime_vehicles")
                    .select("*").execute())
        return response.data
    
    async def get_view_static_stops(self):
        response = await (self.database.table("view_static_stops")
                    .select("*").execute())
        return response.data