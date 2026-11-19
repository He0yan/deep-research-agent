
import hashlib
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import httpx

from .schemas import FetchResult


DEFAULT_EVIDENCE_DIR = Path("artifacts/evidence")


class DeepSeekFetchClient:
    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: float = 60.0,
        evidence_dir: Path | str | None = None,
    ):
        self.api_key = api_key or os.environ["DEEPSEEK_API_KEY"]
        self.base_url = (
            base_url or os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
        ).rstrip("/")
        self.timeout = timeout
        self.evidence_dir = Path(evidence_dir or DEFAULT_EVIDENCE_DIR)
        self.evidence_dir.mkdir(parents=True, exist_ok=True)

    def fetch(self, url: str) -> FetchResult:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {"url": url}


        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(
                f"{self.base_url}/v1/tools/fetch",
                json=payload,
                headers=headers,
            )
            response.raise_for_status()

        data = response.json()
        title = data.get("title") or ""
        content = data.get("content") or ""

        content_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
        evidence_id = f"E_{content_hash[:12]}"
        storage_path = self.evidence_dir / f"{evidence_id}.md"
        storage_path.write_text(content, encoding="utf-8")

        result = FetchResult(
            evidence_id=evidence_id,
            title=title,
            url=url,
            site_name=_extract_site_name(url),
            fetched_at=datetime.now(timezone.utc),
            content_hash=content_hash,
            storage_path=str(storage_path),
            content_markdown=content,
        )

   
        return result


def _extract_site_name(url: str) -> str | None:
    host = urlparse(url).hostname
    if not host:
        return None
    return re.sub(r"^www\.", "", host)