from langgraph.graph import StateGraph,END

from ML_cursor.graph.state import GraphState
from ML_cursor.graph.nodes import eda_node,train_node,supervisor_node,procesosr_node

def supervisor_router(state: GraphState) -> str:
    return state.artifacts.get("supervisor_decision","train")


def build_graph():
    """

    Build  simple linear ML execution graph:

    EDA-> TRAIN -> END
    """

    builder=StateGraph(GraphState)

    # add nodes

    builder.add_node("eda",eda_node)
    builder.add_node("supervisor",supervisor_node)
    builder.add_node("preprocess",procesosr_node)
    builder.add_node("train",train_node)


    builder.set_entry_point("eda")
    builder.add_edge("eda","supervisor")

    builder.add_conditional_edges(
        "supervisor",
        supervisor_router,
        {
            "preprocess":"preprocess",
            "train":"train"
        }
    )

    builder.add_edge("preprocess","train")
    builder.add_edge("train",END)

    return builder.compile()