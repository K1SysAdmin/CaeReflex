from __future__ import annotations
from pathlib import Path
import hashlib


def sha256_file(path: str | Path, max_bytes: int | None = None) -> tuple[str | None, str]:
    """Return (sha256, status) for a file. Status is complete, skipped_large, or failed."""
    p = Path(path)
    try:
        if max_bytes is not None and p.stat().st_size > max_bytes:
            return None, "skipped_large"
        h = hashlib.sha256()
        with p.open("rb") as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b""):
                h.update(chunk)
        return h.hexdigest(), "complete"
    except Exception:
        return None, "failed"


def stable_case_id(seed: str) -> str:
    digest = hashlib.sha1(seed.encode("utf-8", errors="ignore")).hexdigest()[:12]
    return f"case_{digest}"
