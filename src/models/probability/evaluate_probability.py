import numpy as np
from sklearn.metrics import (
    recall_score,
    precision_score,
    roc_auc_score,
    average_precision_score,
    brier_score_loss,
    confusion_matrix,
)


def evaluate_probability_model(y_true, y_proba, threshold=0.5):
    """
    Evaluate probability model using domain-appropriate metrics.
    """

    y_pred = (y_proba >= threshold).astype(int)

    metrics = {
        "recall": recall_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, zero_division=0),
        "roc_auc": roc_auc_score(y_true, y_proba),
        "pr_auc": average_precision_score(y_true, y_proba),
        "brier_score": brier_score_loss(y_true, y_proba),
        "confusion_matrix": confusion_matrix(y_true, y_pred),
    }

    return metrics
