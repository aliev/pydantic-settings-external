from enum import Enum
from typing import Any, Dict


class ErrorType(str, Enum):
    INVALID_FIELD_EXTRA = """Cannot get value for %(field)s: %(msg)s.

    Please use the following pattern:

        Field(..., %(extra_field)s={
            "provider": {
                "instance": provider_instance,
                "options": {...},
            }
        })

    Skipping.
    """

    INVALID_PROVIDER_INSTANCE = (
        "Given provider instance is not an instance of Provider interface."
    )

    PROVIDER_WAS_NOT_SPECIFIED = "No provider was specified. Skipping."


class ProviderError(Exception):
    def __init__(self, error_type: ErrorType, kwargs: Dict[str, Any] = {}) -> None:
        self.error_msg = error_type.value % kwargs
        self.error_type = error_type
        super().__init__(self.error_msg)
