// Thin fetch wrapper. Stores access token via authStore.
import { useAuthStore } from "../stores/auth";

export type ApiError = { status: number; message: string };
const BASE = "/api";
let refreshPromise: Promise<string | null> | null = null;

async function tryRefresh(): Promise<string | null> {
  if (refreshPromise) return refreshPromise;
  refreshPromise = (async () => {
    const refresh = useAuthStore.getState().refreshToken;
    if (!refresh) return null;
    const r = await fetch(BASE + "/auth/refresh", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ refresh_token: refresh }),
    });
    if (!r.ok) { useAuthStore.getState().clear(); return null; }
    const data = await r.json();
    useAuthStore.getState().setTokens(data.access_token, data.refresh_token);
    return data.access_token;
  })();
  try { return await refreshPromise; }
  finally { refreshPromise = null; }
}

export async function api<T = any>(
  path: string,
  init: RequestInit = {},
  opts: { raw?: boolean; noStore?: boolean } = {},
): Promise<T> {
  const headers = new Headers(init.headers || {});
  if (!headers.has("Content-Type") && init.body && typeof init.body === "string") {
    headers.set("Content-Type", "application/json");
  }
  if (opts.noStore) headers.set("Cache-Control", "no-store");
  const token = useAuthStore.getState().accessToken;
  if (token) headers.set("Authorization", "Bearer " + token);
  const r = await fetch(BASE + path, { ...init, headers });
  if (r.status === 401 && token) {
    const newToken = await tryRefresh();
    if (newToken) {
      headers.set("Authorization", "Bearer " + newToken);
      const r2 = await fetch(BASE + path, { ...init, headers });
      if (r2.ok) {
        if (opts.raw) return r2 as any;
        return r2.json() as Promise<T>;
      }
    }
    useAuthStore.getState().clear();
  }
  if (!r.ok) {
    let msg = r.statusText;
    try { const d = await r.json(); msg = d.detail || d.message || JSON.stringify(d); } catch {}
    throw { status: r.status, message: msg } as ApiError;
  }
  if (opts.raw) return r as any;
  if (r.status === 204) return undefined as any;
  return r.json() as Promise<T>;
}

export const apiGet = <T = any>(p: string, noStore = false) => api<T>(p, { method: "GET" }, { noStore });
export const apiPost = <T = any>(p: string, body?: any) =>
  api<T>(p, { method: "POST", body: body ? JSON.stringify(body) : undefined });
export const apiPut = <T = any>(p: string, body?: any) =>
  api<T>(p, { method: "PUT", body: body ? JSON.stringify(body) : undefined });
export const apiDel = <T = any>(p: string) => api<T>(p, { method: "DELETE" });
export const apiPatch = <T = any>(p: string, body?: any) => api<T>(p, { method: "PATCH", body: body !== undefined ? JSON.stringify(body) : undefined });
export const apiPostForm = <T = any>(p: string, form: FormData) =>
  api<T>(p, { method: "POST", body: form });

// Defensive array fetch: some endpoints (e.g. /admin/skills, /admin/mcp,
// /admin/plugins) historically returned an empty object {} when the table was
// empty. Calling .map() on that throws and unmounts the whole admin tree, so
// always coerce to an array here.
export const apiGetArray = async <T = any>(p: string): Promise<T[]> => {
  const r = await apiGet<unknown>(p);
  if (Array.isArray(r)) return r as T[];
  if (r && typeof r === "object") {
    const anyR = r as any;
    if (Array.isArray(anyR.items)) return anyR.items as T[];
    if (Array.isArray(anyR.data)) return anyR.data as T[];
    if (Array.isArray(anyR.rows)) return anyR.rows as T[];
    if (Array.isArray(anyR.list)) return anyR.list as T[];
  }
  return [];
};
