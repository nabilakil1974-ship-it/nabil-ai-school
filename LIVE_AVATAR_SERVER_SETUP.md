# LiveAvatar server configuration

Add these as **server-side environment variables** on the Railway service that runs the FastAPI app. Do not put values in GitHub, HTML, client JavaScript, or chat messages.

- `LIVEAVATAR_API_KEY`: API key from the LiveAvatar developer dashboard.
- `LIVEAVATAR_AVATAR_ID`: ID of the approved custom LiveAvatar (or an avatar permitted by the account).
- `LIVEAVATAR_IS_SANDBOX`: `true` only when testing with the provider sandbox; otherwise `false`.

After deployment, check:
- `GET https://YOUR_BACKEND_HOST/api/live-avatar/status`
- `POST https://YOUR_BACKEND_HOST/api/live-avatar/session`

The status endpoint must report `configured: true`. The session endpoint returns a short-lived `session_token`; it must never return the provider API key.

## Important limits
This backend addition securely creates a LiveAvatar LITE session token. It does not, by itself, connect the NABIL AI answer-generation pipeline or whiteboard to a spoken avatar response. That next integration requires the LiveAvatar Web SDK plus an audio/TTS path that feeds the avatar's audio stream and the existing curriculum-grounded answer events. Do not mark the full feature complete until a real avatar session starts and a new student question produces a new synchronized spoken answer.

Official docs:
- https://docs.liveavatar.com
- https://github.com/heygen-com/liveavatar-web-sdk
