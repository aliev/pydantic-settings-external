# Pydantic Settings External

## The project is currently under active development.

Pydantic Settings External extends Pydantic Settings to support various types of external configuration providers, such as GCP Secret Manager and AWS Secrets Manager. PyDantic Settings External has been developed using a clear abstraction, allowing for easy extension to external providers.

Installation:

```bash
pip install pydantic-settings-external
```

Usage example with `with_settings_external` helper

Pydantic v2.x

```bash
pip install pydantic
pip install pydantic-settings-external
pip install pydantic-settings
```

```python

from pydantic import Field
from pydantic_settings_external import BaseSettings


gcp = GCPProvider(...)
one_password = OnePasswordProvider(...)


class Settings(BaseSettings):
    SENDGRID_API_KEY: str = Field(..., json_schema_extra={
        "provider": {
            "instance": gcp,
            "options": {"name": "sendgrid-api-key", "vesion": "latest"},
            "hint": "The optional hint will be displayed if the secret couldn't be retrieved for any reason.",
        },
    })
    ADMIN_USER: str = Field(..., json_schema_extra={
        "provider": {
            "instance": one_password,
            "options": {"field": "user", "vault": "admin_credentials"},
        },
    })

settings = Settings()

```

Pydantic v1.10.x

```bash
pip install "pydantic>=1.10,<2"
pip install pydantic-settings-external
```

NOTE: For Pydantic v1.10.x replace `json_schema_extra` with `extra`.
