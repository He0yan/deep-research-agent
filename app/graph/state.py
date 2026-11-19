# app/graph/state.py
from typing import TypedDict
from app.providers.schemas import SearchResult


class ResearchState(TypedDict):
    run_id: str
    query: str
    keywords: list[str]
    search_results: list[SearchResult]
    draft: str