from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.schemas.recommendation import (
    RecommendationInput,
    RecommendationResponse
)
from app.recommendation.needs_engine import recommend_policies

app = FastAPI(
    title="Insurance Recommendation Engine",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/recommend", response_model=RecommendationResponse)
def recommend(input: RecommendationInput):
    try:
        result = recommend_policies(input.dict())
        return {"recommended_policies": result["recommended_policies"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
