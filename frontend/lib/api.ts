import type { CandidateSummary, GraphNeighborhood, Match, Overview, SkillFrequency } from "./types";

// The default path uses Next.js's local rewrite; the browser never reads DuckDB.
const baseUrl = process.env.NEXT_PUBLIC_API_URL ?? "/backend";

async function request<T>(path: string): Promise<T> {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 8000);
  try {
    const response = await fetch(`${baseUrl}${path}`, { signal: controller.signal, cache: "no-store" });
    if (!response.ok) throw new Error(`Backend request failed (${response.status})`);
    return response.json() as Promise<T>;
  } finally {
    clearTimeout(timeout);
  }
}

export const getOverview = () => request<Overview>("/api/overview");
export const getSkillFrequency = () => request<{ items: SkillFrequency[]; definition: string }>("/api/insights/skill-frequency");
export const getCandidates = () => request<{ items: CandidateSummary[] }>("/api/candidates?limit=6");
export const getNeighborhood = (nodeId: string, hops = 1, limit = 35) => request<GraphNeighborhood>(`/api/graph/neighborhood?node_id=${encodeURIComponent(nodeId)}&hops=${hops}&limit=${limit}`);
export const getMatches = (candidateId: string, limit = 20) => request<{ items: Match[] }>(`/api/matches?candidate_id=${encodeURIComponent(candidateId)}&limit=${limit}`);
