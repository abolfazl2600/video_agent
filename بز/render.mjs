import {parseHTML} from 'linkedom';
import fs from 'node:fs';import sharp from 'sharp';
const {document,window}=parseHTML('<html><body></body></html>');globalThis.document=document;globalThis.window=window;
const {createFilm}=await import('./scene.mjs');
const f=createFilm();fs.mkdirSync('frames',{recursive:true});
const ids=process.argv.includes('--samples')?[0,60,150,240,330,420]:Array.from({length:450},(_,i)=>i);
for(let i of ids){f.update(i/30);let svg=f.renderer.domElement.outerHTML.replace('<svg ','<svg xmlns="http://www.w3.org/2000/svg" ');await sharp(Buffer.from(svg)).flatten({background:"#050B16"}).png().toFile(`frames/${String(i).padStart(4,'0')}.png`);if(i%60===0)console.log('frame',i);}
