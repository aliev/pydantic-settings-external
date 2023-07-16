# PyDantic Settings External

## The project is currently under active development.

PyDantic Settings External is a library that extends PyDantic Settings to support various types of external configuration providers, such as GCP Secret Manager and AWS Secrets Manager. PyDantic Settings External has been developed using a clear abstraction, allowing for easy extension to external configurations not yet incorporated into the library by the community.

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

from pydantic_settings_external.providers.gcp import GcpProvider, with_settings_external
import os

google_project_id = os.getenv("GOOGLE_PROJECT_ID")
gcp_provider = GcpProvider(google_project_id)

class Settings(with_settings_external(gcp_provider)):
    MY_SECRET_API_KEY: str = Field(gcp={"key": "my-secret-api-key"})
```

PyDantic v2.x

```bash
pip install pydantic
pip install pydantic-settings-external
pip install pydantic-settings
```

```python
from pydantic_settings_external.providers.gcp import GcpProvider, with_settings_external
import os

google_project_id = os.getenv("GOOGLE_PROJECT_ID")
gcp_provider = GcpProvider(google_project_id)

class Settings(with_settings_external(gcp_provider)):
    MY_SECRET_API_KEY: str = Field(
        json_schema_extra={
            {"gcp": "key": "my-secret-api-key"}
        }
    )
```


Usage without `with_settings_external` helper

TODO
