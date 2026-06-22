from __future__ import annotations
from pathlib import Path
from pydantic import BaseModel, Field

class CaeReflexConfig(BaseModel):
    workspace_dir: Path = Field(default_factory=lambda: Path.cwd())
    max_file_size_mb: int = 25
    max_scan_depth: int = 3
    max_scan_files: int = 500
    max_request_body_mb: int = 10
    allow_nonlocal_server: bool = False
    server_api_key: str | None = None
    crossref_mailto: str | None = None
    crossref_cache_enabled: bool = True
    crossref_cache_ttl_days: int = 30

    @property
    def max_file_size_bytes(self) -> int:
        return self.max_file_size_mb * 1024 * 1024
