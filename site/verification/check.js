// Check a live page at desktop, tablet and phone widths: screenshot, horizontal overflow, empty containers,
// title/H1, console errors. Usage: node check.js <full page URL> <output prefix>
const { chromium } = require('playwright');
(async () => {
  const [url, out = 'check'] = process.argv.slice(2);
  const browser = await chromium.launch();
  for (const [name, w] of [['desktop', 1440], ['tablet', 834], ['mobile', 390]]) {
    const page = await browser.newPage({ viewport: { width: w, height: 900 } });
    const errors = []; page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
    const res = await page.goto(url + (url.includes('?') ? '&' : '?') + 'nc=' + Date.now(), { waitUntil: 'networkidle' });
    for (let y = 0; y < 15000; y += 700) { await page.evaluate(v => window.scrollTo(0, v), y); await page.waitForTimeout(40); }
    await page.evaluate(() => window.scrollTo(0, 0));
    await page.screenshot({ path: `${out}-${name}.png`, fullPage: true });
    const info = await page.evaluate(() => ({
      overflow: document.documentElement.scrollWidth > window.innerWidth,
      title: document.title,
      h1: [...document.querySelectorAll('h1')].map(h => h.textContent.trim()),
      emptyContainers: [...document.querySelectorAll('.e-con, .e-flexbox')].filter(e => !e.children.length).map(e => e.id || e.className).slice(0, 5),
      imagesOver400KB: [...performance.getEntriesByType('resource')].filter(r => r.initiatorType === 'img' && r.encodedBodySize > 400 * 1024).map(r => r.name),
    }));
    console.log(name, res.status(), JSON.stringify(info), errors.length ? 'console errors: ' + errors.slice(0, 3).join(' | ') : '');
    await page.close();
  }
  await browser.close();
})();
