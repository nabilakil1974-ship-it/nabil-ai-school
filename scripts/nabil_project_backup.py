"""Create a source/runtime snapshot ZIP and upload it to Google Drive.

This backup intentionally excludes secrets and disposable caches while keeping
all project source, static assets, configuration, audit notes, generated output,
and durable local artifacts present in the deployed /app image.
"""
from __future__ import annotations

import hashlib
import json
import os
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path

from googleapiclient.http import MediaFileUpload

from scripts import nabil_lesson_factory as factory

ROOT = Path("/app")
BACKUP_FOLDER_NAME = "NABIL AI - Project Backups"

EXCLUDED_DIRS = {
    ".git", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache",
    ".venv", "venv", "node_modules",
}
EXCLUDED_FILES = {
    ".env", ".env.local", ".env.production", ".env.development",
}
SECRET_SUFFIXES = {".pem", ".p12", ".pfx", ".key"}


def _safe_file(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    if any(part in EXCLUDED_DIRS for part in rel.parts):
        return False
    if path.name in EXCLUDED_FILES:
        return False
    if path.suffix.lower() in SECRET_SUFFIXES:
        return False
    return path.is_file()


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _find_or_create_backup_folder(service) -> str:
    escaped = BACKUP_FOLDER_NAME.replace("'", "\\'")
    resp = service.files().list(
        q=(
            "name='%s' and mimeType='application/vnd.google-apps.folder' "
            "and trashed=false" % escaped
        ),
        spaces="drive",
        fields="files(id,name,createdTime)",
        orderBy="createdTime desc",
        pageSize=10,
    ).execute()
    folders = resp.get("files") or []
    if folders:
        return folders[0]["id"]
    created = service.files().create(
        body={
            "name": BACKUP_FOLDER_NAME,
            "mimeType": "application/vnd.google-apps.folder",
        },
        fields="id",
    ).execute()
    return created["id"]


def _existing_backup(service, folder_id: str, name: str):
    escaped = name.replace("'", "\\'")
    resp = service.files().list(
        q=(
            "'%s' in parents and name='%s' and trashed=false"
            % (folder_id, escaped)
        ),
        spaces="drive",
        fields="files(id,name,size,md5Checksum,webViewLink,modifiedTime)",
        pageSize=10,
    ).execute()
    return (resp.get("files") or [None])[0]


def create_backup() -> tuple[Path, dict]:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%SZ")
    commit = (
        os.getenv("RAILWAY_GIT_COMMIT_SHA")
        or os.getenv("GIT_COMMIT_SHA")
        or "unknown"
    )
    short = commit[:12] if commit != "unknown" else "unknown"
    name = f"NABIL_AI_FULL_PROJECT_{timestamp}_{short}.zip"
    out = Path(tempfile.gettempdir()) / name

    files = sorted(
        (p for p in ROOT.rglob("*") if _safe_file(p)),
        key=lambda p: p.as_posix(),
    )

    manifest = {
        "backup_schema": "NABIL_PROJECT_BACKUP_V1",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_root": "/app",
        "railway_service": os.getenv("RAILWAY_SERVICE_NAME"),
        "git_commit_sha": commit,
        "file_count": len(files),
        "security_exclusions": {
            "directories": sorted(EXCLUDED_DIRS),
            "files": sorted(EXCLUDED_FILES),
            "secret_suffixes": sorted(SECRET_SUFFIXES),
            "note": "Environment variables/API keys are intentionally not archived.",
        },
    }

    with zipfile.ZipFile(
        out, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6
    ) as zf:
        for path in files:
            rel = path.relative_to(ROOT).as_posix()
            zf.write(path, arcname=f"nabil-ai-school/{rel}")
        zf.writestr(
            "nabil-ai-school/BACKUP_MANIFEST.json",
            json.dumps(manifest, ensure_ascii=False, indent=2),
        )

    manifest["zip_size_bytes"] = out.stat().st_size
    manifest["zip_sha256"] = _sha256(out)
    return out, manifest


def upload_backup(path: Path, manifest: dict) -> dict:
    service = factory.get_drive_service()
    folder_id = _find_or_create_backup_folder(service)

    existing = _existing_backup(service, folder_id, path.name)
    if existing:
        return {
            "status": "ALREADY_EXISTS",
            "folder_id": folder_id,
            "file": existing,
            "sha256": manifest["zip_sha256"],
        }

    media = MediaFileUpload(
        str(path), mimetype="application/zip", resumable=True
    )
    uploaded = service.files().create(
        body={"name": path.name, "parents": [folder_id]},
        media_body=media,
        fields="id,name,size,md5Checksum,webViewLink,modifiedTime",
    ).execute()

    sha_name = path.name + ".sha256.txt"
    sha_path = path.with_name(sha_name)
    sha_path.write_text(
        manifest["zip_sha256"] + "  " + path.name + "\n",
        encoding="utf-8",
    )
    sha_media = MediaFileUpload(
        str(sha_path), mimetype="text/plain", resumable=False
    )
    service.files().create(
        body={"name": sha_name, "parents": [folder_id]},
        media_body=sha_media,
        fields="id",
    ).execute()

    return {
        "status": "UPLOADED",
        "folder_id": folder_id,
        "file": uploaded,
        "sha256": manifest["zip_sha256"],
    }


def main() -> None:
    path, manifest = create_backup()
    result = upload_backup(path, manifest)
    print(json.dumps({
        "stage": "PROJECT_BACKUP_UPLOADED",
        "backup_name": path.name,
        "file_count": manifest["file_count"],
        "zip_size_bytes": manifest["zip_size_bytes"],
        "zip_sha256": manifest["zip_sha256"],
        **result,
    }, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
