from fastapi import FastAPI

from backend.app.schemas import RiskRequest, RiskResponse, Explanation
from backend.app.utils.feature_builder import build_probability_features
from backend.app.inference.probability import predict_probability
from backend.app.inference.risk_logic import probability_to_level, fuse_risk



app = FastAPI(
    title="Road Accident Risk Prediction API",
    version="1.0"
)

# -----------------------------
# Health check
# -----------------------------
@app.get("/health")
def health():
    return {"status": "ok"}


# -----------------------------
# Risk prediction
# -----------------------------
@app.post("/predict-risk", response_model=RiskResponse)
def predict_risk(payload: RiskRequest):

    X = build_probability_features(payload.dict())

    prob = predict_probability(X)
    prob_level = probability_to_level(prob)
    risk_level = fuse_risk(prob_level)

    explanation = Explanation(
        key_factors=[
        f"Hour {payload.hour}",
        f"Weather {payload.weather_condition}"
        if payload.weather_condition else "Weather unknown",
        f"Speed limit {payload.speed_limit}"
        if payload.speed_limit else "Speed limit unknown",
    ],
    model_confidence="High"
        
    )

    return RiskResponse(
        probability_score=round(prob, 4),
        probability_level=prob_level,
        risk_level=risk_level,
        severity_context="Moderate (global prior)",
        explanation=explanation
    )
