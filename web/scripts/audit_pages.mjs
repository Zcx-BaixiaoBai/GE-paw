// Screenshot the new pages (Settings > Memory, Admin > Wiki, Assistant with right pane).
// Usage: node web/scripts/audit_pages.mjs
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
  await sleep(800);

  // 1. Assistant page
  const assistant = await page.evaluate(() => {
    // Count buttons in the composer area
    const wrap = document.querySelector(".composer-wrap");
    const card = document.querySelector(".composer-card");
    const toolbar = document.querySelector(".composer-toolbar"); // should be gone
    const foot = document.querySelector(".composer-foot");
    const more = document.querySelector(".composer-more-btn");
    const allBtns = wrap ? wrap.querySelectorAll("button").length : 0;
    const textArea = document.querySelector(".composer-textarea");
    return {
      hasWebTab: !!document.querySelector(".web-tab"),
      hasWebHome: !!document.querySelector(".web-home"),
      hasWebChrome: !!document.querySelector(".web-chrome"),
      rightPaneOpen: !!document.querySelector(".right-pane .tabs-bar"),
      title: document.querySelector("h1")?.textContent || null,
      hasComposerCard: !!card,
      hasComposerFoot: !!foot,
      hasComposerMore: !!more,
      oldToolbarGone: !toolbar,
      composerBtnCount: allBtns,
      composerTextareaVisible: textArea ? textArea.offsetHeight > 0 : false,
    };
  });
  console.log("assistant:", JSON.stringify(assistant));
  await page.screenshot({ path: path.join(OUT_DIR, "page-assistant.png") });

  // 2. Settings page
  await page.goto("http://localhost:5173/app/settings", { waitUntil: "domcontentloaded" });
  await page.waitForSelector(".settings-shell, .settings-page", { timeout: 8000 }).catch(() => {});
  await sleep(500);
  const tabsList = await page.evaluate(() =>
    Array.from(document.querySelectorAll(".settings-side-item")).map((el) => el.textContent?.trim() || "")
  );
  console.log("settings tabs:", JSON.stringify(tabsList));
  await page.screenshot({ path: path.join(OUT_DIR, "page-settings.png") });

  // 3. Wiki tab
  const wikiTab = (await page.$$(".settings-side-item"))[7];
  if (wikiTab) await wikiTab.click();
  await page.waitForSelector(".wiki-page", { timeout: 8000 }).catch(() => {});
  await sleep(1500);
  const wikiState = await page.evaluate(() => ({
    hasTree: !!document.querySelector(".wiki-page"),
    hasFolder: !!document.querySelector(".wiki-folder"),
    title: document.querySelector("h1")?.textContent || null,
  }));
  console.log("wiki:", JSON.stringify(wikiState));
  await page.screenshot({ path: path.join(OUT_DIR, "page-wiki.png") });

  // 4. Memory section (scroll down to find it; it's in General tab)
  await page.goto("http://localhost:5173/app/settings", { waitUntil: "domcontentloaded" });
  await page.waitForSelector(".settings-side-item", { timeout: 8000 }).catch(() => {});
  await sleep(500);
  const memState = await page.evaluate(() => {
    const memSpan = Array.from(document.querySelectorAll("span, div, label")).find(
      (el) => el.children.length === 0 && el.textContent?.trim() === "启用长期记忆"
    );
    if (!memSpan) return { found: false, reason: "no-label" };
    let container = memSpan;
    for (let i = 0; i < 8 && container; i++) {
      container = container.parentElement;
      if (!container) break;
      const sw = container.querySelector("[role=switch]");
      if (sw) {
        const on = sw.getAttribute("aria-checked") === "true";
        if (!on) sw.click();
        return { found: true, wasOn: on, nowOn: !on };
      }
    }
    return { found: false, reason: "no-switch" };
  });
  console.log("memory:", JSON.stringify(memState));
  await sleep(800);
  // Add a sample topic
  const addBtn = await page.evaluateHandle(() => {
    return Array.from(document.querySelectorAll("button")).find((b) => b.textContent?.includes("+ 主题"));
  });
  if (addBtn && addBtn.asElement()) {
    try { await addBtn.asElement().click(); } catch {}
  }
  await sleep(500);
  await page.screenshot({ path: path.join(OUT_DIR, "page-memory.png"), fullPage: true });

  await browser.close();
}

main().catch((e) => { console.error("FATAL", e); process.exit(1); });
