from fastapi import FastAPI
from pydantic import BaseModel
from recommender.retrieval import recommend_assessments

app = FastAPI(title="SHL Assessment Recommendation API")


class QueryRequest(BaseModel):
    query: str


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/recommend")
def recommend(request: QueryRequest):
    results = recommend_assessments(request.query, top_k=10)

    response = {
        "recommended_assessments": []
    }

    for r in results:
        response["recommended_assessments"].append({
            "name": r.get("name", ""),
            "url": r.get("url", ""),
            "description": r.get("description", ""),
            "duration": r.get("duration", ""),
            "adaptive_support": r.get("adaptive_support", ""),
            "remote_support": r.get("remote_support", ""),
            "test_type": r.get("test_type", [])
        })

    return response
