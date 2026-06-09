// Ambient declarations for the gepaw console host API.
//
// The gepaw console injects a shared `window.gepaw` object at
// runtime; we externalize `react`/`react-dom` (see `vite.config.ts`)
// and pull `React`/`antd` off `host` instead of bundling them. Without
// these declarations every access reduces to `any` and the compiler
// cannot tell us when the host contract drifts (e.g. `host.antd` being
// renamed or replaced).

import type * as ReactNS from "react";

declare global {
  interface gepawHost {
    /** React module re-exported by the host (same major version as antd). */
    React: typeof ReactNS;
    /**
     * antd module re-exported by the host. Typed loosely on purpose:
     * antd's public types are huge and the plugin only uses a handful
     * of named exports through destructuring, so a structural `any`
     * shape here keeps the surface small while still letting `Pick`-
     * style destructuring compile.
     */
    antd: any;
    /** Resolve a console-relative API path to an absolute URL. */
    getApiUrl: (path: string) => string;
    /** Current bearer token for gepaw API calls (may be empty). */
    getApiToken: () => string;
  }

  interface gepawRoute {
    path: string;
    component: unknown;
    label?: string;
    icon?: string;
    priority?: number;
  }

  interface gepawGlobal {
    host: gepawHost;
    registerRoutes?: (pluginId: string, routes: gepawRoute[]) => void;
  }

  interface Window {
    gepaw: gepawGlobal;
  }
}

export {};
