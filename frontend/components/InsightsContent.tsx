"use client";

import { useEffect, useState } from "react";
import { getOverview, getSkillFrequency } from "../lib/api";
import type { Overview, SkillFrequency } from "../lib/types";
import { EvidenceDonut, SkillFrequencyChart } from "./InsightsCharts";
import { ErrorState, Loading } from "./States";

export function InsightsContent() {
  const [data, setData] = useState<{ overview: Overview; skills: SkillFrequency[] }>();
  const [error, setError] = useState<string>();

  useEffect(() => {
    Promise.all([getOverview(), getSkillFrequency()])
      .then(([overview, frequency]) => setData({ overview, skills: frequency.items }))
      .catch((reason: Error) => setError(reason.message));
  }, []);

  if (error) return <ErrorState message={error} />;
  if (!data) return <Loading label="Loading evidence insights" />;

  const { overview, skills } = data;
  // This includes preferred-only and non-required groups; it differs from
  // the chart's narrower "no eligible technical evidence" category.
  const withoutRequired = overview.sampled_jobs - overview.coverage.required;
  return <div className="insights-dashboard">
    <div className="insights-kpis">
      <div className="metric"><span>Sampled jobs</span><strong>{overview.sampled_jobs.toLocaleString()}</strong></div>
      <div className="metric"><span>Synthetic candidates</span><strong>{overview.synthetic_candidates.toLocaleString()}</strong></div>
      <div className="metric"><span>Jobs with required evidence</span><strong>{overview.coverage.required.toLocaleString()}</strong></div>
      <div className="metric"><span>Jobs lacking required evidence</span><strong>{withoutRequired.toLocaleString()}</strong></div>
    </div>
    <div className="insights-charts">
      <section className="surface chart-panel"><h2>Evidence coverage</h2><p className="chart-description">Classification of the sampled jobs by extracted technical evidence.</p><EvidenceDonut coverage={overview.coverage} total={overview.sampled_jobs} /></section>
      <section className="surface chart-panel"><h2>Technical skill frequency</h2><p className="chart-description">Distinct sampled jobs with observed required or preferred evidence for each skill.</p>{skills.length ? <SkillFrequencyChart items={skills} /> : <p className="muted">No eligible technical-skill evidence is available.</p>}</section>
    </div>
    <p className="insights-note">Extraction is heuristic; missing evidence does not mean a job has no skills. {overview.sample_note}</p>
  </div>;
}
