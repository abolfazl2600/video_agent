"""Minimal 3D network advertisement for Advertio, 15s portrait.
Quick Preview: 10 720x1280 JPGs and one contact sheet. No fabricated logo.
Screen text is advertising copy only: Advertio connects users and travelers;
transport eligibility is subject to carrier, customs and destination rules.
"""
from functools import lru_cache
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import os, subprocess, sys
P=Path(__file__).resolve().parent
MODE=os.environ.get('ADVERTIO_RENDER_MODE','preview')
if MODE not in ('preview','final'): raise ValueError(f'Invalid render mode: {MODE}')
W,H=720,1280
FPS=10 if MODE=='preview' else 30
COUNT=15*FPS
OUT_W,OUT_H=(540,960) if MODE=='preview' else (1080,1920)
FONTS=P.parents[1]/'assets'/'fonts'
REG=FONTS/'Vazirmatn-Regular.ttf';BOLD=FONTS/'Vazirmatn-Bold.ttf'
for f in (REG,BOLD):
    if not f.is_file(): raise FileNotFoundError(f)
INK=(34,35,38);ORANGE=(238,102,46);SUBTLE=(111,112,111)
WHITE=(251,251,249);PALE=(232,233,230)
@lru_cache(None)
def font(size,bold=True):
    return ImageFont.truetype(str(BOLD if bold else REG),size)
def fit(draw,text,size,max_w,bold=True,language=None):
    while size>18:
        f=font(size,bold)
        kwargs={'direction':'rtl','language':'fa'} if language=='fa' else {}
        b=draw.textbbox((0,0),text,font=f,**kwargs)
        if b[2]-b[0]<=max_w: return f
        size-=1
    return font(size,bold)
def rtl(d,x,y,s,size=40,color=INK,bold=True,a=255,max_w=614):
    f=fit(d,s,size,max_w,bold,'fa')
    d.text((x,y),s,font=f,direction='rtl',language='fa',
           anchor='mm',fill=(*color,int(a)))
def en(d,x,y,s,size=24,color=INK,bold=True,a=255,anchor='mm'):
    d.text((x,y),s,font=fit(d,s,size,610,bold),anchor=anchor,fill=(*color,int(a)))
def smooth(x):
    x=max(0,min(1,x))
    return x*x*(3-2*x)
def line(d,x0,y0,x1,y1,c=INK,w=3):
    d.line((x0,y0,x1,y1),fill=(*c,255),width=w)
def header(d,t):
    en(d,62,62,'ADVERTIO',28,INK,True,anchor='lm')
    d.ellipse((215,55,225,65),fill=(*ORANGE,255))
    en(d,655,61,f'{1 if t<4 else 2 if t<7 else 3 if t<11 else 4:02d} / 04',17,SUBTLE,False,anchor='rm')
    line(d,62,102,104,102,ORANGE,5)
    line(d,118,102,148,102,INK,5)
    line(d,160,102,182,102,PALE,5)
    line(d,62,1210,658,1210,PALE,2)
    line(d,62,1210,62+int(596*t/15),1210,ORANGE,5)
    en(d,64,1245,'advertio.net',22,INK,True,anchor='lm')
    en(d,654,1245,f'{min(15,int(t)):02d} / 15 s',18,SUBTLE,False,anchor='rm')
def lower(d,tag,s,a):
    en(d,360,1105,tag,20,SUBTLE,True,a=a)
    rtl(d,360,1155,s,28,INK,False,a=a,max_w=610)
    # Editorial graphic mark reminiscent of the supplied sparse dashed diagram
    line(d,268,1191,314,1191,ORANGE,7)
    line(d,330,1191,376,1191,INK,7)
    line(d,392,1191,435,1191,ORANGE,7)
def text_scene(d,t):
    if t<4:
        a=255*smooth((t+.1)/.45)
        rtl(d,360,210,'مامانت توی ایرانه',47,INK,True,a)
        rtl(d,360,279,'و حالش خوب نیست؟',49,INK,True,a)
        rtl(d,360,365,'یه مکمل لازم داره؟',38,ORANGE,True,a)
        lower(d,'THE CHALLENGE','چطور می‌تونی براش بفرستی؟',a)
    elif t<7:
        a=255*smooth((t-4)/.4)
        rtl(d,360,212,'می‌خوای از خارج کشور',46,INK,True,a)
        rtl(d,360,282,'به ایران برسونیش؟',46,INK,True,a)
        rtl(d,360,365,'مسافر مسیر ایران رو پیدا کن',34,ORANGE,True,a)
        lower(d,'THE CONNECTION','از طریق آگهی‌های حمل بار مسافری',a)
    elif t<11:
        a=255*smooth((t-7)/.4)
        rtl(d,360,212,'توی ادورتیو آگهی بذار',45,INK,True,a)
        rtl(d,360,286,'به مسافرها وصل شو',45,ORANGE,True,a)
        rtl(d,360,364,'مستقیم گفت‌وگو کن',38,INK,True,a)
        lower(d,'THE SOLUTION','مسیر مناسب رو با هم هماهنگ کنید',a)
    else:
        a=255*smooth((t-11)/.46)
        rtl(d,360,205,'بیش از ۱۱٬۰۰۰',73,INK,True,a)
        rtl(d,360,299,'آگهی حمل بار و مسافر',40,ORANGE,True,a)
        rtl(d,360,376,'در ادورتیو منتشر شده',37,INK,True,a)
        
        en(d,360,1127,'advertio.net',43,INK,True,a=a)
        rtl(d,360,1174,'حمل مکمل تابع مقررات شرکت حمل‌ونقل و گمرک است',18,SUBTLE,False,a,max_w=624)
def frame(i):
    t=i/FPS
    src=P/'frames'/f'{i:04d}.png'
    with Image.open(src) as source:
        im=source.convert('RGBA')
    if im.size!=(W,H): im=im.resize((W,H),Image.Resampling.BILINEAR)
    layer=Image.new('RGBA',(W,H),(0,0,0,0))
    d=ImageDraw.Draw(layer)
    # White edges preserve readability over 3D network centered in the frame.
    d.rectangle((0,0,W,430),fill=(248,248,246,236))
    d.rectangle((0,1080,W,H),fill=(248,248,246,242))
    header(d,t)
    text_scene(d,t)
    return Image.alpha_composite(im,layer).convert('RGB')
def samples():
    times=[0,1.5,3.5,4.5,6.5,8,9.5,11.5,13.5,14.9]
    images=[]
    for t in times:
        i=min(COUNT-1,round(t*FPS))
        f=P/f'frame-sample-{i:03d}.jpg'
        frame(i).save(f,quality=91,subsampling=0)
        images.append((t,f))
        print('Quick Preview:',f,flush=True)
    cols,tw,th,gap,margin,cap=5,216,384,16,24,42
    rows=(len(images)+cols-1)//cols
    sw=2*margin+cols*tw+(cols-1)*gap
    sh=2*margin+52+rows*(th+cap)+(rows-1)*gap
    sheet=Image.new('RGB',(sw,sh),WHITE)
    d=ImageDraw.Draw(sheet)
    d.text((margin,20),'Advertio | Quick Preview | Supplement Network',font=font(25),fill=INK)
    for j,(t,f) in enumerate(images):
        x=margin+(j%cols)*(tw+gap)
        y=margin+52+(j//cols)*(th+cap+gap)
        with Image.open(f) as img:
            sheet.paste(img.resize((tw,th),Image.Resampling.LANCZOS),(x,y))
        d.text((x+4,y+th+8),f'{t:04.1f}s',font=font(19),fill=INK)
    sheet.save(P/'quick-preview-contact-sheet.jpg',quality=91,subsampling=0)
def render():
    name='preview.mp4' if MODE=='preview' else 'output.mp4'
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo',
         '-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an',
         '-vf',f'scale={OUT_W}:{OUT_H}:flags=lanczos','-c:v','libx264',
         '-preset','ultrafast' if MODE=='preview' else 'fast',
         '-crf','28' if MODE=='preview' else '19','-pix_fmt','yuv420p',
         '-movflags','+faststart',str(P/name)]
    process=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    try:
        for i in range(COUNT):
            process.stdin.write(frame(i).tobytes())
            if i%75==0: print('Encoding',i,'/',COUNT,flush=True)
        process.stdin.close()
    except Exception:
        process.kill();process.wait();raise
    if process.wait(): raise RuntimeError('ffmpeg encoding failed')
    print('Rendered',P/name,flush=True)
if __name__=='__main__':
    samples() if '--samples' in sys.argv else render()
