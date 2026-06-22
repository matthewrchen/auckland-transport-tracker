import os
from dotenv import load_dotenv

load_dotenv()

AT_API_KEY = os.getenv("AT_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SECRET_KEY = os.getenv("SUPABASE_SECRET_KEY")