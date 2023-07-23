from typing import Any, Dict, Optional, Protocol, TypedDict, runtime_checkable


class ProviderSettings(TypedDict):
    provider: str
    """ The name of provider. """
    options: Dict[str, Any]
    """ The provider options. """


@runtime_checkable
class Provider(Protocol):
    def get(self, options: Dict[str, Any]) -> Optional[str]:
        """Returns the value from external provider by key.

        Args:
            options (Dict[str, Any]): key specific options for provider.

        Returns:
            Optional[str]: the value of the key from current provider.
        """


Providers = Dict[str, Provider]
""" Type of providers registry. """
