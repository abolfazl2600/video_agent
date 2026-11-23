import {parseHTML} from 'linkedom';
import fs from 'node:fs';
import sharp from 'sharp';

// Preview is the default for local runs and all folder-change GitHub Actions.
// Final mode is never inferred; it must be explicitly requested.
const MODE=process.env.ADVERTIO_RENDER_MODE||'preview';
if(!['preview','final'].includes(MODE))throw Error('Unknown ADVERTIO_RENDER_MODE: '+MODE);
const FPS=MODE==='preview'?10:30;
const FRAME_COUNT=15*FPS;
const SIZE=MODE==='preview'?[360,640]:[720,1280];
const {document,window}=parseHTML('<html><body></body></html>');
globalThis.document=document;
globalThis.window=window;
const {createFilm}=await import('./scene.mjs');
const film=createFilm();
film.renderer.setSize(...SIZE);
if(MODE==='preview')film.renderer.setQuality('low');
const sampleTimes=[0,1.5,3.5,4.5,6.5,8,9.5,11.5,13.5,14.9];
const ids=process.argv.includes('--samples')
  ? [...new Set(sampleTimes.map(t=>Math.min(FRAME_COUNT-1,Math.round(t*FPS))))]
  : Array.from({length:FRAME_COUNT},(_,i)=>i);
fs.mkdirSync('frames',{recursive:true});
console.log('Rendering',MODE,'at',FPS,'fps,',SIZE.join('x'),'for',ids.length,'frames');
for(const index of ids){
  film.update(index/FPS);
  const raw=film.renderer.domElement.outerHTML;
  const svg=raw.includes('xmlns=')?raw:raw.replace('<svg ','<svg xmlns="http://www.w3.org/2000/svg" ');
  await sharp(Buffer.from(svg)).flatten({background:'#0C1827'}).png().toFile('frames/'+String(index).padStart(4,'0')+'.png');
  if(index%(FPS*2)===0)console.log('Rendered frame',index,'of',FRAME_COUNT);
}
