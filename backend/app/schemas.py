from pydantic import BaseModel, Field
from typing import List
from typing import Optional 

class RiskRequest(BaseModel):
    latitude: float
    longitude: float
    hour: int
    # Optional contextual features
    speed_limit: Optional[int] = None
    road_type: Optional[str] = None
    weather_condition: Optional[str] = None

class Explanation(BaseModel):
    key_factors: List[str]
    model_confidence: str


class RiskResponse(BaseModel):
    probability_score: float
    probability_level: str
    risk_level: str
    severity_context: str
    explanation: Explanation 
