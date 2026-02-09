# Model training

from typing import Dict, Any

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.metrics import accuracy_score, r2_score

from ML_cursor.core.policy import enforce
from ML_cursor.core.artifacts import save_pickle, save_json
from ML_cursor.core.logger import get_logger
from ML_cursor.core.state import MLState


class TrainAgent:
    """
    Deterministic training agent.

    - Validates target column
    - Splits data
    - Trains baseline model
    - Saves model + metadata
    """

    def __init__(
        self,
        task_type: str = "classification",  # classification | regression
        test_size: float = 0.2,
        random_state: int = 42,
    ):
        self.logger = get_logger(self.__class__.__name__)
        self.task_type = task_type
        self.test_size = test_size
        self.random_state = random_state

    def run(self, df: pd.DataFrame, target_column: str) -> Dict[str, Any]:
        enforce("train_model")
        self.logger.info("Starting model training")

        if df is None or df.empty:
            raise ValueError("Input DataFrame is empty or None")

        if target_column not in df.columns:
            raise ValueError(f"Target column '{target_column}' not found")

        X = df.drop(columns=[target_column])
        y = df[target_column]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y,
            test_size=self.test_size,
            random_state=self.random_state
        )

        if self.task_type == "classification":
            model = LogisticRegression(max_iter=1000)
            model.fit(X_train, y_train)
            preds = model.predict(X_test)
            metric_value = accuracy_score(y_test, preds)
            metric_name = "accuracy"

        elif self.task_type == "regression":
            model = LinearRegression()
            model.fit(X_train, y_train)
            preds = model.predict(X_test)
            metric_value = r2_score(y_test, preds)
            metric_name = "r2_score"

        else:
            raise ValueError(f"Unsupported task type: {self.task_type}")

        # Save model
        model_artifact = save_pickle(
            name="trained_model.pkl",
            obj=model,
            step=MLState.TRAIN.value,
            description=f"{self.task_type} model trained"
        )

        # Save training metadata
        metadata = {
            "task_type": self.task_type,
            "target_column": target_column,
            "rows": df.shape[0],
            "features": list(X.columns),
            "metric": metric_name,
            "metric_value": metric_value,
            "test_size": self.test_size,
            "random_state": self.random_state,
        }

        metadata_artifact = save_json(
            name="training_metadata.json",
            payload=metadata,            
            step=MLState.TRAIN.value,
            description="Training configuration and results"
        )

        self.logger.info(
            "Training completed. %s = %.4f | Model saved at %s",
            metric_name, metric_value, model_artifact.path
        )

        return metadata
