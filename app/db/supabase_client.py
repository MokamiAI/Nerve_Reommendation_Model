import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL1")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY1")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError(
        "Supabase credentials missing. "
        "Check SUPABASE_URL1 and SUPABASE_SERVICE_ROLE_KEY1"
    )

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
