// Codex-style tool-call card. Renders the tool name + a small status pill


// output. Used for assistant turns that include tool invocations.


import { useState } from "react";


import { IconChevronDown } from "./Icons";


import { t } from "../lib/i18n";





export type ToolStatus = "running" | "ok" | "err";





export function ToolCallCard({ name, args, result, status }: { name: string; args?: Record<string, any>; result?: any; status: ToolStatus }) {


  const [open, setOpen] = useState(false);


  const statusLabel = status === "running" ? t("chat.tool.running")


    : status === "ok" ? t("chat.tool.ok")


    : t("chat.tool.err");


  return (


    <div className={"tool-call tool-" + status}>


      <button type="button" className="tool-head" onClick={() => setOpen((v) => !v)}>


        <span className={"tool-caret" + (open ? " open" : "")}><IconChevronDown size={11} /></span>


        <span className="tool-icon">


          {status === "running" ? <span className="tool-pulse" /> : status === "ok" ? <span className="tool-dot tool-dot-ok" /> : <span className="tool-dot tool-dot-err" />}


        </span>


        <span className="tool-name">{name || "tool"}</span>


        <span className={"tool-status tool-status-" + status}>{statusLabel}</span>


      </button>


      {open && (


        <div className="tool-body">


          {args !== undefined && (


            <div className="tool-section">


              <div className="tool-section-label">{t("chat.tool.args")}</div>


              <pre className="tool-pre">{format(args)}</pre>


            </div>


          )}


          {result !== undefined && (


            <div className="tool-section">


              <div className="tool-section-label">{t("chat.tool.result")}</div>


              <pre className="tool-pre">{format(result)}</pre>


            </div>


          )}


        </div>


      )}


    </div>


  );


}





function format(v: unknown): string {


  if (typeof v === "string") return v;


  try { return JSON.stringify(v, null, 2); } catch { return String(v); }


}


