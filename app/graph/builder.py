# app/graph/builder.py
from langgraph.graph import StateGraph, START, END

from app.graph.state import ResearchState
from app.nodes.planner import planner_node
from app.nodes.search import search_node
from app.nodes.draft import draft_node


def build_graph():
    builder = StateGraph(ResearchState)

    builder.add_node("planner", planner_node)
    builder.add_node("search", search_node)
    builder.add_node("draft", draft_node)

    builder.add_edge(START, "planner")
    builder.add_edge("planner", "search")
    builder.add_edge("search", "draft")
    builder.add_edge("draft", END)

    return builder.compile()