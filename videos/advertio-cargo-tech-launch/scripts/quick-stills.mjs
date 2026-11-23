import path from 'node:path';
import fs from 'node:fs';
import {bundle} from '@remotion/bundler';
import {openBrowser, selectComposition, renderStill} from '@remotion/renderer';

const root=process.cwd();
const output=path.join(root,'out','stills');
fs.mkdirSync(output,{recursive:true});
const serveUrl=await bundle({entryPoint:path.join(root,'src','index.ts')});
const browser=await openBrowser('chrome',{
 browserExecutable:process.env.CHROME_PATH||undefined,
 logLevel:'error'
});
try{
 const composition=await selectComposition({serveUrl,id:'AdvertioCargoFinal',puppeteerInstance:browser});
 const seconds=[.75,2.25,4.0,6.15,7.85,9.7,11.2,13.8,16.8,19];
 for(let i=0;i<seconds.length;i++){
  const frame=Math.round(seconds[i]*30);
  const name=String(i+1).padStart(2,'0')+'-'+String(seconds[i]).replace('.','p')+'s.jpg';
  await renderStill({serveUrl,composition,puppeteerInstance:browser,
    output:path.join(output,name),frame,imageFormat:'jpeg',jpegQuality:82,scale:.5,logLevel:'error'});
  console.log('Quick Preview',i+1,'/',seconds.length,seconds[i]+'s',name);
 }
}finally{
 await browser.close();
}
