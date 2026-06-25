from supabase import AsyncClient

class ATRepository:
    def __init__(self, supabase_client: AsyncClient):
        self.database = supabase_client
    
    async def upsert_vehicle_locations(self, data: list):
        response = await (self.database.table("Vehicle Positions")
                    .upsert(data).execute())
        
    async def get_vehicle_locations(self) -> list:
        response = await (self.database.table("Vehicle Positions")
                    .select("*").execute())
        return response.data