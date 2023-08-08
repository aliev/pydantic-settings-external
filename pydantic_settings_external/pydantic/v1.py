from pydantic_settings_external.version import PYDANTIC_MAJOR_VERSION

if PYDANTIC_MAJOR_VERSION != "1":
    raise ImportError("This package required Pydantic v1")

from typing import Any, Dict, Tuple

from pydantic import BaseSettings as PydanticBaseSettings
from pydantic.env_settings import SettingsSourceCallable

from pydantic_settings_external.exceptions import ErrorType, ProviderError
from pydantic_settings_external.utils import get_field_value, log_error_msg


def external_settings_source(settings: PydanticBaseSettings) -> Dict[str, Any]:  # C901
    d: Dict[str, Any] = {}

    for field in settings.__fields__.values():
        try:
            d[field.alias] = get_field_value(field.name, field.field_info.extra)
        except ProviderError as exc:
            if exc.error_type is not ErrorType.PROVIDER_WAS_NOT_SPECIFIED:
                log_error_msg(exc)

            if exc.error_type is ErrorType.INVALID_PROVIDER_INSTANCE:
                raise exc

            continue

    return d


class BaseSettings(PydanticBaseSettings):
    class Config:
        @classmethod
        def customise_sources(
            cls,
            init_settings: SettingsSourceCallable,
            env_settings: SettingsSourceCallable,
            file_secret_settings: SettingsSourceCallable,
        ) -> Tuple[SettingsSourceCallable, ...]:
            return (
                init_settings,
                env_settings,
                file_secret_settings,
                external_settings_source,
            )
