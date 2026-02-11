# Controls full ML flow
from ML_cursor.core.logger import get_logger


class SupervisorAgent:
    """
    Suervisor agent decides next step
    based on EDA result
    """

    def __init__(self):
        self.logger=get_logger(self.__class__.__name__)

    def decide(self, state):
        self.logger.info("Supervisor analyzing EDA results to decide next steps")

        eda_result = state.artifacts.get("eda", {})

        total_missing = 0

    # Numeric columns
        numeric_summary = eda_result.get("numeric_summary", {})
        for col_data in numeric_summary.values():
            total_missing += col_data.get("missing", 0)

    # Categorical columns
        categorical_summary = eda_result.get("categorical_summary", {})
        for col_data in categorical_summary.values():
            total_missing += col_data.get("missing", 0)

        if total_missing > 0:
            self.logger.info("Supervisor decision: preprocess")
            return "preprocess"

        self.logger.info("Supervisor decision: train")
        return "train"
    





    