import logging
from typing import Any, Dict, Optional, Union

from pydantic_settings_external.exceptions import ErrorType, ProviderError
from pydantic_settings_external.types import Provider, ProviderDict
from pydantic_settings_external.version import PYDANTIC_MAJOR_VERSION

logger = logging.getLogger(__package__)


def validate_provider_field(
    name: str, field_extra: Dict[str, Any] | None = None
) -> ProviderDict:
    pydantic_extra_field_name = (
        "extra" if PYDANTIC_MAJOR_VERSION == "1" else "json_field_extra"
    )

    if field_extra is None:
        raise ProviderError(ErrorType.PROVIDER_WAS_NOT_SPECIFIED)

    if "provider" not in field_extra:
        raise ProviderError(ErrorType.PROVIDER_WAS_NOT_SPECIFIED)

    provider: ProviderDict = field_extra["provider"]

    if "instance" not in provider:
        raise ProviderError(
            ErrorType.INVALID_FIELD_EXTRA,
            {
                "msg": f"key 'instance' not in {pydantic_extra_field_name}['provider']",
                "extra_field": pydantic_extra_field_name,
                "field": name,
            },
        )

    if "options" not in provider:
        raise ProviderError(
            ErrorType.INVALID_FIELD_EXTRA,
            {
                "msg": f"key 'options' not in {pydantic_extra_field_name}",
                "extra_field": pydantic_extra_field_name,
                "field": name,
            },
        )

    if not isinstance(provider["options"], dict):
        raise ProviderError(
            ErrorType.INVALID_FIELD_EXTRA,
            {
                "msg": f"key {pydantic_extra_field_name}['options'] should be a dict",
                "extra_field": pydantic_extra_field_name,
                "field": name,
            },
        )

    provider_instance = provider["instance"]

    if not isinstance(provider_instance, Provider):
        raise ProviderError(ErrorType.INVALID_PROVIDER_INSTANCE)

    return provider


def log_error_msg(exc: ProviderError):
    logger.warning(exc)


def display_hint(hint: str):
    logger.info(hint)


def get_field_value(
    name: str, field_extra: Optional[Dict[str, Any]] = None
) -> Union[str, None]:
    provider = validate_provider_field(name, field_extra)
    provider_instance = provider["instance"]
    provider_options = provider["options"]
    provider_hint = provider.get("hint")

    value = provider_instance.get(options=provider_options)

    if value is None and provider_hint is not None:
        display_hint(provider_hint)

    return value
