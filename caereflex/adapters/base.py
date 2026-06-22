from __future__ import annotations
from pathlib import Path
from abc import ABC, abstractmethod
from caereflex.core.config import CaeReflexConfig
from caereflex.core.models import AdapterResult

class BaseAdapter(ABC):
    name = "base"
    def __init__(self, config: CaeReflexConfig | None = None):
        self.config = config or CaeReflexConfig()

    @abstractmethod
    def inspect(self, path: str | Path) -> AdapterResult:
        raise NotImplementedError
