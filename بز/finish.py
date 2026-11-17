from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import math,subprocess
P=Path(__file__).parent;W,H=720,1280
fontpath=str(P/'BYekan.ttf')
def unit(v):return max(0,min(1,v))
def out(v):return 1-(1-unit(v))**3

def typography(t):
 ov=Image.new('RGBA',(W,H));d=ImageDraw.Draw(ov)
 a=out((t-7.9)/.65)
 if a:
  d.text((360,72+14*(1-a)),'وقتی می تونی از',font=ImageFont.truetype(fontpath,52),fill=(30,64,82,round(255*a)),stroke_width=1,stroke_fill=(30,64,82,round(255*a)),direction='rtl',language='fa',anchor='mt')
 # Two large kinetic lines form the focal phrase.
 a=out((t-8.35)/.9)
 if a:
  layer=Image.new('RGBA',(W,H));ld=ImageDraw.Draw(layer);font=ImageFont.truetype(fontpath,88)
  # Dimensional offset edge makes the headline feel substantial.
  ld.text((364,155),'فضای خالی',font=font,fill=(166,213,210,255),stroke_width=3,stroke_fill=(166,213,210,255),direction='rtl',language='fa',anchor='mt')
  ld.text((360,150),'فضای خالی',font=font,fill=(25,66,82,255),stroke_width=2,stroke_fill=(25,66,82,255),direction='rtl',language='fa',anchor='mt')
  w=round(W*a);ov.alpha_composite(layer.crop((W-w,0,W,H)),(W-w,0));d=ImageDraw.Draw(ov)
 a=out((t-8.7)/.85)
 if a:
  layer=Image.new('RGBA',(W,H));ld=ImageDraw.Draw(layer)
  # Skewed accent strip, rather than a rounded UI card.
  right=634;left=right-548*a
  ld.polygon([(left+12,275),(right,254),(right-12,368),(left,388)],fill=(43,188,169,round(255*a)))
  font=ImageFont.truetype(fontpath,106);ld.text((360+32*(1-a),267),'چمدونت',font=font,fill=(17,58,72,round(255*a)),stroke_width=2,stroke_fill=(17,58,72,round(255*a)),direction='rtl',language='fa',anchor='mt')
  ov.alpha_composite(layer);d=ImageDraw.Draw(ov)
  q=out((t-9.2)/.6)
  if q:
   d.line([(600,398),(600-478*q,414)],fill=(22,87,97,255),width=4)
 a=out((t-9.35)/.75)
 if a:d.text((360,447+12*(1-a)),'درآمد داشته باشی',font=ImageFont.truetype(fontpath,54),fill=(30,64,82,round(255*a)),stroke_width=1,stroke_fill=(30,64,82,round(255*a)),direction='rtl',language='fa',anchor='mt')
 return ov

def frame(i):
 base=Image.open(P/'frames'/f'{i:04}.png').convert('RGBA')
 if i>300:
  z=1+.02*(1-math.cos(math.pi*unit((i/30-10)/5)))/2
  nw,nh=round(W*z),round(H*z);base=base.resize((nw,nh),Image.Resampling.LANCZOS);x=round((nw-W)/2);y=round((nh-H)*.55);base=base.crop((x,y,x+W,y+H))
 return Image.alpha_composite(base,typography(i/30)).convert('RGB')
if __name__=='__main__':
 import sys
 if '--samples' in sys.argv:
  for i in [0,60,150,240,330,420]:frame(i).save(P/f'preview-{i}.jpg',quality=95)
 else:
  proc=subprocess.Popen(['ffmpeg','-y','-f','rawvideo','-pix_fmt','rgb24','-s','720x1280','-r','30','-i','-','-an','-c:v','libx264','-preset','fast','-crf','17','-pix_fmt','yuv420p','-movflags','+faststart',str(P/'flight-three-modern.mp4')],stdin=subprocess.PIPE,stderr=open('/tmp/flight-three-encode.log','w'))
  for i in range(450):proc.stdin.write(frame(i).tobytes())
  proc.stdin.close();assert proc.wait()==0
  print(P/'flight-three-modern.mp4')
