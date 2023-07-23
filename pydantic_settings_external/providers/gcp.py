import logging
from typing import Any, Dict, Optional

from google.cloud import secretmanager

from .base import BaseProvider

logger = logging.getLogger(__package__)


class GoogleCloudSecretManagerProvider(BaseProvider):
    def __init__(
        self,
        google_project_id: str,
        client: secretmanager.SecretManagerServiceClient = secretmanager.SecretManagerServiceClient(),
    ) -> None:
        self.google_project_id = google_project_id
        self.client = client

    @property
    def name(self) -> str:
        return 'google-cloud-secret-manager'

    def get(self, options: Dict[str, Any] = {'versions': 'latest'}) -> Optional[str]:
        request = secretmanager.AccessSecretVersionRequest(
            name=f"projects/{self.google_project_id}/secrets/{options['name']}/versions/{options['versions']}"
        )

        try:
            response = self.client.access_secret_version(request=request)
            return response.payload.data.decode('utf-8')
        except Exception:
            logger.exception('')
            return None
