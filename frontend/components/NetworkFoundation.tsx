"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { Background, Controls, Handle, MiniMap, Position, ReactFlow, useEdgesState, useNodesState, type Edge, type Node, type NodeProps } from "@xyflow/react";
import "@xyflow/react/dist/style.css";
import { getCandidates, getNeighborhood } from "../lib/api";
import type { CandidateSummary, GraphNeighborhood, GraphNode } from "../lib/types";
import { formatRoleFamily } from "../lib/presentation";
import { ErrorState, Loading } from "./States";

function GraphCard({ data, selected }: NodeProps<Node<{ label: string; kind: string }>>) {
  return <div className={`graph-card ${data.kind}${selected ? " selected" : ""}`}><Handle type="target" position={Position.Left} /><strong>{data.label}</strong><Handle type="source" position={Position.Right} /></div>;
}

const nodeTypes = { candidate: GraphCard, competency: GraphCard, job: GraphCard };

function layoutNodes(nodes: GraphNode[], root: string): Node[] {
  const columns = { candidate: 0, competency: 1, job: 2 } as const;
  const counters = { candidate: 0, competency: 0, job: 0 };
  return [...nodes].sort((a, b) => a.id.localeCompare(b.id)).map((item) => {
    const index = counters[item.type]++;
    return { id: item.id, type: item.type, data: { label: item.label, kind: item.type }, position: { x: columns[item.type] * 320, y: index * 108 }, selected: item.id === root };
  });
}

function mapEdges(graph: GraphNeighborhood): Edge[] {
  // The API supplies evidence classes; dashed preferred edges only change
  // presentation and never promote them to required relationships.
  return graph.edges.map((item, index) => ({ id: `${item.source}-${item.relationship}-${item.target}-${index}`, source: item.source, target: item.target, ariaLabel: item.relationship === "PREFERS_SKILL" ? "Preferred skill relationship" : item.relationship === "REQUIRES_SKILL" ? "Required skill relationship" : "Candidate has skill", className: item.relationship === "PREFERS_SKILL" ? "preferred-edge" : "required-edge" }));
}

export function NetworkFoundation() {
  const [candidates, setCandidates] = useState<CandidateSummary[]>([]);
  const [activeCandidateId, setActiveCandidateId] = useState("");
  const [graph, setGraph] = useState<GraphNeighborhood>();
  const [selected, setSelected] = useState<string>();
  const [query, setQuery] = useState("");
  const [error, setError] = useState<string>();
  const [loading, setLoading] = useState(true);
  const [hops, setHops] = useState(1);
  const [jobLimit, setJobLimit] = useState(6);
  const [nodes, setNodes, onNodesChange] = useNodesState<Node>([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState<Edge>([]);

  const load = async (nodeId: string, nextHops = hops) => { setLoading(true); setError(undefined); try { const result = await getNeighborhood(nodeId, nextHops); setGraph(result); setSelected(result.root); setHops(nextHops); setJobLimit(6); } catch (reason) { setError(reason instanceof Error ? reason.message : "The graph could not be loaded."); } finally { setLoading(false); } };
  useEffect(() => { getCandidates().then((result) => { setCandidates(result.items); const first = result.items.find((item) => item.competency_count > 0); if (first) { setActiveCandidateId(first.candidate_id); void load(first.candidate_id); } }).catch((reason: Error) => { setError(reason.message); setLoading(false); }); }, []);
  const selectedNode = useMemo(() => graph?.nodes.find((item) => item.id === selected), [graph, selected]);
  const connectedSkills = useMemo(() => graph?.edges.filter((edge) => edge.source === selected && edge.relationship === "HAS_SKILL").map((edge) => graph.nodes.find((node) => node.id === edge.target)?.label).filter(Boolean) ?? [], [graph, selected]);
  const supportedSkills = useMemo(() => graph?.edges.filter((edge) => edge.source === selected && (edge.relationship === "REQUIRES_SKILL" || edge.relationship === "PREFERS_SKILL")).map((edge) => ({ label: graph.nodes.find((node) => node.id === edge.target)?.label, relationship: edge.relationship === "REQUIRES_SKILL" ? "Required" : "Preferred" })).filter((item) => item.label) ?? [], [graph, selected]);
  const roleFamily = typeof selectedNode?.properties.role_family === "string" ? formatRoleFamily(selectedNode.properties.role_family) : undefined;
  const findNode = () => {
    const term = query.trim().toLowerCase();
    if (!term) return;
    const node = graph?.nodes.find((item) => item.label.toLowerCase().includes(term));
    if (node) { setSelected(node.id); return; }
    const candidate = candidates.find((item) => `${item.display_name} ${formatRoleFamily(item.role_family)}`.toLowerCase().includes(term));
    if (candidate) { setActiveCandidateId(candidate.candidate_id); void load(candidate.candidate_id, 1); }
  };
  // Limit visible jobs without dropping the candidate and skill context.
  const visibleGraph = useMemo(() => { if (!graph) return undefined; const jobs = graph.nodes.filter((node) => node.type === "job").sort((a, b) => a.id.localeCompare(b.id)); const keep = new Set([...graph.nodes.filter((node) => node.type !== "job"), ...jobs.slice(0, jobLimit)].map((node) => node.id)); return { ...graph, nodes: graph.nodes.filter((node) => keep.has(node.id)), edges: graph.edges.filter((edge) => keep.has(edge.source) && keep.has(edge.target)) }; }, [graph, jobLimit]);
  useEffect(() => { if (visibleGraph) { setNodes(layoutNodes(visibleGraph.nodes, visibleGraph.root)); setEdges(mapEdges(visibleGraph)); } }, [visibleGraph, setNodes, setEdges]);
  useEffect(() => { setEdges((current) => current.map((edge) => ({ ...edge, style: selected ? { opacity: edge.source === selected || edge.target === selected ? 1 : 0.18 } : { opacity: 1 } }))); }, [selected, setEdges]);
  if (error && !graph) return <ErrorState message={error} />;
  return <section className="graph-explorer" aria-label="Interactive talent knowledge graph">
    <div className="graph-toolbar"><label>Candidate<select aria-label="Choose candidate" value={activeCandidateId} onChange={(event) => { setActiveCandidateId(event.target.value); void load(event.target.value, 1); }}>{candidates.map((item) => <option key={item.candidate_id} value={item.candidate_id}>{item.display_name} · {formatRoleFamily(item.role_family)}</option>)}</select></label><label>Search<input aria-label="Search candidates, skills, or jobs" value={query} onChange={(event) => setQuery(event.target.value)} onKeyDown={(event) => event.key === "Enter" && findNode()} placeholder="Search this graph" /></label><button onClick={() => selected && void load(selected, Math.min(2, hops + 1))} disabled={!selected || hops >= 2}>Expand</button><button onClick={() => activeCandidateId && void load(activeCandidateId, 1)} disabled={!activeCandidateId}>Reset</button></div>
    <div className="graph-layout"><div className="graph-surface">{loading ? <Loading /> : <ReactFlow nodes={nodes} edges={edges} nodeTypes={nodeTypes} onNodesChange={onNodesChange} onEdgesChange={onEdgesChange} onNodeClick={(_, node) => setSelected(node.id)} fitView fitViewOptions={{ padding: 0.2 }}><Background color="var(--graph-grid)" gap={24} /><Controls /><MiniMap nodeColor={(node) => node.type === "candidate" ? "var(--candidate)" : node.type === "job" ? "var(--job)" : "var(--skill)"} /></ReactFlow>}</div><aside className="details-panel"><div className="legend"><span><i className="dot candidate" />Candidate</span><span><i className="dot competency" />Skill</span><span><i className="dot job" />Job</span></div><p className="edge-key"><span className="line" />Required <span className="line dashed" />Preferred</p>{selectedNode ? <><p className="eyebrow">{selectedNode.type === "competency" ? "Technical skill" : selectedNode.type}</p><h2>{selectedNode.label}</h2>{selectedNode.type === "candidate" && <><p className="detail-meta">{roleFamily}</p><h3>Technical skills</h3><ul className="detail-list">{connectedSkills.map((skill) => <li key={skill}>{skill}</li>)}</ul></>}{selectedNode.type === "job" && <><p className="detail-meta">{String(selectedNode.properties.company_name ?? "Company not listed")}</p><h3>Supported skills</h3><ul className="detail-list">{supportedSkills.map((skill) => <li key={`${skill.label}-${skill.relationship}`}><span>{skill.label}</span><small>{skill.relationship}</small></li>)}</ul></>}{selectedNode.type === "competency" && <p className="detail-meta">Connected candidates and jobs are shown in the graph.</p>}{selectedNode.type === "candidate" && <Link className="detail-action" href={`/matches?candidate=${encodeURIComponent(selectedNode.id)}`}>Explore matches →</Link>}<details className="evidence-details"><summary>Evidence details</summary><p>Record ID: {selectedNode.id}</p>{selectedNode.type === "job" && <p>Relationships are limited to validated required and preferred evidence.</p>}</details></> : <p className="muted">Select a node to see its skills or connected jobs.</p>}{graph?.truncated && <p className="limit-note">Showing a focused neighborhood. Expand a selected node to continue.</p>}{error && <p className="inline-error">{error}</p>}</aside></div>
    {graph && graph.nodes.filter((node) => node.type === "job").length > jobLimit && <button className="show-more" onClick={() => setJobLimit((current) => Math.min(current + 6, 50))}>Show {Math.min(6, graph.nodes.filter((node) => node.type === "job").length - jobLimit)} more jobs</button>}
  </section>;
}
