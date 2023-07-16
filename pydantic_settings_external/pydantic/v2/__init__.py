from pydantic.fields import FieldInfo
from pydantic import BaseModel
from pydantic_settings_external.providers.base import AbstractBaseProvider

try:
    from pydantic_settings import PydanticBaseSettingsSource
    from pydantic_settings.sources import PydanticBaseSettingsSource
    from pydantic_settings.main import BaseSettings
except ImportError:
    raise ImportError(
        "In order to use this package for Pydantic v2 it is required to install "
        "pydantic-settings package. "
        "Please install it using the following command: pip install pydantic-settings."
    )

from typing import Any, Dict, Type, Tuple, cast


class ExternalSettingsSource(PydanticBaseSettingsSource):
    def __init__(
        self,
        settings_cls: Type[BaseSettings],
        provider: AbstractBaseProvider,
    ) -> None:
        self.provider = provider
        super().__init__(settings_cls)

    def __repr__(self) -> str:
        return (
            f"ExternalSettingsSource(provider={self.provider!r})"
        )

    def get_field_value(self, field: FieldInfo, field_name: str) -> Tuple[Any, str, bool]:
        json_schema_extra = cast(Dict[str, Any], field.json_schema_extra)
        field_provider_options = json_schema_extra[self.provider.name]

        value = self.provider.get(field_provider_options)

        return value, field_name, False

    def __call__(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {}

        for field_name, field in self.settings_cls.model_fields.items():
            if field.json_schema_extra is None:
                continue

            if self.provider.name not in field.json_schema_extra:
                continue

            field_value, field_key, value_is_complex = self.get_field_value(field, field_name)
            field_value = self.prepare_field_value(field_name, field, field_value, value_is_complex)

            if field_value is not None:
                d[field_key] = field_value

        return d


def with_external_provider_v2(
    provider: AbstractBaseProvider,
) -> Type[BaseModel]:
    class Settings(BaseSettings):
        @classmethod
        def settings_customise_sources(
            cls,
            settings_cls: Type[BaseSettings],
            init_settings: PydanticBaseSettingsSource,
            env_settings: PydanticBaseSettingsSource,
            dotenv_settings: PydanticBaseSettingsSource,
            file_secret_settings: PydanticBaseSettingsSource
        ) -> Tuple[PydanticBaseSettingsSource, ...]:
            return (
                init_settings,
                env_settings,
                dotenv_settings,
                file_secret_settings,
                ExternalSettingsSource(settings_cls, provider)
            )

        class Config:
            extra = "allow"

    return Settings
