import React from 'react';
import {useF} from './components';

/**
 * An intentionally unbranded commercial twin-engine airliner, drawn nose-right.
 * All geometry is created by original SVG code: no stock silhouettes, raster layers
 * or synthetic Advertio logos. The caller rotates it to the route tangent.
 */
export const AirlinerDetailed:React.FC<{width?:number}> = ({width=500})=>{
 const f=useF();
 const flash=.65+.35*Math.max(0,Math.sin(f*.16));
 return <svg width={width} height={width*.5} viewBox="0 0 680 340"
   role="img" aria-label="Detailed unbranded commercial passenger aircraft, nose pointing right"
   style={{display:'block',overflow:'visible',filter:'drop-shadow(0 19px 17px rgba(8,56,114,.26))'}}>
 <defs>
  <linearGradient id="av-aircraft-fuselage" x1="0" y1="0" x2="0" y2="1">
   <stop stopColor="#86C0DD"/><stop offset=".17" stopColor="#ECFAFF"/>
   <stop offset=".40" stopColor="#FFFFFF"/><stop offset=".60" stopColor="#F2FAFD"/>
   <stop offset=".81" stopColor="#CCDFEC"/><stop offset="1" stopColor="#699FC4"/>
  </linearGradient>
  <linearGradient id="av-aircraft-mainwing" x1=".2" y1="0" x2=".8" y2="1">
   <stop stopColor="#F6FEFF"/><stop offset=".28" stopColor="#DFEFF8"/>
   <stop offset=".66" stopColor="#9DC8E2"/><stop offset="1" stopColor="#629CC5"/>
  </linearGradient>
  <linearGradient id="av-aircraft-motor" x1="0" y1="0" x2=".1" y2="1">
   <stop stopColor="#F8FDFF"/><stop offset=".43" stopColor="#D7ECF8"/>
   <stop offset=".75" stopColor="#98B9CF"/><stop offset="1" stopColor="#6D95AE"/>
  </linearGradient>
  <linearGradient id="av-aircraft-fin" x1="0" y1="0" x2="1" y2="1"><stop stopColor="#E3FBFF"/><stop offset=".6" stopColor="#6BB3DA"/><stop offset="1" stopColor="#1477B6"/></linearGradient>
  <linearGradient id="av-aircraft-gloss" x1="0" y1="0" x2="1" y2="0"><stop stopColor="#FFFFFF" stopOpacity=".01"/><stop offset=".45" stopColor="#FFFFFF" stopOpacity=".5"/><stop offset="1" stopColor="#FFFFFF" stopOpacity=".04"/></linearGradient>
 </defs>
 {/* Tailplane is behind fuselage; rear stabilizers remain aerodynamically swept. */}
 <path d="M119 156 44 49 61 39 180 150 190 171 180 189 60 304 42 294 116 183Z"
  fill="url(#av-aircraft-mainwing)" stroke="#4A85AD" strokeWidth="3.8"/>
 <path d="M42 49 36 31 52 34 61 39 M42 294 36 312 52 308 60 304" stroke="#187EC2" strokeWidth="7" fill="#2D96CA"/>
 <path d="M80 89 146 154 M80 253 146 186" stroke="#8EB7D3" strokeWidth="3"/>
 <path d="M67 103 124 155 M67 238 124 185" stroke="#6BA5CD" strokeWidth="2" strokeDasharray="9 6"/>
 <path d="M129 166 81 118 112 111 174 165Z" fill="url(#av-aircraft-fin)" stroke="#3F92BD" strokeWidth="2.6"/>
 <path d="M129 175 81 222 111 229 174 177Z" fill="#5BADD9" stroke="#3F92BD" strokeWidth="2.6"/>

 {/* Long swept wings with independently delineated flaps, spoilers and winglets. */}
 <path d="M280 157 192 15 222 12 483 152 483 165Z" fill="url(#av-aircraft-mainwing)" stroke="#427EAC" strokeWidth="4" strokeLinejoin="round"/>
 <path d="M192 15 184 0 196 3 222 12" fill="#0C79B9" stroke="#388DBD" strokeWidth="3"/>
 <path d="M281 182 192 325 222 328 483 188 483 174Z" fill="url(#av-aircraft-mainwing)" stroke="#427EAC" strokeWidth="4" strokeLinejoin="round"/>
 <path d="M192 325 184 340 196 336 222 328" fill="#0C79B9" stroke="#388DBD" strokeWidth="3"/>
 <path d="M227 35 451 159 350 154 225 70Z" fill="#FFFFFF" opacity=".40"/>
 <path d="M227 305 451 182 350 186 225 270Z" fill="#F5FDFF" opacity=".30"/>
 {/* Wing leading edges, slats, spoilers, structural ribs. */}
 <path d="M227 39 434 152 M227 301 434 188" stroke="#FFFFFF" strokeWidth="6" opacity=".82" strokeLinecap="round"/>
 <path d="M239 67 384 153 M239 273 384 186" stroke="#5A9DC6" strokeWidth="2.5" opacity=".85"/>
 <path d="M249 88 272 151 M291 96 319 151 M336 118 354 153 M379 143 387 157"
  stroke="#437FA5" strokeWidth="3.0" opacity=".7"/>
 <path d="M249 252 272 190 M291 244 319 190 M336 222 354 187 M379 197 387 183"
  stroke="#437FA5" strokeWidth="3.0" opacity=".7"/>
 <path d="M201 46 213 37 249 89 239 94Z M201 294 213 303 249 251 239 246Z" fill="#6EB6DA" opacity=".75"/>
 {/* Aileron separation lines on the trailing outer wing panels. */}
 <path d="M207 65 239 86 253 114 M207 275 239 254 253 226" stroke="#327FAE" strokeWidth="3" fill="none" strokeDasharray="8 4"/>
 <path d="M303 139 322 154 380 154 M303 201 322 185 380 185" stroke="#9FD5EE" strokeWidth="4" fill="none"/>

 {/* Engine pylons beneath the fuselage and both swept wings. */}
 <path d="M328 117 366 111 390 123 349 148Z M328 223 366 228 390 216 349 190Z" fill="#8FB8D0" stroke="#609ABE" strokeWidth="2.5"/>
 {/* Upper nacelle and inlet rings; nose points towards +X. */}
 <path d="M310 89 Q311 69 344 66 L401 69 Q425 83 409 100 L345 105 Q322 104 310 89Z" fill="url(#av-aircraft-motor)" stroke="#397AA6" strokeWidth="3.4"/>
 <path d="M314 89 Q332 74 366 76 L388 76" fill="none" stroke="#FFFFFF" strokeWidth="5" opacity=".8"/>
 <ellipse cx="403" cy="85" rx="13" ry="17" fill="#EAF6FC" stroke="#5C93B6" strokeWidth="3"/>
 <ellipse cx="406" cy="85" rx="9" ry="12" fill="#213F5C"/>
 <ellipse cx="406" cy="85" rx="3" ry="4.5" fill="#D8F8FF"/>
 {Array.from({length:8},(_,i)=>{
  const a=2*Math.PI*i/8;
  return <path key={'upper'+i} d={'M406 85 l'+(Math.cos(a)*8).toFixed(2)+' '+(Math.sin(a)*10).toFixed(2)} stroke="#74ABCC" strokeWidth="1.8"/>;
 })}
 <path d="M325 75V100 M349 68V105" stroke="#729DBA" strokeWidth="2" opacity=".5"/>
 {/* Lower nacelle mirrors the upper engine, with symmetric fan. */}
 <path d="M310 251 Q311 271 344 274 L401 271 Q425 257 409 240 L345 235 Q322 236 310 251Z" fill="url(#av-aircraft-motor)" stroke="#397AA6" strokeWidth="3.4"/>
 <path d="M314 251 Q332 266 366 264 L388 264" fill="none" stroke="#FFFFFF" strokeWidth="5" opacity=".8"/>
 <ellipse cx="403" cy="255" rx="13" ry="17" fill="#EAF6FC" stroke="#5C93B6" strokeWidth="3"/>
 <ellipse cx="406" cy="255" rx="9" ry="12" fill="#213F5C"/>
 <ellipse cx="406" cy="255" rx="3" ry="4.5" fill="#D8F8FF"/>
 {Array.from({length:8},(_,i)=>{
  const a=2*Math.PI*i/8;
  return <path key={'lower'+i} d={'M406 255 l'+(Math.cos(a)*8).toFixed(2)+' '+(Math.sin(a)*10).toFixed(2)} stroke="#74ABCC" strokeWidth="1.8"/>;
 })}
 <path d="M325 264V240 M349 271V235" stroke="#729DBA" strokeWidth="2" opacity=".5"/>

 {/* Fuselage with nose cone and illuminated upper/lower shoulders. */}
 <path d="M61 154 Q81 146 131 145 L512 145
   Q562 145 607 152 Q638 160 657 168 Q664 170 657 173
   Q637 183 608 188 Q564 195 512 195 L131 195
   Q80 194 61 186 Q47 176 48 169 Q48 160 61 154Z"
  fill="url(#av-aircraft-fuselage)" stroke="#3779A5" strokeWidth="4.5"/>
 <path d="M85 151 Q263 145 510 151 Q594 152 641 167" fill="none" stroke="#FFFFFF" strokeWidth="6" opacity=".72"/>
 <path d="M86 189 Q263 194 510 189 Q594 188 641 173" fill="none" stroke="#74A4C2" strokeWidth="3" opacity=".6"/>
 <path d="M83 168 Q321 169 645 169" stroke="#0E7DCA" strokeWidth="7" opacity=".90"/>
 <path d="M99 176 Q352 178 642 174" stroke="#4EC8E9" strokeWidth="2.5" opacity=".95"/>
 <path d="M210 152 L210 188 M522 151 L522 190" stroke="#BEDCE9" strokeWidth="2" opacity=".42"/>
 {/* Cabin windows are paired and individually framed. */}
 {Array.from({length:32},(_,i)=>{
  const x=125+i*13.65;
  return <g key={i}>
   <rect x={x} y="151" width="7.3" height="5.5" rx="2.5" fill="#1E557A" stroke="#D9F8FF" strokeWidth="1.1"/>
   <path d={'M'+(x+1.4)+' 152.1h3.6'} stroke="#8FD4EC" strokeWidth=".8"/>
   <rect x={x} y="184" width="7.3" height="5.5" rx="2.5" fill="#1E557A" stroke="#D9F8FF" strokeWidth="1.1"/>
   <path d={'M'+(x+1.4)+' 185.1h3.6'} stroke="#8FD4EC" strokeWidth=".8"/>
  </g>;
 })}
 {/* Passenger entry and service doors, door handles and emergency exit outlines. */}
 {([110,480,546] as const).map((x,i)=><g key={x} stroke="#548EB5" strokeWidth="2" fill="none">
   <rect x={x} y={i===2?174:148} width={i===2?12:16} height={i===2?17:19} rx="3"/>
   <path d={'M'+(x+3)+' '+(i===2?183:158)+'h5'} strokeWidth="1.7"/>
  </g>)}
 <path d="M270 146v22 M282 148v20 M349 147v20" stroke="#75ACC8" strokeWidth="2.4" opacity=".7"/>
 {/* Cockpit glazing must stay near the forward/right nose, not at the tail. */}
 <path d="M575 150 Q596 152 613 162 L610 166 L570 166Z" fill="#234B6F" stroke="#6CA7C7" strokeWidth="2.2"/>
 <path d="M575 190 Q595 187 612 178 L609 174 L570 174Z" fill="#234B6F" stroke="#6CA7C7" strokeWidth="2.2"/>
 <path d="M581 153 600 158 M582 187 600 182" stroke="#83CDE6" strokeWidth="2.3"/>
 <path d="M610 166 618 170 610 174" fill="#B8EFFF"/>
 <path d="M652 169 Q658 170 653 172" stroke="#0D5C98" strokeWidth="2.6" fill="none"/>
 {/* Vents, seams, antenna, nose sensor and in-flight landing gear panel. */}
 <path d="M78 162v16 M302 159h31 M302 183h31 M457 163h25 M457 177h25"
   stroke="#578EB0" strokeWidth="1.8" opacity=".72"/>
 <path d="M151 145 l13 -9 18 9 M518 145 l15 -7 12 8" fill="#E5F5FC" stroke="#5590B6" strokeWidth="2"/>
 <path d="M488 170h39" stroke="#9FC8DF" strokeWidth="2.4" strokeDasharray="4 4"/>
 {/* Stylized neutral aircraft livery is NOT the Advertio logo. */}
 <path d="M73 156 Q98 149 121 151 L127 189 Q98 191 73 184Z" fill="#237BB2" opacity=".52"/>
 <path d="M95 153 105 189" stroke="#A8EEFC" strokeWidth="4" opacity=".8"/>
 <path d="M194 169 213 169 213 177 194 177Z" fill="#E5F6FC" opacity=".75"/>
 <path d="M244 169 264 169 M426 170 445 170" stroke="#E9FCFF" strokeWidth="2" opacity=".7"/>
 {/* FAA-style navigation colors: red left side, green right side, strobe white. */}
 <g opacity={flash}>
  <circle cx="191" cy="8" r="7" fill="#F25166"/>
  <circle cx="191" cy="331" r="7" fill="#35CFA7"/>
  <circle cx="649" cy="170" r="5.5" fill="#FFFFFF" stroke="#2AA0CB" strokeWidth="2"/>
  <circle cx="83" cy="170" r="4" fill="#DFFBFF"/>
 </g>
 <path d="M190 8h-17 M191 330h-17" stroke="#F7FDFF" strokeWidth="1.6" opacity=".7"/>
 </svg>;
};

/** Highly finished 3D isometric package, postal details and printed label. */
export const CargoParcelDetailed:React.FC<{width?:number}> = ({width=530})=>{
 const f=useF();
 return <svg width={width} height={width*440/540} viewBox="0 0 540 440"
  style={{overflow:'visible',display:'block',filter:'drop-shadow(0 28px 21px rgba(72,86,113,.23))',transform:'translateY('+Math.sin(f*.055)*11+'px)'}}>
  <defs>
   <linearGradient id="parcel-front" x1="0" y1="0" x2=".2" y2="1"><stop stopColor="#E4B77F"/><stop offset="1" stopColor="#BB854F"/></linearGradient>
   <linearGradient id="parcel-right" x1="0" y1="0" x2=".6" y2="1"><stop stopColor="#C78C59"/><stop offset="1" stopColor="#9F693C"/></linearGradient>
   <linearGradient id="parcel-top" x1="0" y1="0" x2="1" y2="1"><stop stopColor="#FFE9C9"/><stop offset="1" stopColor="#D6A66F"/></linearGradient>
  </defs>
  <ellipse cx="269" cy="411" rx="204" ry="22" fill="#9FB4C2" opacity=".29"/>
  <path d="M63 104 264 15 472 111 269 215Z" fill="url(#parcel-top)" stroke="#BF8757" strokeWidth="3"/>
  <path d="M63 104 269 215 269 406 63 298Z" fill="url(#parcel-front)" stroke="#B27A47" strokeWidth="3"/>
  <path d="M269 215 472 111 472 299 269 406Z" fill="url(#parcel-right)" stroke="#A77343" strokeWidth="3"/>
  {/* Fold bevels and folded corners. */}
  <path d="M63 104 74 110 74 293 63 298Z" fill="#E8BA89" opacity=".8"/>
  <path d="M269 215 279 210 279 398 269 406Z" fill="#F8D7A6" opacity=".5"/>
  <path d="M63 104 264 15 472 111" fill="none" stroke="#FFEED5" strokeWidth="8" opacity=".55"/>
  {/* Wide real-looking adhesive tape across the lid and front. */}
  <path d="M175 54 383 158 347 177 143 69Z" fill="#FFF0D5" stroke="#D3B78F" strokeWidth="2"/>
  <path d="M143 69 175 54 175 120 143 140Z" fill="#FCEBD0" opacity=".82"/>
  <path d="M347 177 383 158 383 336 347 353Z" fill="#F3D9AE" opacity=".86"/>
  <path d="M218 75 258 95 M285 111 334 134" stroke="#C6A57F" strokeWidth="2.5" opacity=".48"/>
  {/* Printed fragile icon and handling marks on front. */}
  <rect x="89" y="179" width="128" height="112" rx="6" fill="#FEF4E1" stroke="#A57B59" strokeWidth="2.3" transform="skewY(27)"/>
  <g transform="translate(102 229) skewY(27)" stroke="#56758A" strokeWidth="3.1" fill="none" strokeLinecap="round">
   <path d="M21 0 39 0 39 23 31 32 21 23Z M30 32v21 M18 53h25"/>
   <path d="M68 0v51 M56 16 68 2 80 16 M92 2v51 M80 16 92 2 104 16"/>
  </g>
  {/* Shipping label with barcode, route and scan tag on right side. */}
  <path d="M298 245 444 169 444 272 298 350Z" fill="#F9F9F3" stroke="#D7C3AA" strokeWidth="2.4"/>
  <path d="M307 259 430 195 M307 266 396 220" stroke="#7C91A0" strokeWidth="3" opacity=".7"/>
  {Array.from({length:21},(_,i)=>{
   const x=311+i*5.1;
   return <path key={i} d={'M'+x+' '+(299-i*2.6)+' l0 31'} stroke="#1D3950" strokeWidth={i%4===0?3.2:1.5} opacity=".83" transform="skewY(-26)"/>;
  })}
  <path d="M313 335 428 276" stroke="#0C6A9D" strokeWidth="3" strokeDasharray="6 8"/>
  <g fill="#0B6498" fontSize="16" fontFamily="ui-monospace,monospace" fontWeight="700">
   <text x="318" y="239" transform="rotate(-27 318 239)">AIR / DOCUMENTS</text>
  </g>
  {/* Sealing ribbons, realistic scuff marks and depth lines. */}
  <path d="M282 215 459 126" stroke="#FFE3BA" strokeWidth="2" opacity=".75"/>
  <path d="M79 303 250 391" stroke="#9C6A42" strokeWidth="2" opacity=".45"/>
  <path d="M285 394 461 302" stroke="#754D2D" strokeWidth="2" opacity=".29"/>
  </svg>;
};

/** Decorative micro-data HUD, deliberately WITHOUT a counter at top. */
export const TechnicalPill:React.FC<{label:string,sub?:string,accent?:boolean}> = ({label,sub,accent=false})=>
 <div style={{display:'flex',alignItems:'center',gap:13,padding:'13px 19px',border:'1.5px solid '+(accent?'#66CFE9':'#C8E9F6'),borderRadius:14,background:'rgba(248,253,255,.93)',boxShadow:'0 10px 30px #12548D16'}}>
  <span style={{width:8,height:8,borderRadius:'50%',background:accent?'#21CDD8':'#4E9CDB',boxShadow:accent?'0 0 10px #20C9D8':'none'}}/>
  <div><div style={{fontSize:18,fontFamily:'ui-monospace,monospace',fontWeight:800,color:'#0B477F',letterSpacing:1}}>{label}</div>
   {sub&&<div style={{fontFamily:'Vazirmatn,Arial,sans-serif',fontSize:17,color:'#6C849A',direction:'rtl'}}>{sub}</div>}
  </div>
 </div>;
