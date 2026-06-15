// Replace the cyrillic "ассистент" with the Latin "assistant" in the audit script.
import fs from "node:fs";
const p = "C:/Users/Admin/Documents/GE-paw/web/scripts/audit_pages.mjs";
let s = fs.readFileSync(p, "utf8");
const lines = s.split("\n");
for (let i = 0; i < lines.length; i++) {
  // The cyrillic chars are а (0x0430), с (0x0441), и (0x0438), е (0x0435), т (0x0442), н (0x043D)
  // Together they spell "ассистент" in Cyrillic, but JS sees them as valid identifiers.
  // Use a string with the actual code points.
  const cyr = ["а","с","с","и","с","т","е","н","т"].join("");
  if (lines[i].includes(cyr)) {
    console.log("found at line " + (i+1) + ": " + lines[i]);
    lines[i] = lines[i].split(cyr).join("assistant");
  }
}
fs.writeFileSync(p, lines.join("\n"));
console.log("done");
