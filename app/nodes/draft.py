# app/nodes/draft.py
from datetime import datetime, timezone
from pathlib import Path

from app.graph.state import ResearchState


REPORT_DIR = Path("artifacts/reports")


def draft_node(state: ResearchState) -> dict:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    lines = [
        f"# 研究报告：{state['query']}",
        "",
        f"生成时间：{datetime.now(timezone.utc).isoformat()}",
        f"搜索关键词：{', '.join(state['keywords'])}",
        f"搜索结果数：{len(state['search_results'])}",
        "",
        "## 搜索结果摘要",
        "",
    ]

    for i, r in enumerate(state["search_results"], 1):
        lines.extend([
            f"### [{i}] {r.title}",
            f"- URL：{r.url}",
            f"- 来源：{r.site_name or '未知'}",
            f"- 权威度：{r.authority}",
            f"- 发布时间：{r.published_at or '未知'}",
            f"- 摘要：{r.snippet or r.summary[:200]}",
            "",
        ])

    draft = "\n".join(lines)
    report_path = REPORT_DIR / f"{state['run_id']}.md"
    report_path.write_text(draft, encoding="utf-8")

    return {"draft": draft}