
import puppeteer from 'puppeteer-core';
import fs from 'fs';
import path from 'path';

const scriptDir = ''
import {executablePath} from 'puppeteer'

export default async (req) => {
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

async function getHtmlContent(bank, data) {
  let htmlContent = await fs.promises.readFile(path.join(scriptDir, bank, '1.html'), 'utf-8');
  
  for (const [key, value] of Object.entries(data)) {
    htmlContent = htmlContent.replaceAll(key, String(value));
  }
  htmlContent = htmlContent.replaceAll('$URL', 'http://127.0.0.1:5000/' + bank);

  return htmlContent;
}

async function htmlToPdf(htmlContent) {
  const browser = await puppeteer.launch({
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
    ignoreHTTPSErrors: true,
    executablePath: executablePath(),
    headless: false
  });

  try {
    const page = (await browser.pages())[0];
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
const currentTime = new Date().toLocaleString('ru-RU', { day: '2-digit', month: '2-digit', year: '2-digit', hour: '2-digit', minute: '2-digit' });
const htmlContent = await getHtmlContent('tinkoff', {'TIME': currentTime, 'SENDER_NAME': 'Егор Иванович Ж.', 'RECEIVER_NUMBER':'+7 (912) 999-55-66','RECEIVER_NAME': 'Алексей Михайлович З.', "AMOUNT": '59664.10'});
const pdfBuffer = await htmlToPdf(htmlContent);
import { PDFDocument } from 'pdf-lib'
const pdf = await PDFDocument.load(pdfBuffer);
pdf.setTitle('Квитанция-11100399')
pdf.setAuthor('')
pdf.setSubject('"/reports/IB/Receipt"')
pdf.setKeywords(['22.10.2024', '08:41:12|f8848b21-135a-4ad6-b014-15c00b30e714|7258'])
pdf.setProducer('OpenPDF 1.3.30.jaspersoft.2')
pdf.setCreator('JasperReports Library version 6.20.3-415f9428cffdb6805c6f85bbb29ebaf18813a2ab')
pdf.setCreationDate(new Date('2024-10-22 08:41:12+03:00'))
pdf.setModificationDate(new Date('2024-10-22 08:41:12+03:00'))

fs.writeFileSync('tinkoff.pdf', await pdf.save({useObjectStreams: false}));

