import {createFilm} from './scene.mjs';

try {
  const params=new URLSearchParams(window.location.search);
  const width=Number(params.get('width')||360);
  const height=Number(params.get('height')||640);
  if(!Number.isInteger(width)||!Number.isInteger(height)||width<=0||height<=0)throw Error('Invalid frame dimensions');
  const film=createFilm();
  film.renderer.setPixelRatio(1);
  film.renderer.setSize(width,height,false);
  const canvas=film.renderer.domElement;
  canvas.style.display='block';
  document.body.appendChild(canvas);
  window.__advertioRenderAt=(time)=>{
    film.update(time);
    return film.renderer.info.render.calls;
  };
  window.__advertioRendererName='Three.js WebGLRenderer / SwiftShader capable';
  window.__advertioReady=true;
} catch(error) {
  window.__advertioError=String(error?.stack||error);
  console.error(error);
  throw error;
}
