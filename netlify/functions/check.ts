import { launch } from 'puppeteer-core';
import fs from 'fs';
import path from 'path';

const scriptDir = path.dirname(new URL(import.meta.url).pathname);

export async function getCheck(bank, data) {

  let htmlContent = await fs.promises.readFile(path.join(scriptDir, bank, '1.html'), 'utf-8');
  
  for (const [key, value] of Object.entries(data)) {
    htmlContent = htmlContent.replace(key, String(value));
  }
  htmlContent = htmlContent.replace('$URL', '/' + bank);

  await htmlToPdf(htmlContent);
  return await fs.promises.readFile(path.join(scriptDir, 'check.pdf'));
}

async function htmlToPdf(htmlContent) {
  const browser = await launch({
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
    ignoreHTTPSErrors: true
  });

  try {
    const page = await browser.newPage();
    await page.setContent(htmlContent);
    await page.setViewport({ width: 1920, height: 1080 });

    await page.waitForSelector("#p1");
    await new Promise(resolve => setTimeout(resolve, 2000));

    const dimensions = await page.evaluate(() => {
      const element = document.getElementById('p1');
      return {
        width: element.offsetWidth,
        height: element.offsetHeight
      };
    });

    await page.pdf({
      path: path.join(scriptDir, 'check.pdf'),
      width: dimensions.width,
      height: dimensions.height,
      printBackground: true,
      margin: {
        top: '0px',
        right: '0px',
        bottom: '0px',
        left: '0px'
      }
    });
  } finally {
    await browser.close();
  }
}
