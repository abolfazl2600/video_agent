import React from 'react';
import {BrandLogo,C,F,useF} from './components';

/**
 * Fully authored mock UI: intentionally NOT an actual Advertio listing.
 * Every fake route or status is tagged as DEMO; no invented prices or dates.
 */
export const ProductPhone:React.FC<{width?:number}> = ({width=580})=>{
 const f=useF(),scale=width/580, P=(v:number)=>v*scale;
 const rows=[
  {k:'مبدأ',v:'تورنتو، کانادا',icon:'⌖'},
  {k:'مقصد',v:'تهران، ایران',icon:'◎'},
  {k:'نوع مرسوله',v:'بسته و مدارک',icon:'▣'},
  {k:'هماهنگی',v:'گفت‌وگوی مستقیم',icon:'◇'}
 ];
 return <div style={{width,height:width*1.93,borderRadius:P(70),padding:P(18),
  position:'relative',boxSizing:'border-box',
  background:'linear-gradient(118deg,#0B1C35 2%,#52728D 35%,#10263F 63%,#06162D 100%)',
  border:P(2)+'px solid #425F7B',
  boxShadow:'inset 0 0 0 2px #B9D0DB, inset 6px 0 9px #FFFFFF24, 25px 38px 78px rgba(6,47,105,.35)',
  transform:'translateY('+Math.sin(f*.035)*8+'px) rotateZ('+Math.sin(f*.018)*.7+'deg)'}}>
  {/* Visible metal side buttons and camera island; not merely a frame. */}
  <div style={{position:'absolute',left:-P(6),top:P(165),height:P(65),width:P(6),background:'#688CA7',borderRadius:P(3)}}/>
  <div style={{position:'absolute',left:-P(6),top:P(258),height:P(88),width:P(6),background:'#567D9B',borderRadius:P(3)}}/>
  <div style={{position:'absolute',right:-P(6),top:P(272),height:P(95),width:P(6),background:'#567D9B',borderRadius:P(3)}}/>
  <div style={{height:'100%',width:'100%',borderRadius:P(51),background:'linear-gradient(180deg,#FBFEFF 0%,#FFFFFF 76%,#F5FAFE 100%)',
     overflow:'hidden',fontFamily:F,direction:'rtl',position:'relative'}}>
   <div style={{height:P(42),display:'flex',justifyContent:'space-between',alignItems:'center',padding:'0 '+P(26)+'px'}}>
    <span style={{fontFamily:'ui-monospace,monospace',fontSize:P(13),color:'#315777',letterSpacing:P(1)}}>LTE ◉ ▰</span>
    <span style={{width:P(110),height:P(24),background:'#0A1D33',borderRadius:P(20),display:'flex',alignItems:'center',justifyContent:'flex-end',paddingRight:P(10)}}>
     <span style={{height:P(7),width:P(7),borderRadius:'50%',background:'#1E465F',border:P(1)+'px solid #385D75'}}/>
    </span>
    <span style={{fontFamily:'ui-monospace,monospace',fontSize:P(13),color:'#315777'}}>•••</span>
   </div>
   <div style={{display:'flex',alignItems:'center',gap:P(14),padding:P(17)+'px '+P(24)+'px '+P(20)+'px',borderBottom:P(1.5)+'px solid #E0EBF3'}}>
    <BrandLogo size={P(64)}/>
    <div style={{flex:1}}>
     <div style={{fontSize:P(32),fontWeight:900,color:C.navy,lineHeight:1.5}}>ادورتیو <span style={{color:C.blue}}>کارگو</span></div>
     <div style={{fontFamily:'ui-monospace,monospace',fontSize:P(13),color:'#7894A7',letterSpacing:P(1.1),direction:'ltr',textAlign:'right'}}>DIRECT TRAVELER CONNECTION</div>
    </div>
    <div style={{width:P(40),height:P(40),borderRadius:'50%',border:P(2)+'px solid #D3E9F6',display:'flex',alignItems:'center',justifyContent:'center',color:C.blue,fontSize:P(22),fontWeight:900}}>⌕</div>
   </div>
   <div style={{padding:P(20)+'px '+P(27)+'px 0',display:'flex',alignItems:'center',justifyContent:'space-between'}}>
    <div style={{fontSize:P(29),fontWeight:900,color:C.navy}}>ارسال بار مسافری</div>
    <div style={{borderRadius:P(11),padding:P(6)+'px '+P(10)+'px',fontSize:P(14),fontWeight:900,color:'#087FA2',background:'#E5F8FC',border:P(1)+'px solid #9DE0EB'}}>نمونه نمایشی</div>
   </div>
   {/* Tiny isometric cargo thumbnail + animated route card. */}
   <div style={{margin:P(16)+'px '+P(25)+'px 0',padding:P(16),borderRadius:P(21),background:'linear-gradient(145deg,#EAF7FE,#F9FDFF)',
    border:P(1.5)+'px solid #D7EBF5',minHeight:P(167),position:'relative'}}>
    <div style={{display:'flex',alignItems:'center',justifyContent:'space-between',direction:'ltr'}}>
     <div><div style={{fontSize:P(13),fontFamily:'ui-monospace,monospace',color:C.muted,letterSpacing:1}}>FROM / YYZ</div>
      <div style={{fontFamily:F,fontWeight:900,fontSize:P(23),color:C.navy,direction:'rtl'}}>تورنتو</div>
     </div>
     <div style={{fontFamily:'ui-monospace,monospace',fontSize:P(22),color:'#0C80D9',fontWeight:900,transform:'translateY('+Math.sin(f*.08)*P(2)+'px)'}}>✈ ┄ ┄ →</div>
     <div><div style={{fontSize:P(13),fontFamily:'ui-monospace,monospace',color:C.muted,letterSpacing:1,textAlign:'right'}}>TO / THR</div>
      <div style={{fontFamily:F,fontWeight:900,fontSize:P(23),color:C.navy,direction:'rtl'}}>تهران</div>
     </div>
    </div>
    <div style={{height:P(2),margin:P(12)+'px 0',background:'linear-gradient(90deg,#8BC0DF,#2FBFDF,#78B7E2)'}}/>
    <div style={{display:'flex',alignItems:'center',justifyContent:'space-between',gap:P(12)}}>
     <svg width={P(80)} height={P(62)} viewBox="0 0 80 62">
      <path d="M4 24 40 7 76 24 39 45Z" fill="#EFD4AA" stroke="#BA916A" strokeWidth="2"/>
      <path d="M4 24 39 45 39 60 4 40Z" fill="#D5AC7B"/>
      <path d="M39 45 76 24 76 40 39 60Z" fill="#B98956"/>
      <path d="M25 14 61 35 53 39 17 18Z" fill="#FFF2D8"/>
     </svg>
     <div style={{flex:1}}>
      <div style={{fontSize:P(19),color:C.navy,fontWeight:850}}>بسته / مدارک</div>
      <div style={{fontSize:P(14),color:C.muted}}>ارتباط با مسافر مسیر</div>
     </div>
     <div style={{padding:P(6)+'px '+P(11)+'px',background:'#DDF7F1',borderRadius:P(12),color:'#167D75',fontSize:P(13),fontWeight:850}}>DEMO</div>
    </div>
   </div>
   <div style={{margin:P(15)+'px '+P(27)+'px 0',borderRadius:P(18),background:'#FFFFFF',border:P(1.5)+'px solid #DDEBF4',padding:'0 '+P(17)+'px'}}>
    {rows.map((line,i)=><div key={line.k} style={{padding:P(13)+'px '+P(3)+'px',borderBottom:i===rows.length-1?'none':P(1)+'px solid #E5EDF3',
     display:'flex',alignItems:'center',gap:P(12)}}>
     <div style={{width:P(27),height:P(27),background:'#EBF8FF',borderRadius:P(8),color:C.blue,textAlign:'center',fontSize:P(20)}}>{line.icon}</div>
     <span style={{fontSize:P(16),color:C.muted,flex:1}}>{line.k}</span>
     <b style={{fontSize:P(19),color:C.navy,whiteSpace:'nowrap'}}>{line.v}</b>
    </div>)}
   </div>
   <div style={{margin:P(17)+'px '+P(27)+'px 0',borderRadius:P(14),background:'#E6F8FA',border:P(1)+'px solid #A6E0E7',
    padding:P(12)+'px '+P(14)+'px',display:'flex',gap:P(9),alignItems:'center'}}>
    <div style={{width:P(12),height:P(12),borderRadius:'50%',background:'#2DC5C2',boxShadow:'0 0 '+P(7)+'px #4DD6D6'}}/>
    <span style={{fontWeight:800,fontSize:P(18),color:'#137D8E'}}>گفت‌وگو و هماهنگی مستقیم</span>
   </div>
   <div style={{margin:P(21)+'px '+P(27)+'px 0',borderRadius:P(16),background:'linear-gradient(95deg,#0A67D9,#22BFE7)',
    boxShadow:'0 11px 24px #0B73C32B',padding:P(17),textAlign:'center',fontWeight:900,fontSize:P(24),color:'#FFFFFF'}}>مشاهده آگهی‌های مسیر</div>
   {/* Fixed bottom navigation, in addition to meaningful body details. */}
   <div style={{position:'absolute',bottom:0,left:0,right:0,height:P(76),borderTop:P(1)+'px solid #E0EDF4',
     background:'#FAFDFF',display:'flex',justifyContent:'space-around',alignItems:'center',paddingBottom:P(10)}}>
    {[['▣','آگهی‌ها'],['◇','گفت‌وگو'],['◉','حساب من']].map(([symbol,label],i)=><div key={label} style={{display:'flex',flexDirection:'column',alignItems:'center',gap:P(3),color:i===0?C.blue:C.muted}}>
      <div style={{fontSize:P(24),lineHeight:1}}>{symbol}</div><div style={{fontSize:P(12),fontWeight:800}}>{label}</div>
    </div>)}
   </div>
  </div>
 </div>;
};
