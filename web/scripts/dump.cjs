const puppeteer = require('puppeteer-core');
(async () => {
  const url = process.argv[2];
  const exe = process.env.SHOT_EXE || 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
  const browser = await puppeteer.launch({
    executablePath: exe,
    headless: 'new',
    args: ['--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage', '--hide-scrollbars'],
    defaultViewport: { width: 1440, height: 900, deviceScaleFactor: 1 },
  });
  const page = await browser.newPage();
  page.on('framenavigated', (f) => console.log('  nav:', f.url()));
  page.on('pageerror', (e) => console.log('  [pageerror]', e.message.slice(0, 300)));
  page.on('console', (m) => { if (m.type() === 'error' || m.text().includes('AUTH') || m.text().includes('token')) console.log('  [' + m.type() + ']', m.text().slice(0, 300)); });
  try { await page.goto(url, { waitUntil: 'load', timeout: 20000 }); } catch (e) {}
  await new Promise((r) => setTimeout(r, 1500));
  const isLogin = await page.evaluate(() => !!document.querySelector('input[value="admin"]'));
  if (isLogin) {
    await page.click('button[type="submit"]');
  }
  await new Promise((r) => setTimeout(r, 3000));
  const state = await page.evaluate(() => {
    try { return { ls: localStorage.getItem('gepaw-auth'), url: location.pathname }; } catch (e) { return { error: e.message }; }
  });
  console.log('  state:', JSON.stringify(state));
  await browser.close();
})().catch((e) => { console.error('err', e.message); process.exit(1); });
