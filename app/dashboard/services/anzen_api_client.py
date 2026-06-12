import requests

from app.dashboard.config.settings import DashboardSettings


class AnzenApiClient:
    endpoint = "/api/analizar"

    def __init__(self, base_url=None, timeout=60):
        self.base_url = (base_url or DashboardSettings.api_base_url).rstrip("/")
        self.timeout = timeout

    def analizar_repo_github(self, repo_url):
        response = requests.post(
            f"{self.base_url}{self.endpoint}",
            data={"tipo_analisis": "repo_github", "url": repo_url},
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()
