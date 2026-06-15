import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1920, "height": 1080})
        
        # Navigate
        await page.goto('http://localhost:5173/app/admin/llm')
        
        # Wait for network to be idle (or specific selector)
        await page.wait_for_load_state('networkidle')
        
        # Wait a bit more just in case
        await page.wait_for_timeout(5000)
        
        # Take screenshot
        await page.screenshot(path='output/playwright/llm_config_debug.png', full_page=True)
        print("Screenshot taken")
        
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
