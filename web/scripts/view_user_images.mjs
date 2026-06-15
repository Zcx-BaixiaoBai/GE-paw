// Try to extract content from the user's images by rendering them in chrome
// and using getImageData() to find the dominant colors and approximate layout.
import puppeteer from "puppeteer-core";
import fs from "node:fs";
import path from "node:path";

const SRC = "C:/Users/Admin/Documents/GE-paw/web/scripts/_popup_screens/user-images";
const CHROME = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";

async function main() {
  const browser = await puppeteer.launch({
    executablePath: CHROME,
    headless: "new",
    args: ["--window-size=1400,1000"],
    defaultViewport: { width: 1400, height: 1000 },
  });
  const page = await browser.newPage();
  const files = fs.readdirSync(SRC).filter(f => f.endsWith(".png"));
  for (const f of files) {
    const fp = path.join(SRC, f);
    const url = "file:///" + fp.replace(/\\/g, "/");
    await page.goto(url, { waitUntil: "load" });
    await new Promise(r => setTimeout(r, 600));

    // Sample colors at a grid to figure out the layout
    const analysis = await page.evaluate(() => {
      const img = document.querySelector("img");
      if (!img) return null;
      const c = document.createElement("canvas");
      c.width = img.naturalWidth;
      c.height = img.naturalHeight;
      const ctx = c.getContext("2d");
      ctx.drawImage(img, 0, 0);
      const data = ctx.getImageData(0, 0, c.width, c.height).data;
      // Sample at 10x10 grid
      const grid = [];
      for (let gy = 0; gy < 10; gy++) {
        for (let gx = 0; gx < 10; gx++) {
          const px = Math.floor((gx + 0.5) * c.width / 10);
          const py = Math.floor((gy + 0.5) * c.height / 10);
          const idx = (py * c.width + px) * 4;
          const r = data[idx], g = data[idx+1], b = data[idx+2];
          grid.push({ x: gx, y: gy, rgb: `${r},${g},${b}` });
        }
      }
      return { width: c.width, height: c.height, grid };
    });
    console.log("==== " + f + " (" + analysis.width + "x" + analysis.height + ") ====");
    // Print a 10x10 grid of colors as a "image fingerprint"
    for (let y = 0; y < 10; y++) {
      let row = "";
      for (let x = 0; x < 10; x++) {
        const cell = analysis.grid.find(c => c.x === x && c.y === y);
        const [r, g, b] = cell.rgb.split(",").map(Number);
        // Convert to brightness char
        const lum = (r * 0.299 + g * 0.587 + b * 0.114);
        const ch = lum > 220 ? " " : lum > 180 ? "." : lum > 140 ? ":" : lum > 100 ? "o" : lum > 60 ? "O" : "#";
        row += ch;
      }
      console.log(row);
    }
    console.log("");
  }
  await browser.close();
}

main().catch((e) => { console.error(e); process.exit(1); });
