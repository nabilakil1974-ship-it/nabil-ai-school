"""Secure LiveAvatar session-token endpoint.

Provider credentials stay server-side. The browser receives only a short-lived
session token. No API key or avatar ID is embedded in client HTML.
"""
import os
import logging
import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()
log = logging.getLogger("nabil_ai.live_avatar")
LIVEAVATAR_API = "https://api.liveavatar.com"


class LiveAvatarStatus(BaseModel):
    configured: bool
    mode: str = "LITE"
    message: str


@router.get("/live-avatar/status", response_model=LiveAvatarStatus)
async def live_avatar_status():
    configured = bool(
        os.getenv("LIVEAVATAR_API_KEY", "").strip()
        and os.getenv("LIVEAVATAR_AVATAR_ID", "").strip()
    )
    return LiveAvatarStatus(
        configured=configured,
        message=(
            "LiveAvatar credentials are configured on the server."
            if configured
            else "Live mode is not connected yet. Configure LIVEAVATAR_API_KEY and LIVEAVATAR_AVATAR_ID on the server."
        ),
    )


@router.post("/live-avatar/session")
async def create_live_avatar_session():
    """Create a short-lived LiveAvatar LITE session token."""
    api_key = os.getenv("LIVEAVATAR_API_KEY", "").strip()
    avatar_id = os.getenv("LIVEAVATAR_AVATAR_ID", "").strip()
    if not api_key or not avatar_id:
        raise HTTPException(
            status_code=503,
            detail="LiveAvatar is not configured. Set LIVEAVATAR_API_KEY and LIVEAVATAR_AVATAR_ID as server secrets.",
        )

    sandbox_value = os.getenv("LIVEAVATAR_IS_SANDBOX", "false").strip().lower()
    payload = {
        "mode": "LITE",
        "avatar_id": avatar_id,
        "is_sandbox": sandbox_value in {"1", "true", "yes"},
    }
    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.post(
                f"{LIVEAVATAR_API}/v1/sessions/token",
                headers={
                    "X-API-KEY": api_key,
                    "Content-Type": "application/json",
                },
                json=payload,
            )
        if response.status_code >= 400:
            log.warning("LiveAvatar token request rejected with status %s", response.status_code)
            raise HTTPException(
                status_code=502,
                detail="LiveAvatar rejected the session request. Check server credentials, avatar ID, and account access.",
            )
        body = response.json()
        data = body.get("data") or {}
        token = data.get("session_token")
        if not token:
            log.warning("LiveAvatar token response did not include a session token")
            raise HTTPException(status_code=502, detail="LiveAvatar returned an incomplete session response.")
        # Only the short-lived session token is returned. Never expose API_KEY.
        return {"session_token": token, "session_id": data.get("session_id"), "mode": "LITE"}
    except HTTPException:
        raise
    except (httpx.HTTPError, ValueError):
        log.exception("LiveAvatar session creation failed")
        raise HTTPException(status_code=502, detail="Could not reach LiveAvatar. Try again later.")
