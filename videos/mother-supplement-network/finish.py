"""Persian typography & video encoding for four original animated story scenes.
Production uses shared, unaltered version-controlled Vazirmatn fonts.
Only plain brand text is displayed; no brand logo is recreated.
"""
from functools import lru_cache
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import os, subprocess, sys

ROOT=Path(__file__).resolve().parent
MODE=os.environ.get('ADVERTIO_RENDER_MODE','preview').strip()
if MODE not in ('preview','final'):raise ValueError(MODE)
FPS=10 if MODE=='preview' else 30
N=15*FPS
W,H=720,1280
OUT_W,OUT_H=(540,960) if MODE=='preview' else (1080,1920)
TIMES=[.5,1.6,3.3,4.4,6.2,7.5,9.5,11.4,13.1,14.7]
FONTDIR=ROOT.parents[1]/'assets'/'fonts'
REG=FONTDIR/'Vazirmatn-Regular.ttf'
BOLD=FONTDIR/'Vazirmatn-Bold.ttf'
if os.environ.get('ADVERTIO_LOCAL_FONT_FALLBACK')=='1' and not REG.exists():
    REG=Path('/usr/share/fonts/truetype/noto/NotoKufiArabic-Regular.ttf')
    BOLD=Path('/usr/share/fonts/truetype/noto/NotoKufiArabic-Bold.ttf')
LOCAL_FALLBACK=os.environ.get('ADVERTIO_LOCAL_FONT_FALLBACK')=='1'
LAT_REG=Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf') if LOCAL_FALLBACK else REG
LAT_BOLD=Path('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf') if LOCAL_FALLBACK else BOLD
for path in (REG,BOLD):
    if not path.is_file():raise FileNotFoundError('Shared Vazirmatn font not found: '+str(path))
INK=(38,54,69);ORANGE=(242,117,61);TEAL=(87,158,148)
GREY=(117,130,137);BONE=(218,225,223);BG=(248,248,245)
@lru_cache(maxsize=120)
def font(size,bold=True,latin=False):
    return ImageFont.truetype(str((LAT_BOLD if bold else LAT_REG) if latin else (BOLD if bold else REG)),size)
def e(x):
    x=max(0,min(1,x));return x*x*(3-2*x)
def fit(draw,text,size,maxw,bold=True,fa=True):
    kwargs={'direction':'rtl','language':'fa'} if fa else {}
    while size>18:
        f=font(size,bold,not fa)
        b=draw.textbbox((0,0),text,font=f,**kwargs)
        if b[2]-b[0]<=maxw:return f
        size-=1
    return font(size,bold,not fa)
def persian(d,x,y,string,size,bold=True,color=INK,alpha=255,maxw=620):
    if alpha<=0:return
    f=fit(d,string,size,maxw,bold,True)
    d.text((x,y),string,font=f,anchor='mm',direction='rtl',language='fa',fill=(*color,round(alpha)))
def english(d,x,y,string,size,bold=False,color=GREY,alpha=255,anchor='mm'):
    if alpha<=0:return
    f=fit(d,string,size,635,bold,False)
    d.text((x,y),string,font=f,anchor=anchor,fill=(*color,round(alpha)))
def header(d,t):
    english(d,60,57,'ADVERTIO',28,True,INK,anchor='lm')
    index=1 if t<3.8 else 2 if t<7 else 3 if t<11 else 4
    english(d,656,59,f'{index:02d} / 04',17,False,GREY,anchor='rm')
    for i in range(4):
        color=ORANGE if i==index-1 else BONE
        d.rounded_rectangle((60+i*46,104,94+i*46,109),radius=2,fill=(*color,255))
    d.line((60,1213,660,1213),fill=(*BONE,255),width=3)
    d.line((60,1213,60+min(600,round(600*t/15)),1213),fill=(*ORANGE,255),width=5)
    english(d,62,1251,'advertio.net',21,True,INK,anchor='lm')
    english(d,658,1251,'00:15',16,False,GREY,anchor='rm')
def story(d,t):
    if t<3.8:
        u=t
        persian(d,360,196,'مامانت توی ایران',53,True,INK,255*e((u+.05)/.42))
        persian(d,360,288,'حالش خوب نیست؟',56,True,INK,255*e((u-.55)/.52))
        persian(d,360,376,'یه مکمل خوب لازم داره؟',40,True,ORANGE,255*e((u-1.25)/.5))
        english(d,360,1135,'A LITTLE HELP, A BIG DISTANCE',19,True,GREY,255*e((u-.5)/.6))
        persian(d,360,1180,'فاصله نباید مانع کمک‌کردن باشه',24,False,INK,255*e((u-1)/.6))
    elif t<7:
        u=t-3.8
        persian(d,360,207,'مکمل رو تهیه کردی',49,True,INK,255*e((u+.02)/.4))
        persian(d,360,302,'چطور به ایران برسونیش؟',42,True,ORANGE,255*e((u-.55)/.5))
        persian(d,360,1125,'یه مسافرِ مسیر ایران لازمه',31,True,INK,255*e((u-1)/.5))
        english(d,360,1175,'CANADA   →   IRAN',22,True,GREY,255*e((u-1.35)/.55))
    elif t<11:
        u=t-7
        persian(d,360,192,'توی ادورتیو',58,True,INK,255*e((u+.05)/.42))
        persian(d,360,280,'مسافر مسیر ایران رو',44,True,INK,255*e((u-.43)/.47))
        persian(d,360,359,'پیدا کن',57,True,ORANGE,255*e((u-.84)/.47))
        persian(d,360,1133,'آگهی‌ها رو ببین، گفت‌وگو کن',29,True,INK,255*e((u-1.05)/.6))
        english(d,360,1174,'CONNECT WITH TRAVELERS',18,True,GREY,255*e((u-1.4)/.55))
    else:
        u=t-11
        count=round(11000*(.2+.8*e((u-.3)/1.9)))
        persian(d,360,197,f'بیش از {count:,}'.replace(',','٬'),71,True,INK,255*e((u+.05)/.48))
        persian(d,360,290,'آگهی حمل بار و مسافر',42,True,ORANGE,255*e((u-.45)/.48))
        persian(d,360,367,'در ادورتیو منتشر شده',37,True,INK,255*e((u-.86)/.48))
        persian(d,360,1112,'مسافر مناسب رو پیدا کن',29,True,INK,255*e((u-.9)/.52))
        persian(d,360,1173,'حمل مکمل تابع مقررات شرکت حمل‌ونقل و گمرک است',18,False,GREY,255*e((u-1.3)/.6))
def frame(i):
    t=i/FPS
    path=ROOT/'frames'/f'{i:04d}.png'
    with Image.open(path) as img:base=img.convert('RGBA')
    if base.size!=(W,H):base=base.resize((W,H),Image.Resampling.BILINEAR)
    typography=Image.new('RGBA',(W,H),(0,0,0,0))
    d=ImageDraw.Draw(typography)
    header(d,t);story(d,t)
    return Image.alpha_composite(base,typography).convert('RGB')
def samples():
    images=[]
    for t in TIMES:
        i=min(N-1,round(t*FPS));p=ROOT/f'frame-sample-{i:03d}.jpg'
        frame(i).save(p,quality=92,subsampling=0)
        images.append((t,p))
        print('Quick frame',t,p.name,flush=True)
    tw,th=216,384;gap=16;margin=24;cw=5
    sw=2*margin+tw*cw+gap*(cw-1)
    sh=2*margin+57+2*(th+43)+gap
    img=Image.new('RGB',(sw,sh),BG)
    d=ImageDraw.Draw(img)
    d.text((margin,22),'ADVERTIO / ANIMATED STORY - QUICK PREVIEW',font=font(24,True,True),fill=INK)
    for i,(t,p) in enumerate(images):
        x=margin+(i%cw)*(tw+gap);y=margin+57+(i//cw)*(th+43+gap)
        with Image.open(p) as thim:
            img.paste(thim.resize((tw,th),Image.Resampling.LANCZOS),(x,y))
        d.text((x+5,y+th+7),f'{t:04.1f}s',font=font(19,True,True),fill=INK)
    img.save(ROOT/'quick-preview-contact-sheet.jpg',quality=93,subsampling=0)
    print('Saved contact sheet',flush=True)
def movie():
    name='preview.mp4' if MODE=='preview' else 'output.mp4'
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24',
         '-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-vf',f'scale={OUT_W}:{OUT_H}:flags=lanczos',
         '-c:v','libx264','-preset','ultrafast' if MODE=='preview' else 'fast',
         '-crf','26' if MODE=='preview' else '19','-pix_fmt','yuv420p','-movflags','+faststart',str(ROOT/name)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    try:
        for i in range(N):
            proc.stdin.write(frame(i).tobytes())
            if i%30==0:print('Encoding video',i,'/',N,flush=True)
        proc.stdin.close()
    except Exception:
        proc.kill();proc.wait();raise
    if proc.wait():raise RuntimeError('ffmpeg encoding failed')
    print('Video saved',name,flush=True)
if __name__=='__main__':samples() if '--samples' in sys.argv else movie()
