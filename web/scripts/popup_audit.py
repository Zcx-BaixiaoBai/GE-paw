"""Popup positioning audit + visual capture.

Connects to the dev server on http://localhost:5173, logs in as admin/admin,
then opens each popup and records its bounding rect plus the offset viewport
edges so we can verify nothing escapes the screen.
"""
import asyncio
import json
import os
import sys
from playwright.async_api import async_playwright


BASE = "http://localhost:5173"
OUT = os.path.join(os.path.dirname(__file__), "_popup_screens")


async def login(page):
    await page.goto(BASE + "/login", wait_until="domcontentloaded")
    await page.wait_for_selector('input[type="password"]', timeout=10000)
    # First input is username (already prefilled "admin" in the page).
    await page.locator("input").nth(0).fill("admin")
    await page.locator('input[type="password"]').fill("admin")
    await page.click('button[type="submit"]')
    await page.wait_for_url("**/app/assistant**", timeout=10000)
    await page.wait_for_selector(".chat-page", timeout=10000)


async def rect(page, selector):
    """Return the bounding box of the first match; None if not in DOM."""
    loc = page.locator(selector).first
    if await loc.count() == 0:
        return None
    return await loc.bounding_box()


async def record(name, page, selector, viewport):
    bb = await rect(page, selector)
    if bb is None:
        return {"name": name, "selector": selector, "present": False}
    out_of_bounds = []
    if bb["x"] < 0:
        out_of_bounds.append(f"left={bb['x']:.0f}")
    if bb["y"] < 0:
        out_of_bounds.append(f"top={bb['y']:.0f}")
    if bb["x"] + bb["width"] > viewport["width"] + 1:
        out_of_bounds.append(
            f"right={bb['x']+bb['width']:.0f}>{viewport['width']}"
        )
    if bb["y"] + bb["height"] > viewport["height"] + 1:
        out_of_bounds.append(
            f"bottom={bb['y']+bb['height']:.0f}>{viewport['height']}"
        )
    return {
        "name": name,
        "selector": selector,
        "present": True,
        "rect": bb,
        "viewport": viewport,
        "oob": out_of_bounds,
    }


async def shot(page, name):
    os.makedirs(OUT, exist_ok=True)
    await page.screenshot(path=os.path.join(OUT, name + ".png"), full_page=False)


async def run(width, height, suffix):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(
            viewport={"width": width, "height": height},
        )
        page = await ctx.new_page()
        results = []
        viewport = {"width": width, "height": height}

        await login(page)
        await page.wait_for_timeout(400)
        await shot(page, f"chat-{suffix}-base")

        # 1. Slash menu: type "/" in the textarea
        await page.locator(".composer-textarea").click()
        await page.locator(".composer-textarea").fill("/")
        await page.wait_for_timeout(250)
        results.append(await record("slash-menu", page, ".slash-menu", viewport))
        await shot(page, f"chat-{suffix}-slash")

        # 2. ComposerPlus menu
        await page.locator(".composer-textarea").fill("")
        await page.locator(".composer-plus .composer-tool").click()
        await page.wait_for_timeout(250)
        results.append(await record("composer-plus-menu", page, ".composer-plus-menu", viewport))
        await shot(page, f"chat-{suffix}-plus")

        # 3. Permission menu
        # Close any popups first by clicking on a neutral spot.
        await page.locator(".chat-area").click(position={"x": 10, "y": 10})
        await page.wait_for_timeout(150)
        await page.locator(".perm-pill-btn").click()
        await page.wait_for_timeout(250)
        results.append(await record("perm-menu", page, ".perm-menu", viewport))
        await shot(page, f"chat-{suffix}-perm")

        # 4. ThreadHeader menu (caret/button in topbar)
        await page.locator(".chat-area").click(position={"x": 10, "y": 10})
        await page.wait_for_timeout(150)
        # The thread menu only opens if a session is selected; click anyway.
        try:
            await page.locator(".thread-title-btn").click(timeout=1500)
            await page.wait_for_timeout(250)
            results.append(await record("thread-menu", page, ".thread-menu", viewport))
            await shot(page, f"chat-{suffix}-thread")
        except Exception as exc:
            results.append({"name": "thread-menu", "present": False, "error": str(exc)})

        # 5. Theme menu
        await page.locator(".chat-area").click(position={"x": 10, "y": 10})
        await page.wait_for_timeout(150)
        # Theme button has title=topbar.toggleTheme (= 切换主题).
        # Original code used .topbar-right .topbar-icon-btn.first which is the
        # *right panel* toggle, not the theme button. Use a title selector that survives
        # icon-button reordering (e.g. when the right pane is collapsed).
        await page.locator(".topbar-right button[title='切换主题']").click()
        await page.wait_for_timeout(250)
        results.append(await record("theme-menu", page, ".theme-menu", viewport))
        await shot(page, f"chat-{suffix}-theme")

        # 6. User menu (avatar button, last icon-btn in topbar-right).
        await page.locator(".chat-area").click(position={"x": 10, "y": 10})
        await page.wait_for_timeout(150)
        await page.locator(".user-avatar").click()
        await page.wait_for_timeout(250)
        results.append(await record("user-menu", page, ".user-menu", viewport))
        await shot(page, f"chat-{suffix}-user")

        # 7. Tab menu in RightPane (only visible if right pane is open).
        await page.locator(".chat-area").click(position={"x": 10, "y": 10})
        await page.wait_for_timeout(150)
        try:
            await page.locator(".tab-add .icon-btn").click(timeout=1500)
            await page.wait_for_timeout(250)
            results.append(await record("tab-menu", page, ".tab-menu", viewport))
            await shot(page, f"chat-{suffix}-tab")
        except Exception as exc:
            results.append({"name": "tab-menu", "present": False, "error": str(exc)})

        # 8. Left-ctx menu (right-click a session row).
        try:
            session_row = page.locator(".left-row .left-item-session").first
            await session_row.click(button="right", timeout=1500)
            await page.wait_for_timeout(250)
            results.append(await record("left-ctx-menu", page, ".left-ctx-menu", viewport))
            await shot(page, f"chat-{suffix}-leftctx")
        except Exception as exc:
            results.append({"name": "left-ctx-menu", "present": False, "error": str(exc)})

        # 9. RequestUserInputModal — invoke via the test hook.
        try:
            await page.evaluate("window.__gepawTestShowUserInput && window.__gepawTestShowUserInput()")
            await page.wait_for_timeout(300)
            results.append(await record("modal-backdrop", page, ".modal-backdrop.request-user-input", viewport))
            await shot(page, f"chat-{suffix}-modal")
            # Close it.
            await page.keyboard.press("Escape")
            await page.wait_for_timeout(200)
        except Exception as exc:
            results.append({"name": "modal-backdrop", "present": False, "error": str(exc)})

        # 10. ComputerUseOverlay
        # Close any popups first.
        await page.locator(".chat-area").click(position={"x": 10, "y": 10})
        await page.wait_for_timeout(150)
        try:
            # The + menu has the "computer use" button.
            await page.locator(".composer-plus .composer-tool").click()
            await page.wait_for_timeout(200)
            await page.locator(".composer-plus-item").click()
            await page.wait_for_timeout(400)
            results.append(await record("cu-backdrop", page, ".cu-backdrop", viewport))
            await shot(page, f"chat-{suffix}-cu")
            await page.keyboard.press("Escape")
            await page.wait_for_timeout(200)
        except Exception as exc:
            results.append({"name": "cu-backdrop", "present": False, "error": str(exc)})

        await browser.close()
        return results


async def main():
    label = sys.argv[1] if len(sys.argv) > 1 else "before"
    width = int(sys.argv[2]) if len(sys.argv) > 2 else 1280
    height = int(sys.argv[3]) if len(sys.argv) > 3 else 800
    results = await run(width, height, label)
    out_path = os.path.join(os.path.dirname(__file__), f"_audit_{label}.json")
    with open(out_path, "w") as fh:
        json.dump(results, fh, indent=2, ensure_ascii=False)
    print(f"=== {label} ({width}x{height}) ===")
    for r in results:
        if not r.get("present"):
            print(f"  [skip ] {r['name']}: not in DOM" + (f" — {r.get('error','')}" if r.get("error") else ""))
            continue
        bb = r["rect"]
        oob = r.get("oob", [])
        flag = "  OOB!" if oob else "  ok   "
        print(f"{flag} {r['name']:18s} x={bb['x']:6.1f} y={bb['y']:6.1f} w={bb['width']:6.1f} h={bb['height']:6.1f}" + (f"  ({', '.join(oob)})" if oob else ""))


if __name__ == "__main__":
    asyncio.run(main())
