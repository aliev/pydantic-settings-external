from typing import Any, Dict, Optional, Protocol, Tuple, TypedDict, runtime_checkable


@runtime_checkable
class Provider(Protocol):
    def get(self, options: Dict[str, Any]) -> Optional[Any]:
        """Returns the value from external provider by key.

        Args:
            options (Dict[str, Any]): key specific options for provider.

        Returns:
            Optional[str]: the value of the key from current provider.
        """


OptionsType = Dict[str, Any]


class ProviderDict(TypedDict):
    instance: Provider
    options: OptionsType
    hint: Optional[str]


ProviderOptions = Tuple[Provider, OptionsType]
""" Type of providers registry. """
