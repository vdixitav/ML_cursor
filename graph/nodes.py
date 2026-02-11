from ML_cursor.graph.state import GraphState
from ML_cursor.agents.eda_agent import EDAAgent

from ML_cursor.agents.trainer_agent import TrainAgent


def eda_node(state: GraphState) -> GraphState:
    """
    Langgraph node wrappe for EDA agent

    """

    if state.data is None:
        state.errors.append("no data found in Graphstate")
        return state
    
    agent=EDAAgent()
    result=agent.run(state.data)


    # store result inside graph state

    state.artifacts["eda"]=result

    return state

def train_node(state: GraphState) -> GraphState:
    """
    langgraph node wrapper for TarinAgent.
    
    """

    if state.data is None:
        state.errors.append("No data available for training")
        return state

    if state.target is None:
        state.errors.append("Target column not specified")
        return state

    agent = TrainAgent()
    result = agent.run(state.data, state.target)

    state.artifacts["train"] = result

    return state

    