from typing import Any, Dict, Optional

import pytest
from pydantic import Field

from pydantic_settings_external import BaseSettings
from pydantic_settings_external.version import PYDANTIC_MAJOR_VERSION


@pytest.mark.skipif(
    PYDANTIC_MAJOR_VERSION != "2", reason="requires Pydantic 2.0 or higher."
)
def test_pydantic_v2():
    class FakeProvider:
        def get(self, options: Dict[str, Any]) -> Optional[Any]:
            return "123"

    fake_provider = FakeProvider()

    class Settings(BaseSettings):
        SENDGRID_API_KEY: str = Field(
            ...,
            json_schema_extra={
                "provider": {
                    "instance": fake_provider,
                    "options": {"name": "sendgrid-api-key", "vesion": "latest"},
                    "hint": "",
                }
            },
        )

    settings = Settings()
    assert settings.SENDGRID_API_KEY == "123"


@pytest.mark.skipif(
    PYDANTIC_MAJOR_VERSION != "2", reason="requires Pydantic 2.0 or higher."
)
def test_pydantic_v2_dotenv(monkeypatch):
    monkeypatch.setenv("SENDGRID_API_KEY", "444")

    class FakeProvider:
        def get(self, options: Dict[str, Any]) -> Optional[Any]:
            return None

    fake_provider = FakeProvider()

    class Settings(BaseSettings):
        SENDGRID_API_KEY: str = Field(
            ...,
            json_schema_extra={
                "provider": {
                    "instance": fake_provider,
                    "options": {"name": "sendgrid-api-key", "vesion": "latest"},
                    "hint": "",
                }
            },
        )

    settings = Settings()

    assert settings.SENDGRID_API_KEY == "444"
