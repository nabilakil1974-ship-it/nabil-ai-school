# NABIL AI — Real-time digital teacher integration

## Goal
Use the NABIL teacher likeness for a new response on every student turn, with speech and mouth movement generated for that response. The existing file in `public/videos/` is a prerecorded clip and must remain only an introduction/reference; never replay it as if it were answering a new question.

## Selected integration path
Use **HeyGen LiveAvatar** (the real-time conversation product, not ordinary pre-rendered HeyGen video generation). Official overview: https://help.heygen.com/en/articles/12758516-introducing-liveavatar

LiveAvatar provides the streaming avatar/lip-sync layer. NABIL AI remains responsible for the curriculum-grounded answer and synchronized whiteboard steps. Use Lite mode if the platform's existing lesson/chat pipeline must remain the source of answers.

## Required setup before live streaming can be enabled
1. Create/approve a custom LiveAvatar in the LiveAvatar dashboard: https://app.liveavatar.com/home. The short FreeLipSync MP4 currently stored in this repository is not itself a LiveAvatar session or a compatible avatar ID.
2. Obtain the provider credentials/access permitted by the account and store them **only as server environment secrets** on the backend host. Never put API keys in GitHub Pages HTML, JavaScript, or this repository.
3. Configure the backend with the approved LiveAvatar identifier and credentials, then have the backend mint/start a session and return only the short-lived client connection data.
4. Connect each newly generated NABIL answer to the active avatar session. End/close the session on exit; handle expired tokens, unavailable provider, and quota errors without pretending a static video is live.
5. Synchronize whiteboard steps with the same answer sequence. For English voice mode, keep Arabic explanatory writing on the board as specified by NABIL's lesson UX.

## Acceptance checks
- Two different student questions produce two different spoken responses.
- Mouth movement matches each newly generated response; no reuse of the prerecorded MP4 audio.
- The board displays the exact steps associated with the spoken response.
- No provider secret is exposed to the browser.
- If LiveAvatar is not configured, the page clearly reports that live mode is not connected and does not claim success.

## Current status
- The prerecorded video asset and `public/digital-human.html` exist in the repository.
- **LiveAvatar is not yet connected or tested.** This requires a LiveAvatar avatar/account configuration and server-side credentials. Do not mark the feature complete until the acceptance checks pass.
