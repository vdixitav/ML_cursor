# EDA logic

from typing import Dict,Any
import pandas as pd
from ML_cursor.core.policy import enforce
from ML_cursor.core.artifacts import save_json
from ML_cursor.core.logger import get_logger
from ML_cursor.core.state import MLState


class EDAAgent:
    """
    Agent is responsible for Exploratory Data Analysis (EDA)

    -does not train models
    -does not modify data
    - produces explainable, auditable EDA artifacts
    """


    def __init__(self):
        self.logger=get_logger(self.__class__.__name__)

    def run(self,df:pd.DataFrame)-> Dict[str,Any]:
        """"

        Run EDA on the given dataset.


        Parameters
        df: pd.DataFrame
            user-provided dataset


        Returns
        Dict[str,Any]
            EDA summery    
        
        
        
        
        """

        enforce("run_eda")
        self.logger.info("Starting EDA analysis")

        if df is None or df.empty:
            raise ValueError("Input DataFrame is empty or None")
        
        numeric_cols = df.select_dtypes(include="number").columns.tolist()
        categorical_cols = df.select_dtypes(exclude="number").columns.tolist()


        eda_summary = {
            "row_count": int(df.shape[0]),
            "column_count": int(df.shape[1]),
            "numeric_columns": numeric_cols,
            "categorical_columns": categorical_cols,
            "numeric_summary": {},
            "categorical_summary": {},
        }

        # Numeric EDA
        for col in numeric_cols:
            eda_summary["numeric_summary"][col] = {
                "mean": float(df[col].mean()),
                "median": float(df[col].median()),
                "std": float(df[col].std()),
                "min": float(df[col].min()),
                "max": float(df[col].max()),
                "missing": int(df[col].isna().sum()),
            }

        # Categorical EDA
        for col in categorical_cols:
            eda_summary["categorical_summary"][col] = {
                "unique_values": int(df[col].nunique()),
                "top_values": df[col].value_counts().head(5).to_dict(),
                "missing": int(df[col].isna().sum()),
            }

        artifact = save_json(
            name="eda_summary.json",
            payload=eda_summary,
            step=MLState.EDA.value,
            description="Exploratory data analysis summary"
        )
        self.logger.info(
            "EDA completed successfully. Artifact saved at %s",
            artifact.path
        )

        return eda_summary


