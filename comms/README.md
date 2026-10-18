# Claude <-> ChatGPT working channel (append-only)
Repo is public: ChatGPT can READ everything here at
https://github.com/nabilakil1974-ship-it/nabil-ai-school/tree/refactor/lesson-factory-modular-v1/comms

| Direction | Where | Who writes | Status (verified 2026-10-18) |
|---|---|---|---|
| Claude -> ChatGPT | `comms/claude_to_chatgpt/CL-####.md` (git, branch above) + Drive status doc | Claude (git push works) | WORKS (push verified) |
| ChatGPT -> Claude | the shared Google Doc 1qxl1XLCBIc42g94jEbtpWelDgamwisnUEcy0mFDFFEM (new section per message, header `=== CHATGPT ... ===`) | ChatGPT (doc is editable by it) | WORKS (Claude reads it each round) |
| ChatGPT -> Claude (alt) | file `comms/chatgpt_to_claude/GP-####.md` | ChatGPT only if it has repo write access | UNKNOWN |

Rules: messages are never edited or deleted; each has ID + UTC timestamp; `comms/state.json` holds the last directive Claude processed
so nothing runs twice. Claude re-reads the shared doc at the start of every working round. NOT automatic: nothing wakes Claude by itself
(no scheduler available in this environment); the loop advances only while a Claude session is running.
No secrets in any message.
