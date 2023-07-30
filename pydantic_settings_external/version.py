try:
    from pydantic import VERSION as PYDANTIC_VERSION
except ImportError:
    raise ImportError(
        "Neither the 1.10.x nor the 2.0.x version of Pydantic was installed. "
        "Please install one of the required versions of Pydantic."
    )

VERSION = "0.1.0"

PYDANTIC_MAJOR_VERSION = PYDANTIC_VERSION.split(".")[0]
