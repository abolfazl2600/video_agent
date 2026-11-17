import * as T from 'three';
import {SVGRenderer} from 'three/addons/renderers/SVGRenderer.js';
export function createFilm(){
 const scene=new T.Scene(),camera=new T.PerspectiveCamera(42,720/1280,.1,1500),renderer=new SVGRenderer();renderer.setSize(720,1280);renderer.setQuality('high');renderer.setClearColor('#050B16');renderer.overdraw=.3;
 const ink='#2AD9E6',surface='#101E32',plane=new T.Group();scene.add(plane);
 function line(p,c=ink,a=1,parent=scene,w=1){let o=new T.Line(new T.BufferGeometry().setFromPoints(p.map(q=>new T.Vector3(...q))),new T.LineBasicMaterial({color:c,opacity:a,transparent:a<1,linewidth:w}));parent.add(o);return o;}
 function mesh(g,c=surface,parent=scene,edges=true){let o=new T.Mesh(g,new T.MeshBasicMaterial({color:c,side:T.DoubleSide}));parent.add(o);if(edges)o.add(new T.LineSegments(new T.EdgesGeometry(g,28),new T.LineBasicMaterial({color:ink,linewidth:1})));return o;}
 function box(x,y,z,w,h,d,c=surface,parent=scene){let o=mesh(new T.BoxGeometry(w,h,d),c,parent);o.position.set(x,y,z);return o;}
 function poly(p,c=surface,parent=plane){let s=new T.Shape();p.forEach(([x,y],i)=>i?s.lineTo(x,y):s.moveTo(x,y));s.closePath();return mesh(new T.ShapeGeometry(s),c,parent);}
 const rings=[[-12,.08],[-11.6,.6],[-10.5,1.35],[-9,1.8],[-7.5,2],[3,2],[5.8,1.75],[8,1.25],[9.6,.55],[10.4,.17]];
 let body=mesh(new T.LatheGeometry(rings.map(([z,r])=>new T.Vector2(r,z+12)),24),surface,plane,false);body.rotation.x=Math.PI/2;body.position.set(0,3.7,-12);
 for(let z of [-8,4,8]){let i=rings.findIndex(p=>p[0]>=z),a=rings[Math.max(0,i-1)],b=rings[Math.max(0,i)],r=a[1]+(b[1]-a[1])*(z-a[0])/(b[0]-a[0]||1);line(Array.from({length:49},(_,k)=>[r*Math.cos(k*Math.PI/24),3.7+r*Math.sin(k*Math.PI/24),z]),ink,.23,plane,.65);}
 for(let a of [0,Math.PI,Math.PI/2,Math.PI*1.5])line(rings.map(([z,r])=>[r*Math.cos(a),3.7+r*Math.sin(a),z]),ink,1,plane,1.2);
 for(let s of [-1,1]){
  let wing=poly([[s*1.35,-4],[s*5.2,-2],[s*14.7,3.8],[s*15.3,5.1],[s*8.3,4.2],[s*1.5,2.5]]);wing.rotation.x=Math.PI/2;wing.position.y=3;
  line([[s*1.8,3.02,.3],[s*13.9,3.02,4.4]],ink,.7,plane);
  let tail=poly([[s*.4,6.7],[s*5.8,9.2],[s*6.1,10.2],[s*.5,9.3]]);tail.rotation.x=Math.PI/2;tail.position.y=4.25;
  let eng=mesh(new T.CylinderGeometry(1.03,1.13,3.8,18,1,true),'#1A344F',plane);eng.rotation.x=Math.PI/2;eng.position.set(s*6,1.9,-.4);
  let cap=mesh(new T.CircleGeometry(.9,20),ink,plane,false);cap.position.set(s*6,1.9,1.52);let hub=mesh(new T.CircleGeometry(.28,12),'#0CE7ED',plane,false);hub.position.set(s*6,1.9,1.54);
  for(let k=0;k<8;k++){let a=k*Math.PI/4;line([[s*6+.3*Math.cos(a),1.9+.3*Math.sin(a),1.56],[s*6+.78*Math.cos(a+.3),1.9+.78*Math.sin(a+.3),1.56]],'#69F3F9',.9,plane,.7);}
  box(s*5.7,2.8,-1,.45,1.5,1.3,surface,plane);
 }
 let fin=new T.Shape();[[6,4.5],[7,9.4],[9.5,11.4],[10.4,11.4],[10.1,4.3]].forEach(([z,y],i)=>i?fin.lineTo(z,y):fin.moveTo(z,y));fin.closePath();let f=mesh(new T.ExtrudeGeometry(fin,{depth:.2,bevelEnabled:false}),surface,plane);f.rotation.y=-Math.PI/2;f.position.x=.1;
 let apu=mesh(new T.CircleGeometry(.33,24),ink,plane,false);apu.position.set(0,4.35,10.58);
 let rim=mesh(new T.RingGeometry(.34,.44,24),'#51F6F9',plane,false);rim.position.set(0,4.35,10.59);
 let capFin=new T.Shape();[[7.1,8.8],[9.5,11.4],[10.4,11.4],[10.25,8.8]].forEach(([z,y],i)=>i?capFin.lineTo(z,y):capFin.moveTo(z,y));capFin.closePath();let cf=mesh(new T.ExtrudeGeometry(capFin,{depth:.22,bevelEnabled:false}),'#17668F',plane);cf.rotation.y=-Math.PI/2;cf.position.x=.11;
 // Stylized tail emblem drawn on both fin faces, echoing the reference livery.
 for(let side of [-1,1]){
  line([[side*.125,5.4,9.4],[side*.125,5.9,8.7],[side*.125,6.7,8.1],[side*.125,7.2,8.5],[side*.125,6.6,8.8],[side*.125,6.0,9.4]],'#17668F',1,plane,2.2);
  for(let k=0;k<4;k++)line([[side*.13,6.5+k*.16,8.45],[side*.13,6.7+k*.16,9.35]],'#17668F',1,plane,1.4);
 }
 const gear=new T.Group();plane.add(gear);for(let z of [-6,6.5])for(let s of [-1,1]){let x=z<0?s*.45:s*4.3;box(x,1.1,z,.12,1.6,.15,ink,gear);for(let off of [-.24,.24]){let wh=mesh(new T.CylinderGeometry(.62,.62,.36,16),ink,gear,false);wh.rotation.z=Math.PI/2;wh.position.set(x+off,.52,z);}}
 for(let s of [-1,1])for(let z=-8;z<4;z+=.68)line([[s*1.94,4.2,z-.15],[s*2.02,4.43,z-.15],[s*2.02,4.43,z+.12],[s*1.94,4.2,z+.12]],ink,.9,plane,.85);
 for(let x of [-18,18])line([[x,.02,150],[x,.02,-650]],'#1E718B',1,scene,1.5);
 for(let z=100;z>-600;z-=20){box(0,.012,z,.35,.01,8,'#18BBD0');if(z%40===0){box(-13,.018,z,3,.01,8,'#193A52');box(13,.018,z,3,.01,8,'#193A52');}}
 for(let x=-120;x<=120;x+=20)line([[x,0,160],[x,0,-180]],'#153149',.5,scene,.5);for(let z=-180;z<150;z+=20)line([[-160,0,z],[160,0,z]],'#153149',.5,scene,.5);
 box(-48,6,-170,48,12,16,'#132940');box(60,6,-160,60,12,16,'#132940');for(let s of [-1,1])for(let j=0;j<8;j++)box(s*48+j*4-10,8,-151.9,2,5,.1,'#315B79');
 box(25,10.5,-150,2.6,21,2.6,'#19344B');box(25,21,-150,7,2,6);box(25,23,-150,6,2,5,'#3180A5');box(25,24.4,-150,7,.5,6,'#19344B');
 for(let s of [-1,1])for(let z of [-30,-58,-86])line([[s*24,0,z],[s*24,9,z],[s*24-2,9,z]],'#1D7893',1,scene,.8);
 const ease=v=>{v=Math.max(0,Math.min(1,v));return v*v*(3-2*v)};
 function update(t){
  const orbit=ease((t-.35)/4.9),taxi=3*t+1.15*t*t,air=ease((t-7.2)/6.8);
  plane.position.set(0,air*48,-taxi);plane.rotation.x=air*.14;plane.rotation.z=-Math.sin(air*Math.PI)*.015;
  gear.scale.y=1-ease((t-8.7)/2)*.97;gear.position.y=ease((t-8.7)/2)*1.1;
  const pz=plane.position.z,py=plane.position.y;
  camera.fov=18.114+16*orbit;camera.updateProjectionMatrix();
  camera.position.set(-19.714*(1-orbit),1.8+7.2*orbit+py*.52,82.27+8*orbit+pz*.38);
  camera.lookAt(new T.Vector3(-.323*(1-orbit),5.413+1.6*orbit+py*.82,pz*.96));
  camera.updateMatrixWorld();scene.updateMatrixWorld(true);renderer.render(scene,camera);
 }
 update(0);return{scene,camera,renderer,update};
}
