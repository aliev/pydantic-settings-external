import abc
from typing import Any, Dict, Optional, Protocol, runtime_checkable


class BaseProvider(abc.ABC):
    @abc.abstractproperty
    def name(self) -> str:
        ...

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(provider={self.name})'

    @abc.abstractmethod
    def get(self, options: Dict[str, Any]) -> Optional[str]:
        ...


@runtime_checkable
class Provider(Protocol):
    ...
