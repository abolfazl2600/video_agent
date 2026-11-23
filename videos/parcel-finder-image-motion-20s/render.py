#!/usr/bin/env python3
"""Advertio Image-to-Motion Storyboard 20 sec / five independent illustrated scenes.
Assets: original generated scene artwork plus the unmodified original supplied logo.
A static image is placed in a lower rounded viewport; a real virtual camera pans/zooms
it over time while story-relevant overlay graphics animate independently.
"""
from __future__ import annotations
import math, os, sys, subprocess, argparse
from pathlib import Path
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

HERE=Path(__file__).resolve().parent
ASSETS=HERE/'assets'; ASSETS.mkdir(exist_ok=True)
W,H=720,1280
MODE=os.getenv('ADVERTIO_RENDER_MODE','preview')
if MODE not in ('preview','final','quick-preview'):raise ValueError('Unknown render mode: '+MODE)
FPS=int(os.getenv('ADVERTIO_FPS','30' if MODE=='final' else '15'))
DUR=20
TOTAL=FPS*DUR
TIMES=[0,3,7,11,16,20]
FRAME_NAMES=[f'scene-{i:02d}.jpg' for i in range(1,6)]
POSTER=Path(os.getenv('ADVERTIO_STORYBOARD_SOURCE','/mnt/data/a_highly_detailed_vertical_storyboard_poster_col.png'))
SOURCE=Path(os.getenv('ADVERTIO_HOOK_SOURCE','/mnt/data/a_polished_3d_isometric_low_poly_rounded_3d_illust.png'))
LOGO=Path(os.getenv('ADVERTIO_ORIGINAL_LOGO',str(ASSETS/'Advertio Logo.png')))
BOLD=Path(os.getenv('ADVERTIO_FONT_BOLD',str(HERE.parents[1]/'assets/fonts/Vazirmatn-Bold.ttf')))
if not BOLD.exists(): BOLD=Path('/usr/share/fonts/truetype/noto/NotoSansArabic-Bold.ttf')
REG=Path(os.getenv('ADVERTIO_FONT_REGULAR',str(HERE.parents[1]/'assets/fonts/Vazirmatn-Regular.ttf')))
if not REG.exists(): REG=Path('/usr/share/fonts/truetype/noto/NotoSansArabic-Regular.ttf')
LAT=Path('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf')
BG=(249,249,246);INK=(35,42,49);ORANGE=(239,99,44);BLUE=(30,137,219);MUTED=(102,111,115)
CARD=(28,413,692,1063);CW=CARD[2]-CARD[0];CH=CARD[3]-CARD[1]
MOTION=[(0,3),(3,7),(7,11),(11,16),(16,20)]

def E(x):
    x=max(0,min(1,x));return x*x*(3-2*x)
def interp(a,b,x):return a+(b-a)*x
@lru_cache(maxsize=128)
def font(sz,bold=True,latin=False):return ImageFont.truetype(str(LAT if latin else (BOLD if bold else REG)),int(sz))
def txt(d,text,x,y,sz,color=INK,bold=True,maxw=627,align='mm'):
    sz=int(sz)
    while sz>17:
        f=font(sz,bold)
        bbox=d.textbbox((0,0),text,font=f,direction='rtl',language='fa')
        if bbox[2]-bbox[0]<=maxw:break
        sz-=1
    d.text((x,y),text,font=font(sz,bold),anchor=align,direction='rtl',language='fa',fill=color)
def lt(d,text,x,y,sz=22,color=INK,anchor='mm'):
    d.text((x,y),text,font=font(sz,True,True),anchor=anchor,fill=color)
def rounded(d,xy,r,fill,outline=None,width=1):d.rounded_rectangle(tuple(map(int,xy)),radius=int(r),fill=fill,outline=outline,width=width)
def fit_cover(image,width,height):
    sw,sh=image.size; scale=max(width/sw,height/sh)
    im=image.resize((math.ceil(sw*scale),math.ceil(sh*scale)),Image.Resampling.LANCZOS)
    x=(im.width-width)//2;y=(im.height-height)//2
    return im.crop((x,y,x+width,y+height))
def fit_contain(image,width,height):
    im=image.copy();im.thumbnail((width,height),Image.Resampling.LANCZOS);return im

def extracted_original_logo():
    # The official original Advertio Logo.png is sampled directly; no redraw or approximation.
    img=Image.open(LOGO).convert('RGB')
    import numpy as np
    ar=np.asarray(img)
    p=ar.min(axis=2)<180
    ys,xs=np.where(p)
    if len(xs):img=img.crop((int(xs.min()),int(ys.min()),int(xs.max())+1,int(ys.max())+1))
    # White is only transparent for compositing. Colored pixels remain original.
    ar=np.array(img.convert('RGB'))
    alpha=np.clip(((255-ar.min(axis=2).astype(float))/85)*255,0,255).astype('uint8')
    result=Image.fromarray(__import__('numpy').dstack([ar,alpha]),'RGBA')
    return result

def glow_background(size=(1200,900), color=(246,248,247)):
    im=Image.new('RGB',size,color);d=ImageDraw.Draw(im)
    d.ellipse((-100,-160,700,600),fill=(231,239,241));d.ellipse((630,300,1380,1050),fill=(238,234,232))
    return im.filter(ImageFilter.GaussianBlur(85))

def put_panel(canvas,image,xy,radius=45):
    x,y,w,h=xy;im=fit_cover(image,w,h)
    shadow=Image.new('RGBA',canvas.size,(0,0,0,0));sh=ImageDraw.Draw(shadow)
    sh.rounded_rectangle((x+12,y+17,x+w+12,y+h+17),radius=radius,fill=(38,55,73,43))
    canvas.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(16)))
    mask=Image.new('L',(w,h));md=ImageDraw.Draw(mask);md.rounded_rectangle((0,0,w-1,h-1),radius=radius,fill=255)
    canvas.paste(im,(x,y),mask)

def phone(canvas, rect, listing=True, chat=False, bigbrand=True):
    """UI mockup rendered separately with only original logo."""
    x,y,w,h=rect;d=ImageDraw.Draw(canvas)
    rounded(d,(x+15,y+22,x+w+17,y+h+25),54,(47,65,82,56))
    rounded(d,(x,y,x+w,y+h),50,(32,47,61),outline=(80,98,113),width=5)
    rounded(d,(x+13,y+14,x+w-13,y+h-14),38,(255,255,254))
    rounded(d,(x+w//2-48,y+18,x+w//2+48,y+32),12,(32,47,61))
    if bigbrand:
        logo=extracted_original_logo();logo.thumbnail((76,76),Image.Resampling.LANCZOS)
        canvas.alpha_composite(logo,(x+32,y+62))
        d.text((x+122,y+95),'Advertio',font=font(30,True,True),fill=INK,anchor='lm')
    if listing:
        rounded(d,(x+29,y+164,x+w-29,y+218),19,(237,112,58))
        txt(d,'ارسال بار مسافری',x+w/2,y+190,25,(255,255,255))
        for k in range(3):
            yy=y+240+k*107
            rounded(d,(x+30,yy,x+w-30,yy+91),20,(241,247,248),outline=(226,235,235),width=2)
            d.ellipse((x+47,yy+16,x+104,yy+73),fill=(204,225,233))
            d.ellipse((x+66,yy+24,x+83,yy+41),fill=(101,144,160))
            txt(d,['کانادا ← ایران','تورنتو ← تهران','مونترال ← تهران'][k],x+w-115,yy+29,21)
            txt(d,'مسافر هوایی',x+w-105,yy+63,16,MUTED,False)
    if chat:
        for k,(s,c) in enumerate([('جمعه می‌رم تهران',(229,244,250)),('می‌تونم بسته‌ات رو ببرم',(220,241,234))]):
            yy=y+217+k*118
            rounded(d,(x+40,yy,x+w-36,yy+96),22,c)
            txt(d,s,x+w/2,yy+48,22)
    rounded(d,(x+70,y+h-56,x+w-70,y+h-46),6,(191,201,208))

def build_assets():
    if all((ASSETS/n).is_file() for n in FRAME_NAMES):return
    for f in (POSTER,SOURCE,LOGO):
        if not f.is_file():raise FileNotFoundError(f'Required original source not found: {f}')
    s=Image.open(POSTER).convert('RGB')
    h=Image.open(SOURCE).convert('RGB')
    # 1: original premium AI-generated woman/package illustration, no invented mark.
    a=fit_cover(h,1200,900)
    a.save(ASSETS/FRAME_NAMES[0],quality=91,subsampling=0)
    # 2: genuine generated airport traveler + Canada sender, no baked-in text.
    b=glow_background().convert('RGBA')
    traveler=s.crop((122,472,400,686)); girl=s.crop((419,533,635,686))
    put_panel(b,traveler,(44,60,657,755),62)
    put_panel(b,girl,(730,282,415,420),55)
    d=ImageDraw.Draw(b)
    d.rounded_rectangle((780,105,1110,190),radius=43,fill=(255,255,255,232))
    d.ellipse((825,123,875,173),fill=ORANGE);d.ellipse((931,123,981,173),fill=BLUE)
    d.line((873,147,935,147),fill=(123,161,173),width=8)
    b.convert('RGB').save(ASSETS/FRAME_NAMES[1],quality=91,subsampling=0)
    # 3: large readable app mockup with *only official original logo*.
    c=glow_background().convert('RGBA')
    d=ImageDraw.Draw(c)
    d.ellipse((600,70,1170,710),fill=(227,236,239));d.ellipse((40,550,520,1130),fill=(246,236,222))
    phone(c,(285,22,570,841),True,False)
    put_panel(c,s.crop((423,420,623,681)),(30,370,287,360),48)
    d=ImageDraw.Draw(c)
    for x,y in [(121,240),(1040,188),(925,765)]:
        d.ellipse((x,y,x+24,y+24),fill=ORANGE)
    c.convert('RGB').save(ASSETS/FRAME_NAMES[2],quality=92,subsampling=0)
    # 4: two real characters (from the source reference illustration), separate clean UI overlay.
    dimg=glow_background(color=(239,246,248)).convert('RGBA')
    put_panel(dimg,s.crop((120,1014,383,1280)),(30,80,415,720),45)
    put_panel(dimg,s.crop((704,1010,921,1280)),(786,95,382,725),45)
    d=ImageDraw.Draw(dimg)
    d.ellipse((528,350,680,505),fill=(220,240,248));d.ellipse((556,375,652,472),fill=(56,154,211))
    d.line((220,660,570,445,950,660),fill=(38,156,226),width=15,joint='curve')
    dimg.convert('RGB').save(ASSETS/FRAME_NAMES[3],quality=93,subsampling=0)
    # 5: real illustration of flight geography plus cleaned app phone with true logo.
    e=glow_background(color=(237,244,249)).convert('RGBA')
    put_panel(e,s.crop((120,1322,403,1647)),(22,90,615,712),55)
    phone(e,(640,58,505,772),listing=True,chat=False)
    e.convert('RGB').save(ASSETS/FRAME_NAMES[4],quality=92,subsampling=0)

def scene_idx(t):
    if t<3:return 0
    if t<7:return 1
    if t<11:return 2
    if t<16:return 3
    return 4

def camera_crop(img,u,scene):
    # Keep main artwork in a fixed lower viewport, pan within the illustration.
    w,h=img.size
    v=E(u)
    z=1+0.042*v +(0.12*E(min(1,u*2.2)) if scene==0 else 0)
    crop_h=int(min(h,round(780/z)))
    crop_w=int(crop_h*CW/CH)
    if crop_w>w:crop_w=w;crop_h=int(crop_w*CH/CW)
    span=max(0,w-crop_w)
    offsets=[(.53,.40),(.13,.80),(.20,.70),(.06,.92),(.05,.80)]
    start,end=offsets[scene]
    cx=int(span*(interp(start,end,v)+.012*math.sin(2*math.pi*u)))
    cy=int(max(0,h-crop_h)*(.42+.08*math.sin(u*math.pi*2)))
    cx=max(0,min(span,cx));cy=max(0,min(h-crop_h,cy))
    return img.crop((cx,cy,cx+crop_w,cy+crop_h)).resize((CW,CH),Image.Resampling.BICUBIC)

MASK=Image.new('L',(CW,CH),0)
ImageDraw.Draw(MASK).rounded_rectangle((0,0,CW-1,CH-1),radius=40,fill=255)
SCENES=None

def draw_overlay(im,scene,t,u):
    # Special effects on a layer separate from the source illustration.
    a=Image.new('RGBA',(W,H),(0,0,0,0));d=ImageDraw.Draw(a)
    if scene==0:
        # emphasis rings on the sender's package; 2.5D floating annotation.
        for j in range(2):
            phase=((u*2+j*.28)%1);r=23+95*phase;alpha=round(115*(1-phase))
            d.ellipse((466-r,815-r*.4,466+r,815+r*.4),outline=(239,99,44,alpha),width=5)
        d.ellipse((445,798,459,812),fill=(*ORANGE,180))
    if scene==1:
        # top-down camera reveal across two characters, dashed 'not yet connected'.
        for i in range(13):
            x=228+i*31; y=865-65*math.sin(i/12*math.pi)
            if i/12<max(.04,E((u-.1)/.78)):
                d.rounded_rectangle((x,y,x+15,y+6),radius=3,fill=(30,137,219,208))
        d.ellipse((570-38,805-38,570+38,805+38),fill=(255,255,255,230))
        lt(d,'?',570,805,47,ORANGE)
    if scene==2:
        # App highlight and notification, deliberately no fake logo.
        n=E((u-.25)/.4);yy=int(980-(1-n)*75)
        d.rounded_rectangle((332,yy,631,yy+69),radius=23,fill=(255,255,255,int(240*n)))
        if n>.01:
            d.ellipse((344,yy+21,369,yy+46),fill=(239,99,44,int(255*n)))
            txt(d,'آگهی جدید',488,yy+35,23,INK,maxw=220)
    if scene==3:
        # Active blue connection line, traveling spark, and one chat bubble.
        p=E((u-.06)/.62)
        coords=[(165,832),(294,747),(404,772),(539,704),(624,744)]
        if p>0:
            scaled=max(1,int((len(coords)-1)*p)); d.line(coords[:scaled+1],fill=(38,167,245,212),width=8,joint='curve')
            ix=min(len(coords)-2,int((len(coords)-1)*p))
            sub=(len(coords)-1)*p-ix
            px=interp(coords[ix][0],coords[ix+1][0],sub);py=interp(coords[ix][1],coords[ix+1][1],sub)
            d.ellipse((px-13,py-13,px+13,py+13),fill=(255,255,255,255),outline=(32,160,224,255),width=4)
        n=E((u-.28)/.4)
        if n>.01:
            y=int(508+(1-n)*80)
            d.rounded_rectangle((82,y,637,y+134),radius=29,fill=(255,255,255,round(248*n)))
            txt(d,'من جمعه می‌رم تهران،',363,y+46,30,INK,maxw=500)
            txt(d,'می‌تونم بسته‌ات رو ببرم',363,y+96,29,BLUE,maxw=510)
    if scene==4:
        # Flight arc moving to Iran with a white plane/pin.
        coords=[(112,842),(224,780),(345,746),(476,723),(605,672)]
        phase=E(u)
        for i in range(24):
            s=i/24
            if s>phase:continue
            x=interp(108,615,s);y=843-173*s-32*math.sin(s*math.pi)
            d.ellipse((x-4,y-4,x+4,y+4),fill=(34,152,222,230))
        px=interp(109,611,phase);py=843-170*phase-32*math.sin(phase*math.pi)
        pts=[(px-18,py+6),(px+18,py-6),(px+2,py-12),(px+4,py+2),(px-7,py+15)]
        d.polygon(pts,fill=(255,255,255,255))
        # orange CTA label fades into the image.
        fade=E((u-.53)/.28)
        if fade>0:
            d.rounded_rectangle((92,956,615,1030),radius=33,fill=(239,99,44,int(240*fade)))
            txt(d,'مسافرت رو پیدا کن',355,994,34,(255,255,255),maxw=500)
    im.alpha_composite(a)

def base_bg():
    base=Image.new('RGB',(W,H),BG).convert('RGBA')
    sh=Image.new('RGBA',(W,H),(0,0,0,0));d=ImageDraw.Draw(sh)
    d.rounded_rectangle((CARD[0]+10,CARD[1]+16,CARD[2]+8,CARD[3]+19),radius=42,fill=(43,62,73,50))
    base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(15)))
    return base

def text_scene(im,scene,u,t):
    d=ImageDraw.Draw(im)
    lt(d,'ADVERTIO',57,68,29,INK,anchor='lm');lt(d,f'{scene+1:02d} / 05',662,68,19,MUTED,anchor='rm')
    for i in range(5):
        x=58+i*35;d.rounded_rectangle((x,111,x+26,117),radius=3,fill=ORANGE if i==scene else (213,216,216))
    main=[
        ['این بسته باید بره ایران','ولی چطوری؟','یه بسته، ۱۰ هزار کیلومتر فاصله'],
        ['اون طرف یکی همین هفته','داره می‌ره ایران','فقط هنوز همدیگه رو پیدا نکردن'],
        ['اینجاست که ادورتیو','وارد می‌شه','آگهی بذار، مسافر پیدا کن'],
        ['فقط باید همدیگه رو','پیدا کنن','مسافر پیام می‌ده، هماهنگ می‌شید'],
        ['بار داری؟','مسافرت رو پیدا کن','Advertio.net | ارسال بار مسافری']
    ][scene]
    starts=[0,.35,.75]
    sizes=[44,48,27]
    for k,s in enumerate(main):
        alpha=E((u-starts[k])/.38)
        if alpha==0:continue
        lay=Image.new('RGBA',(W,H),(0,0,0,0));dd=ImageDraw.Draw(lay)
        if k==2 and scene==4:
            lt(dd,'advertio.net',360,336,31,ORANGE)
            txt(dd,'ارسال بار مسافری',360,382,23,MUTED,False)
        else:
            txt(dd,s,360+int(28*(1-alpha)),[199,278,365][k],sizes[k],ORANGE if k==1 else (MUTED if k==2 else INK),maxw=632)
        lay.putalpha(lay.getchannel('A').point(lambda a:int(a*alpha)))
        im.alpha_composite(lay)
    # Progress and domain/footer.
    d=ImageDraw.Draw(im)
    d.line((59,1222,661,1222),fill=(221,224,222),width=4)
    d.line((59,1222,round(59+602*min(t/DUR,1)),1222),fill=ORANGE,width=5)
    lt(d,'advertio.net',62,1254,20,INK,anchor='lm');lt(d,f'{t:04.1f}s',655,1254,15,MUTED,anchor='rm')

def frame(t):
    global SCENES
    if SCENES is None:SCENES=[Image.open(ASSETS/n).convert('RGB') for n in FRAME_NAMES]
    i=scene_idx(t);st,ed=MOTION[i];u=max(0,min(1,(t-st)/(ed-st)))
    im=base_bg()
    patch=camera_crop(SCENES[i],u,i)
    im.paste(patch,(CARD[0],CARD[1]),MASK)
    draw_overlay(im,i,t,u)
    text_scene(im,i,u,t)
    return im.convert('RGB')

def render():
    build_assets()
    quick='--samples' in sys.argv or MODE=='quick-preview'
    ids=[0,17,35,48,68,96,110,142,164,190,226,254,282,299] if quick else range(TOTAL)
    if quick:
        thumbs=[]
        for index in ids:
            image=frame(index/FPS);image.save(HERE/f'frame-sample-{index:03d}.jpg',quality=89)
            thumbs.append(image.resize((216,384),Image.Resampling.LANCZOS))
        overview=Image.new('RGB',(1220,1460),BG)
        d=ImageDraw.Draw(overview);lt(d,'ADVERTIO — 5 SCENE QUICK PREVIEW',32,28,24,INK,anchor='lm')
        for j,img in enumerate(thumbs):
            c=j%5;r=j//5
            overview.paste(img,(28+c*237,68+r*467))
        overview.save(HERE/'quick-preview-contact-sheet.jpg',quality=92)
        print('Quick Preview frames and contact sheet created',flush=True)
        return
    out=HERE/('output.mp4' if MODE=='final' else 'preview.mp4')
    cmd=['ffmpeg','-y','-hide_banner','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an'] + (['-vf','scale=1080:1920:flags=lanczos'] if MODE=='final' else []) + ['-c:v','libx264','-preset','veryfast','-crf','21','-pix_fmt','yuv420p','-movflags','+faststart',str(out)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    try:
        for k in range(TOTAL):
            proc.stdin.write(frame(k/FPS).tobytes())
            if k%50==0:print('rendered',k,'/',TOTAL,flush=True)
        proc.stdin.close();code=proc.wait()
        if code:raise RuntimeError(f'ffmpeg exited {code}')
    except BaseException:
        proc.kill();proc.wait();raise
    print('Video:',out,flush=True)
if __name__=='__main__':render()