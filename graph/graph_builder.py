from langgraph.graph import StateGraph,END

from ML_cursor.graph.state import GraphState
from ML_cursor.graph.nodes import eda_node,train_node


def build_graph():
    """

    Build  simple linear ML execution graph:

    EDA-> TRAIN -> END
    """

    builder=StateGraph(GraphState)

    # add nodes

    builder.add_node("eda",eda_node)
    builder.add_node("train",train_node)


    builder.set_entry_point("eda")
    builder.add_edge("eda","train")
    builder.add_edge("train",END)

    return builder.compile()