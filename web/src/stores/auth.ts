import { create } from "zustand";
import { persist } from "zustand/middleware";

export type AuthState = {
  accessToken: string | null;
  refreshToken: string | null;
  username: string | null;
  role: "admin" | "user" | null;
  orgId: string | null;
  orgName: string | null;
  setTokens: (a: string, r: string) => void;
  setIdentity: (i: { username: string; role: "admin" | "user"; orgId: string; orgName: string }) => void;
  clear: () => void;
};

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      accessToken: null,
      refreshToken: null,
      username: null,
      role: null,
      orgId: null,
      orgName: null,
      setTokens: (accessToken, refreshToken) => set({ accessToken, refreshToken }),
      setIdentity: (i: any) => set({ username: i.username, role: i.role, orgId: i.orgId || i.org_id || null, orgName: i.orgName || i.org_name || null }),
      clear: () => set({ accessToken: null, refreshToken: null, username: null, role: null, orgId: null, orgName: null }),
    }),
    { name: "gepaw-auth", partialize: (s) => ({ accessToken: s.accessToken, refreshToken: s.refreshToken }) },
  ),
);
