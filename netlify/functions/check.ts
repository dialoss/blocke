import puppeteer from 'puppeteer-core';
import fs from 'fs';
import path from 'path';

const scriptDir = path.dirname(new URL(import.meta.url).pathname);

export default async (req: Request) => {
  const { bank, data } = await req.json();

  try {
    const htmlContent = await getHtmlContent(bank, data);
    const pdfBuffer = await htmlToPdf(htmlContent);

    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/pdf',
        'Content-Disposition': 'attachment; filename=check.pdf'
      },
      body: pdfBuffer.toString('base64'),
      isBase64Encoded: true
    };
  } catch (error) {
    console.error('Error:', error);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'Internal Server Error' })
    };
  }
};

async function getHtmlContent(bank: string, data: Record<string, string>) {
  let htmlContent = await fs.promises.readFile(path.join(scriptDir, bank, '1.html'), 'utf-8');
  
  for (const [key, value] of Object.entries(data)) {
    htmlContent = htmlContent.replace(key, String(value));
  }
  htmlContent = htmlContent.replace('$URL', '/' + bank);

  return htmlContent;
}

async function htmlToPdf(htmlContent: string) {
  const browser = await puppeteer.launch({
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
      return element ? {
        width: element.offsetWidth,
        height: element.offsetHeight
      } : null;
    });

    if (!dimensions) {
      throw new Error('Failed to get dimensions');
    }

    const pdfBuffer = await page.pdf({
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

    return pdfBuffer;
  } finally {
    await browser.close();
  }
}
