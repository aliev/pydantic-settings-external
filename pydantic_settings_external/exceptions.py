from enum import Enum
from typing import Any, Dict


class ErrorType(str, Enum):
    INVALID_FIELD_EXTRA = """%(msg)s.

    Please use the following pattern:

        Field(..., %(extra_field)s={
            "provider": {
                "instance": provider_instance,
                "options": {...},
            }
        })

    skipping.
    """

    INVALID_PROVIDER_INSTANCE = (
        "Given provider instance is not an instance of Provider interface."
    )


class ProviderError(Exception):
    def __init__(self, error_type: ErrorType, kwargs: Dict[str, Any] = {}) -> None:
        self.error_msg = error_type.value % kwargs
        super().__init__(self.error_msg)
