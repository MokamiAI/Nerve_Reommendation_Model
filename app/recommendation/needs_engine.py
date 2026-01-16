from typing import Dict, List
from app.db.product_repository import fetch_active_products


def employment_risk_from_status(status: str) -> str:
    return {
        "Employed Full-time": "medium",
        "Employed Part-time": "medium",
        "Self-employed": "high",
        "Unemployed": "low",
        "Student": "low",
        "Retired": "low"
    }.get(status, "medium")


def score_product(product: Dict, profile: Dict) -> int:
    score = 0

    category = (product.get("category") or "").lower()
    premium = float(product.get("premium_amount") or 0)
    coverage = float(product.get("coverage_amount") or 0)
    income = float(profile.get("monthly_income") or 0)

    employment_risk = employment_risk_from_status(
        profile.get("employment_status")
    )

    if category == "life" and profile.get("dependants_count", 0) > 0:
        score += 40
    elif category == "accident" and employment_risk in ["medium", "high"]:
        score += 35
    elif category == "car" and profile.get("owns_car"):
        score += 40
    elif category == "funeral":
        score += 15

    if income > 0:
        affordability = premium / income
        if affordability <= 0.03:
            score += 25
        elif affordability <= 0.06:
            score += 15

    if premium > 0:
        value_ratio = coverage / premium
        if value_ratio >= 1000:
            score += 20
        elif value_ratio >= 600:
            score += 10

    if "age" in (product.get("eligibility") or "").lower():
        score += 10

    return min(score, 100)


def priority_band(score: int) -> str:
    if score >= 80:
        return "high"
    if score >= 60:
        return "medium"
    return "low"


def why_this_matters(
    category: str,
    score: int,
    profile: Dict,
    coverage: float,
    premium: float
) -> List[str]:

    reasons = []
    band = priority_band(score)
    category = category.lower()

    if category == "accident":
        reasons.append("Protects you from unexpected injury-related costs")
        if band == "high":
            reasons.append("Highly suitable given your work and activity level")

    elif category == "life":
        reasons.append("Ensures long-term financial protection")
        if profile.get("dependants_count"):
            reasons.append("Important for supporting your dependants")

    elif category == "car":
        reasons.append("Reduces financial risk related to vehicle ownership")

    elif category == "funeral":
        reasons.append("Helps reduce immediate financial burden on family")
        if premium == 0:
            reasons.append("No monthly cost required")

    if premium <= (profile.get("monthly_income", 0) * 0.05):
        reasons.append("Comfortably affordable based on your income")

    return reasons[:3]


def best_for_text(category: str) -> List[str]:
    return {
        "accident": ["Young professionals", "Working professionals"],
        "life": ["People with dependants", "Primary income earners"],
        "car": ["Vehicle owners", "Daily commuters"],
        "funeral": ["All households", "Budget-conscious families"]
    }.get(category.lower(), [])


def recommend_policies(profile: Dict) -> Dict:
    products = fetch_active_products()
    scored = []

    for product in products:
        s = score_product(product, profile)
        if s > 0:
            scored.append({"product": product, "score": s})

    if not scored:
        return {"recommended_policies": []}

    scored.sort(key=lambda x: x["score"], reverse=True)

    def format_output(item: Dict) -> Dict:
        p = item["product"]
        s = item["score"]

        return {
            "policy_type": p["product_name"],
            "company": p["provider"],
            "confidence_score": s,
            "priority_band": priority_band(s),
            "match_label": f"{s}% match",
            "description": p["description"],
            "best_for": best_for_text(p["category"]),
            "why_this_matches_you": why_this_matters(
                p["category"],
                s,
                profile,
                float(p["coverage_amount"]),
                float(p["premium_amount"])
            ),
            "coverage_amount": float(p["coverage_amount"]),
            "coverage_currency": "ZAR",
            "premium_amount": float(p["premium_amount"]),
            "premium_frequency": p["frequency"]
        }

    results = [format_output(scored[0])]
    if len(scored) > 1:
        results.append(format_output(scored[1]))

    return {"recommended_policies": results}
