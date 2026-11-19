from datetime import datetime
from pydantic import BaseModel, Field


class SearchResult(BaseModel):
    title: str
    url: str
    snippet: str = ""
    summary: str = ""
    site_name: str | None = None
    published_at: datetime | None = None   # 对应官方返回的 date 字段
    authority: int = Field(default=-1, ge=-1, le=4)
    rerank_score: float = Field(default=0.0, ge=0.0, le=3.0)


class FetchResult(BaseModel):
    evidence_id: str
    title: str
    url: str
    site_name: str | None = None
    fetched_at: datetime
    content_hash: str
    storage_path: str
    content_markdown: str   # Day 3 临时保留在内存中用于验证，不写入 State