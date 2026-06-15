import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import { App } from "./App";
import "./styles/global.css";

// DEV-mode auto-login: inject mock token if none exists
if (import.meta.env.DEV) {
  try {
    const authData = JSON.parse(localStorage.getItem('gepaw-auth') || '{}');
    if (!authData?.state?.accessToken) {
      localStorage.setItem('gepaw-auth', JSON.stringify({
        state: { accessToken: 'dev-mock-token', refreshToken: 'dev-mock-refresh' },
        version: 0
      }));
    }
  } catch {}
}

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </React.StrictMode>,
);
