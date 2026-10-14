"""Typed public response models for the TalentGraph API."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class Page(BaseModel):
    """Common pagination metadata."""
    total: int
    limit: int
    offset: int


class Evidence(BaseModel):
    """Auditable extracted competency evidence."""
    competency_id: str
    competency_name: str
    classification: str
    evidence_text: str
    source: str
    extraction_rule: str
    extraction_version: str
    source_description_sha256: str
    source_location: dict[str, Any] = Field(default_factory=dict)


class JobSummary(BaseModel):
    """Readable sampled-job summary."""
    job_id: str
    title: str
    company_name: str
    location: str | None = None
    evidence_status: str


class CandidateSummary(BaseModel):
    """Synthetic candidate summary without protected attributes."""
    candidate_id: str
    display_name: str
    role_family: str
    seniority: str
    synthetic: bool = True
    competency_count: int


class Match(BaseModel):
    """Explainable M7 comparison; overlap is not suitability."""
    candidate_id: str
    job_id: str
    title: str
    company_name: str
    evidence_status: str
    required_skill_count: int
    matched_required_count: int
    required_skill_overlap: float | None
    matched_skills: list[str]
    missing_skills: list[str]
    matched_preferred_skills: list[str]
    evidence_source: list[str]
    extraction_version: list[str]
    explanation: str


class GraphNode(BaseModel):
    """Stable graph node with readable display fields."""
    id: str
    type: str
    label: str
    properties: dict[str, Any] = Field(default_factory=dict)


class GraphEdge(BaseModel):
    """Graph edge with requirement class and provenance."""
    source: str
    target: str
    relationship: str
    classification: str | None = None
    provenance: dict[str, Any] = Field(default_factory=dict)


class GraphResponse(BaseModel):
    """Bounded deterministic graph neighborhood."""
    root: str
    nodes: list[GraphNode]
    edges: list[GraphEdge]
    truncated: bool
