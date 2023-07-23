try:
    from pydantic import BaseModel
    from pydantic.version import VERSION
except ImportError:
    raise ImportError(
        'Neither the 1.10.x nor the 2.0.x version of Pydantic was installed. '
        'Please install one of the required versions of Pydantic.'
    )

from typing import Callable, Type

from pydantic_settings_external.providers.base import BaseProvider

MAJOR_VERSION = VERSION.split('.')[0]

with_external_provider: Callable[[BaseProvider,], Type[BaseModel]]

if MAJOR_VERSION == '1':
    from pydantic_settings_external.pydantic.v1 import ExternalSettingsSource, with_external_provider_v1
    with_external_provider = with_external_provider_v1
elif MAJOR_VERSION == '2':
    from pydantic_settings_external.pydantic.v2 import ExternalSettingsSource, with_external_provider_v2
    with_external_provider = with_external_provider_v2
else:
    raise ImportError(f'Installed {VERSION} version of PyDantic is not supporting.')

__all__ = ('with_external_provider', 'ExternalSettingsSource')
