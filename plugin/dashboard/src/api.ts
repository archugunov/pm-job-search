import type { DashboardState, NewCompanyPayload } from "./types";

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

export async function fetchState(): Promise<DashboardState> {
  const res = await fetch("/api/state");
  return jsonOrThrow<DashboardState>(res);
}

export async function patchStatus(folderPath: string, status: string): Promise<void> {
  const res = await fetch(`/api/positions/${encodeURIComponent(folderPath)}/status`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ status }),
  });
  await jsonOrThrow<{ ok: true }>(res);
}

export async function postNote(folderPath: string, note: string): Promise<void> {
  const res = await fetch(`/api/positions/${encodeURIComponent(folderPath)}/notes`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ note }),
  });
  await jsonOrThrow<{ ok: true }>(res);
}

export async function postCompany(payload: NewCompanyPayload): Promise<{ folder_path: string }> {
  const res = await fetch("/api/companies", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return jsonOrThrow<{ folder_path: string }>(res);
}
