# Feature importance / SHAP

from typing import Dict, Any

import pandas as pd
import numpy as np

from ML_cursor.core.policy import enforce
from ML_cursor.core.artifacts import save_json
from ML_cursor.core.logger import get_logger
from ML_cursor.core.state import MLState


class ExplainAgent:
    """
    Explainability agent.

    - Extracts feature importance
    - Supports linear & logistic models
    - Saves explainability artifacts
    """

    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)

    def run(
        self,
        model,
        X: pd.DataFrame
    ) -> Dict[str, Any]:

        enforce("explain_model")
        self.logger.info("Starting model explainability")

        if model is None:
            raise ValueError("Model is None")

        if X is None or X.empty:
            raise ValueError("Feature data is empty or None")

        if not hasattr(model, "coef_"):
            raise ValueError(
                "Model does not expose coefficients. "
                "SHAP/LIME support can be added later."
            )

        coefficients = model.coef_

        # Handle binary classification vs regression
        if coefficients.ndim == 2:
            coefficients = coefficients[0]

        feature_importance = {
            feature: float(weight)
            for feature, weight in zip(X.columns, coefficients)
        }

        explanation = {
            "model_type": model.__class__.__name__,
            "num_features": len(feature_importance),
            "feature_importance": feature_importance
        }

        artifact = save_json(
            name="model_explanation.json",
            payload=explanation,
            step=MLState.EXPLAIN.value,
            description="Model feature importance explanation"
        )

        self.logger.info(
            "Explainability completed. Explanation saved at %s",
            artifact.path
        )

        return explanation
