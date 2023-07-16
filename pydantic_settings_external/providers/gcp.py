from typing import Any, Dict, Optional
from .base import AbstractBaseProvider


class GcpProvider(AbstractBaseProvider):
    @property
    def name(self) -> str:
        return "gcp"

    def get(self, options: Dict[str, Any]) -> Optional[str]:
        return None
