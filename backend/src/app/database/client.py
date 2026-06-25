from supabase import acreate_client, AsyncClient

import sys
from pathlib import Path
parent_dir = str(Path(__file__).resolve().parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

import config

async def create_supabase_client() -> AsyncClient:
    return await acreate_client(config.SUPABASE_URL, config.SUPABASE_SECRET_KEY)