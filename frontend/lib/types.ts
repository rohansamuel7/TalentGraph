export type Coverage = Record<"required" | "preferred_only" | "non_required" | "insufficient", number>;

export interface Overview {
  sampled_jobs: number;
  synthetic_candidates: number;
  coverage: Coverage;
  sample_note: string;
}

export interface SkillFrequency {
  competency_id: string;
  competency_name: string;
  job_count: number;
}

export interface CandidateSummary {
  candidate_id: string;
  display_name: string;
  role_family: string;
  seniority: string;
  synthetic: boolean;
  competency_count: number;
}

export type GraphNodeType = "candidate" | "competency" | "job";
export interface GraphNode { id: string; type: GraphNodeType; label: string; properties: Record<string, unknown>; }
export interface GraphEdge { source: string; target: string; relationship: "HAS_SKILL" | "REQUIRES_SKILL" | "PREFERS_SKILL"; classification?: string | null; provenance: Record<string, unknown>; }
export interface GraphNeighborhood { root: string; nodes: GraphNode[]; edges: GraphEdge[]; truncated: boolean; }
export interface Match { candidate_id: string; job_id: string; title: string; company_name: string; evidence_status: string; required_skill_count: number; matched_required_count: number; required_skill_overlap: number | null; matched_skills: string[]; missing_skills: string[]; matched_preferred_skills: string[]; evidence_source: string[]; extraction_version: string[]; explanation: string; }
