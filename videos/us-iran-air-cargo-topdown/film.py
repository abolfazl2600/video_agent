"""Advertio • USA ⇄ Iran • 18-second six-shot coded motion-design film.

The animation uses original vector artwork drawn in Pillow, not the supplied
reference-image pixels. It uses the project's *original uploaded* BYekan font
at ../../بز/BYekan.ttf for Persian text. No logo is generated or approximated.
Advertio is a listing/matching platform, not the airline or direct carrier.
"""
from __future__ import annotations
import math, os, random, subprocess, sys
from functools import lru_cache
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, features

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
ORIGINAL_FA = REPO / 'بز' / 'BYekan.ttf'
FONT_OVERRIDE = os.getenv('ADVERTIO_FONT_OVERRIDE', '').strip()
FA_FILE = Path(FONT_OVERRIDE) if FONT_OVERRIDE else ORIGINAL_FA
LATIN_FILE = REPO / 'assets' / 'fonts' / 'Vazirmatn-Bold.ttf'
if not LATIN_FILE.exists(): LATIN_FILE = Path('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf')
W,H=720,1280
DURATION=18
MODE=os.environ.get('ADVERTIO_RENDER_MODE','preview')
if MODE not in ('preview','final'): raise ValueError(f'Invalid render mode: {MODE}')
FPS=10 if MODE=='preview' else 30
OUTPUT=(540,960) if MODE=='preview' else (1080,1920)
C=(246,242,233); C2=(227,222,209); MUTED=(244,190,177)
BURG=(102,19,27); DEEP=(57,11,21); RED=(183,36,52); CORAL=(242,91,79)
INK=(47,36,43); BLUE=(64,125,150); TEAL=(54,133,131)
GOLD=(229,171,98)

def clamp(v): return min(1,max(0,v))
def ease(v): v=clamp(v);return v*v*(3-2*v)
def lerp(a,b,p):return a+(b-a)*p
def win(t,a,b,e=.3): return ease((t-a)/e)*(1-ease((t-(b-e))/e))
def op(c,a=255):return tuple(c)+(int(clamp(a/255)*255),)
@lru_cache(maxsize=128)
def fa_font(px):return ImageFont.truetype(str(FA_FILE),px)
@lru_cache(maxsize=128)
def en_font(px):return ImageFont.truetype(str(LATIN_FILE),px)

def fa(d,txt,cx,cy,size,color=C,alpha=255,max_w=625,stroke=0,anchor='mm'):
    size=int(size)
    while size>19:
        bb=d.textbbox((0,0),txt,font=fa_font(size),direction='rtl',language='fa',stroke_width=stroke)
        if bb[2]-bb[0]<=max_w:break
        size-=1
    d.text((int(cx),int(cy)),txt,font=fa_font(size),anchor=anchor,
           direction='rtl',language='fa',fill=op(color,alpha),stroke_width=stroke,
           stroke_fill=op(color,alpha))

def en(d,txt,x,y,size=19,color=C,alpha=255,anchor='mm'):
    d.text((int(x),int(y)),txt,font=en_font(int(size)),anchor=anchor,fill=op(color,alpha))

@lru_cache(maxsize=16)
def bg(theme='red'):
    im=Image.new('RGB',(W,H));p=im.load()
    if theme=='red':a,b=(55,12,23),(144,27,36)
    elif theme=='cream':a,b=(248,245,237),(228,223,209)
    elif theme=='ink':a,b=(30,26,39),(83,20,35)
    else:a,b=(60,18,30),(133,37,47)
    for y in range(H):
        s=y/(H-1)
        for x in range(W):
            v=abs(x-W/2)/(W/2)
            edge=1-.13*v*v
            p[x,y]=tuple(max(0,int(lerp(a[k],b[k],s)*edge)) for k in range(3))
    d=ImageDraw.Draw(im)
    rng=random.Random(20261123+len(theme))
    for i in range(9000):
        x,y=rng.randrange(W),rng.randrange(H)
        c=im.getpixel((x,y))
        a1=rng.choice((-5,-3,-2,1,2,4))
        d.point((x,y),fill=tuple(max(0,min(255,z+a1)) for z in c))
    return im

def layer():return Image.new('RGBA',(W,H))
def shadow_card(im,box,radius=28,fill=op(C),blur=19,off=(10,19),outline=None,width=1):
    x0,y0,x1,y1=map(int,box)
    sh=layer();sd=ImageDraw.Draw(sh)
    sd.rounded_rectangle((x0+off[0],y0+off[1],x1+off[0],y1+off[1]),radius=int(radius),fill=(17,10,20,90))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(blur)))
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((x0,y0,x1,y1),radius=int(radius),fill=fill,outline=outline,width=width)
    return d

def progress(im,t,idx,light=False):
    d=ImageDraw.Draw(im)
    fg=INK if light else C; dim=(99,86,88) if light else MUTED
    d.rounded_rectangle((54,1169,666,1173),radius=2,fill=op(dim,120))
    d.rounded_rectangle((54,1169,54+int(612*clamp(t/DURATION)),1173),radius=2,fill=op(CORAL if light else C))
    en(d,'ADVERTIO  /  AIR NETWORK',54,1214,19,fg,anchor='lm')
    en(d,f'{idx:02d} / 06',663,1213,17,fg,anchor='rm')
    for k in range(6):
        d.ellipse((55+k*22,1244,61+k*22,1250),fill=op(fg,230 if k==idx-1 else 72))

def photo_header(im,tag,light=False):
    d=ImageDraw.Draw(im);dark=INK if light else C
    d.rounded_rectangle((52,54,231,88),radius=16,fill=op(CORAL if not light else RED))
    en(d,tag,140,72,15,C)
    en(d,'18 SEC  /  9:16',654,69,17,dark,anchor='rm')

@lru_cache(maxsize=4)
def airplane_sprite():
    s=260; im=Image.new('RGBA',(s,s));d=ImageDraw.Draw(im)
    # original clean airliner silhouette seen orthographically from above
    body=[(124,14),(136,14),(141,92),(224,143),(230,159),(216,164),(143,143),
          (142,204),(172,222),(172,232),(130,218),(88,232),(88,222),(118,204),
          (117,143),(44,164),(30,159),(36,143),(119,92)]
    d.polygon([(x+7,y+9) for x,y in body],fill=(18,15,17,130))
    d.polygon(body,fill=(248,246,240))
    d.polygon([(126,23),(134,23),(136,126),(124,126)],fill=(190,48,63))
    d.polygon([(36,149),(119,127),(139,127),(224,149),(221,156),(140,140),(119,140),(39,156)],fill=(216,214,207))
    d.line([(130,48),(130,213)],fill=(193,190,188),width=3)
    d.ellipse((121,34,139,59),fill=(38,48,58))
    d.line([(45,155),(118,135)],fill=(168,166,159),width=2)
    d.line([(142,135),(215,155)],fill=(168,166,159),width=2)
    d.ellipse((31,152,42,162),fill=CORAL);d.ellipse((217,152,228,162),fill=TEAL)
    return im

@lru_cache(maxsize=4)
def parcel_sprite():
    im=Image.new('RGBA',(260,250));d=ImageDraw.Draw(im)
    d.ellipse((43,174,229,216),fill=(25,10,13,54))
    d.polygon([(30,89),(133,47),(236,89),(133,131)],fill=(236,206,158))
    d.polygon([(30,89),(133,131),(133,216),(30,177)],fill=(176,125,89))
    d.polygon([(133,131),(236,89),(236,178),(133,216)],fill=(215,173,118))
    d.polygon([(109,57),(135,47),(238,88),(212,101)],fill=(250,236,202))
    d.polygon([(102,118),(126,129),(126,214),(102,206)],fill=(250,231,195))
    d.line((30,89,133,132,236,89),fill=(255,240,208),width=4)
    return im

@lru_cache(maxsize=4)
def passport_sprite():
    im=Image.new('RGBA',(260,310));d=ImageDraw.Draw(im)
    d.rounded_rectangle((45,29,223,282),radius=17,fill=(37,20,25,82))
    d.rounded_rectangle((28,18,209,272),radius=17,fill=(119,27,46),outline=(248,205,164),width=3)
    d.rounded_rectangle((40,30,197,260),radius=10,outline=(201,138,111),width=2)
    d.ellipse((74,97,165,193),outline=(245,210,178),width=6)
    d.arc((92,110,152,179),60,310,fill=(245,210,178),width=5)
    for yy in (76,213,234):d.line((82,yy,163,yy),fill=(241,196,162),width=3)
    return im

@lru_cache(maxsize=4)
def document_sprite():
    im=Image.new('RGBA',(190,230));d=ImageDraw.Draw(im)
    d.rounded_rectangle((18,28,173,217),radius=12,fill=(54,39,37,77))
    d.rounded_rectangle((8,11,160,208),radius=12,fill=C,outline=(205,195,180),width=3)
    d.rounded_rectangle((34,38,91,67),radius=5,fill=RED)
    for yy,s in [(93,113),(117,113),(141,85),(165,105)]:d.rounded_rectangle((33,yy,33+s,yy+6),radius=3,fill=(151,153,149))
    d.ellipse((102,151,140,188),outline=CORAL,width=5)
    return im

def spr(im,sprite,cx,cy,scale=1,angle=0,alpha=255):
    w=max(2,int(sprite.width*scale));h=max(2,int(sprite.height*scale))
    im2=sprite.resize((w,h),Image.Resampling.LANCZOS)
    if angle:im2=im2.rotate(angle,expand=True,resample=Image.Resampling.BICUBIC)
    if alpha<255:im2.putalpha(im2.getchannel('A').point(lambda v:int(v*alpha/255)))
    im.alpha_composite(im2,(round(cx-im2.width/2),round(cy-im2.height/2)))

def route(d,curve,frac,color=C,width=8,steps=110):
    def point(v):
        u=1-v;return((u*u*curve[0][0]+2*u*v*curve[1][0]+v*v*curve[2][0]),(u*u*curve[0][1]+2*u*v*curve[1][1]+v*v*curve[2][1]))
    n=max(2,round(steps*clamp(frac)))
    pts=[point((i/n)*clamp(frac)) for i in range(n+1)]
    d.line(pts,fill=op(color),width=width,joint='curve')
    return point(frac)

def stamp(d,x,y,title,sub,color=C):
    d.ellipse((x-78,y-78,x+78,y+78),fill=op((79,26,39)),outline=op(color,180),width=4)
    d.ellipse((x-64,y-64,x+64,y+64),outline=op((218,159,153)),width=2)
    en(d,title,x,y-12,29,color)
    en(d,sub,x,y+27,14,color)

def scene1(t):
    im=bg('red').convert('RGBA');d=ImageDraw.Draw(im)
    photo_header(im,'01  /  THE HOOK')
    a=ease((t-.05)/.6);push=35*(1-a)
    fa(d,'آمریکا',360,200+push,100,C,int(255*a),stroke=1)
    en(d,'⇅',360,300,63,CORAL,int(255*a))
    fa(d,'ایران',360,388+push,100,C,int(255*a),stroke=1)
    # two staggered white top-down pathways with opposing movement
    d.rounded_rectangle((220,494,496,1122),radius=125,fill=op((36,14,24),175))
    d.rounded_rectangle((248,482,475,1110),radius=108,fill=op(C2))
    d.line((361,521,361,1092),fill=op(RED,220),width=10)
    for y in range(590,1090,98):
        d.rounded_rectangle((282,y,317,y+37),radius=9,fill=op(C,160))
        d.rounded_rectangle((402,y,435,y+37),radius=9,fill=op(C,160))
    spr(im,airplane_sprite(),360,lerp(986,691,ease(t/3)),.89,angle=0)
    fa(d,'بارت رو می‌خوای بفرستی؟',360,1109,36,C)
    progress(im,t,1)
    return im

def scene2(t):
    im=bg('cream').convert('RGBA');d=ImageDraw.Draw(im)
    photo_header(im,'02  /  THE ITEMS',light=True)
    fa(d,'بار یا مدارک؟',360,198,73,INK,stroke=1)
    fa(d,'هر دو، با مسافر هوایی',360,276,39,RED)
    # close shot of two tactile product cards, playful alternation
    shade=ease(t/.55)
    shift=(1-shade)*110
    left=(50-shift,402,353-shift,949)
    right=(367+shift,402,670+shift,949)
    shadow_card(im,left,30,op((251,250,245)),blur=15,outline=op((204,195,183)))
    shadow_card(im,right,30,op((245,241,232)),blur=15,outline=op((204,195,183)))
    d=ImageDraw.Draw(im)
    spr(im,parcel_sprite(),202-shift,628+8*math.sin(t*3),1.02,angle=0)
    spr(im,passport_sprite(),512+shift,620-8*math.sin(t*3),.78,angle=-13)
    spr(im,document_sprite(),544+shift,725,.67,angle=9)
    d=ImageDraw.Draw(im)
    fa(d,'بسته',203-shift,867,47,INK)
    fa(d,'مدارک',516+shift,867,47,INK)
    d.rounded_rectangle((195,999,525,1047),radius=22,fill=op(RED))
    fa(d,'هوایی  •  دوطرفه',360,1021,27,C)
    progress(im,t+3,2,light=True)
    return im

def scene3(t):
    im=bg('ink').convert('RGBA');d=ImageDraw.Draw(im)
    photo_header(im,'03  /  THE FLIGHT')
    fa(d,'یک مسیر، دو جهت',360,186,62,C,stroke=1)
    en(d,'USA  ⇄  IRAN',360,275,40,CORAL)
    # origami-like floating route map, no copied geographical shapes
    for r in (240,307,369):
        d.ellipse((360-r,657-r,360+r,657+r),outline=op((160,110,117),90),width=2)
    for ang in range(0,360,30):
        rr=314;theta=math.radians(ang)
        x=360+rr*math.cos(theta);y=660+rr*math.sin(theta)
        d.ellipse((x-3,y-3,x+3,y+3),fill=op((221,138,142),135))
    stamp(d,156,858,'USA','ORIGIN',C)
    stamp(d,559,487,'IRAN','DEST.',C)
    curve=((178,795),(345,333),(530,549))
    d.line([(178,795),(245,607),(333,511),(530,549)],fill=op(C,42),width=4)
    fraction=ease(t/2.4)
    xx,yy=route(d,curve,fraction,CORAL,9)
    # sparkle after the plane, not dense visual clutter
    for k in range(7):
        p=((t*2.2-k*.13)%1)
        if p<fraction:
            px,py=route_point(curve,p)
            d.ellipse((px-3,py-3,px+3,py+3),fill=op(C,160))
    angle=-42+68*fraction
    spr(im,airplane_sprite(),xx,yy,.8,angle=angle)
    fa(d,'از هر سمت، با پرواز مسافران',360,1053,33,C)
    progress(im,t+6,3)
    return im

def route_point(curve,v):
    u=1-v
    return (u*u*curve[0][0]+2*u*v*curve[1][0]+v*v*curve[2][0],u*u*curve[0][1]+2*u*v*curve[1][1]+v*v*curve[2][1])

def phone_ui(im,t):
    d=ImageDraw.Draw(im)
    x0,y0,x1,y1=126,355,595,1062
    shadow_card(im,(x0,y0,x1,y1),50,op((30,30,35)),blur=23,off=(15,22))
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((x0+10,y0+10,x1-10,y1-10),radius=43,fill=op((251,250,246)))
    d.rounded_rectangle((290,369,432,393),radius=11,fill=op((32,31,34)))
    en(d,'advertio.net',361,438,29,INK)
    d.rounded_rectangle((161,470,559,526),radius=18,fill=op((238,235,229)))
    fa(d,'آگهی‌های مسافران هوایی',361,500,27,INK)
    for i,yy in enumerate((560,694,828)):
        sc=ease((t-(.22+i*.18))/.34)
        shift=65*(1-sc)
        d.rounded_rectangle((164+shift,yy,557+shift,yy+114),radius=18,fill=op((255,255,252),int(255*sc)),outline=op((217,214,209),int(255*sc)),width=2)
        d.ellipse((188+shift,yy+27,240+shift,yy+79),fill=op((218,232,230),int(255*sc)))
        en(d,'✈',214+shift,yy+54,25,TEAL,int(255*sc))
        fa(d,'آمریکا  ⇄  ایران',386+shift,yy+38,27,INK,int(255*sc))
        fa(d,'مسافر هوایی  •  پیام مستقیم',388+shift,yy+83,20,TEAL,int(255*sc))
    d.rounded_rectangle((253,981,474,1026),radius=22,fill=op((71,144,137)))
    fa(d,'مشاهده آگهی‌ها',363,1001,23,C)

def scene4(t):
    im=bg('cream').convert('RGBA');d=ImageDraw.Draw(im)
    photo_header(im,'04  /  THE MATCH',light=True)
    fa(d,'مسافر مسیرت رو',360,183,59,INK,stroke=1)
    fa(d,'توی ادورتیو پیدا کن',360,260,48,RED,stroke=1)
    phone_ui(im,t)
    # a movable reply bubble offsets the composition from earlier shots
    if t>.92:
        a=ease((t-.92)/.36); yy=891-(1-a)*95
        d=ImageDraw.Draw(im)
        d.rounded_rectangle((65,int(yy),365,int(yy+78)),radius=27,fill=op(TEAL,int(255*a)))
        fa(d,'برای حمل بار هماهنگ کنیم؟',216,int(yy+40),24,C,int(255*a))
    progress(im,t+9,4,light=True)
    return im

def scene5(t):
    im=bg('red').convert('RGBA');d=ImageDraw.Draw(im)
    photo_header(im,'05  /  THE TIMELINE')
    fa(d,'زمان تقریبی هماهنگی',360,179,48,C)
    # a kinetic calendar-board graphic instead of a static number
    shadow_card(im,(80,354,638,972),46,op((249,246,240)),blur=20)
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((80,354,638,478),radius=43,fill=op(RED))
    d.rectangle((80,420,638,478),fill=op(RED))
    for x in (171,547):
        d.ellipse((x-13,370,x+13,399),fill=op((244,224,211)))
    fa(d,'حدود',360,552,67,INK)
    fa(d,'۲',360,731,210,RED,stroke=2)
    fa(d,'هفته*',360,856,77,INK,stroke=1)
    # cards filling left->right to visually denote approximate two weeks
    for i in range(14):
        x=133+(i%7)*68;y=916+(i//7)*34
        active=ease((t-.15-i*.055)/.25)
        d.rounded_rectangle((x,y,x+42,y+22),radius=6,fill=op(TEAL if active>.5 else (215,212,208)))
    fa(d,'* بسته به مسیر و توافق با مسافر',360,1070,28,C)
    progress(im,t+12,5)
    return im

def scene6(t):
    im=bg('ink').convert('RGBA');d=ImageDraw.Draw(im)
    photo_header(im,'06  /  ADVERTIO')
    # glowing single path converges to the service name, overhead runway motif
    d.rounded_rectangle((264,330,456,994),radius=95,fill=op((25,18,28),205))
    d.rounded_rectangle((282,331,439,991),radius=74,fill=op((234,229,219)))
    d.line((360,385,360,968),fill=op(RED),width=9)
    for k in range(6):
        yy=445+k*79
        d.rounded_rectangle((298,yy,315,yy+40),radius=7,fill=op(C,165))
        d.rounded_rectangle((407,yy,422,yy+40),radius=7,fill=op(C,165))
    spr(im,airplane_sprite(),360,815-246*ease(t/3),.83)
    # top and bottom are framed like an editorial campaign ending
    d=ImageDraw.Draw(im)
    fa(d,'بار و مدارکت',360,190,61,C,stroke=1)
    fa(d,'با مسافر هوایی',360,267,49,CORAL,stroke=1)
    d.rounded_rectangle((77,992,642,1132),radius=30,fill=op((60,15,28),246),outline=op((231,154,150),130),width=2)
    en(d,'advertio.net',359,1041,52,C)
    fa(d,'آگهی‌ها را ببین و مستقیم هماهنگ کن',360,1097,25,C2)
    progress(im,t+15,6)
    return im

SCENES=[scene1,scene2,scene3,scene4,scene5,scene6]

def frame(t):
    t=max(0,min(DURATION-.00001,float(t)))
    idx=min(5,int(t//3)); local=t-3*idx
    current=SCENES[idx](local)
    # cinematic cross-dissolve between genuinely different compositions
    # 0.24s first; previous composition is never shown with a static background
    if idx>0 and local<.25:
        old=SCENES[idx-1](3+local)
        current=Image.blend(old,current,ease(local/.25))
    return current.convert('RGB')

def samples():
    picks=[0.7,2.35,3.65,5.25,6.35,8.3,9.8,11.4,13.3,16.8]
    thumbs=[]
    for i,t in enumerate(picks):
        f=HERE/f'frame-sample-{i+1:02d}.jpg';frame(t).save(f,quality=88,subsampling=0)
        thumbs.append(f)
    col,tw,th,gap=5,225,400,14
    sheet=Image.new('RGB',(2*24+col*tw+(col-1)*gap,2*31+2*th+46),(246,242,233));d=ImageDraw.Draw(sheet)
    en(d,'ADVERTIO  /  SIX-SCENE REDESIGN  /  18s',26,31,24,INK,anchor='lm')
    for i,(f,t) in enumerate(zip(thumbs,picks)):
        x=24+(i%col)*(tw+gap);y=68+(i//col)*(th+gap)
        with Image.open(f) as im:sheet.paste(im.resize((tw,th),Image.Resampling.LANCZOS),(x,y))
        d.text((x+5,y+4),f'{t:04.1f}s',font=en_font(15),fill=op(C))
    sheet.save(HERE/'quick-preview-contact-sheet.jpg',quality=92,subsampling=0)
    print('10 JPG storyboard frames + quick-preview-contact-sheet.jpg',flush=True)

def render():
    out=HERE/('preview.mp4' if MODE=='preview' else 'output.mp4')
    command=['ffmpeg','-y','-hide_banner','-loglevel','error','-f','rawvideo','-vcodec','rawvideo',
             '-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an',
             '-vf',f'scale={OUTPUT[0]}:{OUTPUT[1]}:flags=bicubic','-c:v','libx264',
             '-preset','ultrafast' if MODE=='preview' else 'medium',
             '-crf','24' if MODE=='preview' else '19','-pix_fmt','yuv420p',
             '-movflags','+faststart',str(out)]
    process=subprocess.Popen(command,stdin=subprocess.PIPE)
    try:
        for i in range(DURATION*FPS):
            process.stdin.write(frame(i/FPS).tobytes())
            if i%30==0:print(f'render {i}/{DURATION*FPS}',flush=True)
        process.stdin.close()
    except Exception:
        process.kill();process.wait();raise
    if process.wait():raise RuntimeError('ffmpeg output failed')
    print(f'Render complete: {out}',flush=True)

if __name__=='__main__':
    if not features.check('raqm'):raise RuntimeError('Pillow libraqm needed to render Persian RTL')
    if not FA_FILE.is_file():raise FileNotFoundError(f'Original font not found: {FA_FILE}')
    samples() if '--samples' in sys.argv else render()
