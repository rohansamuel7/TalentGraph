"use client";

import { useEffect, useMemo, useState } from "react";
import { getCandidates, getMatches } from "../lib/api";
import type { CandidateSummary, Match } from "../lib/types";
import { formatEvidenceStatus, formatRoleFamily } from "../lib/presentation";
import { ErrorState, Loading } from "./States";

function SkillChips({ skills, tone }: { skills: string[]; tone: "matched" | "missing" | "preferred" }) {
  if (skills.length === 0) return <p className="empty-skill-note">None observed</p>;
  return <div className={`skill-chips ${tone}`}>{skills.map((skill) => <span className="skill-chip" key={skill}>{skill}</span>)}</div>;
}

function ComparisonDetails({ match }: { match: Match }) {
  return <div className="split-details">
    <header className="split-detail-header"><div><p className="eyebrow">Job comparison</p><h2>{match.title}</h2><p>{match.company_name}</p></div><div className="detail-count">{match.required_skill_overlap === null ? <strong>Unavailable</strong> : <strong>{match.matched_required_count} of {match.required_skill_count}</strong>}<span>Observed required skills matched</span><small>{formatEvidenceStatus(match.evidence_status)}</small></div></header>
    <section className="detail-section"><h3>Required skills</h3><div className="required-skill-columns"><div><h4>Matched</h4><SkillChips skills={match.matched_skills} tone="matched" /></div><div><h4>Missing</h4><SkillChips skills={match.missing_skills} tone="missing" /></div></div></section>
    {match.matched_preferred_skills.length > 0 && <section className="detail-section"><h3>Matched preferred skills</h3><SkillChips skills={match.matched_preferred_skills} tone="preferred" /></section>}
    <section className="detail-section"><h3>Evidence &amp; limitations</h3><p>Source: {match.evidence_source.join(", ") || "Not available"}</p><p>Extracted competency evidence is partial and does not represent all job requirements.</p><details className="evidence-details"><summary>Technical record details</summary><p>{match.explanation}</p><p>Job ID: {match.job_id}</p>{match.extraction_version.length > 0 && <p>Extraction version: {match.extraction_version.join(", ")}</p>}</details></section>
  </div>;
}

export function MatchesContent() {
  const [data, setData] = useState<{ candidates: CandidateSummary[] }>();
  const [candidateId, setCandidateId] = useState("");
  const [matches, setMatches] = useState<Match[]>();
  const [selectedJobId, setSelectedJobId] = useState("");
  const [loadingMatches, setLoadingMatches] = useState(false);
  const [query, setQuery] = useState("");
  const [sort, setSort] = useState("overlap");
  const [comparableOnly, setComparableOnly] = useState(false);
  const [error, setError] = useState<string>();

  useEffect(() => { getCandidates().then((result) => { setData({ candidates: result.items }); const requested = new URLSearchParams(window.location.search).get("candidate"); setCandidateId(result.items.find((item) => item.candidate_id === requested)?.candidate_id ?? result.items[0]?.candidate_id ?? ""); }).catch((reason: Error) => setError(reason.message)); }, []);
  useEffect(() => {
    if (!candidateId) return;
    let active = true;
    setLoadingMatches(true); setMatches(undefined); setSelectedJobId(""); setError(undefined);
    getMatches(candidateId).then((result) => { if (active) setMatches(result.items); })
      .catch((reason: Error) => { if (active) setError(reason.message); })
      .finally(() => { if (active) setLoadingMatches(false); });
    return () => { active = false; };
  }, [candidateId]);
  // Null overlap means evidence is unavailable; keep it out of the
  // comparable-only view and below observed values when sorting.
  const visibleMatches = useMemo(() => matches?.filter((match) => !comparableOnly || match.required_skill_overlap !== null).filter((match) => `${match.title} ${match.company_name}`.toLowerCase().includes(query.toLowerCase().trim())).sort((a, b) => sort === "required" ? b.required_skill_count - a.required_skill_count || a.job_id.localeCompare(b.job_id) : (b.required_skill_overlap ?? -1) - (a.required_skill_overlap ?? -1) || a.job_id.localeCompare(b.job_id)), [matches, comparableOnly, query, sort]);
  useEffect(() => {
    if (visibleMatches?.length && !visibleMatches.some((match) => match.job_id === selectedJobId)) setSelectedJobId(visibleMatches[0].job_id);
  }, [visibleMatches, selectedJobId]);
  const selectedMatch = visibleMatches?.find((match) => match.job_id === selectedJobId);

  if (error) return <ErrorState message={error} />;
  if (!data) return <Loading />;
  const candidate = data.candidates.find((item) => item.candidate_id === candidateId);
  return <section className="matches-workspace">
    <div className="matches-toolbar"><label className="match-selector">Candidate<select aria-label="Candidate" value={candidateId} onChange={(event) => setCandidateId(event.target.value)}>{data.candidates.map((item) => <option key={item.candidate_id} value={item.candidate_id}>{item.display_name} · {formatRoleFamily(item.role_family)}</option>)}</select></label><label>Search jobs<input aria-label="Search jobs" value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Title or company" /></label><label>Sort by<select aria-label="Sort matches" value={sort} onChange={(event) => setSort(event.target.value)}><option value="overlap">Observed overlap</option><option value="required">Observed required skills</option></select></label><label className="checkbox-label"><input type="checkbox" checked={comparableOnly} onChange={(event) => setComparableOnly(event.target.checked)} /> Comparable only</label></div>
    <p className="matches-limitation">Matches reflect observed technical skill overlap, not hiring suitability.</p>
    {candidate && <div className="candidate-context"><div className="candidate-avatar" aria-hidden="true">{candidate.display_name.split(" ").map((part) => part[0]).join("")}</div><div><strong>{candidate.display_name}</strong><span>{formatRoleFamily(candidate.role_family)} · {candidate.competency_count} technical competencies</span></div></div>}
    <div className="results-heading"><h2>Comparison results</h2>{matches && <span>{visibleMatches?.length ?? 0} of {matches.length} jobs</span>}</div>
    {loadingMatches && <Loading />}{!loadingMatches && matches?.length === 0 && <p className="empty-state">No comparisons are available for this candidate.</p>}{!loadingMatches && matches && matches.length > 0 && visibleMatches?.length === 0 && <p className="empty-state">No comparisons match the current filters.</p>}{!loadingMatches && visibleMatches && visibleMatches.length > 0 && <div className="matches-split"><div className="match-list" aria-label="Job comparisons">{visibleMatches.map((match) => <button className={`match-option${selectedMatch?.job_id === match.job_id ? " selected" : ""}`} key={match.job_id} type="button" aria-pressed={selectedMatch?.job_id === match.job_id} onClick={() => setSelectedJobId(match.job_id)}><span className="match-option-title">{match.title}</span><span className="match-option-company">{match.company_name}</span><span className="match-option-footer"><strong>{match.required_skill_overlap === null ? "No required evidence" : `${match.matched_required_count} of ${match.required_skill_count}`}</strong><small>{formatEvidenceStatus(match.evidence_status)}</small></span></button>)}</div><div className="match-detail-panel" aria-live="polite">{selectedMatch && <ComparisonDetails match={selectedMatch} />}</div></div>}
  </section>;
}
