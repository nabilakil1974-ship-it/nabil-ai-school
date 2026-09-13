#!/usr/bin/env python3
"""Synchronise the public CRDP catalogue with NABIL AI's curriculum index.

The synchroniser is deliberately conservative:

* it accepts links from the official CRDP hosts only;
* it adds newly discovered grades/subjects and official resources;
* it never removes existing lessons, books, or subjects automatically;
* a failed/changed upstream page cannot replace the last good index;
* detailed lesson titles remain verified content and are not invented from a
  page heading.

Run without ``--apply`` for a report-only dry run.  GitHub Actions runs it once
per day with ``--apply``.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "config" / "crdp_sync_sources.json"
DEFAULT_INDEX = ROOT / "app" / "static" / "crdp_scientific_curriculum_index.json"
DEFAULT_REPORT = ROOT / "app" / "static" / "crdp_sync_report.json"
USER_AGENT = "NABIL-AI-CRDP-Sync/1.0 (+curriculum catalogue monitor)"


SUBJECT_ALIASES = {
    "اللغة العربية وآدابها": "اللغة العربية",
    "اللغة العربية": "اللغة العربية",
    "اللغة الفرنسية وآدابها": "اللغة الفرنسية",
    "اللغة الفرنسية": "اللغة الفرنسية",
    "اللغة الانكليزية وآدابها": "اللغة الإنجليزية",
    "اللغة الإنجليزية وآدابها": "اللغة الإنجليزية",
    "اللغة الانكليزية": "اللغة الإنجليزية",
    "اللغة الإنجليزية": "اللغة الإنجليزية",
    "الرياضيات": "رياضيات",
    "رياضيات": "رياضيات",
    "الفيزياء": "فيزياء",
    "فيزياء": "فيزياء",
    "الكيمياء": "كيمياء",
    "كيمياء": "كيمياء",
    "علوم الحياة": "علوم الحياة",
    "العلوم": "علوم",
    "التاريخ": "التاريخ",
    "الجغرافيا": "الجغرافيا",
    "التربية الوطنية والتنشئة المدنية": "التربية الوطنية والتنشئة المدنية",
    "التربية والتنشئة المدنية": "التربية الوطنية والتنشئة المدنية",
    "علم الاجتماع": "علم الاجتماع",
    "علم الاقتصاد": "علم الاقتصاد",
    "الفلسفة والحضارات": "الفلسفة والحضارات",
    "الفلسفة": "الفلسفة والحضارات",
    "المعلوماتية": "المعلوماتية",
    "التربية البدنية": "التربية البدنية",
    "التربية الفنية": "التربية الفنية",
    "الموسيقى": "الموسيقى",
}

GRADE_PATTERNS = (
    (r"(?:الصف|السنة)\s+الأولى(?!\s+ثان)", "الصف الأول"),
    (r"(?:الصف|السنة)\s+الثانية(?!\s+ثان)", "الصف الثاني"),
    (r"(?:الصف|السنة)\s+الثالثة(?!\s+ثان)", "الصف الثالث"),
    (r"(?:الصف|السنة)\s+الرابعة", "الصف الرابع"),
    (r"(?:الصف|السنة)\s+الخامسة", "الصف الخامس"),
    (r"(?:الصف|السنة)\s+السادسة", "الصف السادس"),
    (r"(?:الصف|السنة)\s+السابعة", "الصف السابع"),
    (r"(?:الصف|السنة)\s+الثامنة", "الصف الثامن"),
    (r"(?:الصف|السنة)\s+التاسعة", "الصف التاسع"),
    (r"(?:التعليم\s+الثانوي\s*[-–—:]?\s*)?(?:السنة|الصف)\s+الأولى", "الأول ثانوي"),
    (r"(?:التعليم\s+الثانوي\s*[-–—:]?\s*)?(?:السنة|الصف)\s+الثانية", "الثاني ثانوي"),
    (r"(?:التعليم\s+الثانوي\s*[-–—:]?\s*)?(?:السنة|الصف)\s+الثالثة", "الثالث ثانوي"),
)

BRANCH_ALIASES = {
    "علوم الحياة": "علوم الحياة",
    "العلوم العامة": "العلوم العامة",
    "الاجتماع والاقتصاد": "الاجتماع والاقتصاد",
    "الآداب والإنسانيات": "الآداب والإنسانيات",
    "الإنسانيات": "الإنسانيات",
    "العلوم": "العلوم",
}

RELEVANT_TERMS = (
    "منهج", "مناهج", "درس", "دروس", "كتاب", "كتب", "مادة", "مواد",
    "صف", "السنة", "التعليم", "امتحان", "أهداف", "كفايات", "curriculum",
    "book", "textbook", ".pdf", ".doc", ".xls",
)


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip(" \t\r\n-|–—")


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[tuple[str, str]] = []
        self._href: str | None = None
        self._parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "a":
            return
        self._href = dict(attrs).get("href")
        self._parts = []

    def handle_data(self, data: str) -> None:
        if self._href is not None:
            self._parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "a" and self._href is not None:
            self.links.append((self._href, clean_text(" ".join(self._parts))))
            self._href = None
            self._parts = []


@dataclass(frozen=True)
class FetchResult:
    url: str
    body: bytes
    content_type: str
    etag: str
    last_modified: str


def fetch(url: str, timeout: int = 30, retries: int = 2) -> FetchResult:
    error: Exception | None = None
    for attempt in range(retries + 1):
        try:
            request = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "text/html,*/*;q=0.8"})
            with urlopen(request, timeout=timeout) as response:
                return FetchResult(
                    url=response.geturl(),
                    body=response.read(12 * 1024 * 1024),
                    content_type=response.headers.get("Content-Type", ""),
                    etag=response.headers.get("ETag", ""),
                    last_modified=response.headers.get("Last-Modified", ""),
                )
        except (HTTPError, URLError, TimeoutError) as exc:
            error = exc
            if attempt < retries:
                time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"تعذر جلب المصدر الرسمي {url}: {error}")


def is_official(url: str, allowed_hosts: set[str]) -> bool:
    parsed = urlparse(url)
    return parsed.scheme in {"http", "https"} and (parsed.hostname or "").lower() in allowed_hosts


def infer_grade(text: str) -> str | None:
    normalized = clean_text(text)
    is_secondary = "ثانوي" in normalized
    # Secondary patterns must win over the identically named basic grades.
    if is_secondary:
        for pattern, grade in GRADE_PATTERNS[9:]:
            if re.search(pattern, normalized):
                return grade
    for pattern, grade in GRADE_PATTERNS[:9]:
        if re.search(pattern, normalized):
            return grade
    return None


def infer_subjects(text: str) -> list[str]:
    # A branch name such as "فرع العلوم" is not itself a subject. Book-list
    # headings normally describe only a grade/branch and must not expand the
    # subject selector unless the heading explicitly says "مادة".
    if "فرع" in text and "مادة" not in text:
        return []
    found: list[str] = []
    for alias in sorted(SUBJECT_ALIASES, key=len, reverse=True):
        if alias in text:
            canonical = SUBJECT_ALIASES[alias]
            if canonical not in found:
                found.append(canonical)
    return found


def deduplicate_resources(resources: Iterable[dict]) -> list[dict]:
    """Collapse the same official URL discovered through several source pages."""
    merged: dict[str, dict] = {}
    for item in resources:
        item_id = item["id"]
        previous = merged.get(item_id)
        if previous is None:
            merged[item_id] = deepcopy(item)
            continue
        # Prefer the most descriptive label and retain all inferred metadata.
        if len(item.get("title", "")) > len(previous.get("title", "")):
            previous["title"] = item["title"]
        previous["grade"] = previous.get("grade") or item.get("grade")
        previous["branch"] = previous.get("branch") or item.get("branch")
        previous["subjects"] = list(dict.fromkeys(
            (previous.get("subjects") or []) + (item.get("subjects") or [])
        ))
    return list(merged.values())


def infer_branch(text: str) -> str | None:
    for alias in sorted(BRANCH_ALIASES, key=len, reverse=True):
        if re.search(rf"(?:فرع\s+)?{re.escape(alias)}", text):
            return BRANCH_ALIASES[alias]
    return None


def resource_kind(source_kind: str, url: str, title: str) -> str:
    path = urlparse(url).path.lower()
    if path.endswith(".pdf") or "تحميل" in title:
        return "document"
    if source_kind == "books" or "كتاب" in title:
        return "book_catalog"
    if "منهج" in title or "curriculum" in path:
        return "curriculum"
    return source_kind


def parse_resources(
    html: str,
    base_url: str,
    source_name: str,
    source_kind: str,
    allowed_hosts: set[str],
) -> list[dict]:
    parser = LinkParser()
    parser.feed(html)
    resources: list[dict] = []
    seen: set[str] = set()
    for href, title in parser.links:
        absolute = urljoin(base_url, href).split("#", 1)[0]
        combined = clean_text(f"{title} {absolute}")
        if not title or not is_official(absolute, allowed_hosts):
            continue
        if not any(term.casefold() in combined.casefold() for term in RELEVANT_TERMS):
            continue
        key = hashlib.sha256(absolute.encode("utf-8")).hexdigest()[:16]
        if key in seen:
            continue
        seen.add(key)
        resources.append({
            "id": key,
            "title": title,
            "url": absolute,
            "kind": resource_kind(source_kind, absolute, title),
            "source": source_name,
            "grade": infer_grade(title),
            "branch": infer_branch(title),
            "subjects": infer_subjects(title),
        })
    return resources


def merge_resources(old: Iterable[dict], fresh: Iterable[dict], checked_at: str) -> tuple[list[dict], dict]:
    old_by_id = {item.get("id"): deepcopy(item) for item in old if item.get("id")}
    added: list[str] = []
    changed: list[str] = []
    seen_now: set[str] = set()

    for item in fresh:
        item_id = item["id"]
        seen_now.add(item_id)
        previous = old_by_id.get(item_id)
        if previous is None:
            item["first_seen"] = checked_at
            added.append(item["title"])
        else:
            item["first_seen"] = previous.get("first_seen", checked_at)
            comparable_keys = ("title", "url", "kind", "grade", "branch", "subjects")
            if any(previous.get(key) != item.get(key) for key in comparable_keys):
                changed.append(item["title"])
        item["last_seen"] = checked_at
        item["active"] = True
        old_by_id[item_id] = item

    # Preserve missing entries. A temporary page failure or redesign must not
    # silently remove curriculum content from the learning platform.
    for item_id, item in old_by_id.items():
        if item_id not in seen_now:
            item["active"] = item.get("active", True)

    merged = sorted(old_by_id.values(), key=lambda item: (item.get("kind", ""), item.get("title", ""), item["id"]))
    return merged, {"added": added, "changed": changed}


def merge_availability(index: dict, resources: Iterable[dict]) -> list[dict]:
    availability = index.setdefault("subject_availability", {})
    changes: list[dict] = []
    for item in resources:
        grade = item.get("grade")
        subjects = item.get("subjects") or []
        if not grade or not subjects:
            continue
        current = availability.setdefault(grade, [])
        for subject in subjects:
            if subject not in current:
                current.append(subject)
                changes.append({"grade": grade, "subject": subject, "source": item["url"]})
    return changes


def sync(config_path: Path, index_path: Path) -> tuple[dict, dict]:
    config = json.loads(config_path.read_text(encoding="utf-8"))
    original_index = json.loads(index_path.read_text(encoding="utf-8"))
    index = deepcopy(original_index)
    allowed_hosts = {host.lower() for host in config["allowed_hosts"]}
    checked_at = now_iso()
    fresh_resources: list[dict] = []
    source_states: list[dict] = []

    for source in config["sources"]:
        result = fetch(source["url"])
        if not is_official(result.url, allowed_hosts):
            raise RuntimeError(f"رفض تحويل خارج نطاق CRDP الرسمي: {result.url}")
        html = result.body.decode("utf-8", errors="replace")
        parsed = parse_resources(
            html, result.url, source["name"], source["kind"], allowed_hosts
        )
        fresh_resources.extend(parsed)
        semantic_page = json.dumps(
            [
                {
                    key: item.get(key)
                    for key in ("id", "title", "url", "kind", "grade", "branch", "subjects")
                }
                for item in sorted(parsed, key=lambda value: value["id"])
            ],
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        source_states.append({
            "name": source["name"],
            "url": result.url,
            "kind": source["kind"],
            "checked_at": checked_at,
            # Hash only curriculum-relevant links. CRDP pages contain dynamic
            # markup which changes between requests without a content update.
            "sha256": hashlib.sha256(semantic_page).hexdigest(),
            "etag": result.etag,
            "last_modified": result.last_modified,
            "links_found": len(parsed),
        })

    old_sync = index.get("official_sync", {})
    fresh_resources = deduplicate_resources(fresh_resources)
    previous = old_sync.get("resources", [])
    resources, resource_changes = merge_resources(previous, fresh_resources, checked_at)
    availability_changes = merge_availability(index, resources)
    old_source_hashes = {
        item.get("name"): item.get("sha256")
        for item in old_sync.get("sources", [])
        if item.get("name")
    }
    source_pages_changed = [
        item["name"]
        for item in source_states
        if old_source_hashes.get(item["name"]) != item["sha256"]
    ]
    changed = bool(
        source_pages_changed
        or resource_changes["added"]
        or resource_changes["changed"]
        or availability_changes
    )
    index["official_sync"] = {
        "status": "ok",
        "policy": "official_crdp_only_additive_no_automatic_deletion",
        "last_successful_check": checked_at,
        "sources": source_states,
        "resources": resources,
    }
    index.setdefault("meta", {})["official_source"] = "https://www.crdp.org/"
    index["meta"]["last_crdp_sync"] = checked_at

    report = {
        "status": "ok",
        "changed": changed,
        "checked_at": checked_at,
        "resources_total": len(resources),
        "resources_discovered_now": len(fresh_resources),
        "resources_added": resource_changes["added"],
        "resources_changed": resource_changes["changed"],
        "source_pages_changed": source_pages_changed,
        "availability_added": availability_changes,
        "safety": "No existing curriculum entries were deleted.",
    }
    # Do not create a daily timestamp-only commit when CRDP content is
    # unchanged. The run log/report still proves that the check completed.
    return (index if changed else original_index), report


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Synchronise official CRDP curriculum metadata")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--index", type=Path, default=DEFAULT_INDEX)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--apply", action="store_true", help="write the updated index and report")
    args = parser.parse_args()

    try:
        index, report = sync(args.config, args.index)
    except Exception as exc:
        print(f"CRDP sync failed; existing index was preserved: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(report, ensure_ascii=False, indent=2))
    if args.apply:
        write_json(args.index, index)
        write_json(args.report, report)
    else:
        print("Dry run only. Re-run with --apply to write changes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
