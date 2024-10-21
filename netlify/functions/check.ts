import { Handler } from '@netlify/functions';
import puppeteer from 'puppeteer-core';
import chromium from '@sparticuz/chromium';
import fs from 'fs';
import path from 'path';

const scriptDir = path.dirname(new URL(import.meta.url).pathname);

const getCheck = async (bank: string, d: Record<string, string>) => {
  const data = {
    'DOCUMENT': '4252228616',
    'SENDER_CARD': '2314',
    'RECEIVER_CARD': '2511',
    'CODE': '212251',
    'AMOUNT': '1234.13',
    'TIME': '14.10.2024 13:38',
    'SENDER_NAME': 'Алексей Андреевич Ф.',
    'RECEIVER_NAME': 'Скам Скамыч Ф.',
    'RECEIVER_NUMBER': '+7 (993) 532-49-05',
    ...d
  };

  let htmlContent = await fs.promises.readFile(path.join(scriptDir, bank, '1.html'), 'utf-8');
  
  for (const [key, value] of Object.entries(data)) {
    htmlContent = htmlContent.replace(key, String(value));
  }
  htmlContent = htmlContent.replace('$URL', 'http://127.0.0.1:5000/' + bank);

  const pdfBuffer = await htmlToPdf(htmlContent);
  return pdfBuffer;
};

const htmlToPdf = async (htmlContent: string): Promise<Buffer> => {
  await chromium.font('/tmp/chromium/swiftshader/libEGL.so');
  const browser = await puppeteer.launch({
    args: chromium.args,
    defaultViewport: chromium.defaultViewport,
    executablePath: await chromium.executablePath(),
    headless: chromium.headless,
  });

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

  const pdfBuffer = await page.pdf({
    title: 'чек',
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

  await browser.close();
  return pdfBuffer;
};

export const handler: Handler = async (event, context) => {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method Not Allowed' };
  }

  const { bank, ...data } = JSON.parse(event.body || '{}');

  if (!bank) {
    return { statusCode: 400, body: 'Bank parameter is required' };
  }

  try {
    const pdfBuffer = await getCheck(bank, data);
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
    console.error('Error generating PDF:', error);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'Failed to generate PDF' })
    };
  }
};
