from typing import Dict, List
from app.db.supabase_client import supabase


def fetch_active_products() -> List[Dict]:
    res = (
        supabase
        .table("insurance_products")
        .select(
            "product_name, provider, category, description, "
            "premium_amount, coverage_amount, frequency, eligibility"
        )
        .eq("active", True)
        .execute()
    )

    return res.data or []
