#!/usr/bin/env node
/* Requires chrome-remote-interface in a temporary install. Start Chromium with:
   chromium --headless --no-sandbox --remote-debugging-port=9223 about:blank
   node mobile_layout_check.cjs http://127.0.0.1:3000 dist/manus-routes.json 9223
*/
const CDP = require("chrome-remote-interface");
const fs = require("fs");
const origin = (process.argv[2] || "http://127.0.0.1:3000").replace(/\/$/, "");
const manifest = JSON.parse(fs.readFileSync(process.argv[3] || "dist/manus-routes.json", "utf8"));
const port = Number(process.argv[4] || process.env.CDP_PORT || 9223);
const expected = {
  "/solar-loan-calculator/": '[data-calculator="solar-loan"]',
  "/solar-financing-calculator/": '[data-calculator="solar-financing"]',
  "/solar-proposal-audit/": '[data-calculator="proposal-audit"]'
};
const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));
(async () => {
  const client = await CDP({port}); const {Page, Runtime, Emulation, Log} = client;
  await Promise.all([Page.enable(), Runtime.enable(), Log.enable()]);
  const results=[]; let exceptions=0; let consoleErrors=0;
  Runtime.exceptionThrown(() => exceptions++);
  Log.entryAdded(({entry}) => { if (entry.level === "error") consoleErrors++; });
  for (const {path} of manifest.routes) {
    exceptions=0; consoleErrors=0;
    await Emulation.setDeviceMetricsOverride({width:390,height:844,deviceScaleFactor:2,mobile:true,screenWidth:390,screenHeight:844});
    await Page.navigate({url:origin+path});
    await sleep(300);
    const expression=`(() => { const root=document.documentElement, body=document.body, width=window.innerWidth; const wide=[...document.querySelectorAll('body *')].map(el=>{const r=el.getBoundingClientRect();return {tag:el.tagName.toLowerCase(),className:String(el.className||'').slice(0,80),left:r.left,right:r.right,width:r.width};}).filter(x=>x.width>0&&(x.left < -1 || x.right > width+1)); const mount=${JSON.stringify(expected[path]||null)}; return {path:${JSON.stringify(path)},title:document.title,innerWidth:width,scrollWidth:root.scrollWidth,bodyScrollWidth:body.scrollWidth,horizontalOverflow:root.scrollWidth>width+1||body.scrollWidth>width+1,wideElements:wide,h1Count:document.querySelectorAll('h1').length,mainCount:document.querySelectorAll('main#main-content').length,brokenImages:[...document.images].filter(i=>!i.complete||i.naturalWidth===0).length,mountPresent:mount?Boolean(document.querySelector(mount)):true,viewportMeta:Boolean(document.querySelector('meta[name="viewport"]')),navPresent:Boolean(document.querySelector('.site-nav')),footerPresent:Boolean(document.querySelector('.site-footer')),bodyTextLength:(body.innerText||'').trim().length,exceptions:${exceptions},consoleErrors:${consoleErrors}}; })()`;
    const evaluation=await Runtime.evaluate({expression,returnByValue:true});
    if (evaluation.exceptionDetails) throw new Error(`Runtime evaluation failed on ${path}: ${JSON.stringify(evaluation.exceptionDetails)}`);
    results.push(evaluation.result.value);
  }
  await Emulation.clearDeviceMetricsOverride(); await client.close();
  const meaningful=results.filter(r=>r.horizontalOverflow||r.brokenImages||!r.mountPresent||r.exceptions||r.consoleErrors||r.h1Count!==1||r.mainCount!==1||!r.viewportMeta||!r.navPresent||!r.footerPresent||r.wideElements.some(x=>x.className!=="skip-link"));
  console.log(JSON.stringify({routes:results.length,issues:meaningful,results},null,2));
  process.exit(meaningful.length ? 1 : 0);
})().catch(error=>{ console.error(error); process.exit(1); });
