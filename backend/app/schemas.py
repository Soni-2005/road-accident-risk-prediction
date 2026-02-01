from pydantic import BaseModel, Field
from typing import List

class RiskRequest(BaseModel):
    latitude: float
    longitude: float
    hour: int = Field(ge=0, le=23)
    speed_limit: int

    road_type: str
    junction_detail: str
    urban_or_rural: str
    light_conditions: str


class Explanation(BaseModel):
    key_factors: List[str]
    model_confidence: str


class RiskResponse(BaseModel):
    probability_score: float
    probability_level: str
    risk_level: str
    severity_context: str
    explanation: Explanation
