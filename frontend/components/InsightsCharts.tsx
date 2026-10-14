import type { Coverage, SkillFrequency } from "../lib/types";

const COVERAGE = [
  { key: "required", label: "Required technical evidence", color: "var(--chart-required)" },
  { key: "preferred_only", label: "Preferred only", color: "var(--chart-preferred)" },
  { key: "non_required", label: "Non-required only", color: "var(--chart-nonrequired)" },
  { key: "insufficient", label: "No eligible technical evidence", color: "var(--chart-insufficient)" },
] as const;

export function EvidenceDonut({ coverage, total }: { coverage: Coverage; total: number }) {
  const circumference = 2 * Math.PI * 58;
  let offset = 0;
  return <div className="coverage-layout">
    <figure className="donut-figure">
      <svg viewBox="0 0 160 160" role="img" aria-label={`Evidence coverage across ${total.toLocaleString()} sampled jobs`}>
        <circle cx="80" cy="80" r="58" fill="none" stroke="var(--chart-track)" strokeWidth="18" />
        {COVERAGE.map((group) => {
          const length = total ? coverage[group.key] / total * circumference : 0;
          const segment = <circle key={group.key} cx="80" cy="80" r="58" fill="none" stroke={group.color} strokeWidth="18" strokeDasharray={`${length} ${circumference - length}`} strokeDashoffset={-offset} transform="rotate(-90 80 80)"><title>{group.label}: {coverage[group.key].toLocaleString()} jobs</title></circle>;
          offset += length;
          return segment;
        })}
        <text x="80" y="77" textAnchor="middle" className="donut-total">{total.toLocaleString()}</text>
        <text x="80" y="96" textAnchor="middle" className="donut-caption">sampled jobs</text>
      </svg>
      <figcaption className="sr-only">Mutually exclusive evidence groups; counts and percentages are listed beside the chart.</figcaption>
    </figure>
    <ul className="coverage-legend">{COVERAGE.map((group) => <li key={group.key}><span className="chart-swatch" style={{ backgroundColor: group.color }} aria-hidden="true" /><span>{group.label}</span><strong>{coverage[group.key].toLocaleString()}</strong><small>{total ? (coverage[group.key] / total * 100).toFixed(1) : "0.0"}%</small></li>)}</ul>
  </div>;
}

export function SkillFrequencyChart({ items }: { items: SkillFrequency[] }) {
  // API counts distinct jobs with eligible evidence, not candidate skills.
  const max = Math.max(...items.map((item) => item.job_count), 1);
  return <ol className="frequency-list" aria-label="Jobs with observed required or preferred technical competencies">{items.map((item) => <li key={item.competency_id} title={`${item.competency_name}: ${item.job_count} sampled jobs`}><span className="frequency-label">{item.competency_name}</span><span className="frequency-track"><span className="frequency-fill" style={{ width: `${item.job_count / max * 100}%` }} /></span><strong>{item.job_count}</strong></li>)}</ol>;
}
