"""Code-only, folder-scoped top-down air-cargo film for Advertio.
Reference: quiet crimson editorial layout with a narrow white flight lane;
no pixels, vehicle model, or logo are copied from the reference image.
Advertio connects shippers with independent air travelers; the two-week
estimate is illustrative, not a delivery guarantee.
"""
from __future__ import annotations
import math
import os
import random
import subprocess
import sys
from functools import lru_cache
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont, features

ROOT = Path(__file__).resolve().parent
FONTS = ROOT.parents[1] / 'assets' / 'fonts'
MODE = os.environ.get('ADVERTIO_RENDER_MODE', 'preview')
if MODE not in ('preview', 'final'):
    raise SystemExit('ADVERTIO_RENDER_MODE must be preview or final')
W, H = 720, 1280
DURATION = 15
FPS = 10 if MODE == 'preview' else 30
OUT_SIZE = (540, 960) if MODE == 'preview' else (1080, 1920)
WHITE = (249, 246, 240)
CREAM = (225, 221, 214)
RED = (130, 24, 28)
ACCENT = (250, 89, 66)
DARK = (68, 15, 20)
SILVER = (167, 169, 167)

@lru_cache(None)
def font(n: int, bold: bool = True):
    path = FONTS / ('Vazirmatn-Bold.ttf' if bold else 'Vazirmatn-Regular.ttf')
    if not path.exists():
        fallback = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
        path = Path(fallback)
    return ImageFont.truetype(str(path), n)

def clamp(x): return max(0., min(1., x))
def smooth(x):
    x = clamp(x)
    return x*x*(3-2*x)
def reveal(t, start, stop): return smooth((t-start)/max(.01, stop-start))
def window(t, a, b, fade=.35): return reveal(t, a, a+fade) * (1-reveal(t, b-fade, b))

def rgba(c, a=255): return tuple(c)+(int(clamp(a/255)*255),)

def headline(d, text, cy, size, a=255, color=WHITE, max_width=615, bold=True):
    n=size
    while n>22 and d.textbbox((0,0),text,font=font(n,bold),direction='rtl',language='fa')[2]>max_width:
        n-=1
    d.text((W//2,cy),text,font=font(n,bold),anchor='mm',direction='rtl',language='fa',fill=rgba(color,a))

def latin(d, text, xy, size=20, a=255, color=WHITE, anchor='mm', bold=True):
    d.text(xy,text,font=font(size,bold),anchor=anchor,fill=rgba(color,a))

@lru_cache(None)
def backdrop():
    im=Image.new('RGB',(W,H))
    draw=ImageDraw.Draw(im)
    # matte crimson field: vertical gradient plus a very soft vignette
    for y in range(H):
        s=y/H
        c=(int(85+82*s), int(19+19*s), int(23+24*s))
        draw.line((0,y,W,y),fill=c)
    rng=random.Random(220126)
    for _ in range(11500):
        x=rng.randrange(W); y=rng.randrange(H)
        p=im.getpixel((x,y))
        delta=rng.choice((-5,-3,-1,2,3,5))
        draw.point((x,y),fill=tuple(max(0,min(255,i+delta)) for i in p))
    # restrained central corridor shadow, visually close to an overhead studio render
    draw.polygon([(303,318),(482,318),(482,H),(303,H)],fill=(93,33,35))
    draw.polygon([(282,320),(454,320),(453,H),(282,H)],fill=(112,50,51))
    draw.polygon([(287,319),(445,319),(445,H),(287,H)],fill=(216,212,207))
    draw.polygon([(295,319),(436,319),(436,H),(295,H)],fill=(239,236,230))
    draw.polygon([(356,319),(374,319),(374,H),(356,H)],fill=(173,38,43))
    draw.line([(367,325),(367,H)],fill=(129,29,35),width=5)
    # top-right pill, cropped by the frame, as in the reference composition
    draw.rounded_rectangle((525,-34,763,44),radius=40,fill=(231,22,47))
    return im

@lru_cache(None)
def airplane():
    """Original stylized top-view airliner, hand-drawn in Pillow polygons."""
    S=330
    img=Image.new('RGBA',(S,S),(0,0,0,0))
    d=ImageDraw.Draw(img)
    # original silhouette: shadow and soft bevels, no aircraft brand insignia
    d.polygon([(156,23),(175,23),(190,130),(301,202),(297,223),(178,192),
               (179,266),(241,290),(237,304),(167,293),(94,304),(91,290),
               (153,266),(153,192),(34,223),(29,202),(143,130)],fill=(234,229,221,255))
    d.polygon([(157,20),(174,20),(182,140),(291,205),(288,216),(177,185),
               (175,276),(229,292),(224,299),(165,287),(107,299),(102,292),
               (157,276),(155,185),(44,216),(40,205),(150,140)],fill=(247,247,240,255))
    # beveled wings and top-view panel separations
    d.line([(46,213),(158,177),(175,177),(287,213)],fill=(177,181,179,255),width=3)
    d.line([(164,46),(164,274)],fill=(215,210,204,255),width=6)
    d.polygon([(157,37),(171,37),(172,148),(157,148)],fill=(194,39,47,255))
    d.line([(110,293),(158,281)],fill=(160,166,163,255),width=3)
    d.line([(175,281),(222,293)],fill=(160,166,163,255),width=3)
    d.ellipse((156,46,174,77),fill=(48,60,73,255),outline=(212,212,209,255),width=2)
    d.line((164,87,164,123),fill=(191,54,59,255),width=4)
    d.ellipse((153,130,178,154),fill=(205,205,199,255),width=2)
    # delicate orange wingtip markers
    d.ellipse((38,206,49,217),fill=(236,104,69,255))
    d.ellipse((284,206,295,217),fill=(236,104,69,255))
    sh=Image.new('RGBA',img.size,(0,0,0,0));sh.paste((30,8,10,165),(0,0,S,S),img.getchannel('A'))
    sh=sh.filter(ImageFilter.GaussianBlur(17))
    layer=Image.new('RGBA',(S+58,S+58),(0,0,0,0))
    layer.alpha_composite(sh,(28,33));layer.alpha_composite(img,(0,0))
    return layer

@lru_cache(None)
def parcel():
    img=Image.new('RGBA',(176,158),(0,0,0,0)); d=ImageDraw.Draw(img)
    # minimal isometric cuboid, entirely from code
    d.polygon([(22,55),(91,25),(157,54),(89,86)],fill=(234,205,156))
    d.polygon([(22,55),(89,86),(89,145),(22,111)],fill=(177,129,80))
    d.polygon([(89,86),(157,54),(157,110),(89,145)],fill=(203,161,108))
    d.polygon([(61,38),(74,33),(140,61),(127,67)],fill=(247,231,198))
    d.line([(126,68),(126,124)],fill=(247,231,198),width=10)
    d.line([(22,56),(89,87),(157,54)],fill=(250,224,178),width=3)
    return img

@lru_cache(None)
def documents():
    img=Image.new('RGBA',(150,177),(0,0,0,0)); d=ImageDraw.Draw(img)
    d.rounded_rectangle((22,13,132,165),radius=8,fill=(37,34,40,120))
    d.rounded_rectangle((11,7,123,154),radius=7,fill=(247,247,239),outline=(219,218,206),width=2)
    d.rounded_rectangle((26,29,70,55),radius=4,fill=(202,45,52))
    d.line((27,81,103,81),fill=(121,132,135),width=5)
    d.line((27,96,97,96),fill=(167,175,177),width=4)
    d.line((27,111,85,111),fill=(167,175,177),width=4)
    d.ellipse((76,116,110,149),outline=(199,56,56),width=5)
    return img

def floating(im, art, cx, cy, s=1, a=255):
    if a<=0: return
    tw=max(1,int(art.width*s)); th=max(1,int(art.height*s))
    stamp=art.resize((tw,th),Image.Resampling.LANCZOS)
    if a<254:
        stamp.putalpha(stamp.getchannel('A').point(lambda x:int(x*a/255)))
    im.alpha_composite(stamp,(int(cx-tw/2),int(cy-th/2)))

def diagram(d,t):
    # On-screen labels use neutral codes rather than flag approximations
    opacity=240*window(t,.8,10.9,.7)
    if opacity>0:
        for side,y,label,small in [('l',664,'USA','مبدأ / مقصد'),('r',880,'IRAN','مقصد / مبدأ')]:
            x=116 if side=='l' else 604
            col=WHITE
            d.rounded_rectangle((x-70,y-29,x+70,y+24),radius=23,fill=(92,22,28,int(opacity*.85)),outline=(249,239,226,int(opacity*.7)),width=2)
            latin(d,label,(x,y-3),24,opacity,col)
            d.text((x,y+47), small, font=font(18,False), anchor='mm', direction='rtl', language='fa', fill=rgba((251,220,212),opacity))
        # small nodes at both sides of the central aircraft path
        d.ellipse((347,655,378,686),fill=(255,248,234,int(opacity)),outline=(201,54,58,int(opacity)),width=4)
        d.ellipse((347,856,378,887),fill=(255,248,234,int(opacity)),outline=(201,54,58,int(opacity)),width=4)

def scene_layer(t):
    layer=Image.new('RGBA',(W,H),(0,0,0,0));d=ImageDraw.Draw(layer)
    # The main headline is entirely editable source text, never raster artwork.
    if t<3.4:
        a=255*window(t,0,3.4,.3)
        headline(d,'آمریکا به ایران؟',137,55,a)
        headline(d,'یا ایران به آمریکا؟',207,44,a)
        latin(d,'AIR CARGO  /  TWO-WAY', (360,267),20,a,(255,216,207))
    if 3.4<=t<7.2:
        a=255*window(t,3.4,7.2,.3)
        headline(d,'بار یا مدارک داری؟',139,54,a)
        headline(d,'مسیر هوایی رو انتخاب کن',212,37,a,(255,218,204))
    if 7.2<=t<11:
        a=255*window(t,7.2,11,.3)
        headline(d,'توی ادورتیو',139,54,a)
        headline(d,'مسافر هوایی پیدا کن',212,43,a,(255,219,209))
    if t>=11:
        a=255*reveal(t,11,11.65)
        headline(d,'حدود ۲ هفته*',132,72,a)
        headline(d,'برای هماهنگی ارسال',211,37,a,(255,221,212))
    # A simple time-coded highlight / rule, without reproducing source typography
    d.line((62,89,120,89),fill=rgba((255,243,227),245),width=6)
    d.line((131,89,172,89),fill=rgba(ACCENT,250),width=6)
    # parcel/documents appear as flat hand-crafted models alongside aircraft
    p=255*window(t,3.0,11.0,.6)
    if p>0:
        slide=(1-reveal(t,3.1,4.1))*135
        floating(layer,parcel(),182,730+slide+math.sin(t*3)*8,.81,p)
        floating(layer,documents(),553,795-slide*.35+math.sin(t*2.7)*6,.84,p)
        latin(d,'PARCEL',(165,862),16,p,(255,222,203))
        latin(d,'DOCUMENTS',(566,920),16,p,(255,222,203))
    diagram(d,t)
    # stylized airliner moves along the line throughout the animation
    aircraft_y=765-300*smooth(t/11.7)+8*math.sin(t*1.2)
    floating(layer,airplane(),360,aircraft_y,0.83+0.07*smooth(t/11.7),255)
    # footer ribbon and story progress
    d.rectangle((0,1051,W,H),fill=(57,13,19,232))
    d.line((57,1072,663,1072),fill=(137,64,66,255),width=2)
    d.line((57,1072,57+int(606*clamp(t/DURATION)),1072),fill=(249,231,220,255),width=5)
    if t<3.4:
        headline(d,'ارسال بار بین آمریکا و ایران',1128,34,255)
        headline(d,'رفت و برگشت، با مسافران هوایی',1182,27,238,(240,195,183),bold=False)
    elif t<7.2:
        headline(d,'بسته یا مدارک مهمت رو',1128,36,255)
        headline(d,'به مسافر مسیر بسپار',1182,31,238,(240,195,183),bold=False)
    elif t<11:
        headline(d,'آگهی‌های مسافران رو ببین',1128,35,255)
        headline(d,'مستقیم هماهنگ کن',1182,32,238,(240,195,183),bold=False)
    else:
        headline(d,'با مسافران هوایی',1124,39,255)
        latin(d,'advertio.net',(360,1180),39,255,WHITE)
        headline(d,'* زمان ارسال تابع مسیر و توافق با مسافر است',1244,19,225,(218,168,157),bold=False)
    latin(d,'ADVERTIO',(83,1239),19,235,WHITE,anchor='lm') if t<11 else None
    latin(d,f'{min(15,int(t)):02d} / 15',(647,1239),16,235,(233,171,163),anchor='rm') if t<11 else None
    return layer

def frame(t):
    base=backdrop().convert('RGBA')
    return Image.alpha_composite(base,scene_layer(t)).convert('RGB')

def samples():
    times=[.5,1.8,3.3,4.3,5.6,7.2,8.6,10.3,12.3,14.4]
    imgs=[]
    for i,t in enumerate(times):
        out=ROOT/f'frame-sample-{i+1:02d}.jpg'
        frame(t).save(out,quality=90,subsampling=0)
        imgs.append(out)
    thumb=(216,384); gap=14; cols=5
    sheet=Image.new('RGB',(2*22+cols*thumb[0]+4*gap,2*24+2*thumb[1]+64),(249,246,240))
    sd=ImageDraw.Draw(sheet)
    latin(sd,'ADVERTIO / US-IRAN / TOP-DOWN',(25,21),22,255,(68,15,20),anchor='lm')
    for i,path in enumerate(imgs):
        img=Image.open(path).resize(thumb,Image.Resampling.LANCZOS)
        x=22+(i%cols)*(thumb[0]+gap); y=55+(i//cols)*(thumb[1]+gap)
        sheet.paste(img,(x,y))
    sheet.save(ROOT/'quick-preview-contact-sheet.jpg',quality=90)
    print('Saved 10 samples and quick-preview-contact-sheet.jpg')

def render():
    name='preview.mp4' if MODE=='preview' else 'output.mp4'
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo',
         '-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-',
         '-an','-vf',f'scale={OUT_SIZE[0]}:{OUT_SIZE[1]}:flags=lanczos',
         '-c:v','libx264','-preset','ultrafast' if MODE=='preview' else 'fast',
         '-crf','24' if MODE=='preview' else '18','-pix_fmt','yuv420p',
         '-movflags','+faststart',str(ROOT/name)]
    process=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    try:
        for i in range(DURATION*FPS):
            process.stdin.write(frame(i/FPS).tobytes())
            if i%50==0: print(f'frame {i}/{DURATION*FPS}',flush=True)
        process.stdin.close()
    except Exception:
        process.kill();process.wait();raise
    if process.wait()!=0: raise RuntimeError('FFmpeg failed to encode video')
    print('Output:',ROOT/name)

if __name__=='__main__':
    if not features.check('raqm'):
        raise SystemExit('Pillow with libraqm required for Persian text shaping')
    samples() if '--samples' in sys.argv else render()
