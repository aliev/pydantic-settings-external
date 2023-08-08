from typing import Type

from pydantic import BaseModel

from pydantic_settings_external.version import PYDANTIC_MAJOR_VERSION, PYDANTIC_VERSION

BaseSettings: Type[BaseModel]

if PYDANTIC_MAJOR_VERSION == "1":
    from pydantic_settings_external.pydantic.v1 import BaseSettings as _BaseSettings

    BaseSettings = _BaseSettings
elif PYDANTIC_MAJOR_VERSION == "2":
    from pydantic_settings_external.pydantic.v2 import BaseSettings as _BaseSettings

    BaseSettings = _BaseSettings
else:
    raise ImportError(
        f"Installed version {PYDANTIC_VERSION} of PyDantic is not supporting."
    )

__all__ = ("BaseSettings",)
