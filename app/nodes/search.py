# app/nodes/search.py
from app.graph.state import ResearchState
from app.providers.deepseek_search import DeepSeekSearchClient


def search_node(state: ResearchState) -> dict:
    client = DeepSeekSearchClient()
    all_results = []
    seen_urls = set()

    for keyword in state["keywords"]:
        results = client.search(query=keyword, count=5)
        for r in results:
            if r.url not in seen_urls:
                seen_urls.add(r.url)
                all_results.append(r)

    return {"search_results": all_results}