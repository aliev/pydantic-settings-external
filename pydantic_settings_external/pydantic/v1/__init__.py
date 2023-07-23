from typing import Any, Dict, Tuple, Type

from pydantic import BaseModel, BaseSettings
from pydantic.env_settings import SettingsSourceCallable

from pydantic_settings_external.providers.base import BaseProvider


class ExternalSettingsSource:
    def __init__(
        self,
        provider: BaseProvider,
    ) -> None:
        self.provider = provider

    def __repr__(self) -> str:
        return (
            f'ExternalSettingsSource(provider={self.provider!r})'
        )

    def __call__(self, settings: BaseSettings) -> Dict[str, Any]:  # C901
        d: Dict[str, Any] = {}

        for field in settings.__fields__.values():
            if self.provider.name not in field.field_info.extra:
                # NOTE: Skip if provider configuration is not in extra
                continue
            field_provider_options = field.field_info.extra[self.provider.name]
            d[field.alias] = self.provider.get(field_provider_options) or field.default

        return d


def with_external_provider_v1(
    provider: BaseProvider,
) -> Type[BaseModel]:
    class Settings(BaseSettings):
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
                    ExternalSettingsSource(provider),
                )

    return Settings
