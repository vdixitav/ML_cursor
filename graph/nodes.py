from ML_cursor.graph.state import GraphState
from ML_cursor.agents.eda_agent import EDAAgent

from ML_cursor.agents.trainer_agent import TrainAgent
from ML_cursor.agents.supervisor import SupervisorAgent
from ML_cursor.agents.preprocess_agent import PreprocessAgent


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


# supervisor agent node

def supervisor_node(state: GraphState) -> str:
    """
    Supervisor node only logs decision.
    Does NOT return routing string.
    """
    supervisor=SupervisorAgent()
    decision =supervisor.decide(state)

    # store decision inside state

    state.artifacts["supervisor_decision"]=decision
    return state

    
# processor node 
# 
def procesosr_node(state: GraphState) -> GraphState:
       """
       Langgraph node wrapper for PreprcessAgent
      
       """

       if state.data is None:
           state.errors.append("No data avaibale for preprocessing")
           return state
       
       agent=PreprocessAgent()
       result=agent.run(state.data)

       # update state after preprocessing

       state.data=result.get("processed_data",state.data)
       state.artifacts["preprocess"]=result

       return state