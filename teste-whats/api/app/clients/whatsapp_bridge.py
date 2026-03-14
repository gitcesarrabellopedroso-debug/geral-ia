from typing import Any

import httpx

from app.core.config import Settings


class WhatsAppBridgeError(Exception):
    """Raised when the WhatsApp bridge request fails."""


class WhatsAppBridgeNotConfiguredError(WhatsAppBridgeError):
    """Raised when the bridge is disabled or missing configuration."""


class WhatsAppBridgeClient:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def _build_headers(self) -> dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.settings.whatsapp_bridge_api_key:
            headers["X-API-Key"] = self.settings.whatsapp_bridge_api_key
        return headers

    async def _request(self, method: str, path: str, json: dict[str, Any] | None = None) -> dict[str, Any]:
        if not self.settings.whatsapp_bridge_enabled:
            raise WhatsAppBridgeNotConfiguredError("WhatsApp bridge is not enabled.")

        base_url = self.settings.whatsapp_bridge_base_url.rstrip("/")
        url = f"{base_url}{path}"

        try:
            async with httpx.AsyncClient(timeout=self.settings.whatsapp_bridge_timeout_seconds) as client:
                response = await client.request(method, url, headers=self._build_headers(), json=json)
                response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            detail = exc.response.text.strip() or str(exc)
            raise WhatsAppBridgeError(f"Bridge returned an error: {detail}") from exc
        except httpx.HTTPError as exc:
            raise WhatsAppBridgeError(f"Bridge request failed: {exc}") from exc

        payload = response.json()
        if not isinstance(payload, dict):
            raise WhatsAppBridgeError("Bridge returned an invalid JSON payload.")
        return payload

    async def start_session(self, session_key: str) -> dict[str, Any]:
        return await self._request("POST", f"/sessions/{session_key}/start")

    async def get_status(self, session_key: str) -> dict[str, Any]:
        return await self._request("GET", f"/sessions/{session_key}")

    async def disconnect_session(self, session_key: str) -> dict[str, Any]:
        return await self._request("POST", f"/sessions/{session_key}/disconnect")

    async def send_message(self, session_key: str, phone: str, text: str) -> dict[str, Any]:
        return await self._request(
            "POST",
            f"/sessions/{session_key}/messages",
            json={
                "phone": phone,
                "text": text,
            },
        )
