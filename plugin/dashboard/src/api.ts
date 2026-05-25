import { BASE_URL, DEMO_MODE } from "./config";
import type { DashboardState } from "./types";

async function jsonOrThrow<T>(res: Response): Promise<T> {
  if (!res.ok) {
    let detail = "";
    try {
      const body = await res.json();
      detail = typeof body?.error === "string" ? body.error : "";
    } catch {
      detail = await res.text().catch(() => "");
    }
    throw new ApiError(res.status, detail || res.statusText);
  }
  return res.json();
}

export class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
  }
}

// ---------- Demo-mode in-memory store ----------
//
// In demo mode, all reads return module-level cached data and all writes
// mutate that cache without ever hitting the network. State persists across
// re-renders but resets on a hard refresh — which is the point: visitors can
// play with the dashboard, but nothing leaks between sessions.

let demoState: DashboardState | null = null;
const demoNotes = new Map<string, string>();
const demoArtifacts = new Map<string, Artifacts>();

async function fetchDemoFile(path: string): Promise<Response> {
  const res = await fetch(`${BASE_URL}demo/${path}`);
  if (!res.ok) throw new ApiError(res.status, `demo asset missing: ${path}`);
  return res;
}

async function ensureDemoState(): Promise<DashboardState> {
  if (demoState === null) {
    const res = await fetchDemoFile("state.json");
    demoState = (await res.json()) as DashboardState;
  }
  // Return a fresh deep clone so React sees a new reference and re-renders
  // after in-place mutations (status changes, has_notes flips).
  return structuredClone(demoState);
}

async function ensureDemoNotes(folderPath: string): Promise<string> {
  const cached = demoNotes.get(folderPath);
  if (cached !== undefined) return cached;
  try {
    const res = await fetchDemoFile(`notes/${folderPath}.md`);
    const text = await res.text();
    demoNotes.set(folderPath, text);
    return text;
  } catch {
    demoNotes.set(folderPath, "");
    return "";
  }
}

async function ensureDemoArtifacts(folderPath: string): Promise<Artifacts> {
  const cached = demoArtifacts.get(folderPath);
  if (cached !== undefined) return cached;
  const res = await fetchDemoFile(`artifacts/${folderPath}.json`);
  const value = (await res.json()) as Artifacts;
  demoArtifacts.set(folderPath, value);
  return value;
}

function mutateDemoStatus(folderPath: string, status: string): void {
  if (!demoState) return;
  const hit = demoState.companies.find((c) => c.folder_path === folderPath);
  if (hit) hit.status = status;
}

function nowTimestamp(): string {
  const d = new Date();
  const pad = (n: number) => String(n).padStart(2, "0");
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}`;
}

function appendDemoNote(folderPath: string, note: string): void {
  const prev = demoNotes.get(folderPath) ?? "";
  const header = prev.trim() ? "" : "# Notes\n";
  const next = `${prev}${header}\n## ${nowTimestamp()}\n\n${note.trim()}\n`;
  demoNotes.set(folderPath, next);
  const company = demoState?.companies.find((c) => c.folder_path === folderPath);
  if (company) company.has_notes = true;
}

// Split a notes markdown string on `## ` headings into preamble + sections.
// Mirrors the server's split_notes logic so editNote/deleteNote produce
// markdown the frontend's parseEntries() reads back identically.
function splitDemoNotes(md: string): { preamble: string; sections: Array<{ heading: string; body: string }> } {
  const lines = md.split("\n");
  const preambleLines: string[] = [];
  const sections: Array<{ heading: string; lines: string[] }> = [];
  let current: { heading: string; lines: string[] } | null = null;
  for (const line of lines) {
    const m = line.match(/^##\s+(.+?)\s*$/);
    if (m) {
      if (current) sections.push(current);
      current = { heading: m[1], lines: [] };
    } else if (current) {
      current.lines.push(line);
    } else {
      preambleLines.push(line);
    }
  }
  if (current) sections.push(current);
  return {
    preamble: preambleLines.join("\n"),
    sections: sections.map((s) => ({ heading: s.heading, body: s.lines.join("\n").replace(/^\n+|\n+$/g, "") })),
  };
}

function joinDemoNotes(preamble: string, sections: Array<{ heading: string; body: string }>): string {
  const parts: string[] = [];
  if (preamble.trim()) parts.push(preamble.replace(/\n+$/, "") + "\n");
  for (const s of sections) parts.push(`\n## ${s.heading}\n\n${s.body.trim()}\n`);
  return parts.join("");
}

function editDemoNote(folderPath: string, index: number, heading: string, body: string): void {
  const md = demoNotes.get(folderPath) ?? "";
  const { preamble, sections } = splitDemoNotes(md);
  if (index < 0 || index >= sections.length) throw new ApiError(409, "index out of range");
  if (sections[index].heading !== heading) throw new ApiError(409, "heading mismatch");
  sections[index] = { heading, body };
  demoNotes.set(folderPath, joinDemoNotes(preamble, sections));
}

function deleteDemoNote(folderPath: string, index: number, heading: string): void {
  const md = demoNotes.get(folderPath) ?? "";
  const { preamble, sections } = splitDemoNotes(md);
  if (index < 0 || index >= sections.length) throw new ApiError(409, "index out of range");
  if (sections[index].heading !== heading) throw new ApiError(409, "heading mismatch");
  sections.splice(index, 1);
  demoNotes.set(folderPath, joinDemoNotes(preamble, sections));
  if (sections.length === 0) {
    const company = demoState?.companies.find((c) => c.folder_path === folderPath);
    if (company) company.has_notes = false;
  }
}

// ---------- Public API ----------

export async function fetchState(): Promise<DashboardState> {
  if (DEMO_MODE) return ensureDemoState();
  const res = await fetch("/api/state");
  return jsonOrThrow<DashboardState>(res);
}

export async function patchStatus(folderPath: string, status: string): Promise<void> {
  if (DEMO_MODE) {
    mutateDemoStatus(folderPath, status);
    return;
  }
  const res = await fetch(`/api/positions/${encodeURIComponent(folderPath)}/status`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ status }),
  });
  await jsonOrThrow<{ ok: true }>(res);
}

export async function postNote(folderPath: string, note: string): Promise<void> {
  if (DEMO_MODE) {
    await ensureDemoNotes(folderPath);
    appendDemoNote(folderPath, note);
    return;
  }
  const res = await fetch(`/api/positions/${encodeURIComponent(folderPath)}/notes`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ note }),
  });
  await jsonOrThrow<{ ok: true }>(res);
}

export async function fetchNotes(folderPath: string): Promise<string> {
  if (DEMO_MODE) return ensureDemoNotes(folderPath);
  const res = await fetch(`/api/positions/${encodeURIComponent(folderPath)}/notes`);
  const body = await jsonOrThrow<{ markdown: string }>(res);
  return body.markdown;
}

export interface PrepDoc {
  date: string;
  filename: string;
  markdown: string;
}

export interface DebriefDoc {
  date: string;
  stage: string;
  filename: string;
  markdown: string;
}

export interface Artifacts {
  research: string | null;
  preps: PrepDoc[];
  debriefs: DebriefDoc[];
}

export async function fetchArtifacts(folderPath: string): Promise<Artifacts> {
  if (DEMO_MODE) return ensureDemoArtifacts(folderPath);
  const res = await fetch(`/api/positions/${encodeURIComponent(folderPath)}/artifacts`);
  return jsonOrThrow<Artifacts>(res);
}

export async function editNote(
  folderPath: string,
  index: number,
  heading: string,
  body: string,
): Promise<void> {
  if (DEMO_MODE) {
    editDemoNote(folderPath, index, heading, body);
    return;
  }
  const res = await fetch(`/api/positions/${encodeURIComponent(folderPath)}/notes`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ index, heading, body }),
  });
  await jsonOrThrow<{ ok: true }>(res);
}

export async function deleteNote(
  folderPath: string,
  index: number,
  heading: string,
): Promise<void> {
  if (DEMO_MODE) {
    deleteDemoNote(folderPath, index, heading);
    return;
  }
  const res = await fetch(`/api/positions/${encodeURIComponent(folderPath)}/notes`, {
    method: "DELETE",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ index, heading }),
  });
  await jsonOrThrow<{ ok: true }>(res);
}
