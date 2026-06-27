from supabase import AsyncClient

from datetime import datetime, timedelta, timezone

class ATRepository:
    def __init__(self, supabase_client: AsyncClient):
        self.database = supabase_client
    
    async def upsert_vehicle_locations(self, data: list):
        response = await (self.database.table("realtime_vehicles")
                    .upsert(data).execute())
        
    async def clean_vehicle_locations(self):
        cutoff = datetime.now(timezone.utc) - timedelta(minutes=1)
        cutoff_iso = cutoff.isoformat()
        response = await (self.database.table("realtime_vehicles")
                    .delete().lt("last_updated", cutoff_iso).execute())
        
    async def get_vehicle_locations(self) -> list:
        response = await (self.database.table("realtime_vehicles")
                    .select("*").execute())
        return response.data