from supabase import Client

class ATRepository:
    def __init__(self, supabase_client: Client):
        self.database = supabase_client
    
    def upsert_vehicle_locations(self, data: list):
        response = (self.database.table("Vehicle Positions")
                    .upsert(data).execute())
        
    def get_vehicle_locations(self) -> list:
        response = (self.database.table("Vehicle Positions")
                    .select("*").execute())
        return response.data