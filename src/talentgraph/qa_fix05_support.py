"""Small I/O and evidence helpers for QA-FIX-05."""

from __future__ import annotations

import csv
import io
import re
import zipfile
from pathlib import Path

from .qa_fix_extraction import RULES


def load_descriptions(archive: Path) -> dict[str, tuple[str, int]]:
    """Load source descriptions keyed by the extractor's job key."""
    descriptions: dict[str, tuple[str, int]] = {}
    with zipfile.ZipFile(archive) as archive_file:
        with archive_file.open("postings.csv") as stream:
            text_stream = io.TextIOWrapper(stream, encoding="utf-8-sig", newline="")
            for row_number, row in enumerate(csv.DictReader(text_stream), 2):
                descriptions["linkedin:" + row["job_id"]] = (
                    row.get("description") or "", row_number
                )
    return descriptions


def evidence_snippet(text: str, competency_id: str | None) -> str:
    """Return a bounded, whitespace-normalized source snippet."""
    if not competency_id or competency_id not in RULES:
        return "[No dictionary term detected in sampled description]"
    for pattern in RULES[competency_id][1]:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            start = max(0, match.start() - 90)
            end = min(len(text), match.end() + 110)
            return re.sub(r"\s+", " ", text[start:end]).strip()[:240]
    return "[Competency retained by extractor; evidence text unavailable]"
