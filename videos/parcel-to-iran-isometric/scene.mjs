import * as T from 'three';
import {SVGRenderer} from 'three/addons/renderers/SVGRenderer.js';

// Advertio / bright architectural miniature: real Three.js 3D and isometric camera.
// Reference mood: porcelain-white city blocks, powder-blue windows, pastel transit,
// tiny vivid pedestrians, understated warm daylight. No logo is fabricated.
export function createFilm(){
 const scene=new T.Scene();
 scene.background=new T.Color('#F0F1EF');
 const camera=new T.OrthographicCamera(-8,8,14.23,-14.23,.1,160);
 const renderer=new SVGRenderer();
 renderer.setSize(720,1280);
 renderer.setClearColor('#F0F1EF');
 renderer.overdraw=.2;
 const C={ground:'#E7E9E7',road:'#D9DDDE',walk:'#F8F8F5',white:'#F8F9F6',stone:'#EEF1F0',shadow:'#C7CFD0',win:'#BED7DB',glass:'#C9E1E2',yellow:'#F6BF4D',pink:'#EB7997',coral:'#F27B74',teal:'#31B7AD',blue:'#4B9DBB',ink:'#24394C',orange:'#EAA34E'};
 const mats=new Map();
 const mat=c=>{if(!mats.has(c))mats.set(c,new T.MeshBasicMaterial({color:c,side:T.DoubleSide}));return mats.get(c);};
 const mesh=(p,g,c)=>{const o=new T.Mesh(g,mat(c));p.add(o);return o};
 // Cache soft, directional porcelain shading; camera sees +X and +Z facets.
 const boxColors=new Map();
 function box(p,x,y,z,w,h,d,c){
  let colors=boxColors.get(c);
  if(!colors){
   const base=new T.Color(c);
   colors=[.90,.97,1.04,.84,.93,.98].map(k=>mat('#'+base.clone().multiplyScalar(k).getHexString()));
   boxColors.set(c,colors);
  }
  const o=new T.Mesh(new T.BoxGeometry(w,h,d),colors);
  o.position.set(x,y,z);p.add(o);return o;
 }
 function sphere(p,x,y,z,r,c,n=10){const o=mesh(p,new T.SphereGeometry(r,n,7),c);o.position.set(x,y,z);return o;}
 function cyl(p,x,y,z,r1,r2,h,c,n=10){const o=mesh(p,new T.CylinderGeometry(r1,r2,h,n),c);o.position.set(x,y,z);return o;}
 function rod(p,a,b,r,c){const v=new T.Vector3(...a),w=new T.Vector3(...b),o=mesh(p,new T.CylinderGeometry(r,r,v.distanceTo(w),7),c);o.position.copy(v).add(w).multiplyScalar(.5);o.quaternion.setFromUnitVectors(new T.Vector3(0,1,0),w.sub(v).normalize());return o;}
 function shadow(p,x,y,z,sx,sz,a=.15){const o=new T.Mesh(new T.CircleGeometry(1,18),new T.MeshBasicMaterial({color:'#B7BDBD',transparent:true,opacity:a,depthWrite:false,side:T.DoubleSide}));o.rotation.x=-Math.PI/2;o.scale.set(sx,sz,1);o.position.set(x,y,z);p.add(o);}

 // Pale city floor and intersecting streets, modeled without outline/HUD styling.
 box(scene,0,-.18,0,43,.30,43,C.ground);
 for(const [x,z] of [[-10,-10],[10,-10],[-10,10],[10,10]])box(scene,x,-.005,z,15,.14,15,C.walk);
 box(scene,0,-.035,0,43,.045,5.7,C.road);
 box(scene,0,-.028,0,5.7,.052,43,C.road);
 for(const s of [-1,1]){
  box(scene,s*3.15,.045,0,.16,.10,39,'#F2F2EF');
  box(scene,0,.041,s*3.15,39,.11,.16,'#F2F2EF');
 }
 for(let k=-3;k<=3;k++){
  box(scene,k*.70,.05,0,.42,.018,4.90,'#F8F9F8');
  box(scene,0,.053,k*.70,4.90,.015,.42,'#F8F9F8');
 }
 for(let z=-20;z<20;z+=4.7)if(Math.abs(z)>4)box(scene,0,.04,z,.08,.013,2.10,'#F5F6F4');
 for(let x=-20;x<20;x+=4.7)if(Math.abs(x)>4)box(scene,x,.041,0,2.20,.013,.08,'#F6F7F4');

 function roofMachine(p,dx,dz,y){
  box(p,dx,y+.15,dz,1.6,.25,1.6,'#E4E8E6');
  cyl(p,dx,y+.42,dz,.56,.56,.38,'#D4DCDA',12);
  cyl(p,dx,y+.65,dz,.42,.42,.09,'#EDF1EF',12);
  for(let i=0;i<5;i++){const a=i*Math.PI*2/5;box(p,dx+Math.cos(a)*.24,y+.70,dz+Math.sin(a)*.24,.09,.045,.55,'#DCE4E2');}
 }
 function building(x,z,w,d,floors,opt={}){
  const root=new T.Group();root.position.set(x,.02,z);scene.add(root);
  const h=floors*1.25+.75;
  box(root,.12,.16,.10,w+.45,.30,d+.48,'#E4E8E6');
  shadow(root,.18,.34,.20,w*.65,d*.60,.11);
  box(root,0,h/2+.30,0,w,h,d,C.white);
  box(root,0,h+.37,0,w+.15,.25,d+.15,'#FBFBF8');
  box(root,0,h+.53,0,w+.48,.13,d+.48,'#E4E8E6');
  for(let j=0;j<floors;j++){
   const wy=.90+j*1.27;
   // Only render the camera-visible +Z and +X facades. The occluded rear
   // windows previously tripled SVG triangles without improving the picture.
   const n=Math.max(2,Math.floor(w/2.1));
   for(let k=0;k<n;k++){
    const xx=-w/2+(k+.5)*w/n;
    box(root,xx,wy,d/2+.025,.52,.68,.05,C.win);
    box(root,xx,wy-.36,d/2+.14,.71,.08,.20,'#FCFCFA');
   }
   const nz=Math.max(2,Math.floor(d/2.15));
   for(let k=0;k<nz;k++){
    const zz=-d/2+(k+.5)*d/nz;
    box(root,w/2+.03,wy,zz,.05,.67,.53,'#BDD5D8');
    box(root,w/2+.14,wy-.36,zz,.20,.08,.70,'#FCFCFA');
   }
  }
  if(floors>2)roofMachine(root,w*.12,-d*.12,h+.6);
  if(opt.store){
   const fascia=opt.store==='yellow'?C.yellow:opt.store==='pink'?C.pink:C.teal;
   box(root,0,.78,d/2+.09,w-.43,1.25,.12,C.glass);
   box(root,0,1.52,d/2+.30,w-.20,.34,.76,fascia);
   box(root,0,1.22,d/2+.65,w-.36,.11,.17,'#F9F8F5');
   box(root,0,.79,d/2+.25,.17,1.25,.12,'#F7F8F5');
  }
  return root;
 }
 const buildings=[
  [-16,-16,5.8,5.8,6],[-9.2,-15,5.4,5.1,4],[9.8,-16,5.4,5.7,5],[16.1,-15,5,5.6,6],
  [-16,-8.8,5.5,5.4,4],[-9.3,-9.1,5.7,5.6,3],[9.2,-9.3,5.8,5.1,2],[16,-8.3,5.5,6,4],
  [-16,9.2,5.5,5.3,4],[-9.2,9.3,5.8,5.6,3],[9.2,9.3,6.2,5.2,4],[16,8.4,5.6,5.8,6],
  [-16,16,5.9,5.6,5],[-9,16,5.6,6,5],[9.2,16,5.8,5.6,4],[16.2,16,5.7,6.1,5]
 ];
 for(const [x,z,w,d,f] of buildings){
  const store=(x===-9.3&&z===-9.1)?'yellow':(x===9.2&&z===-9.3)?'pink':null;
  building(x,z,w,d,f,{store});
 }
 function lamp(x,z,h=2.6){
  const p=new T.Group();p.position.set(x,.1,z);scene.add(p);
  rod(p,[0,0,0],[0,h,0],.065,'#F8F8F5');
  rod(p,[0,h,0],[.72,h,0],.065,'#FCFCF8');
  box(p,.78,h-.12,0,.43,.18,.24,'#FDFDF9');
 }
 for(const [x,z] of [[-3.3,-10],[3.3,-10],[-3.3,9.8],[3.3,9.8],[-10,-3.3],[9,-3.3],[-10,3.3],[9,3.3]])lamp(x,z);
 function tree(x,z,s=1){
  const p=new T.Group();p.position.set(x,0,z);p.scale.setScalar(s);scene.add(p);
  rod(p,[0,0,0],[0,1.1,0],.16,'#D4D5D0');
  for(const [dx,dy,dz,r] of [[0,1.75,0,.82],[-.45,1.6,.1,.62],[.43,1.85,-.1,.59],[0,2.24,.09,.56]])sphere(p,dx,dy,dz,r,'#F4F5F2',10);
 }
 for(const [x,z,s] of [[-6,-5.5,.75],[6.2,-5.1,.68],[-5.8,5.5,.68],[5.9,6.3,.88],[-13,-5.8,.70],[13.1,6.2,.65]])tree(x,z,s);

 const traffic=[];
 function car(x,z,c,axis=0,scale=1){
  const p=new T.Group();p.position.set(x,.25,z);p.scale.setScalar(scale);scene.add(p);
  const q=new T.Group();p.add(q);if(axis)q.rotation.y=Math.PI/2;
  box(q,0,.34,0,1.18,.54,2.05,c);
  box(q,0,.72,-.17,1.02,.52,1.12,'#2E4654');
  box(q,0,.99,-.13,1,.06,1.13,c);
  for(const s of [-1,1])for(const zz of [-.68,.67]){const wh=cyl(q,s*.68,.27,zz,.23,.23,.17,'#34444C',9);wh.rotation.z=Math.PI/2;}
  box(q,0,.41,-1.06,.64,.12,.065,'#F5F5E8');
  box(q,0,.41,1.06,.67,.13,.065,'#DD7C7C');
  traffic.push({p,axis,x,z});
 }
 car(-1.35,-14,C.pink,0,.94);car(1.2,-12.5,C.yellow,0,1.05);
 car(-1.3,12,C.blue,0,.92);car(1.32,11.2,'#E9A765',0,.87);
 car(-14,-1.35,'#72B6D6',1,1.05);car(11.2,1.31,C.yellow,1,.89);
 car(16,-1.34,'#FC8C95',1,.84);car(-10,1.3,'#FFFFFF',1,.91);
 function bus(x,z){
  const p=new T.Group();p.position.set(x,.3,z);p.rotation.y=Math.PI/2;scene.add(p);
  box(p,0,.70,0,1.45,1.32,4.7,C.pink);
  box(p,0,1.10,0,1.35,.48,4.62,'#F3A9B4');
  box(p,0,1.52,0,1.33,.12,4.68,'#F6C7C9');
  for(let zz=-1.85;zz<1.75;zz+=.87){box(p,.755,1.05,zz,.045,.44,.60,'#304755');box(p,-.755,1.05,zz,.045,.44,.60,'#304755');}
  for(const zz of [-1.55,1.55])for(const s of [-1,1]){const o=cyl(p,s*.79,.3,zz,.36,.36,.16,'#34444B',10);o.rotation.z=Math.PI/2;}
  traffic.push({p,axis:1,x,z});
 }
 bus(-9,-1.32);

 function pedestrian(x,z,shirt,scale=.68,skin='#D7AF92'){
  const p=new T.Group();p.position.set(x,.09,z);p.scale.setScalar(scale);scene.add(p);
  const body=new T.Group();p.add(body);shadow(p,0,-.01,0,.45,.30,.11);
  for(const s of [-1,1]){rod(body,[s*.16,.85,0],[s*.16,.13,.07],.105,'#5E6974');box(body,s*.17,.13,.17,.34,.18,.41,'#4D5C66');}
  cyl(body,0,1.40,0,.37,.40,.95,shirt,9);
  sphere(body,0,2.17,0,.37,skin,10);
  sphere(body,0,2.40,-.05,.36,'#79584F',10);
  for(const s of [-1,1])rod(body,[s*.37,1.68,0],[s*.51,1.13,.05],.14,shirt);
  return {p,body};
 }
 for(const [x,z,c] of [
  [-2.7,-5.9,C.orange],[2.8,-8.4,C.teal],[-3,6,C.pink],[3,6.9,'#D99D38'],
  [-7.5,-3.3,'#6D9FB7'],[7.7,3.3,C.teal],[-15,1.9,'#E9865A'],[14,-3.4,'#E3A33E'],
  [-12,4.6,C.teal],[12.5,4.1,'#EC9B75'],[6.9,-10.8,'#4F95C7']
 ])pedestrian(x,z,c,.53);
 const girl=pedestrian(-1.12,1.05,'#EB7892',1.28,'#F1BEA6');
 const friend=pedestrian(1.36,.8,'#28B3B0',1.25,'#DFB18E');
 const parcel=new T.Group();girl.body.add(parcel);parcel.position.set(.55,1.45,.57);
 box(parcel,0,0,0,.76,.65,.67,'#D8A16C');
 box(parcel,0,.335,0,.78,.052,.70,'#EAC794');
 box(parcel,0,0,.354,.15,.67,.042,'#F6D9A7');
 box(parcel,0,.37,0,.15,.024,.74,'#F8DEB0');
 const handheld=new T.Group();friend.body.add(handheld);handheld.position.set(-.48,1.53,.55);
 box(handheld,0,.10,0,.43,.82,.13,'#3C5164');
 box(handheld,0,.1,.08,.36,.71,.04,'#F3F8F5');
 box(handheld,0,.37,.11,.31,.14,.015,C.teal);
 for(const y of [.15,-.05])box(handheld,0,y,.11,.22,.08,.014,'#B2CCCF');

 const app=new T.Group();scene.add(app);app.rotation.x=-.08;
 box(app,0,0,0,3.8,6.8,.30,'#26394A');
 box(app,0,0,.17,3.54,6.46,.055,'#FBFBF8');
 box(app,0,2.83,.215,3.49,.66,.06,'#60BEC3');
 box(app,0,3.20,.22,.55,.10,.065,'#FBF9F4');
 for(const y of [1.8,.88,-.04,-.97]){
  box(app,0,y,.223,3.10,.67,.035,'#E7EFF0');
  box(app,.27,y+.10,.253,1.72,.06,.023,'#A7C6CB');
  box(app,-1.1,y,.252,.5,.43,.026,'#B6D7D5');
 }
 box(app,0,-2.63,.24,3.10,.55,.04,C.teal);
 const smooth=x=>{x=Math.max(0,Math.min(1,x));return x*x*(3-2*x)};
 function update(t){
  const phase=t<4?0:t<7?1:t<11?2:3,sway=Math.sin(t*2.5);
  girl.body.position.y=.018*sway;friend.body.position.y=.016*Math.sin(t*2.5+1.3);
  girl.body.rotation.y=phase===1?-.18:0;friend.body.rotation.y=phase===1?-.27:0;
  girl.body.rotation.z=phase===3?-.075*sway:0;
  parcel.visible=phase!==2;handheld.visible=phase===1;app.visible=phase>=2;
  app.position.set(phase===2?0:5.2,phase===2?3.4:3.1,3.8);
  app.scale.setScalar(phase===2?1.0:.66);
  for(let i=0;i<traffic.length;i++){
   const v=traffic[i],speed=(i%3+1)*.13;
   if(v.axis===0)v.p.position.z=v.z+(t-7.5)*speed*(i%2?1:-1);
   else v.p.position.x=v.x+(t-7.5)*speed*(i%2?1:-1);
  }
  camera.position.set(24+Math.sin(t*.15)*.9,29,33+Math.sin(t*.1)*.9);
  camera.lookAt(0,1.05,phase===2?1.15:0);
  camera.zoom=phase===2?1.04:1;
  camera.updateProjectionMatrix();camera.updateMatrixWorld();
  scene.updateMatrixWorld(true);renderer.render(scene,camera);
 }
 update(0);return{scene,camera,renderer,update};
}
