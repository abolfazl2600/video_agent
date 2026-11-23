import React from 'react';
import {AbsoluteFill, Audio, Sequence, staticFile, useCurrentFrame, useVideoConfig, interpolate} from 'remotion';
import {C,F,pop,fp,useF,range,BrandLogo,Backdrop,SmallTag,Persian,TechRings,Parcel,Person,Plane,Header,Footer} from './components';

const style=(p:React.CSSProperties):React.CSSProperties=>({position:'absolute',...p});
const ShadowCard:React.FC<{children:React.ReactNode,css?:React.CSSProperties}>=({children,css})=>
 <div style={{border:'1px solid #BCE6F5',boxShadow:'0 30px 80px rgba(13,72,141,.11)',borderRadius:28,background:'rgba(255,255,255,.88)',backdropFilter:'blur(16px)',...css}}>{children}</div>;
const Bar:React.FC<{label:string,value:string}>=({label,value})=>
 <div style={{display:'flex',flexDirection:'row-reverse',justifyContent:'space-between',padding:'21px 0',borderBottom:'1px solid #E0EDF3'}}>
  <span style={{color:C.muted,fontFamily:F,fontSize:22}}>{label}</span>
  <span style={{color:C.ink,fontFamily:F,fontWeight:800,fontSize:25}}>{value}</span>
 </div>;

const Phone:React.FC<{compact?:boolean}>=({compact=false})=>{
 const f=useF(), w=compact?285:423, h=compact?562:770;
 return <div style={{width:w,height:h,position:'relative',background:'linear-gradient(115deg,#0C2143,#355A80 45%,#09152D)',padding:compact?12:17,borderRadius:compact?45:61,boxShadow:'24px 30px 75px rgba(6,39,82,.30),inset 0 0 0 3px #839AB6',transform:`translateY(${Math.sin(f*.035)*12}px) rotateY(-7deg) rotateZ(${Math.sin(f*.018)*1.6}deg)`,transformStyle:'preserve-3d'}}>
  <div style={{height:'100%',overflow:'hidden',background:'#FCFEFF',borderRadius:compact?32:44,padding:compact?20:27,boxSizing:'border-box',fontFamily:F,direction:'rtl'}}>
   <div style={{position:'absolute',left:'50%',top:compact?17:20,width:compact?80:118,height:compact?18:25,borderRadius:20,background:'#0B1930',transform:'translateX(-50%)'}}/>
   <div style={{height:compact?26:42}}/>
   <div style={{display:'flex',gap:9,alignItems:'center',justifyContent:'flex-start',borderBottom:'1px solid #E1EBF2',paddingBottom:compact?10:15}}>
    <BrandLogo size={compact?41:57}/>
    <div style={{fontSize:compact?15:23,color:C.navy,fontWeight:900}}>ادورتیو <span style={{color:C.blue}}>کارگو</span></div>
   </div>
   <div style={{marginTop:compact?13:24,fontSize:compact?16:25,fontWeight:900,color:C.ink,lineHeight:1.5}}>آگهی ارسال بار مسافری</div>
   <div style={{fontSize:compact?11:14,color:C.muted,marginTop:6}}>نمونه نمایشی / DEMO LISTING</div>
   <div style={{border:'1px solid #DCECF6',background:'#F5FAFF',borderRadius:compact?13:22,marginTop:compact?12:20,padding:compact?12:22}}>
    <Bar label="مبدأ" value="تورنتو، کانادا"/>
    <Bar label="مقصد" value="تهران، ایران"/>
    <Bar label="نوع مرسوله" value="بسته / مدارک"/>
    <div style={{marginTop:compact?12:17,fontSize:compact?11:18,color:'#087AA7',background:'#E5F9FC',padding:compact?9:13,borderRadius:12,fontWeight:700}}>ارتباط مستقیم با مسافر</div>
   </div>
   <div style={{background:'linear-gradient(90deg,#0870DD,#23B6E4)',borderRadius:compact?10:16,marginTop:compact?15:24,color:'white',textAlign:'center',padding:compact?10:17,fontWeight:800,fontSize:compact?14:22}}>مشاهده آگهی‌های مسیر</div>
   <div style={{textAlign:'center',fontSize:compact?10:13,color:C.muted,marginTop:compact?11:23}}>Advertio.net</div>
  </div>
 </div>;
};

const SceneFrame:React.FC<{children:React.ReactNode,duration:number,index:string}>=({children,duration,index})=>{
 const f=useF(),opacity=interpolate(f,[0,9,duration-9,duration],[0,1,1,0],{extrapolateLeft:'clamp',extrapolateRight:'clamp'});
 return <AbsoluteFill style={{opacity}}>
  <Header index={index}/>
  {children}
 </AbsoluteFill>;
};

const SceneOne:React.FC=()=>{
 const f=useF(),s=pop(f,5,150),second=pop(f,30,180);
 return <SceneFrame duration={90} index="01">
  <div style={style({top:200,left:95,width:1020,transform:`translateX(${(1-s)*-130}px) scale(${3-2*s})`,transformOrigin:'center left',opacity:fp(f,2,16)})}>
   <SmallTag>01 // PARCEL DETECTED</SmallTag>
   <Persian size={135} color={C.navy} style={{marginTop:20,whiteSpace:'nowrap',textShadow:'0 14px 32px rgba(9,51,110,.09)'}}>بسته داری؟</Persian>
  </div>
  <div style={style({left:112,top:475,transform:`translateY(${(1-second)*80}px)`,opacity:fp(f,27,48)})}>
   <Persian size={81} color={C.blue}>مسافرش رو پیدا کن!</Persian>
   <div style={{fontSize:28,letterSpacing:6,color:C.muted,fontFamily:'ui-monospace,monospace',marginTop:15}}>THE CONNECTION STARTS HERE</div>
  </div>
  <div style={style({right:100,top:130,transform:`scale(${.60+.4*pop(f,9,110)}) rotate(${(1-s)*30}deg)`,transformOrigin:'center'})}>
   <TechRings size={690} opacity={.85}/>
  </div>
  <div style={style({right:162,top:280,transform:`scale(${.4+.6*pop(f,15,160)}) rotate(${(1-pop(f,15,150))*-22}deg)`})}>
   <Parcel width={465}/>
  </div>
  <div style={style({right:260,top:790,opacity:fp(f,46,63)})}>
   <div style={{fontFamily:'ui-monospace,monospace',fontSize:20,color:C.blue,letterSpacing:3}}>AIR CARGO / CONNECT / 001</div>
  </div>
 </SceneFrame>
};

const SceneTwo:React.FC=()=>{
 const f=useF(),l=pop(f,4),r=pop(f,23),progress=fp(f,42,103);
 return <SceneFrame duration={120} index="02">
  <div style={style({left:110,top:175,right:110,textAlign:'center'})}>
   <SmallTag>02 // TWO SIDES, ONE ROUTE</SmallTag>
   <Persian size={68} color={C.navy} style={{textAlign:'center',marginTop:10}}>دو نفر، یک مسیر مشترک</Persian>
  </div>
  <div style={style({left:180,top:345,width:630,opacity:fp(f,2,18),transform:`translateX(${(1-l)*-240}px)`})}>
   <ShadowCard css={{height:505,padding:26,position:'relative',background:'linear-gradient(145deg,#FBFFFF,#E9F7FF)'}}>
    <div style={style({top:8,left:70})}><Person width={325}/></div>
    <div style={style({top:16,right:22})}><SmallTag>CANADA</SmallTag></div>
    <div style={style({bottom:7,right:32})}><Persian color={C.navy} size={38}>یکی بار داره...</Persian></div>
   </ShadowCard>
  </div>
  <div style={style({right:180,top:345,width:630,opacity:fp(f,16,32),transform:`translateX(${(1-r)*240}px)`})}>
   <ShadowCard css={{height:505,padding:26,position:'relative',background:'linear-gradient(145deg,#FAFEFF,#E8F8FF)'}}>
    <div style={style({top:4,left:65})}><Person traveler width={315}/></div>
    <div style={style({top:16,right:22})}><SmallTag>IRAN</SmallTag></div>
    <div style={style({bottom:7,right:32})}><Persian color={C.blue} size={38}>یکی مسافره!</Persian></div>
   </ShadowCard>
  </div>
  <svg style={style({left:728,top:430,overflow:'visible'})} width={490} height={200} viewBox="0 0 490 200">
   <path d="M 15 125 Q 246 -48 480 125" stroke="#C3E9F4" strokeWidth={9} strokeDasharray="12 18" fill="none"/>
   <path d="M 15 125 Q 246 -48 480 125" stroke={C.blue} strokeWidth={7} strokeLinecap="round" fill="none" strokeDasharray="560" strokeDashoffset={560*(1-progress)}/>
   <circle cx={15+465*progress} cy={125-173*4*progress*(1-progress)} r={9} fill={C.cyan} stroke="white" strokeWidth={4}/>
  </svg>
  <div style={style({left:750,top:690,background:C.navy,color:'white',fontFamily:F,fontSize:23,borderRadius:20,padding:'15px 28px',opacity:fp(f,50,70),boxShadow:'0 16px 36px #0D5CA32B'})}>فقط باید همدیگه رو پیدا کنن!</div>
 </SceneFrame>;
};

const SceneThree:React.FC=()=>{
 const f=useF(),p=pop(f,7,130),h=pop(f,22,95);
 const captions=['ثبت آگهی ارسال بار','انتخاب مبدأ و مقصد','ارتباط مستقیم با مسافر'];
 return <SceneFrame duration={150} index="03">
  <div style={style({left:138,top:180})}>
   <SmallTag>03 // PRODUCT REVEAL</SmallTag>
   <Persian color={C.navy} size={66} style={{marginTop:7}}>اینجاست که ادورتیو وارد می‌شه!</Persian>
  </div>
  <div style={style({right:320,top:250,opacity:.45})}><TechRings size={670}/></div>
  <div style={style({right:450,top:218,transform:`translateY(${(1-p)*750}px) scale(${.53+.47*p}) rotate(${(1-p)*18}deg)`,opacity:fp(f,2,18)})}>
   <Phone/>
  </div>
  <div style={style({left:105,top:360,width:610,transform:`translateX(${(1-h)*-700}px)`,opacity:fp(f,13,36)})}>
   <div style={{background:'linear-gradient(155deg,rgba(7,34,76,.93),rgba(12,78,136,.82))',clipPath:'polygon(0 0,95% 0,100% 12%,100% 100%,4% 100%,0 92%)',border:'2px solid rgba(38,201,229,.60)',padding:'44px 55px 48px',boxShadow:'0 32px 70px rgba(0,46,98,.26)',backdropFilter:'blur(20px)'}}>
    <div style={{fontFamily:'ui-monospace,monospace',color:'#81DDF7',fontSize:22,letterSpacing:3,marginBottom:17}}>ADVERTIO / CONNECTION HUD</div>
    {captions.map((line,i)=> <div key={line} style={{display:'flex',alignItems:'center',gap:19,opacity:fp(f,36+i*17,48+i*17),transform:`translateX(${(1-pop(f,36+i*17))*-85}px)`,padding:'20px 0',borderBottom:'1px solid #FFFFFF24'}}>
      <div style={{width:35,height:35,borderRadius:'50%',background:'#30D4E8',color:C.navy,textAlign:'center',fontWeight:900,fontSize:23,lineHeight:'35px'}}>✓</div>
      <div style={{fontFamily:F,color:'white',fontSize:29,fontWeight:800,direction:'rtl'}}>{line}</div>
    </div>)}
    <div style={{fontSize:18,fontFamily:'ui-monospace,monospace',color:'#B9EAF5',marginTop:29}}>NETWORK: CANADA → IRAN / SAMPLE DATA</div>
   </div>
  </div>
  <div style={style({right:110,top:600,width:230,opacity:fp(f,70,90)})}>
   <div style={{color:C.blue,fontFamily:'ui-monospace,monospace',fontSize:22,letterSpacing:2}}>LISTING ONLINE</div>
   <div style={{width:130,height:5,marginTop:16,background:C.cyan}}/>
  </div>
 </SceneFrame>;
};

const RouteWorld:React.FC<{f:number}>=({f})=>{
 const t=range(f,15,100);
 const x=(1-t)*(1-t)*320+2*(1-t)*t*960+t*t*1575;
 const y=(1-t)*(1-t)*638+2*(1-t)*t*175+t*t*624;
 return <svg viewBox="0 0 1920 780" width={1920} height={780} style={{position:'absolute',left:0,top:180,overflow:'visible'}}>
  <defs>
   <radialGradient id="disc" cx=".5" cy=".5"><stop stopColor="#E5F9FF"/><stop offset="1" stopColor="#E5F9FF" stopOpacity=".12"/></radialGradient>
   <linearGradient id="route" x1="0" x2="1"><stop stopColor="#0A6DDA"/><stop offset=".65" stopColor="#2DDEEA"/><stop offset="1" stopColor="#0A6DDA"/></linearGradient>
  </defs>
  <ellipse cx="960" cy="440" rx="790" ry="285" fill="url(#disc)" stroke="#C5EAF9" strokeWidth="3"/>
  {Array.from({length:9},(_,i)=><ellipse key={i} cx="960" cy="440" rx={115+i*85} ry={42+i*27} stroke="#72C6E8" strokeWidth="1.4" strokeDasharray="8 12" opacity=".42" fill="none"/>)}
  <path d="M320 638 Q960 175 1575 624" stroke="#71DDEB" strokeWidth="27" opacity=".14" fill="none" strokeLinecap="round"/>
  <path d="M320 638 Q960 175 1575 624" stroke="#65BEEB" strokeWidth="5" strokeDasharray="7 17" fill="none"/>
  <path d="M320 638 Q960 175 1575 624" stroke="url(#route)" strokeWidth="9" fill="none" strokeLinecap="round" strokeDasharray="2000" strokeDashoffset={2000*(1-t)}/>
  <g fill={C.blue} stroke="#fff" strokeWidth="7"><circle cx="320" cy="638" r="22"/><circle cx="1575" cy="624" r="22"/></g>
  <g transform={`translate(${x-105} ${y-55}) rotate(${(1-t)*-10})`}>
    <path d="M0 47 99 39 174 0 211 3 157 42 239 46 Q253 51 239 58 L153 62 202 96 169 98 99 64 0 61Z" fill="#FBFEFF" stroke="#1678CD" strokeWidth="5"/>
    <path d="M99 44 181 7 192 8 147 50 179 82 167 88Z" fill="#9DDDF6"/>
  </g>
  <g fontFamily="ui-monospace,monospace" fontWeight="bold" fontSize="27" fill={C.navy}><text x="235" y="695">TORONTO</text><text x="1530" y="685">TEHRAN</text></g>
  <g transform="translate(165 480)">
    <path d="M0 116 95 65 190 116 90 172Z" fill="#C9EBF5"/>
    <path d="M42 75 42 12 89 -7 130 15 130 113 89 137 42 114Z" fill="#C1DFEF"/>
    <path d="M42 12 89 -7 130 15 88 36Z" fill="#F9FEFF"/>
    <path d="M88 36 130 15 130 113 88 137Z" fill="#9DC7E3"/>
    <path d="M61 49v56M81 38v60M108 40v70" stroke="#7EACCC" strokeWidth="8" strokeDasharray="12 9"/>
  </g>
  <g transform="translate(1590 465)">
    <path d="M0 116 95 65 190 116 90 172Z" fill="#C9EBF5"/>
    <path d="M42 75 42 15 89 -7 130 15 130 113 89 137 42 114Z" fill="#D7E9F5"/>
    <path d="M42 15 89 -7 130 15 88 36Z" fill="#FFFFFF"/>
    <path d="M88 36 130 15 130 113 88 137Z" fill="#86C7E8"/>
    <path d="M61 49v56M81 38v60M108 40v70" stroke="#7EACCC" strokeWidth="8" strokeDasharray="12 9"/>
  </g>
 </svg>;
};
const SceneFour:React.FC=()=>{
 const f=useF();
 const words=['فرستنده','و','مسافر،','به','هم','وصل','می‌شن!'];
 return <SceneFrame duration={120} index="04">
  <div style={style({left:160,top:170})}><SmallTag>04 // GLOBAL ROUTE CONNECTED</SmallTag></div>
  <RouteWorld f={f}/>
  <div style={style({left:135,right:135,top:235,display:'flex',flexDirection:'row-reverse',justifyContent:'center',gap:18})} dir="rtl">
    {words.map((word,i)=><span key={i} style={{fontFamily:F,fontSize:61,fontWeight:900,color:i>=5?C.blue:C.navy,display:'inline-block',opacity:fp(f,5+i*7,20+i*7),transform:`translateY(${(1-pop(f,7+i*7,150))*70}px)`}}>{word}</span>)}
  </div>
  <div style={style({right:180,top:745,opacity:fp(f,50,67),transform:`translateY(${(1-pop(f,50))*80}px)`})}>
   <ShadowCard css={{padding:'24px 40px',display:'flex',alignItems:'center',gap:20,borderRadius:24}}>
    <div style={{width:18,height:18,borderRadius:'50%',background:'#20D4D9',boxShadow:'0 0 20px #20D4D9'}}/>
    <Persian size={25}>مسیر مشترک پیدا شد؛ گفتگو و هماهنگی مستقیم</Persian>
   </ShadowCard>
  </div>
 </SceneFrame>
};
const SceneFive:React.FC=()=>{
 const f=useF(),p=pop(f,8,125);
 return <SceneFrame duration={120} index="05">
  <div style={style({left:1080,top:177,opacity:.5})}><TechRings size={720}/></div>
  <div style={style({right:310,top:278,transform:`scale(${.65+.2*p}) translateY(${Math.sin(f*.042)*8}px)`,transformOrigin:'center top'})}><Phone compact/></div>
  <div style={style({right:36,top:330,transform:`rotate(${Math.sin(f*.03)*7-6}deg)`})}><Plane width={345}/></div>
  <div style={style({right:585,top:670,transform:`scale(.50) rotate(${Math.sin(f*.03)*4}deg)`,transformOrigin:'left top'})}><Parcel width={450}/></div>
  <div style={style({left:115,top:260,width:960,opacity:fp(f,3,20),transform:`translateY(${(1-p)*80}px)`})}>
   <SmallTag>05 // ADVERTIO CARGO</SmallTag>
   <div style={{fontFamily:'Knewave,Impact,sans-serif',fontSize:103,color:C.navy,margin:'20px 0',lineHeight:1.3,whiteSpace:'nowrap',textShadow:'0 16px 40px #1D5CA522'}}>ADVERTIO <span style={{color:C.blue}}>CARGO</span></div>
   <Persian size={62} color={C.navy}>بار داری؟ مسافرت رو پیدا کن!</Persian>
   <div style={{height:5,width:455,margin:'28px 0 22px',background:'linear-gradient(90deg,#0E6BE0,#24CFE5)'}}/>
   <Persian size={29} color={C.muted}>پلتفرم ارتباط فرستنده بار و مسافر هوایی</Persian>
   <div style={{display:'flex',gap:18,alignItems:'center',marginTop:36}}>
    <BrandLogo size={110}/>
    <div style={{padding:'19px 40px',background:C.navy,color:'#fff',fontFamily:'ui-monospace,monospace',fontSize:36,borderRadius:18,boxShadow:'0 18px 38px #05285C33'}}>Advertio.net</div>
   </div>
  </div>
 </SceneFrame>;
};

export const CargoLaunch:React.FC=()=>{
 const f=useCurrentFrame(),{fps,width,height}=useVideoConfig();
 const scale=width/1920;
 return <AbsoluteFill style={{background:'#FFFFFF',overflow:'hidden'}}>
  <div style={{width:1920,height:1080,transform:`scale(${scale})`,transformOrigin:'0 0',position:'relative',overflow:'hidden'}}>
   <Backdrop/>
   <Sequence from={0} durationInFrames={Math.round(3*fps)}><SceneOne/></Sequence>
   <Sequence from={Math.round(3*fps)} durationInFrames={Math.round(4*fps)}><SceneTwo/></Sequence>
   <Sequence from={Math.round(7*fps)} durationInFrames={Math.round(5*fps)}><SceneThree/></Sequence>
   <Sequence from={Math.round(12*fps)} durationInFrames={Math.round(4*fps)}><SceneFour/></Sequence>
   <Sequence from={Math.round(16*fps)} durationInFrames={Math.round(4*fps)}><SceneFive/></Sequence>
   <Footer progress={f/(fps*20)}/>
  </div>
  <Audio src={staticFile('audio/original-tech-bed.wav')} volume={0.40}/>
  <style>{`@font-face {font-family: Vazirmatn; src:url("${staticFile('fonts/Vazirmatn-Regular.ttf')}") format("truetype"); font-weight:400;} @font-face {font-family: Vazirmatn;src:url("${staticFile('fonts/Vazirmatn-Bold.ttf')}") format("truetype");font-weight:700 1000;} *{box-sizing:border-box;}`}</style>
 </AbsoluteFill>;
};
