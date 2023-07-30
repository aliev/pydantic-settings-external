# PyDantic Settings External

## The project is currently under active development.

PyDantic Settings External extends PyDantic Settings to support various types of external configuration providers, such as GCP Secret Manager and AWS Secrets Manager. PyDantic Settings External has been developed using a clear abstraction, allowing for easy extension to external providers.

Installation:

```bash
pip install pydantic-settings-external
```

Usage example with `with_settings_external` helper

PyDantic v1.10.x

```bash
pip install "pydantic>=1.10,<2"
pip install pydantic-settings-external
```

```python

from pydantic import Field
from pydantic_settings_external import BaseSettings
from pydantic_settings_external.providers import GCPProvider, OnePasswordProvider


class MySettings(BaseSettings):
    SENDGRID_API_KEY: str = Field(..., provider={
            "gcp": {
                "name": "sendgrid-api-key",
                "vesion": "latest",
            },
            "hint": "Here you can provide the hint.",
        }
    )
    ADMIN_USER: str = Field(..., provider={
            "one_password": {
                "field": "user",
                "vault": "admin_credentials"
            },
            "hint": "Here you can provide the hint.",
        },
    )

    class Config:
        providers = {
            "gcp": GCPProvider(...),
            "one_password": OnePasswordProvider(...),
        }

```

PyDantic v2.x

```bash
pip install pydantic
pip install pydantic-settings-external
pip install pydantic-settings
```

```python

from pydantic import Field
from pydantic_settings_external import BaseSettings
from pydantic_settings_external.providers import GCPProvider, OnePasswordProvider


gcp = GCPProvider(...)
one_password = OnePasswordProvider(...)


class MySettings(BaseSettings):
    SENDGRID_API_KEY: str = Field(..., json_schema_extra={
        "provider": {
            "instance": gcp,
            "options": {"name": "sendgrid-api-key", "vesion": "latest"},
            "hint": "",
        },
    })
    ADMIN_USER: str = Field(..., json_schema_extra={
        "provider": {
            "instance": one_password,
            "options": {"field": "user", "vault": "admin_credentials"},
            "hint": "",
        },
    })
```
