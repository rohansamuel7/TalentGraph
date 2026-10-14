"""Evidence-preservation and human-label helpers for QA-FIX-06."""

from __future__ import annotations

import csv
import hashlib
import io
import re
import zipfile
from pathlib import Path
from typing import Iterable

from .qa_fix_extraction import RULES

ALLOWED_LABELS = {"required", "preferred", "incidental", "negated", "ambiguous"}


def load_descriptions(archive: Path, wanted: set[str]) -> dict[str, tuple[str, int]]:
    """Read complete source descriptions for the requested extractor job keys."""
    found: dict[str, tuple[str, int]] = {}
    with zipfile.ZipFile(archive) as source:
        with source.open("postings.csv") as stream:
            reader = csv.DictReader(io.TextIOWrapper(stream, encoding="utf-8-sig", newline=""))
            for row_number, row in enumerate(reader, 2):
                job_key = "linkedin:" + row["job_id"]
                if job_key in wanted:
                    found[job_key] = (row.get("description") or "", row_number)
    return found


def source_hash(text: str) -> str:
    """Hash the exact UTF-8 source description, without normalization."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def clean_display(text: str) -> str:
    """Make a readable display string while retaining source meaning and tokens."""
    cleaned = text.replace("\r\n", "\n").replace("\r", "\n")
    cleaned = re.sub(r"<br\s*/?>", "\n", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"</?(?:p|div|li|h[1-6])[^>]*>", "\n", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"[ \t]+", " ", cleaned)
    return re.sub(r"\n{3,}", "\n\n", cleaned).strip()


def _sentence_preview(text: str, limit: int = 360) -> str:
    """Return complete sentence/list units where possible, never a half-word."""
    if len(text) <= limit:
        return text
    units = re.split(r"(?<=[.!?])\s+|\n+|(?<=•)\s*", text)
    preview = ""
    for unit in units:
        candidate = f"{preview} {unit}".strip()
        if len(candidate) > limit and preview:
            break
        preview = candidate
    if not preview:
        preview = text[:limit].rsplit(" ", 1)[0]
    return preview.rstrip() + " [preview; full evidence preserved]"


def evidence_excerpt(text: str, competency_id: str | None) -> tuple[str, str, str]:
    """Return original excerpt, cleaned full excerpt, and readable preview."""
    if not competency_id or competency_id not in RULES:
        cleaned = clean_display(text)
        return text, cleaned, _sentence_preview(cleaned)
    for pattern in RULES[competency_id][1]:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            start = max(0, text.rfind("\n", 0, match.start()) + 1)
            stops = [text.find(mark, match.end()) for mark in ".!?\n" if text.find(mark, match.end()) >= 0]
            end = min(stops) + 1 if stops else len(text)
            original = text[start:end].strip()
            cleaned = clean_display(original)
            return original, cleaned, _sentence_preview(cleaned)
    cleaned = clean_display(text)
    return text, cleaned, _sentence_preview(cleaned)


def validate_labels(rows: Iterable[dict[str, str]], expected: set[tuple[str, str]]) -> None:
    """Reject missing, duplicate, unknown, or unsupported reviewed records."""
    rows = list(rows)
    keys = [(row["job_key"], row["competency"]) for row in rows]
    if len(rows) != 25 or len(set(keys)) != 25 or set(keys) != expected:
        raise ValueError("QA-FIX-06 human labels must contain exactly the 25 worksheet keys")
    invalid = [row["confirmed_label"] for row in rows if row["confirmed_label"] not in ALLOWED_LABELS and row["confirmed_label"] != "required/preferred"]
    if invalid:
        raise ValueError(f"Unsupported human labels: {sorted(set(invalid))}")
