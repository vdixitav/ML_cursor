from typing import Dict, Any

import pandas as pd
from sklearn.metrics import accuracy_score, r2_score

from ML_cursor.core.policy import enforce
from ML_cursor.core.artifacts import save_json
from ML_cursor.core.logger import get_logger
from ML_cursor.core.state import MLState


class EvaluateAgent:
    """
    Evaluation agent.

    - Evaluates trained model on test data
    - Computes metrics
    - Stores evaluation results
    """

    def __init__(self, task_type: str = "classification"):
        self.logger = get_logger(self.__class__.__name__)
        self.task_type = task_type

    def run(
        self,
        model,
        X_test: pd.DataFrame,
        y_test: pd.Series
    ) -> Dict[str, Any]:

        enforce("eveluate_model")
        self.logger.info("Starting model evaluation")

        if model is None:
            raise ValueError("Model is None")

        if X_test is None or y_test is None:
            raise ValueError("Test data is missing")

        preds = model.predict(X_test)

        if self.task_type == "classification":
            metric_name = "accuracy"
            metric_value = accuracy_score(y_test, preds)

        elif self.task_type == "regression":
            metric_name = "r2_score"
            metric_value = r2_score(y_test, preds)

        else:
            raise ValueError(f"Unsupported task type: {self.task_type}")

        evaluation_result = {
            "task_type": self.task_type,
            "metric": metric_name,
            "metric_value": metric_value,
            "rows_tested": int(len(y_test))
        }

        artifact = save_json(
            name="evaluation_metrics.json",
            payload=evaluation_result,
            step=MLState.EVALUATE.value,
            description="Model evaluation metrics"
        )

        self.logger.info(
            "Evaluation completed. %s = %.4f",
            metric_name, metric_value
        )

        return evaluation_result
