import * as THREE from 'three';
import {SVGRenderer} from 'three/addons/renderers/SVGRenderer.js';

// All geometry is authored in real 3D space and rendered from a fixed isometric
// orthographic camera; there is no generated image or fake logo in this film.
export function createFilm(){
  const scene=new THREE.Scene();
  scene.background=new THREE.Color('#0C1827');
  const camera=new THREE.OrthographicCamera(-6.35,6.35,11.30,-11.30,0.1,100);
  camera.position.set(19,20,24);
  const renderer=new SVGRenderer();
  renderer.setSize(720,1280);
  renderer.setQuality('high');
  renderer.setClearColor('#0C1827');
  renderer.overdraw=0.5;

  const navy='#10273C', cyan='#31D6D4', light='#DFF7FC',
        white='#ECF7F8', orange='#FDAD67', red='#F07172';
  const mat=(color,extra={})=>new THREE.MeshBasicMaterial({color,side:THREE.DoubleSide,...extra});
  const colorShift=(value,mult)=>new THREE.Color(value).multiplyScalar(mult);
  const edgeMat=new THREE.LineBasicMaterial({color:'#62D4DF',transparent:true,opacity:0.33});
  function addMesh(geometry,color,parent=scene){
    const result=new THREE.Mesh(geometry,typeof color==='string'?mat(color):color);
    parent.add(result);return result;
  }
  function box(parent,x,y,z,w,h,d,color,edge=false){
    const colors=[1.00,.74,1.13,.67,.95,.85].map(s=>mat(colorShift(color,s)));
    const mesh=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),colors);
    mesh.position.set(x,y,z);parent.add(mesh);
    if(edge){
      const lines=new THREE.LineSegments(new THREE.EdgesGeometry(mesh.geometry),edgeMat);
      mesh.add(lines);
    }
    return mesh;
  }
  function sph(parent,x,y,z,r,color,segments=16){
    const mesh=addMesh(new THREE.SphereGeometry(r,segments,12),color,parent);
    mesh.position.set(x,y,z);return mesh;
  }
  function cyl(parent,x,y,z,rTop,rBottom,h,color,segments=14){
    const mesh=addMesh(new THREE.CylinderGeometry(rTop,rBottom,h,segments),color,parent);
    mesh.position.set(x,y,z);return mesh;
  }
  function disc(parent,x,y,z,rx,rz,color,opacity=.2){
    const mesh=addMesh(new THREE.CircleGeometry(1,32),mat(color,{transparent:true,opacity}),parent);
    mesh.rotation.x=-Math.PI/2;
    mesh.scale.set(rx,rz,1);
    mesh.position.set(x,y,z);return mesh;
  }
  function limb(parent,ax,ay,az,bx,by,bz,r,color){
    const a=new THREE.Vector3(ax,ay,az),b=new THREE.Vector3(bx,by,bz);
    const part=addMesh(new THREE.CylinderGeometry(r,r,b.distanceTo(a),12),color,parent);
    part.position.copy(a).add(b).multiplyScalar(.5);
    part.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),b.clone().sub(a).normalize());
    return part;
  }

  // Compact floating city block with three-dimensional, bevel-free isometric styling.
  box(scene,0,-.88,0,17.0,1.25,12.5,'#07121F',true);
  box(scene,0,-.18,0,16.35,.22,11.85,'#16354B',true);
  box(scene,0,-.045,0,14.85,.07,10.5,'#213C4E');
  for(const x of [-6.1,-3.05,0,3.05,6.1]){
    box(scene,x,.008,-4.55,.055,.025,1.4,'#4E7182');
  }
  for(let x=-5.75;x<6;x+=1.45){
    box(scene,x,.008,4.60,.55,.023,.085,'#47717B');
  }
  for(const [x,z,w,h,c] of [
    [-6.7,-6.2,2.8,5.6,'#285A71'],
    [-3.5,-7.2,2.1,6.7,'#1B435D'],
    [4.5,-7.1,3.0,4.5,'#234D69'],
    [7.0,-5.5,1.9,6.3,'#214056']
  ]){
    box(scene,x,h/2-.13,z,w,h,2.2,c);
    box(scene,x,h-.11,z,w+.1,.13,2.35,'#38829B');
    for(let j=1;j<4;j++)for(const side of [-1,1]){
      const wy=0.55+j*1.06;
      if(wy<h-.35) box(scene,x+side*(w*.22),wy,z+1.135,w*.20,.44,.04,'#7DD5E1');
    }
  }
  function pine(x,z,s){
    const tree=new THREE.Group();tree.position.set(x,0,z);tree.scale.setScalar(s);scene.add(tree);
    cyl(tree,0,.45,0,.17,.19,.9,'#6D554A');
    for(let i=0;i<3;i++){
      const crown=addMesh(new THREE.ConeGeometry(1.05-i*.19,1.6,7),'#166D73',tree);
      crown.position.y=1.12+i*.62;
    }
    sph(tree,0,2.93,0,.14,'#84DFDB',9);
  }
  pine(-6.25,-1.8,.93); pine(6.2,-2.3,.82);
  pine(-6.8,3.0,.75); pine(6.35,3.1,.90);
  for(let i=0;i<10;i++){
    const x=(i%5-2)*2.6, z=i<5?-3.4:3.9;
    disc(scene,x,.034,z,.38,.18,'#51B1C1',.07);
  }

  function makePerson(color,skin,pants,hair,x,z,skirt=false){
    const root=new THREE.Group();root.position.set(x,0,z);scene.add(root);
    const bob=new THREE.Group();root.add(bob);
    disc(root,0,.043,0,.83,.53,'#030B13',.45);
    for(const side of [-1,1]){
      const leg=cyl(bob,side*.33,.95,0,.22,.24,1.64,pants);
      leg.rotation.z=side*.055;
      box(bob,side*.33,.20,.31,.56,.26,.87,'#132638');
    }
    const body=cyl(bob,0,2.65,0,.66,skirt?.90:.75,1.85,color);
    box(bob,0,3.22,.50,.73,.15,.12,'#94CFD7');
    // Thick collar, neck, head, hair silhouette and readable facial features.
    cyl(bob,0,3.69,0,.26,.27,.48,skin);
    sph(bob,0,4.34,0,.78,skin,20);
    sph(bob,0,4.65,-.22,.79,hair,18);
    const fringe=addMesh(new THREE.SphereGeometry(.795,18,12,0,Math.PI*2,0,Math.PI/2),hair,bob);
    fringe.position.set(0,4.54,.02);
    for(const px of [-.245,.245]){
      sph(bob,px,4.34,.718,.071,'#162437',10);
      sph(bob,px+.018,4.36,.772,.020,white,8);
    }
    sph(bob,0,4.05,.753,.062,'#B56869',10);
    const left=new THREE.Group(),right=new THREE.Group();
    left.position.set(-.78,3.24,.08);
    right.position.set(.78,3.24,.08);
    bob.add(left,right);
    function arm(g,side){
      const sleeve=cyl(g,0,-.57,0,.235,.20,1.22,color);
      sleeve.rotation.z=side*.035;
      sph(g,0,-1.19,0,.22,skin);
    }
    arm(left,-1);arm(right,1);
    return {root,bob,left,right};
  }
  const girl=makePerson('#F4777C','#EFC1A4','#1B314B','#172B39',-2.45,.45,true);
  const friend=makePerson('#2CC5CB','#DDAF91','#243752','#152A3D',2.45,-.35);
  const parcel=new THREE.Group();
  girl.bob.add(parcel);
  parcel.position.set(.80,2.38,.95);
  box(parcel,0,0,0,1.22,1.0,1.03,'#E6A56E',true);
  box(parcel,0,.515,0,1.24,.10,1.08,'#F8C58E');
  box(parcel,0,.013,.532,.22,.96,.032,'#F8D9A3');
  box(parcel,0,.53,0,.22,.022,1.1,'#F4D39B');
  box(parcel,.325,.06,.535,.28,.23,.035,'#FAF1D9');

  const tinyPhone=new THREE.Group();
  friend.bob.add(tinyPhone);
  tinyPhone.position.set(-.89,2.3,.88);
  tinyPhone.rotation.y=-.18;
  box(tinyPhone,0,0,0,.81,1.48,.15,'#101A2A');
  box(tinyPhone,0,.02,.088,.68,1.28,.02,'#F3FBFA');
  box(tinyPhone,0,.42,.115,.54,.14,.015,'#20BBC6');
  for(const y of [.15,-.07,-.29]){
    box(tinyPhone,-.07,y,.114,.4,.08,.01,'#AEC5CD');
  }
  // The physically modeled phone gives the close-up its 3D isometric context.
  const appPhone=new THREE.Group();scene.add(appPhone);
  appPhone.position.set(0,3.25,1.48);
  appPhone.rotation.y=-.13;appPhone.rotation.x=-.06;
  box(appPhone,0,0,-.04,4.15,7.24,.33,'#070F1B',true);
  box(appPhone,0,0,.135,3.82,6.86,.035,'#E9F4F6');
  box(appPhone,0,2.95,.17,3.77,.62,.044,'#19B8C7');
  box(appPhone,0,3.42,.17,.72,.09,.058,'#263E53');
  for(const [y,w] of [[1.85,3.24],[.86,3.25],[-.15,3.25],[-1.15,3.22]]){
    box(appPhone,0,y,.178,w,.67,.026,'#D7E6E9');
    box(appPhone,.22,y+.14,.196,w*.58,.085,.027,'#7EA9B4');
  }
  box(appPhone,0,-2.66,.185,3.24,.54,.028,'#11B4BC');

  // Decorative airport-flight dotted route, visible as real 3D meshes.
  const route=new THREE.Group();scene.add(route);
  route.position.set(0,.06,3.6);
  for(let i=0;i<13;i++){
    const a=i/12;
    const marker=sph(route,-4.6+a*9.2,.12+Math.sin(a*Math.PI)*1.5,-.15+.18*Math.sin(a*3),.085,cyan,8);
    marker.scale.setScalar(.7+.3*Math.sin(a*Math.PI));
  }
  const routeStart=sph(route,-4.8,.14,-.15,.23,orange,12);
  const routeEnd=sph(route,4.75,.14,-.15,.23,cyan,12);

  const ease=v=>{const x=Math.max(0,Math.min(1,v));return x*x*(3-2*x);};
  function update(t){
    const phase=t<4?0:t<7?1:t<11?2:3;
    girl.bob.position.y=.035*Math.sin(t*3.8);
    friend.bob.position.y=.035*Math.sin(t*3.8+1.4);
    girl.bob.rotation.y=phase===1?-.17:phase===2?-.10:.02;
    friend.bob.rotation.y=phase===1?-.22:.03;
    girl.left.rotation.z=phase===0?-.32+Math.sin(t*2.2)*.16:phase===3?-.65:-.12;
    girl.right.rotation.z=phase===0?-.16+Math.sin(t*2.6)*.08:phase===3?-.8:-.12;
    friend.left.rotation.z=phase===1?-.9+Math.sin(t*3)*.05:phase===3?-.72:-.12;
    friend.right.rotation.z=phase===3?.65:.10;
    parcel.visible=(phase!==2);
    tinyPhone.visible=(phase===1);
    route.visible=(phase===2||phase===3);
    appPhone.visible=(phase===2||phase===3);
    if(phase===2){
      appPhone.position.set(0,3.45,2.2);
      appPhone.scale.setScalar(.99+ease((t-7)/.8)*.07);
      girl.root.position.x=-2.45;
      friend.root.position.x=2.45;
    }else if(phase===3){
      appPhone.position.set(4.0,2.90,-.15);
      appPhone.scale.setScalar(.61);
      girl.root.position.x=-2.25;
      friend.root.position.x=1.15;
      girl.bob.rotation.z=-.025*Math.sin(t*5);
    }else{
      girl.root.position.x=-2.45;
      friend.root.position.x=2.45;
    }
    // Gentle camera moves; isometric composition never becomes perspective.
    const turn=phase===2?ease((t-7)/1.5):phase===3?ease((t-11)/1.1):0;
    const cx=phase===2?0:phase===3?.1:0;
    const lookY=phase===2?2.75:2.1;
    camera.position.set(19-turn*.9,20+turn*.5,24-turn*.6);
    camera.lookAt(cx,lookY,phase===2?.3:0);
    camera.zoom=phase===2?1.05:phase===3?1.03:1;
    camera.updateProjectionMatrix();
    camera.updateMatrixWorld();
    scene.updateMatrixWorld(true);
    renderer.render(scene,camera);
  }
  update(0);
  return {scene,camera,renderer,update};
}
