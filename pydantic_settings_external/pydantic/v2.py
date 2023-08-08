from pydantic_settings_external.version import PYDANTIC_MAJOR_VERSION

if PYDANTIC_MAJOR_VERSION != "2":
    raise ImportError("This package required Pydantic v2")

from pydantic.fields import FieldInfo

from pydantic_settings_external.exceptions import ErrorType, ProviderError
from pydantic_settings_external.utils import get_field_value, log_error_msg

try:
    from pydantic_settings.main import BaseSettings as PyDanticBaseSettings
    from pydantic_settings.sources import PydanticBaseSettingsSource
except ImportError:
    raise ImportError(
        "In order to use this package for Pydantic v2 it is required to install "
        "pydantic-settings package. "
        "Please install it using the following command: pip install pydantic-settings."
    )

from typing import Any, Dict, Tuple, Type


class ExternalSettingsSource(PydanticBaseSettingsSource):
    def get_field_value(
        self, field: FieldInfo, field_name: str
    ) -> Tuple[Any, str, bool]:
        return get_field_value(field_name, field.json_schema_extra), field_name, False

    def __call__(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {}

        for field_name, field in self.settings_cls.model_fields.items():
            try:
                field_value, field_key, value_is_complex = self.get_field_value(
                    field, field_name
                )
            except ProviderError as exc:
                if exc.error_type is not ErrorType.PROVIDER_WAS_NOT_SPECIFIED:
                    log_error_msg(exc)

                if exc.error_type is ErrorType.INVALID_PROVIDER_INSTANCE:
                    raise exc
                continue

            field_value = self.prepare_field_value(
                field_name, field, field_value, value_is_complex
            )

            if field_value is not None:
                d[field_key] = field_value

        return d


class BaseSettings(PyDanticBaseSettings):
    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[PyDanticBaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            file_secret_settings,
            ExternalSettingsSource(settings_cls),
        )
