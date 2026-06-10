const puppeteer = require('puppeteer-core');
const fs = require('fs');
(async () => {
  const url = process.argv[2];
  const out = process.argv[3];
  const waitMs = Number(process.argv[4] || 4000);
  const w = Number(process.argv[5] || 1440);
  const h = Number(process.argv[6] || 900);
  const exe = process.env.SHOT_EXE || 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
  const browser = await puppeteer.launch({
    executablePath: exe,
    headless: 'new',
    args: ['--no-sandbox', '--disable-gpu', '--disable-software-rasterizer', '--disable-dev-shm-usage', '--hide-scrollbars'],
    defaultViewport: { width: w, height: h, deviceScaleFactor: 1 },
  });
  const page = await browser.newPage();
  await page.setViewport({ width: w, height: h });
  page.on('console', m => console.log('  [console]', m.text().slice(0,200)));
  page.on('pageerror', e => console.log('  [pageerror]', e.message.slice(0,200)));
  await page.goto(url, { waitUntil: 'networkidle0', timeout: 30000 }).catch((e) => console.log('goto warn:', e.message));
  await new Promise((r) => setTimeout(r, waitMs));
  const ready = await page.evaluate(() => {
    const root = document.getElementById('root');
    return { hasRoot: !!root, rootLen: root?.innerHTML?.length || 0, title: document.title, body: document.body?.children?.length };
  });
  console.log('ready', ready);
  await page.screenshot({ path: out, fullPage: false, type: 'png' });
  console.log('saved', out, fs.statSync(out).size, 'bytes');
  await browser.close();
})().catch((e) => { console.error('err', e.message); process.exit(1); });
