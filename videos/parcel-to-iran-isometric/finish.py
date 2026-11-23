"""Advertio / 3D isometric parcel delivery — Persian typographic finishing.
All spoken dialogue is communicated through animated on-screen speech bubbles.
This project intentionally does not recreate or generate an Advertio logo.
"""
from functools import lru_cache
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import os
import subprocess
import sys

P = Path(__file__).resolve().parent
MODE = os.environ.get('ADVERTIO_RENDER_MODE','preview').strip().lower()
if MODE not in ('preview','final'):
    raise ValueError(f'Unknown ADVERTIO_RENDER_MODE: {MODE}')
W,H = 720,1280   # master typography canvas; preview 3D gets upsampled onto this
FPS = 10 if MODE == 'preview' else 30
COUNT = 15*FPS
OUTPUT = P/('preview.mp4' if MODE == 'preview' else 'output.mp4')
OUT_W,OUT_H = (540,960) if MODE == 'preview' else (1080,1920)
# Always use the repository's version-controlled Persian fonts, not runner fonts.
FONT_DIR = P.parents[1] / 'assets' / 'fonts'
FONT = FONT_DIR / 'Vazirmatn-Regular.ttf'
BOLD = FONT_DIR / 'Vazirmatn-Bold.ttf'
for required in (FONT, BOLD):
    if not required.is_file():
        raise FileNotFoundError(f'Required shared Persian font is missing: {required}')
# Porcelain-city editorial palette (adapted to the uploaded style reference).
CYAN = (49, 164, 172)
WHITE = (255, 255, 252)
INK = (36, 54, 67)
DARK = (36, 54, 67)
CORAL = (230, 114, 133)
GOLD = (238, 177, 85)
MINT = (221, 242, 239)
SUBTLE = (119, 141, 151)

@lru_cache(None)
def font(size, bold=False):
    return ImageFont.truetype(str(BOLD if bold else FONT), size)

def fit_font(draw, text, size, bold, max_width, direction=None):
    if not max_width:
        return font(size,bold)
    while size > 16:
        f=font(size,bold)
        kw={'direction': direction,'language':'fa'} if direction else {}
        bbox=draw.textbbox((0,0),text,font=f,**kw)
        if bbox[2]-bbox[0] <= max_width:
            return f
        size-=1
    return font(size,bold)

def ease(x):
    x=max(0,min(1,x))
    return x*x*(3-2*x)

def rtl(draw,x,y,txt,size,color=INK,bold=True,alpha=255,anchor='mm',max_width=None):
    if max_width is None:
        max_width=405 if anchor=='rm' else 590
    f=fit_font(draw,txt,size,bold,max_width,'rtl')
    draw.text((x,y),txt,font=f,anchor=anchor,
              language='fa',direction='rtl',fill=(*color,int(alpha)))

def latin(draw,x,y,txt,size=24,color=INK,alpha=255,anchor='mm',bold=True):
    f=fit_font(draw,txt,size,bold,590)
    draw.text((x,y),txt,font=f,anchor=anchor,fill=(*color,int(alpha)))

def panel(draw,xy,fill,outline,radius=28,width=2):
    draw.rounded_rectangle(xy,radius=radius,fill=fill,outline=outline,width=width)

def background_tint(image):
    # Bright reference: no midnight overlays, scanlines or large dark vignette.
    layer=Image.new('RGBA',(W,H),(0,0,0,0))
    d=ImageDraw.Draw(layer)
    d.rectangle((0,0,W,117),fill=(253,252,249,222))
    d.rectangle((0,117,W,120),fill=(217,221,220,102))
    d.rectangle((0,1170,W,H),fill=(252,251,248,230))
    return Image.alpha_composite(image,layer)

def draw_header(draw,t):
    latin(draw,55,61,'ADVERTIO',27,INK,anchor='lm')
    draw.ellipse((247,53,261,67),fill=(*CORAL,255))
    rtl(draw,660,63,'ارسال بار مسافری',24,(70,102,113),anchor='rm',max_width=330)
    draw.line((52,1167,668,1167),fill=(194,205,206,190),width=2)
    draw.rounded_rectangle((55,1190,665,1197),radius=4,fill=(218,225,223,200))
    draw.rounded_rectangle((55,1190,55+round(610*t/15),1197),
                           radius=4,fill=(*CYAN,245))
    latin(draw,56,1245,'Advertio.net',22,INK,anchor='lm')
    latin(draw,665,1245,'00:15',17,SUBTLE,anchor='rm',bold=False)

def scene_one(draw,t):
    a=ease(t/.38)
    panel(draw,(129,162,591,234),(255,255,253,int(229*a)),(222,227,224,int(180*a)),radius=22)
    rtl(draw,360,196,'کانادا  ←  ایران',29,(74,125,133),alpha=255*a)
    panel(draw,(58,274,662,481),(255,255,252,int(244*a)),(219,223,221,int(225*a)),radius=30)
    draw.rounded_rectangle((90,310,102,447),radius=6,fill=(*CORAL,int(248*a)))
    rtl(draw,374,351,'کاش یکی بود این بسته رو',38,INK,alpha=255*a,max_width=535)
    rtl(draw,374,424,'برام ببره ایران!',46,INK,alpha=255*a,max_width=530)
    if t>2.15:
        b=ease((t-2.15)/.5)
        panel(draw,(118,995,602,1080),(255,255,251,int(227*b)),(225,229,226,int(160*b)),radius=22)
        rtl(draw,360,1038,'یه راه ساده برای ارسال بسته...',27,(81,118,125),alpha=250*b)

def scene_two(draw,t):
    a=ease((t-4)/.38)
    panel(draw,(82,169,638,246),(255,255,252,int(229*a)),(224,231,228,int(170*a)),radius=22)
    rtl(draw,360,209,'دوستش گوشی رو نشون می‌ده',30,(80,126,129),alpha=255*a)
    panel(draw,(65,287,655,490),(255,255,252,int(242*a)),(195,224,219,int(230*a)),radius=30)
    draw.rounded_rectangle((95,320,106,462),radius=6,fill=(*CYAN,int(244*a)))
    rtl(draw,365,356,'چرا تو ادورتیو',47,INK,alpha=255*a,max_width=530)
    rtl(draw,365,433,'آگهی نمی‌ذاری؟',47,INK,alpha=255*a,max_width=535)
    if t>=5.2:
        b=ease((t-5.2)/.48)
        panel(draw,(195,996,525,1071),(232,248,246,int(245*b)),(146,208,200,int(220*b)),radius=20)
        rtl(draw,360,1035,'ارسال بار مسافری',29,(34,124,127),alpha=255*b)

def form_row(draw,y,label,value,a):
    panel(draw,(129,y,591,y+84),(247,250,248,int(250*a)),(214,226,222,int(235*a)),radius=16)
    rtl(draw,555,y+28,label,18,(105,134,136),alpha=255*a,anchor='rm')
    rtl(draw,555,y+62,value,28,INK,alpha=255*a,anchor='rm')

def scene_three(draw,t):
    a=ease((t-7)/.4)
    panel(draw,(85,173,635,278),(249,252,249,int(249*a)),(202,223,219,int(225*a)),radius=25)
    rtl(draw,360,216,'ثبت آگهی در ادورتیو',37,INK,alpha=255*a)
    rtl(draw,360,259,'سریع و ساده',24,(49,151,153),alpha=255*a)
    if t<8.75:
        b=ease((t-7.1)/.5)
        panel(draw,(99,342,621,818),(255,255,252,int(235*a*b)),(206,226,223,int(222*a*b)),radius=30)
        form_row(draw,374,'مبدأ','کانادا',a*b)
        form_row(draw,473,'مقصد','ایران',a*b)
        form_row(draw,572,'نوع مرسوله','بسته',a*b)
        panel(draw,(161,708,559,784),(69,175,173,int(250*a*b)),(51,158,156,int(255*a*b)),radius=21)
        rtl(draw,360,748,'ثبت آگهی',34,WHITE,alpha=255*a*b)
        panel(draw,(174,922,546,990),(255,255,250,int(234*b)),(219,231,225,int(140*b)),radius=18)
        rtl(draw,360,957,'چند لحظه بعد...',26,(80,118,124),alpha=255*b)
    else:
        b=ease((t-8.75)/.38)
        panel(draw,(83,347,637,762),(255,255,253,int(244*a*b)),(178,216,213,int(220*a*b)),radius=30)
        panel(draw,(119,377,601,443),(224,245,241,int(250*b)),(184,221,214,int(222*b)),radius=17)
        rtl(draw,360,411,'پیام جدید از مسافر',29,(33,126,127),alpha=255*b)
        rtl(draw,360,516,'من هفته دیگه می‌رم ایران،',35,INK,alpha=255*b,max_width=520)
        rtl(draw,360,590,'می‌تونم ببرمش!',41,INK,alpha=255*b,max_width=510)
        panel(draw,(173,651,547,724),(64,178,175,int(250*b)),(42,159,154,int(250*b)),radius=20)
        rtl(draw,360,689,'مشاهده پیام',31,WHITE,alpha=255*b)

def scene_four(draw,t):
    a=ease((t-11)/.45)
    panel(draw,(65,214,655,448),(255,255,252,int(243*a)),(213,226,222,int(230*a)),radius=30)
    draw.rounded_rectangle((94,250,107,409),radius=6,fill=(*CORAL,int(246*a)))
    rtl(draw,365,289,'مسافرت رو پیدا کن،',45,INK,alpha=255*a,max_width=530)
    rtl(draw,365,377,'بارتو ارسال کن!',51,(40,145,147),alpha=255*a,max_width=520)
    panel(draw,(85,956,635,1101),(255,255,252,int(244*a)),(188,216,210,int(235*a)),radius=28)
    latin(draw,360,1006,'Advertio.net',44,INK,alpha=255*a)
    rtl(draw,360,1070,'ارسال بار مسافری',29,(39,142,146),alpha=255*a)

def make_frame(i):
    t=i/FPS
    src=P/'frames'/f'{i:04d}.png'
    im=Image.open(src).convert('RGBA')
    if im.size!=(W,H):
        im=im.resize((W,H),Image.Resampling.BILINEAR)
    im=background_tint(im)
    layer=Image.new('RGBA',(W,H),(0,0,0,0))
    d=ImageDraw.Draw(layer)
    draw_header(d,t)
    if t<4:scene_one(d,t)
    elif t<7:scene_two(d,t)
    elif t<11:scene_three(d,t)
    else:scene_four(d,t)
    return Image.alpha_composite(im,layer).convert('RGB')

def render_samples():
    for t in [0,1.5,3.5,4.5,6.5,8,9.5,11.5,13.5,14.9]:
        i=min(COUNT-1,round(t*FPS))
        filename=P/f'frame-sample-{i:03d}.jpg'
        make_frame(i).save(filename,quality=91)
        print(filename)

def render_mp4():
    out=OUTPUT
    cmd=[
        'ffmpeg','-hide_banner','-loglevel','error','-y',
        '-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}',
        '-r',str(FPS),'-i','-','-an',
        '-vf',f'scale={OUT_W}:{OUT_H}:flags=lanczos',
        '-c:v','libx264','-preset','ultrafast' if MODE=='preview' else 'fast',
        '-crf','28' if MODE=='preview' else '19',
        '-pix_fmt','yuv420p','-movflags','+faststart',str(out)
    ]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    try:
        for index in range(COUNT):
            proc.stdin.write(make_frame(index).tobytes())
            if index%90==0:print('Encoding frame',index,'/',COUNT,flush=True)
        proc.stdin.close()
    except Exception:
        proc.kill()
        proc.wait()
        raise
    if proc.wait()!=0:raise RuntimeError('FFmpeg video encoding failed')
    print('Finished:',out)

if __name__=='__main__':
    if '--samples' in sys.argv:render_samples()
    else:render_mp4()
