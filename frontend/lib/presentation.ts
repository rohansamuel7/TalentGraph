const ROLE_FAMILY_LABELS: Record<string, string> = {
  analytics: "Analytics",
  cloud_platform: "Cloud & Platform",
  data_engineering: "Data Engineering",
  software_engineering: "Software Engineering",
};

export function formatRoleFamily(value: string): string {
  return ROLE_FAMILY_LABELS[value] ?? value.replaceAll("_", " ").replace(/\b\w/g, (letter) => letter.toUpperCase());
}

export function formatEvidenceStatus(value: string): string {
  const labels: Record<string, string> = {
    sufficient_for_limited_comparison: "Comparable · limited evidence",
    limited_evidence: "Comparable · limited evidence",
    insufficient_evidence: "Insufficient required evidence",
  };
  return labels[value] ?? value.replaceAll("_", " ");
}
