#!/usr/bin/env python3
"""Advertio 'empty suitcase -> dollar income' image-based cinematic motion, 6 scenes.
Standalone folder; NO logo layers: AI-embedded artwork marks are cleaned prior to rendering.
"""
from __future__ import annotations
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, features
from functools import lru_cache
import json, math, os, subprocess, sys

ROOT=Path(__file__).resolve().parent
ASSETS=ROOT/'assets'
MODE=os.environ.get('ADVERTIO_RENDER_MODE','preview')
assert MODE in ('preview','final','quick-preview')
W,H=(720,1280) if MODE!='final' else (1080,1920)
FPS=30
DURATIONS=[3.5,3.5,4,4,4,4]
TOTAL_SECONDS=sum(DURATIONS)
TOTAL=int(TOTAL_SECONDS*FPS)
BG=(250,246,242)
TEAL=(11,111,122)
ORANGE=(241,115,41)
INK=(40,43,45)
SCALE=W/720
IMGBOX=(round(34*SCALE),round(472*SCALE),round(686*SCALE),round(1156*SCALE))
BLANK=(253,247,241)
DEFAULT_FONTS=['/usr/share/fonts/truetype/noto/NotoNaskhArabic-Regular.ttf','/usr/share/fonts/truetype/noto/NotoNaskhArabic-Bold.ttf']
SHARED_FONTS=[ROOT.parents[1]/'assets/fonts/Vazirmatn-Regular.ttf',ROOT.parents[1]/'assets/fonts/Vazirmatn-Bold.ttf']
FONT_PATHS=[str(p) for p in SHARED_FONTS] if all(p.is_file() for p in SHARED_FONTS) else DEFAULT_FONTS

SCENES=[
 {'image':'scene-01.webp','badge':'badge-01.webp','start':'اگر مسافری و فضای خالی داری','effect':'room'},
 {'image':'scene-02.webp','badge':'badge-02.webp','start':'می‌تونی درآمد دلاری داشته باشی','effect':'dollar'},
 {'image':'scene-03.webp','badge':'badge-03.webp','start':'به شرط حمل مدارک و وسایل شخصی','effect':'carry'},
 {'image':'scene-04.webp','badge':'badge-04-connection.webp','start':'ما در ادورتیو مسافران و ارسال‌کنندگان را وصل می‌کنیم','effect':'match'},
 {'image':'scene-05.webp','badge':'badge-05-direct.webp','start':'رایگان و مستقیم با هم ارتباط بگیرید','effect':'chat'},
 {'image':'scene-06.webp','badge':'badge-05.webp','start':'بیش از ۱۱ هزار آگهی؛ فرصت را از دست نده','effect':'proof'},
]

@lru_cache(maxsize=24)
def fnt(size,bold=False):return ImageFont.truetype(FONT_PATHS[1 if bold else 0],round(size))

def E(x):
 x=max(0,min(1,x));return x*x*(3-2*x)

def clamp(x,a,b):return max(a,min(b,x))

# Remove AI-embedded brand marks from the ORIGINAL scene illustrations.
# Reconstruct neutral regions using nearby wall / phone-header pixels, preserving
# the airport, passengers, luggage, app content and typography as source artwork.
# Coordinates are in the original 941x1672 scene images, BEFORE cropping.
BRAND_REGIONS = [
 (731,731,916,985,929), # scenes 1-3: two marks on airport wall
 (731,731,916,985,929),
 (731,731,916,985,929),
 (411,724,524,849,548), # scene 4: app header mark
 (347,734,527,848,541), # scene 5: app chat header marks
 (411,722,648,858,658), # scene 6: app header and Advertio wordmark
]

def remove_embedded_brand_marks(source, idx):
 x0,y0,x1,y1,donor_x=BRAND_REGIONS[idx]
 replacement=source.copy()
 draw=ImageDraw.Draw(replacement)
 # Use row-based donor color from the adjacent unbranded wall or blank UI.
 # Avoid blurring subject faces, luggage, messages and other meaningful content.
 for yy in range(y0,y1+1):
  c=source.getpixel((donor_x,yy))
  draw.line((x0,yy,x1,yy),fill=c,width=1)
 mask=Image.new('L',source.size,0)
 ImageDraw.Draw(mask).rectangle((x0+5,y0+5,x1-5,y1-5),fill=255)
 mask=mask.filter(ImageFilter.GaussianBlur(7))
 return Image.composite(replacement,source,mask)

# Cache all prepared illustration and text-art layers; render interpolates their transforms.
@lru_cache(maxsize=1)
def prepared_assets():
 scenes=[]
 for i,spec in enumerate(SCENES):
  full=remove_embedded_brand_marks(Image.open(ASSETS/'scenes'/spec['image']).convert('RGB'),i)
  # Crop only the generated empty top half; preserve people, packages, phones.
  tops=[516,516,524,490,490,500]
  lower=full.crop((0,tops[i],full.width,full.height))
  sw,sh=IMGBOX[2]-IMGBOX[0],IMGBOX[3]-IMGBOX[1]
  # Create a softly blended illustration stage; entire meaningful art remains in frame.
  back=ImageOps.fit(lower,(sw,sh),method=Image.Resampling.BICUBIC,centering=(.5,.55))
  back=back.filter(ImageFilter.GaussianBlur(max(4,round(14*SCALE))))
  tint=Image.new('RGB',(sw,sh),BLANK)
  back=Image.blend(back,tint,0.58).convert('RGBA')
  foreground=lower.copy()
  foreground.thumbnail((round(sw*.97),round(sh*.97)),Image.Resampling.LANCZOS)
  fg=Image.new('RGBA',(sw,sh),(0,0,0,0))
  fg.paste(foreground,((sw-foreground.width)//2,(sh-foreground.height)//2))
  # Soft feather blending around full original image; no hard side bands.
  alpha=Image.new('L',foreground.size,255)
  aa=ImageDraw.Draw(alpha)
  # Side feather keeps important content fully visible with minimal crop.
  for k in range(max(1,round(21*SCALE))):
   col=round(255*(k/max(1,round(21*SCALE))))
   aa.rectangle((k,0,k,foreground.height-1),fill=col)
   aa.rectangle((foreground.width-k-1,0,foreground.width-k-1,foreground.height-1),fill=col)
  alpha=alpha.filter(ImageFilter.GaussianBlur(round(4*SCALE)))
  fg.putalpha(Image.new('L',(sw,sh),0)) # replace only foreground area with feathered mask
  fg.paste(foreground,((sw-foreground.width)//2,(sh-foreground.height)//2),alpha)
  back=Image.alpha_composite(back,fg)
  # We choose to suppress AI-drawn in-artwork brand marks from the visual system:
  # the only intentional logo displayed is the official top-left logo layer.
  badge=Image.open(ASSETS/'typography'/spec['badge']).convert('RGBA')
  max_w,max_h=round(605*SCALE),round(365*SCALE)
  badge.thumbnail((max_w,max_h),Image.Resampling.LANCZOS)
  scenes.append((back,badge))
 return scenes

@lru_cache(maxsize=1)
def base_background():
 im=Image.new('RGBA',(W,H),BG+(255,))
 layer=Image.new('RGBA',(W,H),(0,0,0,0));d=ImageDraw.Draw(layer)
 d.ellipse((int(-160*SCALE),int(-220*SCALE),int(520*SCALE),int(640*SCALE)),fill=(252,202,162,45))
 d.ellipse((int(330*SCALE),int(270*SCALE),int(940*SCALE),int(1200*SCALE)),fill=(91,153,164,24))
 layer=layer.filter(ImageFilter.GaussianBlur(round(72*SCALE)))
 im.alpha_composite(layer)
 return im


def overlaid_art(base,idx,local,duration):
 u=clamp(local/duration,0,1)
 back,badge=prepared_assets()[idx]
 x0,y0,x1,y1=IMGBOX
 sw,sh=x1-x0,y1-y0
 posx=round(8*SCALE*math.sin((u+.09*idx)*math.pi*1.4))
 posy=round(-4*SCALE*math.sin(u*math.pi*1.8))
 # Dedicated framed image viewport with subtle shadow.
 shadow=Image.new('RGBA',(W,H),(0,0,0,0));sd=ImageDraw.Draw(shadow)
 rad=round(37*SCALE)
 sd.rounded_rectangle((x0+round(7*SCALE),y0+round(12*SCALE),x1+round(7*SCALE),y1+round(12*SCALE)),rad,fill=(39,45,48,38))
 base.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(round(15*SCALE))))
 zoom=1.035+0.025*E(u)
 # Fractional smooth translation with per-frame resize, no repeated 15->30 FPS frames.
 zw,zh=round(sw*zoom),round(sh*zoom)
 visual=back.resize((zw,zh),Image.Resampling.BICUBIC)
 ox=(zw-sw)//2 + posx
 oy=(zh-sh)//2 + posy
 ox=clamp(ox,0,zw-sw);oy=clamp(oy,0,zh-sh)
 visual=visual.crop((ox,oy,ox+sw,oy+sh))
 mask=Image.new('L',(sw,sh),0);ImageDraw.Draw(mask).rounded_rectangle((0,0,sw-1,sh-1),rad,fill=255)
 base.paste(visual,(x0,y0),mask)
 d=ImageDraw.Draw(base)
 d.rounded_rectangle((x0,y0,x1,y1),rad,outline=(255,255,255,215),width=max(1,round(2*SCALE)))

 # Render generated transparent 3D typography as independent compositing layer.
 op=E(local/.55)*E((duration-local)/.28) if local>duration-.3 else E(local/.55)
 op=clamp(op,0,1)
 if op>0:
  bx=(W-badge.width)//2
  by=round(70*SCALE + 18*SCALE*(1-E(local/.7)))
  scale=.9+.1*E(local/.7)
  if scale<.999:
   nw,nh=round(badge.width*scale),round(badge.height*scale)
   b=badge.resize((nw,nh),Image.Resampling.BICUBIC)
  else:b=badge
  x=(W-b.width)//2;y=by+(badge.height-b.height)//2
  alpha=b.getchannel('A').point(lambda z:round(z*op));b.putalpha(alpha)
  base.alpha_composite(b,(x,y))

 # No extra icons, lines, sparkles or unrelated on-image embellishments.
 return base

def render_one(idx,t):
 elapsed=0
 for j,length in enumerate(DURATIONS):
  if t<elapsed+length or j==len(DURATIONS)-1:idx=j;local=t-elapsed;duration=length;break
  elapsed+=length
 a=base_background().copy()
 a=overlaid_art(a,idx,local,duration)
 return a.convert('RGB')

def shot(t):
 boundaries=[];v=0
 for length in DURATIONS[:-1]:v+=length;boundaries.append(v)
 k=next((b for b in boundaries if abs(t-b)<.22 and t<b+.12),None)
 if k is None:return render_one(0,t)
 # True crossfade between scene art, preserving same visual layout.
 after=render_one(0,t)
 before=render_one(0,max(0,k-.001))
 mix=E((t-(k-.22))/.34)
 return Image.blend(before,after,mix)

def poster():
 frames=[]
 stamps=[1,2.6,4.9,6.4,8.6,10.4,12.8,14.8,16.7,18.5,20.5,22.3]
 w=220;h=391
 out=Image.new('RGB',(5*w+6*12,3*(h+37)+80),BG)
 d=ImageDraw.Draw(out)
 d.text((24,18),'ADVERTIO / Traveler Dollar Income / Quick Preview',font=fnt(27,True),fill=INK)
 for k,stamp in enumerate(stamps):
  im=shot(stamp).resize((w,h),Image.Resampling.LANCZOS)
  x=12+(k%5)*(w+12);y=66+(k//5)*(h+37)
  out.paste(im,(x,y));d.text((x+5,y+h+5),f'{stamp:.1f}s',font=fnt(17),fill=INK)
 p=ROOT/'renders'/'quick-preview-contact-sheet.jpg';out.save(p,quality=89)
 print('CONTACT',p,flush=True)

def video():
 out=ROOT/('preview.mp4' if MODE!='final' else 'output.mp4')
 cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','veryfast' if MODE!='final' else 'fast','-crf','21' if MODE!='final' else '17','-pix_fmt','yuv420p','-movflags','+faststart',str(out)]
 process=subprocess.Popen(cmd,stdin=subprocess.PIPE)
 try:
  for i in range(TOTAL):
   process.stdin.write(shot(i/FPS).tobytes())
   if i%120==0:print('RENDER',i,TOTAL,flush=True)
  process.stdin.close()
  if process.wait()!=0:raise RuntimeError('FFmpeg failed')
 except BaseException:
  process.kill();process.wait();raise
 print('VIDEO',out,flush=True)

if __name__=='__main__':
 if '--samples' in sys.argv or MODE=='quick-preview':poster()
 else:poster();video()