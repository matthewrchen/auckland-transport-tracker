from supabase import acreate_client, AsyncClient
import config

async def create_supabase_client() -> AsyncClient:
    return await acreate_client(config.SUPABASE_URL, config.SUPABASE_SECRET_KEY)