// popup_audit_iab.mjs - Re-audit popups via puppeteer-core (headless Chrome).
// Usage: node web/scripts/popup_audit_iab.mjs [suffix] [width] [height]
import puppeteer from "puppeteer-core";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const SUFFIX = process.argv[2] || "verify";
const WIDTH = parseInt(process.argv[3] || "1280", 10);
const HEIGHT = parseInt(process.argv[4] || "800", 10);
const BASE = "http://localhost:5173";
const OUT_DIR = path.join(__dirname, "_popup_screens");

const CHROME = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

async function rect(page, selector) {
  return await page.evaluate((sel) => {
    const el = document.querySelector(sel);
    if (!el) return null;
    const r = el.getBoundingClientRect();
    return { x: r.x, y: r.y, w: r.width, h: r.height };
  }, selector);
}

function oob(rect, vp) {
  if (!rect) return [];
  const o = [];
  if (rect.x < 0) o.push(`left=${rect.x.toFixed(0)}`);
  if (rect.y < 0) o.push(`top=${rect.y.toFixed(0)}`);
  if (rect.x + rect.w > vp.width + 1) o.push(`right=${(rect.x + rect.w).toFixed(0)}>${vp.width}`);
  if (rect.y + rect.h > vp.height + 1) o.push(`bottom=${(rect.y + rect.h).toFixed(0)}>${vp.height}`);
  return o;
}

async function record(page, name, sel, vp) {
  const r = await rect(page, sel);
  if (!r) return { name, sel, present: false };
  return { name, sel, present: true, rect: r, oob: oob(r, vp) };
}

async function shot(page, name) {
  fs.mkdirSync(OUT_DIR, { recursive: true });
  const fp = path.join(OUT_DIR, `chat-${name}.png`);
  await page.screenshot({ path: fp, fullPage: false });
  return fp;
}

const results = [];
const consoleErrors = [];
const vp = { width: WIDTH, height: HEIGHT };
const outPath = path.join(__dirname, `_audit_${SUFFIX}.json`);

function savePartial() {
  const out = { ts: new Date().toISOString(), label: SUFFIX, viewport: vp, items: results, consoleErrors };
  fs.writeFileSync(outPath, JSON.stringify(out, null, 2));
}

async function runStep(name, fn) {
  const start = Date.now();
  try {
    await fn();
    console.log(`[ok] ${name} (${Date.now() - start}ms)`);
  } catch (e) {
    console.log(`[err] ${name}: ${e.message?.slice(0, 200)}`);
    results.push({ name, present: false, error: e.message });
    savePartial();
  }
}

async function main() {
  const browser = await puppeteer.launch({
    executablePath: CHROME,
    headless: "new",
    args: [`--window-size=${WIDTH},${HEIGHT}`],
    defaultViewport: { width: WIDTH, height: HEIGHT },
    protocolTimeout: 180000,
  });
  const page = await browser.newPage();
  page.on("console", (msg) => {
    if (msg.type() === "error") consoleErrors.push(`[error] ${msg.text()}`);
    else if (msg.type() === "warning") consoleErrors.push(`[warn] ${msg.text()}`);
  });
  page.on("pageerror", (err) => {
    consoleErrors.push(`[pageerror] ${err.message}`);
  });
  page.on("requestfailed", (req) => {
    consoleErrors.push(`[reqfail] ${req.url()} - ${req.failure()?.errorText}`);
  });
  page.setDefaultTimeout(20000);

  // Login
  await runStep("login", async () => {
    await page.goto(BASE + "/login", { waitUntil: "domcontentloaded" });
    await page.waitForSelector('input[type="password"]', { timeout: 10000 });
    await page.locator('input[type="password"]').fill("admin");
    await page.locator('button[type="submit"]').click();
    await page.waitForSelector(".chat-page", { timeout: 12000 });
    await sleep(400);
    await shot(page, `${SUFFIX}-base`);
  });

  // 1. Slash menu
  await runStep("slash-menu", async () => {
    await page.locator(".composer-textarea").click();
    await page.locator(".composer-textarea").fill("/");
    await sleep(300);
    results.push(await record(page, "slash-menu", ".slash-menu", vp));
    savePartial();
    await shot(page, `${SUFFIX}-slash`);
  });

  // 2. Composer more menu (replaces the old composer-plus toolbar)
  await runStep("composer-more-menu", async () => {
    await page.locator(".composer-textarea").fill("");
    await page.locator(".composer-more-btn").click();
    await sleep(300);
    results.push(await record(page, "composer-more-menu", ".composer-more-menu", vp));
    savePartial();
    await shot(page, `${SUFFIX}-plus`);
  });

  // 3. Permission menu
  await runStep("perm-menu", async () => {
    await page.locator(".chat-area").click({ offset: { x: 10, y: 10 } });
    await sleep(200);
    await page.locator(".perm-pill-btn").click();
    await sleep(300);
    results.push(await record(page, "perm-menu", ".perm-menu", vp));
    savePartial();
    await shot(page, `${SUFFIX}-perm`);
  });

  // 4. Thread menu
  await runStep("thread-menu", async () => {
    await page.locator(".chat-area").click({ offset: { x: 10, y: 10 } });
    await sleep(200);
    await page.locator(".thread-title-btn").click({ timeout: 2000 });
    await sleep(300);
    results.push(await record(page, "thread-menu", ".thread-menu", vp));
    savePartial();
    await shot(page, `${SUFFIX}-thread`);
  });

  // 5. Theme menu
  await runStep("theme-menu", async () => {
    await page.locator(".chat-area").click({ offset: { x: 10, y: 10 } });
    await sleep(200);
    await page.locator('.topbar-right button[title="\u5207\u6362\u4e3b\u9898"]').click();
    await sleep(300);
    results.push(await record(page, "theme-menu", ".theme-menu", vp));
    savePartial();
    await shot(page, `${SUFFIX}-theme`);
  });

  // 6. User menu
  await runStep("user-menu", async () => {
    await page.locator(".chat-area").click({ offset: { x: 10, y: 10 } });
    await sleep(200);
    await page.locator(".user-avatar").click();
    await sleep(300);
    results.push(await record(page, "user-menu", ".user-menu", vp));
    savePartial();
    await shot(page, `${SUFFIX}-user`);
  });

  // 7. Tab menu (right pane must be open; toggle via the right-panel icon-btn in topbar-right)
  await runStep("tab-menu", async () => {
    // Ensure right pane is open
    const paneOpen = await page.evaluate(() => !!document.querySelector(".right-pane .tabs-bar"));
    if (!paneOpen) {
      await page.locator('.topbar-right button[title^="\u5207\u6362\u53f3\u4fa7\u9762\u677f"]').click();
      await sleep(300);
    }
    await page.locator(".chat-area").click({ offset: { x: 10, y: 10 } });
    await sleep(200);
    await page.locator(".tab-add .icon-btn").click({ timeout: 2000 });
    await sleep(300);
    results.push(await record(page, "tab-menu", ".tab-menu", vp));
    savePartial();
    await shot(page, `${SUFFIX}-tab`);
  });

  // 8. Left context menu
  await runStep("left-ctx-menu", async () => {
    const rowHandle = (await page.$$(".left-row .left-item-session"))[0];
    if (rowHandle) await rowHandle.click({ button: "right" });
    await sleep(300);
    results.push(await record(page, "left-ctx-menu", ".left-ctx-menu", vp));
    savePartial();
    await shot(page, `${SUFFIX}-leftctx`);
  });

  // 9. RequestUserInputModal (test hook)
  await runStep("modal-backdrop", async () => {
    // The test hook calls `requestUserInput` which updates zustand state and
    // re-renders the modal. Give the modal a generous wait (React + zustand).
    await page.evaluate(() => window.__gepawTestShowUserInput && window.__gepawTestShowUserInput());
    await page.waitForSelector(".modal-backdrop.request-user-input", { timeout: 15000 });
    await sleep(300);
    results.push(await record(page, "modal-backdrop", ".modal-backdrop.request-user-input", vp));
    savePartial();
    await shot(page, `${SUFFIX}-modal`);
    await page.keyboard.press("Escape");
    await sleep(300);
  });

  // 10. Computer use indicator (replaces the old cu-backdrop modal)
  await runStep("cu-halo", async () => {
    // Close any leftover modal first.
    await page.keyboard.press("Escape");
    await sleep(200);
    await page.locator(".composer-more-btn").click();
    await sleep(300);
    const itemHandle = (await page.$$(".composer-more-item:not([disabled])"))[0];
    if (itemHandle) await itemHandle.click();
    await sleep(600);
    // The new UI shows: edge halo + topbar status pill + optional floater.
    results.push(await record(page, "cu-halo", ".cu-halo", vp));
    savePartial();
    await shot(page, `${SUFFIX}-cu-halo`);
    // Stop the run.
    const stop = (await page.$$(".cu-status-stop"))[0];
    if (stop) await stop.click();
    await sleep(300);
  });

  await browser.close();

  savePartial();

  console.log("");
  console.log(`=== ${SUFFIX} (${WIDTH}x${HEIGHT}) ===`);
  for (const r of results) {
    if (!r.present) {
      console.log(`  [skip ] ${r.name}: ${r.error || "not in DOM"}`);
      continue;
    }
    const flag = r.oob && r.oob.length ? "  OOB!" : "  ok   ";
    const o = r.oob && r.oob.length ? `  (${r.oob.join(", ")})` : "";
    console.log(`${flag} ${r.name.padEnd(20)} x=${r.rect.x.toFixed(1).padStart(6)} y=${r.rect.y.toFixed(1).padStart(6)} w=${r.rect.w.toFixed(1).padStart(6)} h=${r.rect.h.toFixed(1).padStart(6)}${o}`);
  }
  console.log(`console errors: ${consoleErrors.length}`);
  for (const e of consoleErrors.slice(0, 5)) console.log("  " + e);
}

main().catch((e) => {
  console.error("FATAL", e);
  savePartial();
  process.exit(1);
});
