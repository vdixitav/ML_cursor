from ML_cursor.graph.state import GraphState
from ML_cursor.agents.eda_agent import EDAAgent


def dea_node(state: GraphState) -> GraphState:
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