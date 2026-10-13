"""Memory-bounded inspection and deterministic sampling for the M1 archive."""

from __future__ import annotations

import csv
import hashlib
import heapq
import json
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable
from zipfile import ZipFile


EXPECTED_POSTING_COLUMNS = {
    "job_id", "company_name", "title", "description", "max_salary",
    "pay_period", "location", "company_id", "views", "med_salary",
    "min_salary", "formatted_work_type", "applies", "original_listed_time",
    "remote_allowed", "job_posting_url", "application_url", "application_type",
    "expiry", "closed_time", "formatted_experience_level", "skills_desc",
    "listed_time", "posting_domain", "sponsored", "work_type", "currency",
    "compensation_type", "normalized_salary", "zip_code", "fips",
}


@dataclass(frozen=True)
class ArchiveInspection:
    archive: str
    archive_size_bytes: int
    archive_sha256: str
    members: tuple[dict[str, object], ...]
    posting_header: tuple[str, ...]
    posting_rows: int
    unique_job_ids: int
    duplicate_job_id_rows: int
    empty_job_id_rows: int
    malformed_rows: int
    listed_time_valid_rows: int
    listed_time_empty_rows: int
    listed_time_invalid_rows: int


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _safe_members(archive: Path) -> tuple[dict[str, object], ...]:
    with ZipFile(archive) as zipped:
        members = []
        for info in zipped.infolist():
            path = Path(info.filename)
            if path.is_absolute() or ".." in path.parts or "\\" in info.filename:
                raise ValueError(f"unsafe archive path: {info.filename}")
            members.append({
                "name": info.filename,
                "file_size": info.file_size,
                "compressed_size": info.compress_size,
                "compression": info.compress_type,
            })
        return tuple(members)


def _posting_rows(archive: Path) -> Iterable[tuple[int, list[str], list[str]]]:
    with ZipFile(archive) as zipped, zipped.open("postings.csv") as binary:
        import io

        with io.TextIOWrapper(binary, encoding="utf-8-sig", newline="") as text:
            rows = csv.reader(text)
            header = next(rows)
            for row_number, row in enumerate(rows, 2):
                yield row_number, header, row


def inspect_archive(archive: Path) -> ArchiveInspection:
    archive = archive.resolve()
    members = _safe_members(archive)
    names = {str(member["name"]) for member in members}
    if "postings.csv" not in names:
        raise ValueError("archive does not contain postings.csv")

    rows = unique_ids = duplicates = empty_ids = malformed = 0
    valid_times = empty_times = invalid_times = 0
    ids: set[str] = set()
    header: tuple[str, ...] = ()
    for row_number, raw_header, row in _posting_rows(archive):
        if not header:
            header = tuple(raw_header)
            if set(header) != EXPECTED_POSTING_COLUMNS:
                raise ValueError("postings.csv header differs from expected observed schema")
        rows += 1
        if len(row) != len(header):
            malformed += 1
            continue
        values = dict(zip(header, row))
        job_id = values["job_id"].strip()
        if not job_id:
            empty_ids += 1
        elif job_id in ids:
            duplicates += 1
        else:
            ids.add(job_id)
        listed = values["listed_time"].strip()
        if not listed:
            empty_times += 1
        else:
            try:
                datetime.fromtimestamp(float(listed) / 1000, tz=timezone.utc)
            except (ValueError, OverflowError, OSError):
                invalid_times += 1
            else:
                valid_times += 1
    return ArchiveInspection(
        str(archive), archive.stat().st_size, _sha256(archive), members, header,
        rows, len(ids), duplicates, empty_ids, malformed, valid_times,
        empty_times, invalid_times,
    )


def _listed_sort_value(value: str) -> float:
    return float(value) if value.strip() else float("-inf")


def sample_postings(archive: Path, output_csv: Path, metadata_json: Path,
                    rejects_csv: Path, sample_size: int = 1500) -> dict[str, object]:
    """Select the lowest SHA-256 job-id ranks without retaining full input rows."""
    if sample_size < 1:
        raise ValueError("sample_size must be positive")
    inspection = inspect_archive(archive)
    winners: dict[str, tuple[float, int]] = {}
    rejects: list[tuple[int, str]] = []
    for row_number, header, row in _posting_rows(Path(archive)):
        if len(row) != len(header):
            rejects.append((row_number, "column_count_mismatch"))
            continue
        values = dict(zip(header, row))
        job_id = values["job_id"].strip()
        if not job_id:
            rejects.append((row_number, "missing_job_id"))
            continue
        listed = values["listed_time"].strip()
        try:
            listed_value = _listed_sort_value(listed)
            if listed:
                datetime.fromtimestamp(listed_value / 1000, tz=timezone.utc)
        except (ValueError, OverflowError, OSError):
            rejects.append((row_number, "invalid_listed_time"))
            continue
        current = winners.get(job_id)
        candidate = (listed_value, row_number)
        if current is None or candidate > current:
            winners[job_id] = candidate

    heap: list[tuple[int, str, int]] = []
    for job_id, (_, row_number) in winners.items():
        rank = int.from_bytes(hashlib.sha256(job_id.encode("utf-8")).digest(), "big")
        item = (-rank, job_id, row_number)
        heapq.heappush(heap, item)
        if len(heap) > sample_size:
            heapq.heappop(heap)
    selected_rows = {item[2]: item[1] for item in heap}
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    metadata_json.parent.mkdir(parents=True, exist_ok=True)
    rejects_csv.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(archive) as zipped, zipped.open("postings.csv") as binary:
        import io

        with io.TextIOWrapper(binary, encoding="utf-8-sig", newline="") as text:
            rows = csv.reader(text)
            header = next(rows)
            with output_csv.open("w", encoding="utf-8", newline="") as target:
                writer = csv.writer(target)
                writer.writerow(header)
                for row_number, row in enumerate(rows, 2):
                    if row_number in selected_rows:
                        writer.writerow(row)
    with rejects_csv.open("w", encoding="utf-8", newline="") as target:
        writer = csv.writer(target)
        writer.writerow(["source_row_number", "reason"])
        writer.writerows(rejects)
    metadata = {
        "archive": str(Path(archive).resolve()),
        "archive_sha256": inspection.archive_sha256,
        "archive_size_bytes": inspection.archive_size_bytes,
        "archive_members": list(inspection.members),
        "source_dataset": "arshkon/linkedin-job-postings",
        "source_version": "unknown_from_archive; user-approved target was version 13",
        "source_member": "postings.csv",
        "sample_size_requested": sample_size,
        "sample_size_selected": len(selected_rows),
        "sample_method": "lowest_sha256_unsigned_rank_by_job_id_after_latest_listed_time_deduplication",
        "hash_algorithm": "sha256",
        "input_rows": inspection.posting_rows,
        "unique_job_ids": inspection.unique_job_ids,
        "reject_rows": len(rejects),
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "raw_data_policy": "local_only; do_not_redistribute_raw_postings_or_urls",
    }
    metadata_json.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    return metadata
