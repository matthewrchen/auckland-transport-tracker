from supabase import AsyncClient

from datetime import datetime, timedelta, timezone

class ATRepository:
    def __init__(self, supabase_client: AsyncClient):
        self.database = supabase_client

    async def upsert_realtime_trips(self, data: list):
        response = await (self.database.table("realtime_trips")
                    .upsert(data).execute())
    
    async def upsert_realtime_vehicles(self, data: list):
        response = await (self.database.table("realtime_vehicles")
                    .upsert(data).execute())
        
    async def clean_realtime_vehicles(self):
        cutoff = datetime.now(timezone.utc) - timedelta(minutes=1)
        cutoff_iso = cutoff.isoformat()
        response = await (self.database.table("realtime_vehicles")
                    .delete().lt("updated_at", cutoff_iso).execute())
        
    async def get_realtime_vehicles(self) -> list:
        response = await (self.database.table("realtime_vehicles")
                    .select("*").execute())
        return response.data
    
    async def upsert_realtime_alerts(self, data: list):
        response = await (self.database.table("realtime_alerts")
                    .upsert(data).execute())
        
    async def get_view_realtime_vehicles(self):
        response = await (self.database.table("view_realtime_vehicles")
                    .select("*").execute())
        return response.data