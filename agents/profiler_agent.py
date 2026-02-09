# Dataset profiling

from typing import Dict,Any

import pandas as pd

from ML_cursor.core.policy import enforce
from ML_cursor.core.artifacts import save_json
from ML_cursor.core.logger import get_logger
from ML_cursor.core.state import  MLState 


class ProfilerAgent:
    """
Agent responsible for basic dataset profiling.

-Does not modify data
-Does not guess target or task
- produces a profiling artifacts fro downstream agents

"""


def __init__(self):
    self.logger=get_logger(self.__class__.__name__)

def run(self,df:pd.DataFrame)-> Dict[str,Any]:
    """
    Run dataset profiling.

    parameters

    df: pd.DtataFrame
        user-provided dataset

    Returns

    Dict[str,Any]
        Profiling summery    
    
    """

    enforce("profile_data")
    self.logger.info("Starting dataset profiling...")

    if df is None or df.empty:
        raise ValueError("Input dataframe is empty or None")
    

    profile={
        "rows": int(df.shape[0]),
        "coloumns": int(df.shape[1]),
        "coloumns_names": list(df.columns),
        "dtypes":{col: str(df[col].dtype) for col in df.columns},
        "missing_values": {col: int(df[col].isna().sum()) for col in df.columns},
        "duplicate_rows": int(df.duplicated().sum()),
    }

    artifact=save_json(
        name="data_profile.json",
        payload=profile,
        step=MLState.PROFILE.value,
        description="Basic dataset profiling results"
    )

    self.logger.info(f"Dataset profiling completed. Profile saved at {artifact.path}")


    return profile
