from typing import Dict, Any, List

import pandas as pd
import numpy as np

from ML_cursor.core.policy import enforce
from ML_cursor.core.artifacts import save_json
from ML_cursor.core.logger import get_logger
from ML_cursor.core.state import MLState


DEFAULT_PLACEHOLDERS = {"", " ", "NA", "N/A", "na", "unknown", "Unknown", "(null)", "(none)"}


class PreprocessAgent:
    """
    Agent responsible for deterministic data preprocessing.

    - Normalizes placeholders to NaN
    - Handles missing values via explicit strategies
    - Does NOT train models
    - Produces auditable preprocessing artifacts
    """

    def __init__(
        self,
        numeric_strategy: str = "median",   # options: mean | median | drop
        categorical_strategy: str = "mode", # options: mode | constant | drop
        categorical_constant: str = "UNKNOWN",
        placeholders: List[str] = None,
    ):
        self.logger = get_logger(self.__class__.__name__)
        self.numeric_strategy = numeric_strategy
        self.categorical_strategy = categorical_strategy
        self.categorical_constant = categorical_constant
        self.placeholders = set(placeholders) if placeholders else DEFAULT_PLACEHOLDERS

    def run(self, df: pd.DataFrame) -> Dict[str, Any]:
        enforce("build_proprocess_pipeline")
        self.logger.info("Starting preprocessing")

        if df is None or df.empty:
            raise ValueError("Input DataFrame is empty or None")

        df_clean = df.copy(deep=True)

        # 1) Normalize placeholders to NaN
        self.logger.info("Normalizing placeholders to NaN")
        for col in df_clean.columns:
            if df_clean[col].dtype == object:
                df_clean[col] = df_clean[col].apply(
                    lambda x: np.nan if isinstance(x, str) and x in self.placeholders else x
                )

        # 2) Split columns
        numeric_cols = df_clean.select_dtypes(include="number").columns.tolist()
        categorical_cols = df_clean.select_dtypes(exclude="number").columns.tolist()

        preprocessing_report = {
            "placeholders_normalized": sorted(list(self.placeholders)),
            "numeric_strategy": self.numeric_strategy,
            "categorical_strategy": self.categorical_strategy,
            "numeric_columns": numeric_cols,
            "categorical_columns": categorical_cols,
            "actions": [],
        }

        # 3) Handle numeric missing values
        for col in numeric_cols:
            missing_before = int(df_clean[col].isna().sum())
            if missing_before == 0:
                continue

            if self.numeric_strategy == "mean":
                fill_value = df_clean[col].mean()
                df_clean[col] = df_clean[col].fillna(fill_value)
                action = f"Filled NaN in numeric '{col}' with mean"
            elif self.numeric_strategy == "median":
                fill_value = df_clean[col].median()
                df_clean[col] = df_clean[col].fillna(fill_value)
                action = f"Filled NaN in numeric '{col}' with median"
            elif self.numeric_strategy == "drop":
                df_clean = df_clean.dropna(subset=[col])
                action = f"Dropped rows with NaN in numeric '{col}'"
            else:
                raise ValueError(f"Unsupported numeric strategy: {self.numeric_strategy}")

            preprocessing_report["actions"].append({
                "column": col,
                "type": "numeric",
                "missing_before": missing_before,
                "strategy": self.numeric_strategy,
                "action": action,
            })

        # 4) Handle categorical missing values
        for col in categorical_cols:
            missing_before = int(df_clean[col].isna().sum())
            if missing_before == 0:
                continue

            if self.categorical_strategy == "mode":
                mode_val = df_clean[col].mode(dropna=True)
                fill_value = mode_val.iloc[0] if not mode_val.empty else self.categorical_constant
                df_clean[col] = df_clean[col].fillna(fill_value)
                action = f"Filled NaN in categorical '{col}' with mode"
            elif self.categorical_strategy == "constant":
                df_clean[col] = df_clean[col].fillna(self.categorical_constant)
                action = f"Filled NaN in categorical '{col}' with constant '{self.categorical_constant}'"
            elif self.categorical_strategy == "drop":
                df_clean = df_clean.dropna(subset=[col])
                action = f"Dropped rows with NaN in categorical '{col}'"
            else:
                raise ValueError(f"Unsupported categorical strategy: {self.categorical_strategy}")

            preprocessing_report["actions"].append({
                "column": col,
                "type": "categorical",
                "missing_before": missing_before,
                "strategy": self.categorical_strategy,
                "action": action,
            })

        # 5) Save artifacts
        data_artifact = save_json(
            name="preprocessing_report.json",
            payload=preprocessing_report,
            step=MLState.PREPROCESS.value,
            description="Deterministic preprocessing actions and strategies"
        )

        # Save cleaned dataset separately (CSV)
        cleaned_path = save_json(
            name="preprocessed_preview.json",
            payload=df_clean.head(50).to_dict(orient="records"),
            step=MLState.PREPROCESS.value,
            description="Preview of preprocessed dataset (first 50 rows)"
        )

        self.logger.info(
            "Preprocessing completed. Report at %s; preview at %s",
            data_artifact.path, cleaned_path.path
        )

        return {
            "processed_data": df_clean,   # <-- THIS IS MISSING
        "rows_before": int(df.shape[0]),
        "rows_after": int(df_clean.shape[0]),
        "report": preprocessing_report,
}
