import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath, pathToFileURL} from 'node:url';
import {execFileSync} from 'node:child_process';
import puppeteer from 'puppeteer-core';

const MODE=process.env.ADVERTIO_RENDER_MODE||'preview';
if(!['preview','final'].includes(MODE))throw Error('Unknown ADVERTIO_RENDER_MODE: '+MODE);
const FPS=MODE==='preview'?10:30;
const FRAME_COUNT=15*FPS;
const [width,height]=MODE==='preview'?[360,640]:[720,1280];
const sampleTimes=[0,1.5,3.5,4.5,6.5,8,9.5,11.5,13.5,14.9];
const ids=process.argv.includes('--samples')
  ? [...new Set(sampleTimes.map(t=>Math.min(FRAME_COUNT-1,Math.round(t*FPS))))]
  : Array.from({length:FRAME_COUNT},(_,i)=>i);

function findChrome(){
  const candidates=[
    process.env.PUPPETEER_EXECUTABLE_PATH,process.env.CHROME_PATH,
    '/usr/bin/google-chrome','/usr/bin/google-chrome-stable',
    '/usr/bin/chromium','/usr/bin/chromium-browser',
    '/opt/google/chrome/chrome'
  ];
  for(const executable of candidates)if(executable&&fs.existsSync(executable))return executable;
  for(const name of ['google-chrome','chromium','chromium-browser']){
    try{
      const result=execFileSync('which',[name],{encoding:'utf8'}).trim();
      if(result)return result;
    }catch{}
  }
  throw Error('Chromium/Chrome not found. Install Chrome or set CHROME_PATH.');
}
const root=path.dirname(fileURLToPath(import.meta.url));
fs.mkdirSync(path.join(root,'frames'),{recursive:true});
const browser=await puppeteer.launch({
  executablePath:findChrome(),
  headless:true,
  args:[
    '--no-sandbox','--disable-dev-shm-usage','--disable-gpu-sandbox',
    '--enable-webgl','--use-gl=angle','--use-angle=swiftshader',
    '--enable-unsafe-swiftshader','--hide-scrollbars'
  ]
});
try{
  const page=await browser.newPage();
  await page.setViewport({width,height,deviceScaleFactor:1});
  page.on('pageerror',err=>console.error('Browser renderer error:',err.message));
  const url=pathToFileURL(path.join(root,'index.html'));
  url.searchParams.set('width',String(width));
  url.searchParams.set('height',String(height));
  await page.goto(url.href,{waitUntil:'load',timeout:60000});
  await page.waitForFunction(()=>window.__advertioReady===true||Boolean(window.__advertioError),{timeout:60000});
  const loadError=await page.evaluate(()=>window.__advertioError);
  if(loadError)throw Error(loadError);
  const gpu=await page.evaluate(()=>window.__advertioRendererName);
  console.log('Renderer:',gpu,'Chrome:',browser.process()?.spawnfile);
  console.log('Rendering',MODE,'at',FPS,'fps,',width+'x'+height,'for',ids.length,'frames');
  let start=performance.now();
  for(const [position,index] of ids.entries()){
    await page.evaluate((time)=>window.__advertioRenderAt(time),index/FPS);
    await page.screenshot({
      path:path.join(root,'frames',String(index).padStart(4,'0')+'.png'),
      type:'png',animations:'disabled'
    });
    if(position===0||position%10===0||position===ids.length-1){
      console.log('Rendered frame',position+1,'/',ids.length,'(index',index,') in',Math.round(performance.now()-start),'ms');
    }
  }
}finally{
  await browser.close();
}
