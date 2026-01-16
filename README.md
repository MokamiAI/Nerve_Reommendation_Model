# Insurance Recommendation Engine

A FastAPI-based insurance recommendation engine that scores and recommends
insurance products based on user needs and affordability.

## Features
- Needs-based scoring engine
- Supabase-backed product storage
- Clean architecture (DB separated from logic)
- FastAPI REST API

## Run locally
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
