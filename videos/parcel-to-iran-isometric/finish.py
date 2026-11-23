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
CYAN = (61, 225, 223)
WHITE = (238, 250, 252)
INK = (7, 21, 35)
DARK = (13, 34, 53)
CORAL = (247, 121, 124)

@lru_cache(None)
def font(size, bold=False):
    return ImageFont.truetype(str(BOLD if bold else FONT), size)

def fit_font(draw, text, size, bold, max_width, direction=None):
    """Keep Persian labels in the safe zone with the chosen Vazirmatn weight."""
    if not max_width:
        return font(size, bold)
    while size > 16:
        f = font(size, bold)
        kwargs = {'direction': direction, 'language': 'fa'} if direction else {}
        box = draw.textbbox((0, 0), text, font=f, **kwargs)
        if box[2]-box[0] <= max_width:
            return f
        size -= 1
    return font(size, bold)

def ease(x):
    x = max(0, min(1, x))
    return x*x*(3-2*x)

def rtl(draw, x, y, txt, size, color=WHITE, bold=True, alpha=255, anchor='mm', max_width=None):
    # Center titles use up to 610 px; right-aligned form values use 405 px.
    if max_width is None:
        max_width = 405 if anchor == 'rm' else 605
    f = fit_font(draw,txt,size,bold,max_width,'rtl')
    draw.text((x,y),txt,font=f,anchor=anchor,
              language='fa',direction='rtl',fill=(*color,int(alpha)))

def latin(draw,x,y,txt,size=24,color=WHITE,alpha=255,anchor='mm',bold=True):
    f = fit_font(draw,txt,size,bold,590)
    draw.text((x,y),txt,font=f,anchor=anchor,fill=(*color,int(alpha)))

def panel(draw, xy, fill, outline, radius=28, width=3):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)

def background_tint(image):
    layer=Image.new('RGBA',(W,H),(0,0,0,0))
    d=ImageDraw.Draw(layer)
    # The dark top/bottom bands are translucent so the 3D isometric world stays visible.
    for y in range(0,465,5):
        a=int(163*(1-y/465)**1.15)
        d.rectangle((0,y,W,y+5),fill=(5,15,27,a))
    for y in range(920,H,5):
        a=int(155*((y-920)/(H-920))**1.15)
        d.rectangle((0,y,W,y+5),fill=(5,15,27,a))
    return Image.alpha_composite(image,layer)

def draw_header(draw,t):
    latin(draw,56,70,'ADVERTIO',24,CYAN,anchor='lm')
    latin(draw,664,70,'3D / ISOMETRIC',15,(158,215,225),anchor='rm',bold=False)
    draw.line([(55,101),(665,101)],fill=(*CYAN,95),width=2)
    # Thin scene progress indicator, safe within short-form video margins.
    draw.rounded_rectangle((55,1194,665,1200),radius=3,fill=(56,88,105,170))
    draw.rounded_rectangle((55,1194,55+round(610*t/15),1200),
                           radius=3,fill=(*CYAN,230))
    latin(draw,55,1235,'ADVERTIO.NET',18,(198,239,242),anchor='lm')
    latin(draw,665,1235,'00:15',17,(145,187,198),anchor='rm',bold=False)

def scene_one(draw,t):
    a=ease(t/.45)
    rtl(draw,360,180,'کانادا به ایران',50,CYAN,alpha=255*a)
    rtl(draw,360,254,'یه بسته، یه دغدغه...',30,WHITE,alpha=220*a)
    panel(draw,(56,312,664,477),(17,39,58,int(237*a)),(*CORAL,int(208*a)),radius=30)
    rtl(draw,360,369,'کاش یکی بود این بسته رو',39,WHITE,alpha=255*a)
    rtl(draw,360,426,'برام ببره ایران!',46,WHITE,alpha=255*a)
    if t>2.35:
        b=ease((t-2.35)/.45)
        rtl(draw,360,1037,'راه‌حل نزدیک‌تر از چیزیه که فکر می‌کنی...',24,CYAN,alpha=245*b)

def scene_two(draw,t):
    a=ease((t-4)/.4)
    rtl(draw,360,184,'دوستش یه راه نشونش می‌ده',31,CYAN,alpha=255*a)
    panel(draw,(64,282,656,472),(17,42,61,int(240*a)),(*CYAN,int(210*a)),radius=29)
    rtl(draw,360,345,'چرا تو ادورتیو',48,WHITE,alpha=255*a)
    rtl(draw,360,419,'آگهی نمی‌ذاری؟',51,WHITE,alpha=255*a)
    if t>=5.2:
        b=ease((t-5.2)/.5)
        panel(draw,(182,985,538,1052),(5,49,65,int(226*b)),(*CYAN,int(195*b)),radius=24)
        rtl(draw,360,1020,'ارسال بار مسافری',29,WHITE,alpha=255*b)

def form_row(draw,y,label,value,a):
    panel(draw,(118,y,602,y+85),(227,240,242,int(247*a)),(170,201,207,int(205*a)),radius=14,width=2)
    rtl(draw,565,y+25,label,18,(54,87,103),alpha=255*a,anchor='rm')
    rtl(draw,565,y+61,value,25,(14,51,70),alpha=255*a,anchor='rm')

def scene_three(draw,t):
    a=ease((t-7)/.42)
    panel(draw,(80,211,640,1102),(5,17,30,int(218*a)),(*CYAN,int(190*a)),radius=35)
    panel(draw,(95,226,625,1087),(238,248,249,int(248*a)),(130,192,201,int(206*a)),radius=27,width=2)
    panel(draw,(95,226,625,328),(18,177,189,int(250*a)),(18,177,189,int(250*a)),radius=25,width=1)
    rtl(draw,360,270,'ادورتیو',40,WHITE,alpha=255*a)
    rtl(draw,360,309,'ارسال بار مسافری',19,WHITE,alpha=235*a)
    if t<8.75:
        b=ease((t-7.12)/.5)
        rtl(draw,360,385,'ثبت آگهی جدید',34,(19,56,72),alpha=255*a)
        form_row(draw,436,'مبدأ','کانادا',a*b)
        form_row(draw,549,'مقصد','ایران',a*b)
        form_row(draw,662,'نوع مرسوله','بسته',a*b)
        panel(draw,(138,812,582,899),(13,164,174,int(255*a*b)),(4,145,155,int(255*a*b)),radius=20)
        rtl(draw,360,857,'ثبت آگهی',34,WHITE,alpha=255*a*b)
        rtl(draw,360,970,'چند لحظه بعد...',26,(42,102,113),alpha=225*a*b)
    else:
        b=ease((t-8.75)/.38)
        rtl(draw,360,389,'پیام جدید از مسافر',31,(16,87,101),alpha=255*a*b)
        panel(draw,(127,464,593,748),(216,241,244,int(254*a*b)),(93,174,185,int(230*a*b)),radius=26,width=2)
        rtl(draw,360,525,'من هفته دیگه می‌رم ایران،',31,(13,63,79),alpha=255*a*b)
        rtl(draw,360,589,'می‌تونم ببرمش!',36,(13,63,79),alpha=255*a*b)
        panel(draw,(193,825,527,901),(14,175,183,int(255*a*b)),(11,153,160,int(255*a*b)),radius=18)
        rtl(draw,360,865,'مشاهده پیام',27,WHITE,alpha=255*a*b)
        rtl(draw,360,981,'مسافر در مسیرت پیدا شد!',27,(13,91,101),alpha=255*a*b)

def scene_four(draw,t):
    a=ease((t-11)/.48)
    rtl(draw,360,177,'مسافرت رو پیدا کن،',48,WHITE,alpha=255*a)
    rtl(draw,360,249,'بارتو ارسال کن!',53,CYAN,alpha=255*a)
    # Clear final CTA, not a fabricated logo.
    panel(draw,(68,954,652,1091),(5,44,57,int(238*a)),(*CYAN,int(217*a)),radius=28)
    latin(draw,360,1000,'Advertio.net',42,WHITE,alpha=255*a)
    rtl(draw,360,1057,'ارسال بار مسافری',27,CYAN,alpha=255*a)
    if t>=12:
        b=ease((t-12)/.48)
        rtl(draw,360,858,'ساده‌تر از همیشه',30,WHITE,alpha=255*b)

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
