//Author: Tarek R.

'use strict';

const puppeteer = require('puppeteer');
const fs = require('fs');

async function initiate_browser () {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  page.setViewport({ width: 1920, height: 1080 });
  return page
};

async function scrap_emails(page, url) {
  page.goto(url)
  await new Promise(r => setTimeout(r, 3000));
  var results = [];
  //
  //
  //
  console.log(results)
  fs.writeFileSync('email_from_domain_export.json', JSON.stringify(results, null, 2));
  await browser.close();
};
