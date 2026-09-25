#!/usr/bin/env python3
"""One-time LOCAL Google OAuth authorization for NABIL Factory personal Drive uploads.

Run on YOUR computer (not Railway and never inside GitHub Actions):
    py -m pip install google-auth-oauthlib google-api-python-client
    py authorize_drive_owner.py --client client_secret.json --folder-id <Drive folder ID>

Use an OAuth Desktop client JSON created in your own Google Cloud project.
This script only saves private tokens to a local file, never prints them.
"""
import argparse
import json
import os
from pathlib import Path

SCOPES = ["https://www.googleapis.com/auth/drive"]


def main():
    ap = argparse.ArgumentParser(description="Authorize owner upload access for NABIL")
    ap.add_argument("--client", required=True, type=Path,
                    help="Desktop OAuth client JSON downloaded from Google Cloud")
    ap.add_argument("--folder-id", required=True,
                    help="NABIL AI - Interactive Curriculum Drive folder ID")
    ap.add_argument("--output", type=Path,
                    default=Path("nabil_drive_oauth_token.json"))
    args = ap.parse_args()

    if not args.client.is_file():
        ap.error("Desktop OAuth client file not found: " + str(args.client))
    client = json.loads(args.client.read_text(encoding="utf-8"))
    if "installed" not in client:
        ap.error("Expected OAuth Desktop app JSON; do NOT use a service account JSON")

    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
    except ImportError as exc:
        raise SystemExit(
            "Missing library: py -m pip install google-auth-oauthlib google-api-python-client"
        ) from exc

    flow = InstalledAppFlow.from_client_secrets_file(str(args.client), SCOPES)
    print("Opening Google login on this computer. Select the Google account owning the folder.")
    credentials = flow.run_local_server(
        host="localhost", port=0,
        access_type="offline", prompt="consent",
        authorization_prompt_message="Open the following URL if the browser did not open:\n{url}",
        success_message="NABIL Drive authorization complete. Return to the terminal.",
    )
    if not credentials.refresh_token:
        raise SystemExit(
            "Google did not issue a refresh token. Nothing saved; revoke the old app "
            "grant for this client, then repeat using consent."
        )

    service = build("drive", "v3", credentials=credentials, cache_discovery=False)
    folder = service.files().get(
        fileId=args.folder_id,
        fields="id,name,mimeType,capabilities(canAddChildren)",
    ).execute()
    if (folder.get("mimeType") != "application/vnd.google-apps.folder"
            or folder.get("capabilities", {}).get("canAddChildren") is not True):
        raise SystemExit("Selected Google account cannot upload to that folder. Nothing saved.")

    email = service.about().get(fields="user(emailAddress)").execute().get(
        "user", {}).get("emailAddress", "(unknown)")
    if args.output.exists():
        raise SystemExit("Output already exists; choose another --output (no overwrite).")
    # Personal OAuth token is a secret, including the refresh token and client secret.
    descriptor = os.open(str(args.output), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    with os.fdopen(descriptor, "w", encoding="utf-8") as output:
        output.write(credentials.to_json())
        output.write("\n")
    print("Authorized Google user:", email)
    print("Verified destination:", folder.get("name"))
    print("Private credential JSON saved to:", args.output.resolve())
    print("COPY its entire contents ONLY into Railway nabil-ai-school > Variables")
    print("Variable name: NABIL_DRIVE_OAUTH_TOKEN_JSON")
    print("Do NOT paste the token into chat, logs, GitHub, or a screenshot.")


if __name__ == "__main__":
    main()
