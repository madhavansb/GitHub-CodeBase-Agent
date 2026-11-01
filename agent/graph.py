from langgraph.graph import StateGraph, START, END

from agent.state import AgentState
from agent.nodes import retrieve_code, generate_answer


def build_graph():

    graph = StateGraph(AgentState)

    graph.add_node("retrieve_code", retrieve_code)
    graph.add_node("generate_answer", generate_answer)

    graph.add_edge(START, "retrieve_code")
    graph.add_edge("retrieve_code", "generate_answer")
    graph.add_edge("generate_answer", END)

    return graph.compile()


agent = build_graph()