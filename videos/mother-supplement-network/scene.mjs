import * as T from 'three';

// Original isometric geometry based on the supplied minimal orange connection-graph
// art direction. No third-party image or AI-generated brand mark is embedded.
export function createFilm(){
  const scene=new T.Scene();
  const BG='#F7F7F5', ORANGE='#F36B2C', ORANGE_LIGHT='#FF9558';
  const BLACK='#222326', WHITE='#FAFAF7', GREY='#D8D9D6', BLUE='#A5C9D2';
  scene.background=new T.Color(BG);
  const camera=new T.OrthographicCamera(-7.6,7.6,13.51,-13.51,.1,120);
  const renderer=new T.WebGLRenderer({antialias:false,alpha:false,preserveDrawingBuffer:true,powerPreference:'high-performance'});
  renderer.setPixelRatio(1);
  renderer.setSize(720,1280,false);
  renderer.setClearColor(BG);
  renderer.outputColorSpace=T.SRGBColorSpace;
  const colors=new Map();
  function mat(c){if(!colors.has(c))colors.set(c,new T.MeshBasicMaterial({color:c,side:T.DoubleSide}));return colors.get(c);}
  function group(x=0,y=0,z=0){const g=new T.Group();g.position.set(x,y,z);scene.add(g);return g;}
  function mesh(p,geom,c){const o=new T.Mesh(geom,mat(c));p.add(o);return o;}
  function box(p,x,y,z,w,h,d,c){const o=mesh(p,new T.BoxGeometry(w,h,d),c);o.position.set(x,y,z);return o;}
  function sphere(p,x,y,z,r,c){const o=mesh(p,new T.SphereGeometry(r,12,8),c);o.position.set(x,y,z);return o;}
  function cyl(p,x,y,z,rt,rb,h,c,n=18){const o=mesh(p,new T.CylinderGeometry(rt,rb,h,n),c);o.position.set(x,y,z);return o;}
  function rod(p,a,b,r,c){const v=new T.Vector3(...a),w=new T.Vector3(...b),vec=w.clone().sub(v);
    const o=mesh(p,new T.CylinderGeometry(r,r,vec.length(),10),c);
    o.position.copy(v).add(w).multiplyScalar(.5);o.quaternion.setFromUnitVectors(new T.Vector3(0,1,0),vec.normalize());return o;}
  function discShadow(p,x,z,rx=1,rz=.72){const o=mesh(p,new T.CircleGeometry(1,22),'#E1E2DF');o.rotation.x=-Math.PI/2;
    o.position.set(x,.075,z);o.scale.set(rx,rz,1);return o;}
  box(scene,0,-.17,0,17,.26,17,'#F5F5F3');
  box(scene,0,-.34,0,17.08,.12,17.08,'#E7E7E3');
  for(const [x,z] of [[-6,-6],[6,-6],[-6,6],[6,6]]){discShadow(scene,x,z,.18,.18);}
  const nodes={
    abroad:[-4.45,-3.65], parcel:[-1.65,-1.25], hub:[.7,.15],
    traveler:[4.25,-2.75], mother:[4.15,3.70], app:[-2.45,4.15]
  };
  // Orange physical 3D tube network, assembled from straight spans and elbows.
  function route(name,coords){
    const g=group();g.visible=false;
    for(let i=0;i<coords.length-1;i++){
      const a=coords[i],b=coords[i+1];
      rod(g,[a[0],.24,a[1]],[b[0],.24,b[1]],.175,ORANGE);
      sphere(g,a[0],.24,a[1],.175,ORANGE);
    }
    const last=coords[coords.length-1];sphere(g,last[0],.24,last[1],.175,ORANGE);
    return g;
  }
  const paths=[
    route('abroad',[[...nodes.abroad],[-4.45,-1.25],[...nodes.parcel]]),
    route('center',[[...nodes.parcel],[-1.65,.15],[...nodes.hub]]),
    route('traveler',[[...nodes.hub],[2.1,.15],[2.1,-2.75],[...nodes.traveler]]),
    route('mother',[[...nodes.hub],[.7,2.15],[4.15,2.15],[...nodes.mother]]),
    route('phone',[[...nodes.app],[-2.45,2.15],[.7,2.15]])
  ];
  function base(key,c){const [x,z]=nodes[key],p=group(x,0,z);
    discShadow(p,.18,.20,1.05,.86);
    box(p,0,.32,0,1.48,.56,1.48,c);
    box(p,0,.63,0,1.33,.08,1.33,c===BLACK?'#343438':'#E9EAE7');
    return p;
  }
  function pawn(root,c,skin=null){
    cyl(root,0,1.0,0,.34,.42,.70,c,16);
    sphere(root,0,1.61,0,.37,skin||c);
    cyl(root,0,.73,0,.51,.49,.11,c,18);
    return root;
  }
  const sender=base('abroad',BLACK);pawn(sender,BLACK);
  const recipient=base('mother',WHITE);pawn(recipient,WHITE,'#E9E9E5');
  const traveler=base('traveler',BLACK);pawn(traveler,BLACK);
  const bag=base('parcel',WHITE);
  box(bag,0,1.07,0,.89,.67,.88,'#D3D4D0');
  box(bag,0,1.41,0,.92,.085,.92,WHITE);
  box(bag,0,1.09,.46,.13,.68,.055,ORANGE);
  box(bag,0,1.44,0,.12,.025,.95,ORANGE);
  const center=base('hub',ORANGE);
  cyl(center,0,.94,0,.57,.57,.20,BLACK);
  cyl(center,0,1.09,0,.43,.43,.12,'#38393C');
  const tick=group(.7,1.22,.15);
  const t1=box(tick,-.12,.02,0,.10,.10,.35,WHITE);t1.rotation.y=-.3;
  const t2=box(tick,.14,.11,0,.11,.10,.60,WHITE);t2.rotation.y=.65;
  const supplement=group(3.85,0,1.15);
  discShadow(supplement,0,0,.65,.53);
  cyl(supplement,0,.57,0,.42,.42,.84,WHITE,16);
  cyl(supplement,0,1.06,0,.32,.32,.22,'#D0D4D1',16);
  cyl(supplement,0,1.24,0,.34,.34,.12,WHITE,16);
  box(supplement,0,.65,.425,.48,.11,.045,'#93B9C3');
  box(supplement,0,.65,.452,.12,.40,.035,'#93B9C3');
  const phone=base('app',BLACK);
  box(phone,0,1.41,0,.92,1.40,.22,BLACK);
  box(phone,0,1.43,.12,.76,1.14,.025,WHITE);
  box(phone,0,1.83,.144,.56,.10,.028,ORANGE);
  for(let i=0;i<3;i++){
    box(phone,0,1.52-i*.25,.143,.59,.17,.027,'#E9EAE6');
    box(phone,-.20,1.52-i*.25,.16,.12,.10,.03,ORANGE_LIGHT);
  }
  // Small restrained 3D status markers, drawn with geometry rather than UI effects.
  for(const [x,z] of [[-5.7,.7],[-3.2,1.6],[2.7,-4.2],[4.8,.1]]){
    cyl(scene,x,.13,z,.085,.085,.10,BLACK,14);
  }
  for(const [x,z] of [[-5.2,-.1],[-3.6,.8],[2.8,4.8]]){
    box(scene,x,.15,z,.52,.07,.07,ORANGE);
    box(scene,x+.67,.15,z,.35,.07,.07,BLACK);
  }
  const spark=group();sphere(spark,0,0,0,.30,WHITE);
  const smooth=v=>{v=Math.max(0,Math.min(1,v));return v*v*(3-2*v)};
  function update(t){
    const phase=t<4?0:t<7?1:t<11?2:3;
    const revealed=phase===0?1:phase===1?3:5;
    paths.forEach((p,i)=>{p.visible=i<revealed;});
    const bob=Math.sin(t*2.1)*.045;
    sender.position.y=bob;recipient.position.y=-bob*.6;traveler.position.y=bob*.6;
    bag.position.y=Math.sin(t*2.4+1)*.035;
    phone.scale.setScalar(phase===2?1.10:1);
    supplement.scale.setScalar(phase===0?1.12:1);
    const track=phase===0?[[...nodes.abroad],[-4.45,-1.25],[...nodes.parcel]]:
                phase===1?[[...nodes.parcel],[-1.65,.15],[...nodes.hub],[2.1,.15],[2.1,-2.75],[...nodes.traveler]]:
                [[...nodes.app],[-2.45,2.15],[.7,2.15],[4.15,2.15],[...nodes.mother]];
    const ix=Math.min(track.length-2,Math.floor((t%3.2)/3.2*(track.length-1)));
    const a=track[ix],b=track[ix+1],f=((t%3.2)/3.2*(track.length-1))%1;
    spark.position.set(a[0]+(b[0]-a[0])*f,.60,a[1]+(b[1]-a[1])*f);
    spark.visible=t>1;
    camera.position.set(18+Math.sin(t*.21)*.6,24,22+Math.cos(t*.18)*.5);
    camera.lookAt(0,0,0);camera.zoom=phase===3?.92:1.02;
    camera.updateProjectionMatrix();camera.updateMatrixWorld();scene.updateMatrixWorld(true);
    renderer.render(scene,camera);
  }
  update(0);
  return {scene,camera,renderer,update};
}
