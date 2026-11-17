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

 // Aircraft skin: circumferential panel seams, cockpit glazing and twin cabin window rows.
 const hullRadius=(z)=>{
  for(let i=1;i<rings.length;i++)if(z<=rings[i][0]){
   const a=rings[i-1],b=rings[i],u=(z-a[0])/(b[0]-a[0]);
   return a[1]+u*(b[1]-a[1]);
  }
  return rings[rings.length-1][1];
 };
 for(let z of [-10.8,-9.4,-6.7,-3.5,-.5,2.4,5.3,7.7,9.1]){
  const r=hullRadius(z)+.035;
  line(Array.from({length:33},(_,i)=>{const a=i*Math.PI/16;return [r*Math.cos(a),3.7+r*Math.sin(a),z]}),'#427F9D',.48,plane,.5);
 }
 for(const side of [-1,1]){
  for(let z=-7.2;z<=4.25;z+=.84){
   const x=side*(hullRadius(z)+.075),y=4.02;
   line([[x,y-.12,z-.16],[x,y+.13,z-.16],[x,y+.19,z-.08],[x,y+.19,z+.12],[x,y+.11,z+.17],[x,y-.12,z+.17],[x,y-.12,z-.16]],'#96EDF4',.9,plane,.72);
  }
  for(const z of [-8.6,4.8]){
   const x=side*(hullRadius(z)+.13),y=3.72;
   line([[x,y-.37,z-.42],[x,y+.89,z-.42],[x,y+1.03,z-.26],[x,y+1.03,z+.30],[x,y+.88,z+.44],[x,y-.37,z+.44],[x,y-.37,z-.42]],'#5BC6D8',.88,plane,.9);
   line([[x+side*.008,y+.13,z+.30],[x+side*.008,y+.13,z+.4]],'#CFFBFF',1,plane,1.3);
  }
  // L-shaped forward cockpit glazing and adjacent technical access panels.
  const cx=side*(hullRadius(-10.05)+.13);
  line([[cx,4.4,-10.48],[cx,4.87,-10.33],[cx,4.94,-9.88],[cx,4.5,-9.82],[cx,4.4,-10.48]],'#BEFBFF',1,plane,1.5);
  const hx=side*(hullRadius(6.6)+.10);
  line([[hx,3.36,6.1],[hx,4.15,6.1],[hx,4.15,7.25],[hx,3.36,7.25],[hx,3.36,6.1]],'#4B9FB8',.9,plane,.7);
  // Longitudinal airline pinstripe for additional body definition.
  line(Array.from({length:26},(_,i)=>{const z=-7.0+i*.54;return [side*(hullRadius(z)+.065),3.39,z]}),'#3E99BA',.58,plane,.75);
 }
 for(let s of [-1,1]){
  let wing=poly([[s*1.35,-4],[s*5.2,-2],[s*14.7,3.8],[s*15.3,5.1],[s*8.3,4.2],[s*1.5,2.5]]);wing.rotation.x=Math.PI/2;wing.position.y=3;
  line([[s*1.8,3.02,.3],[s*13.9,3.02,4.4]],ink,.7,plane);

  // Wing-surface detailing: flap breaks, spoiler panels and outer ailerons.
  line([[s*2.6,3.055,1.55],[s*8.25,3.055,3.76],[s*13.8,3.055,4.75]],'#A3EDF4',.78,plane,.8);
  line([[s*3.5,3.07,1.9],[s*4.1,3.07,.23]],'#427E9D',.85,plane,.6);
  line([[s*6.2,3.07,2.9],[s*6.9,3.07,1.5]],'#427E9D',.85,plane,.6);
  line([[s*9.1,3.07,3.96],[s*9.65,3.07,3.29]],'#427E9D',.85,plane,.6);
  for(const x of [5.6,8.7,11.3])line([[s*x,3.085,3.15],[s*(x+.42),3.085,3.52]],'#37D1E1',.7,plane,.7);
  // Winglet and navigation beacon: red on port side, green on starboard.
  let winglet=box(s*15.05,3.66,4.55,.14,1.48,.35,'#1D668A',plane);
  winglet.rotation.z=s*.16;
  let beacon=mesh(new T.SphereGeometry(.23,8,6),s<0?'#FF5D70':'#5CF5B9',plane,false);
  beacon.position.set(s*15.1,4.43,4.61);
  let tail=poly([[s*.4,6.7],[s*5.8,9.2],[s*6.1,10.2],[s*.5,9.3]]);tail.rotation.x=Math.PI/2;tail.position.y=4.25;
  let eng=mesh(new T.CylinderGeometry(1.03,1.13,3.8,18,1,true),'#1A344F',plane);eng.rotation.x=Math.PI/2;eng.position.set(s*6,1.9,-.4);
  let cap=mesh(new T.CircleGeometry(.9,20),ink,plane,false);cap.position.set(s*6,1.9,1.52);let hub=mesh(new T.CircleGeometry(.28,12),'#0CE7ED',plane,false);hub.position.set(s*6,1.9,1.54);
  for(let k=0;k<8;k++){let a=k*Math.PI/4;line([[s*6+.3*Math.cos(a),1.9+.3*Math.sin(a),1.56],[s*6+.78*Math.cos(a+.3),1.9+.78*Math.sin(a+.3),1.56]],'#69F3F9',.9,plane,.7);}

  // Turbofan exhaust ring, intake lip, acoustic bands and central spinner.
  const intake=mesh(new T.RingGeometry(.67,1.05,24),'#9DECF5',plane,false);
  intake.position.set(s*6,1.9,-2.34);
  const inletCore=mesh(new T.CircleGeometry(.64,20),'#071423',plane,false);
  inletCore.position.set(s*6,1.9,-2.338);
  for(let k=0;k<12;k++){
   const a=k*Math.PI/6;
   line([[s*6+.16*Math.cos(a),1.9+.16*Math.sin(a),-2.345],[s*6+.58*Math.cos(a+.21),1.9+.58*Math.sin(a+.21),-2.345]],'#63BBCB',.93,plane,.65);
  }
  for(const z of [-1.45,.52]){
   line(Array.from({length:25},(_,i)=>{const a=i*Math.PI/12;return[s*6+1.13*Math.cos(a),1.9+1.13*Math.sin(a),z]}),'#4A9CB8',.82,plane,.55);
  }
  let exhaust=mesh(new T.RingGeometry(.77,1.07,24),'#D4F9FC',plane,false);
  exhaust.position.set(s*6,1.9,1.575);
  box(s*5.7,2.8,-1,.45,1.5,1.3,surface,plane);
 }
 let fin=new T.Shape();[[6,4.5],[7,9.4],[9.5,11.4],[10.4,11.4],[10.1,4.3]].forEach(([z,y],i)=>i?fin.lineTo(z,y):fin.moveTo(z,y));fin.closePath();let f=mesh(new T.ExtrudeGeometry(fin,{depth:.2,bevelEnabled:false}),surface,plane);f.rotation.y=-Math.PI/2;f.position.x=.1;
 let apu=mesh(new T.CircleGeometry(.33,24),ink,plane,false);apu.position.set(0,4.35,10.58);
 let rim=mesh(new T.RingGeometry(.34,.44,24),'#51F6F9',plane,false);rim.position.set(0,4.35,10.59);
 let capFin=new T.Shape();
 // Additional rudder hinge, fin panel and tail marker detailing.
 line([[.15,4.65,8.5],[.15,9.1,9.38]],'#7ECAE2',.85,plane,.9);
 line([[-.16,5.1,9.62],[-.16,8.4,9.85]],'#397EAC',.78,plane,.9);
 let tailBeacon=mesh(new T.SphereGeometry(.19,8,6),'#B9F8FF',plane,false);
 tailBeacon.position.set(0,11.35,9.95);
[[7.1,8.8],[9.5,11.4],[10.4,11.4],[10.25,8.8]].forEach(([z,y],i)=>i?capFin.lineTo(z,y):capFin.moveTo(z,y));capFin.closePath();let cf=mesh(new T.ExtrudeGeometry(capFin,{depth:.22,bevelEnabled:false}),'#17668F',plane);cf.rotation.y=-Math.PI/2;cf.position.x=.11;
 // Stylized tail emblem drawn on both fin faces, echoing the reference livery.
 for(let side of [-1,1]){
  line([[side*.125,5.4,9.4],[side*.125,5.9,8.7],[side*.125,6.7,8.1],[side*.125,7.2,8.5],[side*.125,6.6,8.8],[side*.125,6.0,9.4]],'#17668F',1,plane,2.2);
  for(let k=0;k<4;k++)line([[side*.13,6.5+k*.16,8.45],[side*.13,6.7+k*.16,9.35]],'#17668F',1,plane,1.4);
 }
 const gear=new T.Group();plane.add(gear);for(let z of [-6,6.5])for(let s of [-1,1]){let x=z<0?s*.45:s*4.3;box(x,1.1,z,.12,1.6,.15,ink,gear);for(let off of [-.24,.24]){let wh=mesh(new T.CylinderGeometry(.62,.62,.36,16),ink,gear,false);wh.rotation.z=Math.PI/2;wh.position.set(x+off,.52,z);}}

 // Hydraulic strut braces, bogie crossbar, disc hubs and tire outlines.
 for(const z of [-6,6.5])for(const side of [-1,1]){
  const x=z<0?side*.45:side*4.3;
  line([[x,.78,z-.3],[x+side*.34,1.5,z+.16]],'#8DD9EC',.95,gear,1.2);
  box(x,.72,z,.8,.12,.18,'#4FADC0',gear);
  for(const off of [-.24,.24]){
   const disc=mesh(new T.CircleGeometry(.26,12),'#ADD8E1',gear,false);
   disc.rotation.y=side*Math.PI/2;disc.position.set(x+off+side*.2,.52,z);
   line([[x+off,.52,z-.23],[x+off,.52,z+.23]],'#C0EBF2',.75,gear,.65);
  }
 }
 for(let s of [-1,1])for(let z=-8;z<4;z+=.68)line([[s*1.94,4.2,z-.15],[s*2.02,4.43,z-.15],[s*2.02,4.43,z+.12],[s*1.94,4.2,z+.12]],ink,.9,plane,.85);
 for(let x of [-18,18])line([[x,.02,150],[x,.02,-650]],'#1E718B',1,scene,1.5);

 // Parked narrow-body aircraft on apron stands. These are separate static 3D meshes
 // in the same airport world (not overlays), so perspective naturally changes.
 function createParkedAirliner({x,z,heading=0,scale=1,accent='#2493B9'}){
  const parked=new T.Group();parked.position.set(x,.05,z);
  parked.rotation.y=heading;parked.scale.setScalar(scale);scene.add(parked);
  const fuselage=mesh(new T.CylinderGeometry(.92,.92,13.7,14), '#23394D',parked,false);
  fuselage.rotation.x=Math.PI/2;fuselage.position.y=2.85;
  const nose=mesh(new T.ConeGeometry(.92,2.5,14),'#345875',parked,false);
  nose.rotation.x=-Math.PI/2;nose.position.set(0,2.85,-7.95);
  const tailCone=mesh(new T.ConeGeometry(.92,1.6,14),'#19374D',parked,false);
  tailCone.rotation.x=Math.PI/2;tailCone.position.set(0,2.85,7.65);
  for(const s of [-1,1]){
   const wingShape=poly([[s*.72,-2.1],[s*3,-1.7],[s*9.2,2.9],[s*9.5,3.8],[s*4.7,2.9],[s*.7,1.5]],'#24475F',parked);
   wingShape.rotation.x=Math.PI/2;wingShape.position.y=2.67;
   const stabilizer=poly([[s*.46,5.4],[s*3.45,6.48],[s*3.72,7.23],[s*.46,6.75]],'#24455C',parked);
   stabilizer.rotation.x=Math.PI/2;stabilizer.position.y=3.18;
   // Single engine per wing, with visible intakes and pylons.
   const nacelle=mesh(new T.CylinderGeometry(.46,.52,2.35,12), '#244B62',parked,false);
   nacelle.rotation.x=Math.PI/2;nacelle.position.set(s*3.6,1.84,-.35);
   box(s*3.6,2.32,-.4,.2,.95,.85,'#346981',parked);
   const intakeRing=mesh(new T.RingGeometry(.3,.5,16),'#A7F2F7',parked,false);
   intakeRing.position.set(s*3.6,1.84,-1.54);
   for(let wz=-5.5;wz<=5.0;wz+=1.12){
    line([[s*1.005,3.12,wz-.19],[s*1.005,3.3,wz-.19],[s*1.005,3.3,wz+.12]],'#80D5E8',.85,parked,.5);
   }
   for(const dz of [-6.2,3.9])line([[s*1.06,2.58,dz-.35],[s*1.06,3.5,dz-.35],[s*1.06,3.5,dz+.35],[s*1.06,2.58,dz+.35]],'#78BBD5',.75,parked,.65);
   // Wheel bogies visible beneath stationary airplane.
   box(s*2.55,.95,1.55,.18,1.5,.18,'#3A889F',parked);
   for(const shift of [-.37,.37]){
    const tire=mesh(new T.CylinderGeometry(.36,.36,.32,10),'#0B1827',parked,false);
    tire.rotation.z=Math.PI/2;tire.position.set(s*2.55+shift,.39,1.55);
   }
  }
  const fin=new T.Shape();
  [[4.4,3.4],[5.4,6.8],[7.1,8.6],[7.65,8.6],[7.15,3.35]].forEach(([zz,y],i)=>i?fin.lineTo(zz,y):fin.moveTo(zz,y));
  fin.closePath();
  const tail=mesh(new T.ExtrudeGeometry(fin,{depth:.14,bevelEnabled:false}),accent,parked);
  tail.rotation.y=-Math.PI/2;tail.position.x=.07;
  line([[.13,4.4,6.55],[.13,7.8,7.06]],'#C7F8FC',.7,parked,.7);
  const cockpit=mesh(new T.BoxGeometry(.95,.38,.6),'#0A2035',parked,false);
  cockpit.position.set(0,3.29,-6.25);
  box(0,.8,-5.55,.1,1.1,.1,'#5F9FB2',parked);
  line([[-.9,2.9,-5.6],[.9,2.9,-5.6]],accent,.8,parked,.8);
  return parked;
 }
 // Arranged away from the runway (-18..18) at terminal and remote parking stands.
 createParkedAirliner({x:-27,z:-105,heading:1.13,scale:1.0,accent:'#1B8CB3'});
 createParkedAirliner({x:28,z:-132,heading:-1.12,scale:1.02,accent:'#2D6C96'});
 createParkedAirliner({x:-28,z:-179,heading:1.24,scale:.92,accent:'#247CA0'});
 createParkedAirliner({x:29,z:-215,heading:-1.24,scale:.95,accent:'#1C819B'});
 // Taxiway edge guide lines, parking stand lead-ins and stop bars.
 for(const side of [-1,1]){
  line([[side*25,.038,70],[side*25,.038,-245]],'#17728C',.78,scene,.8);
  for(const z of [-105,-132,-179,-215]){
   const edge=side*21,stop=side*31;
   line([[edge,.048,z-5],[stop,.048,z-5],[stop,.048,z+6]],'#2C839D',.78,scene,.8);
   line([[stop-side*2,.05,z-3],[stop+side*2,.05,z-3]],'#B7EEF6',.75,scene,.7);
  }
 }
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
