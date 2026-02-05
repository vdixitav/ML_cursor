# ML state machine
from enum import Enum

class MLState(Enum):
    """
    Docstring for MLState: Representing high level phases of an ML workflow.
    Therse are PHASES , not blocking steps.
    Parallel execution is allowed within a phase.

    """

    INGEST= "INGEST" # data loading & basic checks
    PROFILE="PROFILE" # schema, nulls, stats
    EDA="EDA"         # exploratory analysis
    PREPROCESS="PREPROCESS"  # feature engineering, pipelines
    TRAIN="TRAIN"     # model training (parallel allowed)
    EVALUATE="EVALUATE"  # metrics, comparison
    EXPLAIN="EXPLAIN"  # feature importance / reasoning
    PACKAGE="PACKAGE" # model + artifacts packaging




