import React from 'react';
import {interpolate, spring, staticFile, useCurrentFrame, useVideoConfig, Img} from 'remotion';

export const C={navy:'#06214C',deep:'#102C51',blue:'#086DE0',cyan:'#26C9E5',pale:'#D9F3FF',ink:'#142B44',muted:'#5E7894',white:'#FFFFFF'};
export const F='Vazirmatn, Arial, sans-serif';
export const ease=(t:number)=>Math.max(0,Math.min(1,t));
export const range=(x:number,a:number,b:number)=>ease((x-a)/(b-a));
export const useF=()=>{const f=useCurrentFrame(),{fps}=useVideoConfig();return f*30/fps;};
export const pop=(f:number,at=0,stiffness=130)=>spring({frame:Math.max(0,f-at),fps:30,config:{damping:15,mass:.85,stiffness}});
export const fp=(f:number,a:number,b:number)=>interpolate(f,[a,b],[0,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp'});
export const numberStyle:React.CSSProperties={fontVariantNumeric:'tabular-nums',fontFamily:'ui-monospace,monospace'};

export const BrandLogo:React.FC<{size?:number}> = ({size=100})=>(
  <Img src={staticFile('brand/Advertio-Logo-Original-Source.png')} 
    style={{width:size,height:size,objectFit:'contain',display:'block',mixBlendMode:'multiply'}}/>
);

export const Backdrop:React.FC=()=>{
 const f=useF();
 return <div style={{position:'absolute',inset:0,overflow:'hidden',background:'radial-gradient(ellipse 47% 62% at 70% 43%, #D9F5FF 0%, #F1FAFF 54%,#FFFFFF 100%)'}}>
  <div style={{position:'absolute',inset:0,opacity:.33,backgroundImage:'linear-gradient(to right, #ACD5ED 1px, transparent 1px), linear-gradient(to bottom,#ACD5ED 1px, transparent 1px)',backgroundSize:'80px 80px',maskImage:'radial-gradient(ellipse at 56% 47%,black, transparent 76%)'}}/>
  <div style={{position:'absolute',inset:0,opacity:.11,backgroundImage:'repeating-radial-gradient(circle at 65% 60%, #8CBBD3 0px,#8CBBD3 1px,transparent 2px,transparent 8px)'}}/>
  <div style={{position:'absolute',top:0,bottom:0,left:`${(f*3.1)%2180-260}px`,width:3,background:'linear-gradient(180deg,transparent,#51DCE9,transparent)',opacity:.24,boxShadow:'0 0 50px #22D3ED',filter:'blur(.4px)'}}/>
  {Array.from({length:25},(_,i)=>{
    const x=(i*117.49+26)%1920,y=(i*263.13+83)%1080;
    const a=.16+.12*Math.sin(i*3+f*.036);
    return <span key={i} style={{position:'absolute',left:x,top:y+Math.sin(f*.032+i)*13,width:i%6===0?6:3,height:i%6===0?6:3,background:i%3===0?C.blue:C.cyan,opacity:a,borderRadius:i%2?'50%':'0'}}/>;
  })}
  <div style={{position:'absolute',left:44,top:36,width:35,height:35,borderLeft:'3px solid #6ED3E5',borderTop:'3px solid #6ED3E5'}}/>
  <div style={{position:'absolute',right:44,top:36,width:35,height:35,borderRight:'3px solid #6ED3E5',borderTop:'3px solid #6ED3E5'}}/>
  <div style={{position:'absolute',left:44,bottom:36,width:35,height:35,borderLeft:'3px solid #6ED3E5',borderBottom:'3px solid #6ED3E5'}}/>
  <div style={{position:'absolute',right:44,bottom:36,width:35,height:35,borderRight:'3px solid #6ED3E5',borderBottom:'3px solid #6ED3E5'}}/>
 </div>
};
export const SmallTag:React.FC<{children:React.ReactNode,light?:boolean}> = ({children,light=false})=><span style={{fontFamily:'ui-monospace,monospace',fontSize:22,letterSpacing:4,color:light?'#C8EEFF':C.blue,fontWeight:700}}>{children}</span>;
export const Persian:React.FC<{children:React.ReactNode,size?:number,color?:string,weight?:number,style?:React.CSSProperties}> = ({children,size=54,color=C.ink,weight=800,style})=>
 <div dir="rtl" style={{fontFamily:F,fontWeight:weight,fontSize:size,color,letterSpacing:-1,lineHeight:1.6,textAlign:'right',...style}}>{children}</div>;

export const TechRings:React.FC<{size?:number,opacity?:number}> = ({size=680,opacity=.75})=>{
 const f=useF();
 return <svg width={size} height={size} viewBox="0 0 700 700" style={{opacity,overflow:'visible'}}>
  <defs><linearGradient id="rg" x1="0" y1="0" x2="1" y2="1"><stop stopColor="#5EDBED"/><stop offset="1" stopColor="#0A64D7"/></linearGradient></defs>
  <g transform={`rotate(${f*.24} 350 350)`} stroke="url(#rg)" fill="none">
   <circle cx="350" cy="350" r="300" strokeWidth="2" strokeDasharray="30 22" opacity=".7"/>
   <circle cx="350" cy="350" r="268" strokeWidth="3" strokeDasharray="4 19" opacity=".47"/>
   <circle cx="350" cy="350" r="236" strokeWidth="2" strokeDasharray="95 56" opacity=".55"/>
  </g>
  <g transform={`rotate(${-f*.37} 350 350)`} fill="none" stroke="#73D7F1" strokeWidth="6" strokeLinecap="round">
   <circle cx="350" cy="350" r="322" strokeDasharray="64 1960" opacity=".85"/>
   <circle cx="350" cy="350" r="210" strokeDasharray="112 1400" opacity=".65"/>
  </g>
  <circle cx="350" cy="350" r="170" stroke="#B6E9FA" strokeWidth="1" fill="none"/>
 </svg>
};
export const Parcel:React.FC<{width?:number}> = ({width=450})=>{
 const f=useF();
 return <svg width={width} viewBox="0 0 520 480" style={{overflow:'visible',filter:'drop-shadow(0 27px 24px rgba(15,54,100,.22))',transform:`translateY(${Math.sin(f*.06)*9}px)`}}>
   <defs>
    <linearGradient id="parcelTop" x1="0" x2="1" y1="0" y2="1"><stop stopColor="#F8D9AE"/><stop offset="1" stopColor="#E6B982"/></linearGradient>
    <linearGradient id="parcelSide" x1="0" y1="0" x2="1" y2="1"><stop stopColor="#C28A56"/><stop offset="1" stopColor="#AB774A"/></linearGradient>
   </defs>
   <path d="M82 134 279 37 467 137 259 243Z" fill="url(#parcelTop)" stroke="#D4A274" strokeWidth="3"/>
   <path d="M82 134 259 243 259 442 82 338Z" fill="#D7A36F" stroke="#BC8956" strokeWidth="3"/>
   <path d="M259 243 467 137 467 336 259 442Z" fill="url(#parcelSide)" stroke="#B77C48" strokeWidth="3"/>
   <path d="M179 87 361 190 361 391 327 408 327 205 144 105Z" fill="#FBE9C6" opacity=".8"/>
   <path d="M110 229 206 284 206 334 110 281Z" fill="#F5E6CA"/>
   <path d="M122 250 190 287 M122 266 180 299 M122 280 168 305" stroke="#AA8B67" strokeWidth="4" opacity=".8"/>
   <path d="M284 281 429 207" stroke="#F3D8AC" strokeWidth="8" opacity=".5"/>
 </svg>
};
export const Person:React.FC<{traveler?:boolean,width?:number}> = ({traveler=false,width=310})=>{
 const f=useF();
 return <svg width={width} viewBox="0 0 350 490" style={{overflow:'visible',filter:'drop-shadow(0 20px 18px rgba(13,51,89,.18))',transform:`translateY(${Math.sin(f*.055+(traveler?2:0))*8}px)`}}>
  <ellipse cx="175" cy="445" rx="118" ry="23" fill="#B9D5E4" opacity=".45"/>
  <path d="M137 254 164 256 163 426 123 426Z" fill="#273C5C"/>
  <path d="M178 256 219 257 226 425 187 425Z" fill="#344F73"/>
  <path d="M115 420h56v22h-75q-7-20 19-22M181 421h58v21h-69q-7-17 11-21" fill="#10243F"/>
  <path d="M122 146 Q175 116 226 155 L237 276 Q175 302 106 276Z" fill={traveler?'#42A8DC':'#F3B4BB'}/>
  <path d="M125 150 99 167 73 292 97 308 148 201" fill={traveler?'#3595C8':'#E8A5AD'}/>
  <path d="M218 150 248 176 260 300 233 307 207 210" fill={traveler?'#3595C8':'#E8A5AD'}/>
  <rect x="71" y="286" width="29" height="38" rx="13" fill="#EAC19F"/>
  <rect x="230" y="291" width="31" height="37" rx="13" fill="#EAC19F"/>
  <circle cx="175" cy="89" r="61" fill="#F0CBA9"/>
  <path d="M116 89 Q105 16 181 19 Q260 27 238 111 Q233 87 221 75 Q184 85 156 53 Q141 88 116 89" fill={traveler?'#243C54':'#513C41'}/>
  <path d="M153 112 Q174 125 197 110" stroke="#AF7A69" strokeWidth="4" fill="none"/>
  <path d="M146 148h55l-24 29Z" fill="#FCF4EF"/>
  {traveler && <g><rect x="246" y="314" width="74" height="116" rx="15" fill="#1E6AAB"/><rect x="267" y="304" width="32" height="15" rx="6" fill="none" stroke="#2B658E" strokeWidth="6"/><path d="M284 332v80" stroke="#70CDE8" strokeWidth="4"/><circle cx="263" cy="431" r="8" fill="#21344D"/><circle cx="303" cy="431" r="8" fill="#21344D"/></g>}
  {!traveler&&<g><path d="M42 299 139 340 130 398 42 361Z" fill="#C89360"/><path d="M139 340 175 309 168 373 130 398Z" fill="#B17E4E"/><path d="M42 299 79 268 175 309 139 340Z" fill="#E6BA88"/><path d="M87 283 182 324" stroke="#F6DAB9" strokeWidth="9"/></g>}
 </svg>
};
export const Plane:React.FC<{width?:number}> = ({width=230})=><svg width={width} viewBox="0 0 320 135" style={{filter:'drop-shadow(0 10px 12px rgba(0,62,143,.14))'}}>
 <path d="M17 74 144 62 229 16 266 14 210 63 305 66 Q317 71 306 79 L208 84 257 118 226 121 146 86 17 83 Q6 81 17 74Z" fill="#F9FCFF" stroke="#2377BB" strokeWidth="5"/>
 <path d="M150 70 220 21 240 19 193 73 239 112 226 113Z" fill="#9BDCF4"/><path d="M28 78 113 75" stroke="#2697DB" strokeWidth="6"/>
 <path d="M102 72h58" stroke="#0876D1" strokeDasharray="6 7" strokeWidth="4"/>
 </svg>;
export const Header:React.FC<{index:string}> = ({index})=> <div style={{position:'absolute',top:34,left:65,right:65,display:'flex',alignItems:'center',justifyContent:'space-between'}}>
 <div style={{display:'flex',alignItems:'center',gap:18}}><BrandLogo size={65}/><div><div style={{fontFamily:'Knewave,Impact,sans-serif',fontSize:35,color:C.navy,letterSpacing:1}}>ADVERTIO <span style={{color:C.blue}}>CARGO</span></div><div style={{fontFamily:'ui-monospace,monospace',fontSize:15,letterSpacing:3,color:C.muted}}>CONNECTION PLATFORM</div></div></div>
 <div style={{fontFamily:'ui-monospace,monospace',fontSize:22,color:C.blue,letterSpacing:2}}>SECURE LINK / {index} / 05</div>
 </div>;
export const Footer:React.FC<{progress:number}> = ({progress})=><div style={{position:'absolute',left:70,right:70,bottom:34,display:'flex',justifyContent:'space-between',alignItems:'center',fontFamily:'ui-monospace,monospace',fontSize:20,color:C.muted}}>
 <span>ADVERTIO.NET / AIR TRAVEL NETWORK</span><div style={{width:450,height:6,borderRadius:20,background:'#D2E7F1',overflow:'hidden'}}><div style={{width:(Math.max(0,Math.min(1,progress))*100)+'%',height:6,background:'linear-gradient(90deg,#0E6FE0,#22D5E5)'}}/></div><span>00 : 20</span>
 </div>;
