from backend.app.config import MODERATE_T, HIGH_T, SEVERE_T


def probability_to_level(prob: float) -> str:
    if prob >= SEVERE_T:
        return "Very High"
    elif prob >= HIGH_T:
        return "High"
    elif prob >= MODERATE_T:
        return "Moderate"
    else:
        return "Low"


def fuse_risk(probability_level: str) -> str:
    if probability_level == "Very High":
        return "Severe"
    elif probability_level == "High":
        return "High"
    elif probability_level == "Moderate":
        return "Moderate"
    else:
        return "Low"
