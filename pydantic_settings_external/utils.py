import logging
from typing import Any, Dict, Optional

from pydantic_settings_external.exceptions import ErrorType, ProviderError
from pydantic_settings_external.types import Provider, ProviderDict
from pydantic_settings_external.version import PYDANTIC_MAJOR_VERSION

logger = logging.getLogger(__package__)


def validate_provider_field(
    field_extra: Optional[Dict[str, Any]] = None
) -> ProviderDict:
    pydantic_extra_field_name = (
        "extra" if PYDANTIC_MAJOR_VERSION == "1" else "json_field_extra"
    )

    if field_extra is None:
        raise ProviderError(
            ErrorType.INVALID_FIELD_EXTRA,
            {
                "msg": f"key {pydantic_extra_field_name} cannot be None.",
                "extra_field": pydantic_extra_field_name,
            },
        )

    if "provider" not in field_extra:
        raise ProviderError(
            ErrorType.INVALID_FIELD_EXTRA,
            {
                "msg": f"key 'provider' not in {pydantic_extra_field_name}",
                "extra_field": pydantic_extra_field_name,
            },
        )

    provider: ProviderDict = field_extra["provider"]

    if "instance" not in provider:
        raise ProviderError(
            ErrorType.INVALID_FIELD_EXTRA,
            {
                "msg": f"key 'instance' not in {pydantic_extra_field_name}['provider']",
                "extra_field": pydantic_extra_field_name,
            },
        )

    if "options" not in provider:
        raise ProviderError(
            ErrorType.INVALID_FIELD_EXTRA,
            {
                "msg": f"key 'options' not in {pydantic_extra_field_name}",
                "extra_field": pydantic_extra_field_name,
            },
        )

    if not isinstance(provider["options"], dict):
        raise ProviderError(
            ErrorType.INVALID_FIELD_EXTRA,
            {
                "msg": f"key {pydantic_extra_field_name}['options'] should be a dict",
                "extra_field": pydantic_extra_field_name,
            },
        )

    provider_instance = provider["instance"]

    if not isinstance(provider_instance, Provider):
        raise ProviderError(ErrorType.INVALID_PROVIDER_INSTANCE)

    return provider


def log_error_msg(exc: ProviderError):
    logger.error(exc)


def display_hint(hint: str):
    logger.info(hint)


def get_field_value(field_extra: Optional[Dict[str, Any]] = None) -> str | None:
    provider = validate_provider_field(field_extra)
    provider_instance = provider["instance"]
    provider_options = provider["options"]
    provider_hint = provider.get("hint")

    value = provider_instance.get(options=provider_options)

    if value is None and provider_hint is not None:
        display_hint(provider_hint)

    return value
