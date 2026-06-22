from supabase import create_client, Client

import sys
from pathlib import Path
parent_dir = str(Path(__file__).resolve().parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

import config

def create_supabase_client() -> Client:
    return create_client(config.SUPABASE_URL, config.SUPABASE_SECRET_KEY)