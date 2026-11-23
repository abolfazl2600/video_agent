import React from 'react';
import {AbsoluteFill, Audio, Sequence, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {C,F,BrandLogo,Person,TechRings,pop,fp,useF} from './components';
import {AirlinerDetailed,CargoParcelDetailed,TechnicalPill} from './DetailAssets';
import {ProductPhone} from './ProductPhone';
import {TerminalBackdrop,AirportDistrict,DocumentAndPassport} from './SceneProps';

const at=(left:number,top:number,extra:React.CSSProperties={}):React.CSSProperties=>({position:'absolute',left,top,...extra});
const text=(size:number,color=C.navy,weight=850):React.CSSProperties=>({fontFamily:F,fontSize:size,fontWeight:weight,color,lineHeight:1.46,letterSpacing:-1.5,direction:'rtl',textAlign:'center'});

const Back:React.FC=()=>{
 const f=useF();
 return <div style={{position:'absolute',inset:0,overflow:'hidden',background:'radial-gradient(ellipse 88% 49% at 55% 56%, #DDF4FF 0%,#F4FBFF 58%,#FFFFFF 100%)'}}>
  <div style={{position:'absolute',inset:0,opacity:.33,backgroundImage:'linear-gradient(90deg,#B9DFEE 1px,transparent 1px),linear-gradient(#B9DFEE 1px,transparent 1px)',backgroundSize:'68px 68px',maskImage:'radial-gradient(ellipse 77% 68% at 50% 52%,black,transparent)'}}/>
  <div style={{position:'absolute',inset:0,opacity:.14,backgroundImage:'repeating-radial-gradient(circle at 50% 52%, #80BAD9 0px,#80BAD9 1px,transparent 2px,transparent 11px)'}}/>
  <div style={at((f*2.9)%1300-120,130,{width:2,height:1500,opacity:.25,background:'linear-gradient(180deg,transparent,#18BBE7,transparent)',filter:'blur(1px)',boxShadow:'0 0 40px #42D8EC'})}/>
  {Array.from({length:32},(_,i)=>{
   const x=(i*189.97+91)%1080,y=(i*271.31+310)%1920;
   return <i key={i} style={at(x,y+Math.sin(f*.031+i)*19,{width:i%7===0?6:3,height:i%7===0?6:3,background:i%3===0?C.blue:C.cyan,borderRadius:i%2?'50%':0,opacity:.12+.17*(1+Math.sin(i+f*.023))/2})}/>;
  })}
  <div style={at(46,128,{width:35,height:35,borderLeft:'2px solid #5BCBE6',borderTop:'2px solid #5BCBE6'})}/>
  <div style={{position:'absolute',right:46,top:128,width:35,height:35,borderRight:'2px solid #5BCBE6',borderTop:'2px solid #5BCBE6'}}/>
  <div style={at(46,1677,{width:35,height:35,borderLeft:'2px solid #5BCBE6',borderBottom:'2px solid #5BCBE6'})}/>
  <div style={{position:'absolute',right:46,top:1677,width:35,height:35,borderRight:'2px solid #5BCBE6',borderBottom:'2px solid #5BCBE6'}}/>
 </div>;
};

// Branding only. No page, frame, progress, or section counters at the top.
const Header:React.FC=()=><div style={at(90,194,{display:'flex',alignItems:'center',gap:18,height:90})}>
 <BrandLogo size={82}/>
 <div>
  <div style={{fontFamily:'Knewave,Impact,sans-serif',fontSize:44,color:C.navy,letterSpacing:1}}>ADVERTIO <span style={{color:C.blue}}>CARGO</span></div>
  <div style={{fontFamily:'ui-monospace,monospace',fontSize:14,color:C.muted,letterSpacing:4}}>AIR TRAVEL CONNECTION PLATFORM</div>
 </div>
</div>;

const Scene:React.FC<{duration:number,children:React.ReactNode}>=({duration,children})=>{
 const f=useF();
 const opacity=Math.min(fp(f,0,9),1-fp(f,duration-10,duration));
 return <AbsoluteFill style={{opacity}}>
  <Header/>{children}
 </AbsoluteFill>;
};
const Tag:React.FC<{children:React.ReactNode,light?:boolean}>=({children,light=false})=><span style={{fontFamily:'ui-monospace,monospace',fontSize:24,letterSpacing:2,fontWeight:700,color:light?'#BBEEFF':C.blue}}>{children}</span>;
const Card:React.FC<{children:React.ReactNode,css?:React.CSSProperties}>=({children,css})=><div style={{background:'rgba(255,255,255,.92)',border:'2px solid #C7E7F4',borderRadius:34,boxShadow:'0 24px 65px rgba(17,75,129,.14)',backdropFilter:'blur(12px)',...css}}>{children}</div>;

// A nose-right, top-down airliner. Cabin windows, cockpit, winglets, both
// engines, tailplane, doors and wingtip navigation lights are actual geometry.
const cube=<svg viewBox="0 0 240 210" width="200" height="180">
 <path d="M16 72 119 14 224 73 120 133Z" fill="#F6DFBD" stroke="#D8B48A" strokeWidth="4"/>
 <path d="M16 72 120 133 120 201 16 143Z" fill="#D3A16C"/><path d="M120 133 224 73 224 142 120 201Z" fill="#B67A48"/>
 <path d="M75 39 178 100 178 172 156 184 156 111 53 53Z" fill="#FFF1D4" opacity=".82"/>
 </svg>;

const SceneOne:React.FC=()=>{
 const f=useF(),s=pop(f,5,140),sub=pop(f,25,140);
 return <Scene duration={90}>
  <div style={at(80,365,{width:920,opacity:fp(f,0,15),transform:'translateY('+((1-s)*140)+'px) scale('+(2.7-1.7*s)+')',transformOrigin:'center'})}>
   <div style={text(120,C.navy,950)}>بسته داری؟</div>
  </div>
  <div style={at(85,550,{width:900,opacity:fp(f,25,45),transform:'translateY('+((1-sub)*70)+'px)'})}>
   <div style={text(74,C.blue,900)}>مسافرش رو پیدا کن!</div>
  </div>
  <div style={at(164,725,{opacity:.75,transform:'scale(1.15)'})}><TechRings size={730}/></div>
  <div style={at(240,855,{transform:'scale(' +(.48+.52*pop(f,13,150))+') rotate('+((1-s)*-12)+'deg)'})}><CargoParcelDetailed width={600}/></div>
  <div style={at(115,980,{opacity:fp(f,28,45),transform:'rotate(-8deg) scale(.72)',transformOrigin:'left top'})}><DocumentAndPassport/></div>
  <div style={at(722,1050,{opacity:fp(f,33,48)})}><TechnicalPill label="INT'L TRAVEL" sub="مسیرهای هوایی"/></div>
  <div style={at(98,1370,{opacity:fp(f,50,63)})}><TechnicalPill label="PACKAGE / DOCUMENTS" sub="ثبت آگهی بار"/></div>
  <div style={at(165,1545,{width:750,textAlign:'center',opacity:fp(f,43,67)})}><Tag>PARCEL / TRAVELER / CONNECTION</Tag></div>
 </Scene>;
};

const SceneTwo:React.FC=()=>{
 const f=useF(),p=fp(f,35,104);
 return <Scene duration={120}>
  <div style={at(83,330,{width:910})}><div style={text(65,C.navy)}>یه نفر بار داره،</div><div style={text(63,C.blue)}>یکی هم مسافر ایرانه!</div></div>
  <div style={at(85,560,{opacity:fp(f,1,20),transform:'translateX('+((1-pop(f,2))*-160)+'px)'})}>
   <Card css={{width:440,height:470,padding:'22px 25px',position:'relative',background:'linear-gradient(145deg,#FFF,#E8F7FE)',overflow:'hidden'}}>
    <div style={at(-20,98,{opacity:.62})}><TerminalBackdrop variant="yyz"/></div>
    <div style={at(73,-8)}><Person width={310}/></div>
    <div style={at(23,25)}><Tag>CANADA</Tag></div>
    <div style={at(20,388,{width:390})}><div style={text(34,C.ink)}>فرستنده بار</div></div>
   </Card>
  </div>
  <div style={at(552,995,{opacity:fp(f,17,39),transform:'translateX('+((1-pop(f,22))*160)+'px)'})}>
   <Card css={{width:440,height:475,padding:24,position:'relative',background:'linear-gradient(145deg,#FFF,#E5F6FF)',overflow:'hidden'}}>
    <div style={at(-21,105,{opacity:.60})}><TerminalBackdrop variant="ika"/></div>
    <div style={at(76,-4)}><Person traveler width={315}/></div>
    <div style={at(28,24)}><Tag>IRAN</Tag></div>
    <div style={at(20,394,{width:390})}><div style={text(34,C.blue)}>مسافر هوایی</div></div>
   </Card>
  </div>
  <svg style={at(390,840)} width={360} height={360} viewBox="0 0 360 360">
   <path d="M15 13 Q360 -20 337 336" fill="none" stroke="#A1DDEE" strokeWidth="8" strokeDasharray="10 17"/>
   <path d="M15 13 Q360 -20 337 336" fill="none" stroke={C.blue} strokeWidth="8" strokeDasharray="630" strokeDashoffset={630*(1-p)}/>
  </svg>
  <div style={at(70,1095,{opacity:fp(f,43,61)})}><TechnicalPill label="YYZ → IKA" sub="پرواز بین‌المللی"/></div>
  <div style={at(675,720,{opacity:fp(f,32,48)})}><TechnicalPill label="TRAVEL READY" sub="ظرفیت چمدان"/></div>
  <div style={at(160,1550,{opacity:fp(f,51,70)})}><Card css={{padding:'22px 40px',width:760,textAlign:'center'}}><div style={text(35,C.navy)}>فقط باید همدیگه رو پیدا کنن!</div></Card></div>
 </Scene>;
};

const SceneThree:React.FC=()=>{
 const f=useF(),a=pop(f,4,125);
 return <Scene duration={150}>
  <div style={at(80,325,{width:920})}><div style={text(61,C.navy)}>اینجاست که ادورتیو</div><div style={text(66,C.blue)}>وارد می‌شه!</div></div>
  <div style={at(135,515,{opacity:.52})}><TechRings size={800}/></div>
  <div style={at(67,744,{opacity:fp(f,25,44)})}><TechnicalPill label="ADVERTIO / LISTINGS" sub="پلتفرم ارتباط کاربران" accent/></div>
  <div style={at(760,1030,{opacity:fp(f,55,73)})}><TechnicalPill label="YYZ → IKA" sub="نمونه مسیر"/></div>
  <div style={at(255,495,{opacity:fp(f,2,19),transform:'translateY('+((1-a)*600)+'px) scale('+(0.55+.45*a)+')'})}><ProductPhone width={565}/></div>
  {['ثبت آگهی ارسال بار','انتخاب مبدأ و مقصد','ارتباط مستقیم با مسافر'].map((label,i)=>{
   const px=i===0?68:i===1?525:78,py=[1120,1290,1460][i];
   return <div key={label} style={at(px,py,{padding:'18px 27px',border:'2px solid #58C7E0',borderRadius:18,background:'rgba(10,52,97,.91)',boxShadow:'0 18px 35px rgba(4,62,122,.23)',transform:'translateX('+((1-pop(f,37+i*19))* (i===1?400:-420))+'px)',opacity:fp(f,32+i*19,48+i*19)})}>
    <div style={{fontFamily:F,fontSize:27,fontWeight:800,color:'white',direction:'rtl'}}>✓ {label}</div>
   </div>;
  })}
 </Scene>;
};

// Cubic from Toronto (left) to Tehran (right). An airplane is drawn nose-right
// and rotated by the curve tangent, so it never flies backwards.
const p0={x:190,y:1140},p1={x:355,y:770},p2={x:700,y:790},p3={x:876,y:1190};
const pathAt=(t:number)=>{
 const u=1-t;
 const x=u*u*u*p0.x+3*u*u*t*p1.x+3*u*t*t*p2.x+t*t*t*p3.x;
 const y=u*u*u*p0.y+3*u*u*t*p1.y+3*u*t*t*p2.y+t*t*t*p3.y;
 const dx=3*u*u*(p1.x-p0.x)+6*u*t*(p2.x-p1.x)+3*t*t*(p3.x-p2.x);
 const dy=3*u*u*(p1.y-p0.y)+6*u*t*(p2.y-p1.y)+3*t*t*(p3.y-p2.y);
 return {x,y,angle:Math.atan2(dy,dx)*180/Math.PI};
};
const City:React.FC<{name:string}> =({name})=><svg width={240} height={220} viewBox="0 0 240 220">
 <ellipse cx="120" cy="180" rx="110" ry="34" fill="#BDE3F5" opacity=".65"/>
 <path d="M18 137 112 87 225 142 117 200Z" fill="#D2ECF8" stroke="#86BEDA" strokeWidth="3"/>
 <path d="M45 107 45 49 88 25 130 48 130 135 88 158 45 137Z" fill="#BDDDEE" stroke="#7FAFCE" strokeWidth="2"/>
 <path d="M45 49 88 25 130 48 87 73Z" fill="#FFFFFF"/>
 <path d="M87 73 130 48 130 135 87 158Z" fill="#8FC8E4"/>
 <path d="M68 72v61 M105 79v52" stroke="#6CA6C7" strokeWidth="9" strokeDasharray="16 9"/>
 <path d="M142 129 142 76 170 59 201 76 201 158 170 178 142 158Z" fill="#C0E2F1"/>
 <path d="M142 76 170 59 201 76 172 92Z" fill="#F8FDFF"/>
 <path d="M172 92 201 76 201 158 172 178Z" fill="#8DC8E5"/>
 <text x="120" y="215" textAnchor="middle" fontSize="18" fontWeight="bold" fontFamily="Arial,sans-serif" fill={C.navy}>{name}</text>
 </svg>;

const SceneFour:React.FC=()=>{
 const f=useF(),progress=fp(f,18,109),pos=pathAt(progress);
 const headline=['فرستنده','و مسافر،','به هم وصل می‌شن!'];
 return <Scene duration={120}>
  <div style={at(70,336,{width:940})}>
   <Tag>CONNECTED / AIR ROUTE</Tag>
   {headline.map((line,i)=><div key={line} style={{...text(i===2?60:65,i===2?C.blue:C.navy),opacity:fp(f,i*8,22+i*8),transform:'translateY('+((1-pop(f,i*8,130))*42)+'px)'}}>{line}</div>)}
  </div>
  <svg style={at(0,0,{width:1080,height:1920,overflow:'visible'})} viewBox="0 0 1080 1920">
   <defs><linearGradient id="flightline" x1="0" y1="0" x2="1" y2="0"><stop stopColor="#0878DE"/><stop offset=".6" stopColor="#44D5E7"/><stop offset="1" stopColor="#0F79D6"/></linearGradient></defs>
   {Array.from({length:5},(_,i)=><ellipse key={i} cx="540" cy="1010" rx={205+i*89} ry={125+i*66} stroke="#B7E1F2" strokeWidth="2" strokeDasharray="13 17" opacity=".4" fill="none"/>)}
   <path d="M190 1140 C355 770 700 790 876 1190" stroke="#8ACFDB" strokeWidth="18" fill="none" opacity=".18" strokeLinecap="round"/>
   <path d="M190 1140 C355 770 700 790 876 1190" stroke="#94CEDD" strokeWidth="7" fill="none" strokeDasharray="12 20"/>
   <path d="M190 1140 C355 770 700 790 876 1190" stroke="url(#flightline)" strokeWidth="10" fill="none" strokeDasharray="1160" strokeDashoffset={1160*(1-progress)} strokeLinecap="round"/>
   <circle cx={p0.x} cy={p0.y} r="15" fill={C.blue} stroke="white" strokeWidth="5"/>
   <circle cx={p3.x} cy={p3.y} r="15" fill={C.blue} stroke="white" strokeWidth="5"/>
  </svg>
  <div style={at(44,1159)}><AirportDistrict city="TORONTO"/></div>
  <div style={at(759,1185)}><AirportDistrict city="TEHRAN"/></div>
  <div style={at(95,1369,{opacity:fp(f,19,44)})}><TechnicalPill label="AIR ROUTE" sub="کانادا به ایران" accent/></div>
  <div style={at(758,1378,{opacity:fp(f,45,69)})}><TechnicalPill label="CONNECT" sub="گفتگوی مستقیم"/></div>
  <div style={at(pos.x,pos.y,{transform:'translate(-50%,-50%) rotate('+pos.angle+'deg)',transformOrigin:'center',filter:'drop-shadow(0 17px 23px rgba(13,99,161,.30))'})}><AirlinerDetailed width={422}/></div>
  <div style={at(104,1515,{width:866,opacity:fp(f,50,74)})}>
   <Card css={{padding:'27px 30px',background:'#FFFFFFEE'}}>
    <div style={text(32,C.navy)}>ارتباط برقرار می‌شه، هماهنگی مستقیمه</div>
   </Card>
  </div>
 </Scene>;
};

const SceneFive:React.FC=()=>{
 const f=useF(),p=pop(f,4,120);
 return <Scene duration={120}>
  <div style={at(82,355,{width:920,textAlign:'center',opacity:fp(f,2,20),transform:'translateY('+((1-p)*90)+'px)'})}>
   <div style={{fontFamily:'Knewave,Impact,sans-serif',fontSize:82,color:C.navy}}>ADVERTIO <span style={{color:C.blue}}>CARGO</span></div>
   <div style={{height:5,width:400,margin:'19px auto',background:'linear-gradient(90deg,#0F69D7,#21CBE1)'}}/>
  </div>
  <div style={at(175,540,{opacity:.48})}><TechRings size={730}/></div>
  <div style={at(80,800,{opacity:fp(f,23,47)})}><TechnicalPill label="DIRECT MESSAGE" sub="ارتباط بدون واسطه" accent/></div>
  <div style={at(741,1070,{opacity:fp(f,36,56)})}><TechnicalPill label="AIR TRAVEL" sub="مسافر مسیر ایران"/></div>
  <div style={at(330,600,{transform:'scale(.70)',transformOrigin:'left top'})}><ProductPhone width={565}/></div>
  <div style={at(66,1000,{transform:'rotate(-17deg)'})}><AirlinerDetailed width={560}/></div>
  <div style={at(650,1120,{transform:'scale(.67)',transformOrigin:'left top'})}><CargoParcelDetailed width={330}/></div>
  <div style={at(95,1440,{width:890,opacity:fp(f,20,43)})}>
   <div style={text(55,C.navy)}>بار داری؟ مسافرت رو پیدا کن!</div>
   <div style={{...text(26,C.muted,600),marginTop:12}}>پلتفرم ارتباط فرستنده بار و مسافر هوایی</div>
   <div style={{display:'flex',alignItems:'center',justifyContent:'center',gap:18,marginTop:23}}>
    <BrandLogo size={78}/>
    <div style={{padding:'17px 42px',borderRadius:17,color:'#FFFFFF',background:C.navy,fontSize:31,fontWeight:900,fontFamily:'ui-monospace,monospace'}}>Advertio.net</div>
   </div>
  </div>
 </Scene>;
};

export const CargoReels:React.FC=()=>{
 const {fps,width}=useVideoConfig();
 return <AbsoluteFill style={{background:'#FFFFFF',overflow:'hidden'}}>
  <div style={{width:1080,height:1920,position:'relative',overflow:'hidden',transform:'scale('+(width/1080)+')',transformOrigin:'top left'}}>
   <Back/>
   <Sequence from={0} durationInFrames={Math.round(3*fps)}><SceneOne/></Sequence>
   <Sequence from={Math.round(3*fps)} durationInFrames={Math.round(4*fps)}><SceneTwo/></Sequence>
   <Sequence from={Math.round(7*fps)} durationInFrames={Math.round(5*fps)}><SceneThree/></Sequence>
   <Sequence from={Math.round(12*fps)} durationInFrames={Math.round(4*fps)}><SceneFour/></Sequence>
   <Sequence from={Math.round(16*fps)} durationInFrames={Math.round(4*fps)}><SceneFive/></Sequence>
  </div>
  <Audio src={staticFile('audio/original-tech-bed.wav')} volume={0.40}/>
  <style>{'@font-face{font-family:Vazirmatn;src:url("'+staticFile('fonts/Vazirmatn-Regular.ttf')+'") format("truetype");font-weight:400;}@font-face{font-family:Vazirmatn;src:url("'+staticFile('fonts/Vazirmatn-Bold.ttf')+'") format("truetype");font-weight:700 1000;}*{box-sizing:border-box;}'}</style>
 </AbsoluteFill>;
};
