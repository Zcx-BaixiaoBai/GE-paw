// Screenshot the agent-writeable memory + computer-use-indicator flows.
// Usage: node web/scripts/audit_memory_cu.mjs
import puppeteer from "puppeteer-core";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const OUT_DIR = path.join(__dirname, "_popup_screens");
const CHROME = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";

function sleep(ms) { return new Promise((r) => setTimeout(r, ms)); }

async function main() {
  fs.mkdirSync(OUT_DIR, { recursive: true });
  const browser = await puppeteer.launch({
    executablePath: CHROME,
    headless: "new",
    args: ["--window-size=1280,800"],
    defaultViewport: { width: 1280, height: 800 },
    protocolTimeout: 120000,
  });
  const page = await browser.newPage();
  page.on("pageerror", (e) => console.log("[pageerror]", e.message));
  page.setDefaultTimeout(12000);

  // Login
  await page.goto("http://localhost:5173/login", { waitUntil: "domcontentloaded" });
  await page.waitForSelector('input[type="password"]');
  await page.locator('input[type="password"]').fill("admin");
  await page.locator('button[type="submit"]').click();
  await page.waitForSelector(".chat-page");
  await sleep(500);

  // 1. Open settings > memory
  await page.goto("http://localhost:5173/app/settings", { waitUntil: "domcontentloaded" });
  await page.waitForSelector(".settings-side-item", { timeout: 8000 }).catch(() => {});
  await sleep(500);
  // Toggle memory on
  await page.evaluate(() => {
    const all = Array.from(document.querySelectorAll("span, div, label"));
    const memSpan = all.find((el) => el.children.length === 0 && el.textContent?.trim() === "启用长期记忆");
    if (memSpan) {
      let container = memSpan;
      for (let i = 0; i < 8 && container; i++) {
        container = container.parentElement;
        const sw = container?.querySelector("[role=switch]");
        if (sw && sw.getAttribute("aria-checked") !== "true") sw.click();
      }
    }
  });
  await sleep(500);

  // 2. Trigger agent writes via the test hook
  const writeTopic = await page.evaluate(async () => {
    if (!(window).__gepawTestAgentWriteMemory) return "no-hook";
    return await (window).__gepawTestAgentWriteMemory({ kind: "topic" });
  });
  console.log("agent topic:", JSON.stringify(writeTopic));
  const writeSummary = await page.evaluate(async () => {
    if (!(window).__gepawTestAgentWriteMemory) return "no-hook";
    return await (window).__gepawTestAgentWriteMemory({ kind: "summary" });
  });
  console.log("agent summary:", JSON.stringify(writeSummary));
  const writeTopic2 = await page.evaluate(async () => {
    return await (window).__gepawTestAgentWriteMemory({ kind: "topic" });
  });
  console.log("agent topic 2:", JSON.stringify(writeTopic2));
  await sleep(500);

  // 3. Read what the agent wrote
  const memory = await page.evaluate(() => {
    const raw = localStorage.getItem("gepaw-settings-v1");
    if (!raw) return null;
    const parsed = JSON.parse(raw);
    return {
      outline: parsed.state?.memory?.outline?.slice(0, 200) || null,
      topicCount: parsed.state?.memory?.topics?.length || 0,
      datedCount: Object.keys(parsed.state?.memory?.dated || {}).length,
      tagCount: Object.keys(parsed.state?.memory?.tags || {}).length,
      sampleTopic: parsed.state?.memory?.topics?.[0] || null,
      sampleEntry: Object.values(parsed.state?.memory?.dated || {})[0] || null,
    };
  });
  console.log("memory state:", JSON.stringify(memory, null, 2));
  await page.screenshot({ path: path.join(OUT_DIR, "page-memory-after-agent.png"), fullPage: true });

  // 4. Trigger computer use
  await page.goto("http://localhost:5173/app/assistant", { waitUntil: "domcontentloaded" });
  await page.waitForSelector(".composer-plus .composer-tool", { timeout: 8000 }).catch(() => {});
  await sleep(500);
  // Click + button
  await page.locator(".composer-plus .composer-tool").click();
  await sleep(300);
  // Click the computer use item
  const itemHandle = (await page.$$(".composer-plus-item:not([disabled])"))[0];
  if (itemHandle) await itemHandle.click();
  await sleep(500);
  // Simulate the agent pushing an action via the test hook
  const cuState = await page.evaluate(() => {
    const halo = document.querySelector(".cu-halo");
    const status = document.querySelector(".cu-status");
    const floater = document.querySelector(".cu-floater");
    return {
      hasHalo: !!halo,
      haloRunning: halo?.classList.contains("cu-halo-running") || false,
      hasStatus: !!status,
      hasFloater: !!floater,
      statusText: status?.textContent?.slice(0, 80) || null,
    };
  });
  console.log("cu state:", JSON.stringify(cuState));
  await page.screenshot({ path: path.join(OUT_DIR, "page-cu-halo.png") });

  // Stop the run
  const stopBtn = (await page.$$(".cu-status-stop"))[0];
  if (stopBtn) await stopBtn.click();
  await sleep(300);
  const cuAfter = await page.evaluate(() => ({
    hasHalo: !!document.querySelector(".cu-halo"),
  }));
  console.log("after stop:", JSON.stringify(cuAfter));

  await browser.close();
}

main().catch((e) => { console.error("FATAL", e); process.exit(1); });
