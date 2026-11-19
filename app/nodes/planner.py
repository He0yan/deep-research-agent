# app/nodes/planner.py
from app.graph.state import ResearchState


def planner_node(state: ResearchState) -> dict:
    query = state["query"]
    keywords = [query, f"{query} 融资事件", f"{query} 投资机构"]
    return {"keywords": keywords}