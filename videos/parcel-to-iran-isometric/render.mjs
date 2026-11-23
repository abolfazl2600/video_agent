import {parseHTML} from 'linkedom';
import fs from 'node:fs';
import sharp from 'sharp';
const {document,window}=parseHTML('<html><body></body></html>');
globalThis.document=document;
globalThis.window=window;
const {createFilm}=await import('./scene.mjs');
const film=createFilm();
const SAMPLE=[0,45,105,135,195,240,285,335,395,449];
const ids=process.argv.includes('--samples')?SAMPLE:Array.from({length:450},(_,i)=>i);
fs.mkdirSync('frames',{recursive:true});
for(const index of ids){
  film.update(index/30);
  const raw=film.renderer.domElement.outerHTML;
  const svg=raw.includes('xmlns=')?raw:raw.replace('<svg ','<svg xmlns="http://www.w3.org/2000/svg" ');
  await sharp(Buffer.from(svg)).flatten({background:'#0C1827'}).png().toFile('frames/'+String(index).padStart(4,'0')+'.png');
  if(index%30===0)console.log('Rendered frame',index,'of 450');
}
