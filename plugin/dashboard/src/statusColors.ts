// Single source of truth for statuses. Order here drives:
//   - the order of accordion groups in ApplicationsTable
//   - the order of options in the StatusSelect dropdown
//   - the dot color shown next to the status in both views
//
// To add a status: append one entry here. No other file needs to change.

export interface StatusSpec {
  key: string;
  color: string;
}

// Order: engagement-first. The most active states sit at the top of the
// dashboard so the daily scan answers "what's hot right now?" before
// "what's still in flight?" or "what's done?"
export const STATUSES: StatusSpec[] = [
  { key: "new", color: "var(--mantine-color-yellow-5)" },
  { key: "interviewing", color: "var(--mantine-color-green-5)" },
  { key: "applied", color: "var(--mantine-color-blue-5)" },
  { key: "offer", color: "var(--mantine-color-violet-5)" },
  { key: "rejected", color: "var(--mantine-color-red-6)" },
  { key: "closed", color: "var(--mantine-color-gray-6)" },
];

export const STATUS_KEYS: string[] = STATUSES.map((s) => s.key);

const STATUS_COLOR_MAP = new Map(STATUSES.map((s) => [s.key, s.color]));

const FALLBACK_COLOR = "var(--mantine-color-gray-6)";

export function statusColor(status: string): string {
  return STATUS_COLOR_MAP.get(status) ?? FALLBACK_COLOR;
}
