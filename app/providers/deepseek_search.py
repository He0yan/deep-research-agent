
import os
from datetime import datetime
import httpx
from .schemas import SearchResult



class DeepSeekSearchClient:
    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: float = 20.0,
    ):
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        self.base_url = os.getenv("DEEPSEEK_BASE_URL")
        self.timeout = timeout

    def search(
        self,
        query: str,
        count: int = 10,
        need_content: bool = False,
    ) -> list[SearchResult]:
        payload = {
            "query": query,
            "count": count,
            "need_content": need_content,
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(
                f"{self.base_url}/v1/tools/search",
                json=payload,
                headers=headers,
            )
            response.raise_for_status()

        raw_results = response.json().get("results", [])
        if not raw_results:
            return []

        results = [
            SearchResult(
                title=item.get("title", ""),
                url=item.get("url", ""),
                snippet=item.get("snippet") or "",
                summary=item.get("summary") or "",
                site_name=item.get("site_name"),
                published_at=_parse_date(item.get("date")),
                authority=item.get("authority", -1),
                rerank_score=item.get("rerank_score", 0.0),
            )
            for item in raw_results
        ]

        return results


def _parse_date(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None