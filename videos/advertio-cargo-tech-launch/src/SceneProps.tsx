import React from 'react';
import {C,F,useF} from './components';

export const TerminalBackdrop:React.FC<{variant?:'yyz'|'ika'}> = ({variant='yyz'})=>{
 const f=useF();const isCanada=variant==='yyz';
 return <svg width="440" height="340" viewBox="0 0 440 340" style={{overflow:'hidden',display:'block'}}>
 <defs>
  <linearGradient id={'terminal'+variant} x1="0" y1="0" x2="1" y2="1"><stop stopColor="#F7FEFF"/><stop offset="1" stopColor="#C5E6F6"/></linearGradient>
 </defs>
 <path d="M0 230 168 151 438 229 280 340Z" fill="#D9EFF9" opacity=".75"/>
 <path d="M30 255 191 181 393 242 225 323Z" fill="#C6DFEB" opacity=".65" stroke="#A9D2E7" strokeWidth="2"/>
 {/* Terminal buildings and transparent multi-level curtain wall. */}
 <path d="M127 132 260 72 404 117 270 183Z" fill="#FCFEFF" stroke="#93C4E2" strokeWidth="2"/>
 <path d="M127 132 270 183 270 250 127 198Z" fill={`url(#terminal${variant})`} stroke="#75A9C9" strokeWidth="2.3"/>
 <path d="M270 183 404 117 404 187 270 250Z" fill="#A7CDE4" stroke="#79AACA" strokeWidth="2"/>
 {Array.from({length:6},(_,i)=><g key={i}>
  <path d={'M'+(142+i*20)+' '+(144+i*7.2)+' v45'} stroke="#7CAFD0" strokeWidth="2"/>
  <path d={'M'+(287+i*17)+' '+(177-i*8.2)+' v55'} stroke="#7BAECB" strokeWidth="2"/>
 </g>)}
 <path d="M130 174 268 223 400 159" stroke="#9DD8EE" strokeWidth="3" fill="none"/>
 <path d="M142 201 275 251 406 188" stroke="#6CA1BE" strokeWidth="3" fill="none" opacity=".48"/>
 {/* Tower, beacon, windows and taxiway marking. */}
 <path d="M66 211 66 96 106 76 142 96 142 179Z" fill="#D0EAF7" stroke="#80ADCB" strokeWidth="2"/>
 <path d="M66 96 106 76 142 96 101 115Z" fill="#FFFFFF"/>
 <path d="M101 115 142 96 142 179 101 199Z" fill="#A6D3E8"/>
 <path d="M95 80 95 55 109 49 117 76" stroke="#4A9CC9" strokeWidth="4" fill="#BFE9F8"/>
 <circle cx="107" cy="49" r={4+Math.sin(f*.16)*.8} fill="#44DAEA"/>
 {Array.from({length:5},(_,i)=><rect key={i} x={76+i*10} y={118+i*2} width="6" height="9" fill="#81BEDD" opacity=".85"/>)}
 <path d="M4 284 150 218 217 239 71 310Z" fill="#B4D3E3" stroke="#7DB2CD" strokeWidth="2"/>
 <path d="M31 283 137 237 M64 295 172 249" stroke="#F9FDFF" strokeWidth="4" strokeDasharray="15 12"/>
 <path d="M290 276 358 241 429 265" fill="none" stroke="#7DB8D7" strokeWidth="5" strokeDasharray="8 8"/>
 {/* Baggage cart: four wheels, rails and parcel load. */}
 <g transform="translate(302 263)">
  <path d="M0 10 67 10 73 26 4 26Z" fill="#6C9BBB"/>
  <path d="M6 10 13-5 51-5 63 10" fill="#B9D5E6" stroke="#6198B7" strokeWidth="2"/>
  <path d="M13-5 31-14 48-5 29 4Z" fill="#E9C59F"/>
  <path d="M29 4 48-5 48 8 29 18Z" fill="#CDA078"/>
  <circle cx="12" cy="27" r="6" fill="#315A79"/><circle cx="57" cy="27" r="6" fill="#315A79"/>
 </g>
 <rect x="305" y="41" width="115" height="35" rx="10" fill="#FFFFFF" stroke="#93CBE3" strokeWidth="2"/>
 <text x="362" y="64" textAnchor="middle" fontFamily="ui-monospace,monospace" fontSize="18" fontWeight="bold" fill="#0A609F">{isCanada?'TORONTO YYZ':'TEHRAN IKA'}</text>
 </svg>;
};

export const AirportDistrict:React.FC<{city:'TORONTO'|'TEHRAN'}> = ({city})=>{
 const f=useF(),iran=city==='TEHRAN';
 return <svg width="280" height="270" viewBox="0 0 280 270" style={{display:'block',filter:'drop-shadow(0 11px 15px rgba(12,72,115,.13))'}}>
 <defs><linearGradient id={'district'+city} x1="0" y1="0" x2="1" y2="1"><stop stopColor="#EFFCFF"/><stop offset="1" stopColor="#9DCADE"/></linearGradient></defs>
 <ellipse cx="137" cy="226" rx="117" ry="24" fill="#91C6E0" opacity=".38"/>
 <path d="M13 174 132 114 274 184 142 250Z" fill="#C9E5F3" stroke="#80B8D4" strokeWidth="2.5"/>
 <path d="M35 178 136 126 245 183 142 238Z" stroke="#F8FDFF" strokeWidth="4" fill="none" strokeDasharray="14 8"/>
 <path d="M21 215 127 158 252 218" stroke="#73B6D8" strokeWidth="5" strokeDasharray="9 10" fill="none"/>
 {/* Main terminal and check-in concourse */}
 <path d="M95 108 156 74 230 109 164 148Z" fill="#FFFFFF" stroke="#6FA5C7" strokeWidth="2.5"/>
 <path d="M95 108 164 148 164 194 95 156Z" fill="#BCDFF1" stroke="#76A9C8" strokeWidth="2"/>
 <path d="M164 148 230 109 230 157 164 194Z" fill="#8FBFDA" stroke="#689CBF" strokeWidth="2"/>
 {Array.from({length:5},(_,i)=><g key={i}>
  <path d={'M'+(106+i*11)+' '+(125+i*6.2)+' v30'} stroke="#6EA4C4" strokeWidth="3"/>
  <path d={'M'+(176+i*10)+' '+(145-i*6)+' v32'} stroke="#C4E8F7" strokeWidth="3"/>
 </g>)}
 {/* Control tower with cab and operating beacon */}
 <path d="M44 144V77l26-12 29 14v62l-26 13Z" fill={`url(#district${city})`} stroke="#669DBC" strokeWidth="2"/>
 <path d="M44 77 70 65 99 79 72 91Z" fill="#F7FDFF"/>
 <path d="M72 91 99 79v62l-26 13Z" fill="#7BAECC"/>
 <path d="M55 73V53l15-7 17 8v21" fill="#D5F3FB" stroke="#65A6CA" strokeWidth="3"/>
 <path d="M52 51 68 44 87 52 70 61Z" fill="#F8FDFF"/>
 <circle cx="70" cy="43" r="4" fill={iran?'#38C6C0':'#F7817D'} opacity={.7+.3*Math.sin(f*.2)}/>
 {/* Parked aircraft on apron. It is intentionally stationary at the terminal. */}
 <g transform="translate(136 204) rotate(-25)">
  <path d="M-28 -4 17 -4 40-12 46-10 30-1 49 1 51 6 30 8 43 19 35 21 16 11-28 11-37 5Z" fill="#FFFFFF" stroke="#237CB7" strokeWidth="2"/>
  <path d="M-14 -2-30 -17-35 -17-27 4-35 21-30 21-14 8" fill="#9AD1E8" stroke="#338BB8" strokeWidth="1.5"/>
 </g>
 {/* Airside vegetation and light poles */}
 {[[33,170],[257,177],[81,223],[215,217]].map(([x,y],i)=><g key={i}>
  <path d={'M'+x+' '+y+'v-15'} stroke="#75A0B3" strokeWidth="2"/>
  <circle cx={x} cy={y-18} r="6" fill="#8DD2C0"/>
 </g>)}
 <rect x="58" y="243" width="165" height="25" rx="11" fill="#F7FCFF" stroke="#B5DAE9" strokeWidth="2"/>
 <text x="141" y="260" fontFamily="ui-monospace,monospace" fontSize="17" fill="#165681" fontWeight="bold" textAnchor="middle">{city} / {iran?'IKA':'YYZ'}</text>
 </svg>;
};

export const DocumentAndPassport:React.FC=()=> <svg width="225" height="178" viewBox="0 0 225 178" style={{filter:'drop-shadow(0 9px 7px rgba(34,79,124,.18))'}}>
 <g transform="rotate(-11 100 88)">
  <rect x="70" y="9" width="126" height="153" rx="13" fill="#1B5489" stroke="#123B67" strokeWidth="3"/>
  <path d="M85 33h96M85 41h96" stroke="#83C8EA" opacity=".7"/>
  <circle cx="133" cy="79" r="21" stroke="#F3CE7C" strokeWidth="2.4" fill="none"/>
  <path d="M112 79h42M133 58v42M118 65q20 15 31 27" stroke="#F3CE7C" strokeWidth="1.6" fill="none"/>
  <path d="M101 132h65" stroke="#DDBB76" strokeWidth="4"/>
 </g>
 <g transform="rotate(8 60 70)">
  <rect x="18" y="21" width="116" height="126" rx="6" fill="#FFFFFF" stroke="#B9D9E6" strokeWidth="3"/>
  <path d="M39 46h76M39 58h61M39 68h72" stroke="#7CB3D1" strokeWidth="4" opacity=".8"/>
  <rect x="37" y="83" width="78" height="49" rx="4" fill="#EDF6F9"/>
  {Array.from({length:14},(_,i)=><path key={i} d={'M'+(43+i*5)+' 89v35'} stroke="#234E69" strokeWidth={i%3===0?2.7:1}/>)}
 </g>
 </svg>;
