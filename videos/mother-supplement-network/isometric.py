"""Fast deterministic isometric rasterization, avoiding SVGRenderer and floor occlusion.
Outputs 720x1280 scene PNGs; finish.py adds Persian typography and encodes video.
"""
from pathlib import Path
from PIL import Image, ImageDraw
import math, os, sys

ROOT=Path(__file__).resolve().parent
MODE=os.environ.get('ADVERTIO_RENDER_MODE','preview')
if MODE not in ('preview','final'): raise ValueError(MODE)
FPS=10 if MODE=='preview' else 30
TIMES=[0,1.5,3.5,4.5,6.5,8,9.5,11.5,13.5,14.9]
W,H=720,1280
ORANGE=(245,102,42); LIGHT=(255,146,79); DARK=(213,75,29)
INK=(32,33,36); WHITE=(250,250,247)
POINTS={'sender':(130,651),'package':(300,797),'hub':(400,691),
        'traveler':(562,858),'mother':(390,994),'phone':(139,969),'supplement':(590,657)}
PATHS=[[(130,651),(237,735),(300,797)],
       [(300,797),(319,761),(400,691)],
       [(400,691),(480,751),(480,796),(562,858)],
       [(400,691),(490,618),(590,657)],
       [(139,969),(240,899),(300,797)],
       [(300,797),(337,925),(390,994)]]

def lerp(a,b,t):return a+(b-a)*t
def ease(t):t=max(0,min(1,t));return t*t*(3-2*t)
def ellipse(draw,rect,fill,outline=None,width=1):draw.ellipse(tuple(map(int,rect)),fill,outline,width)
def poly(draw,points,fill):draw.polygon([(round(x),round(y)) for x,y in points],fill=fill)
def bg():
    img=Image.new('RGB',(W,H),(249,249,247))
    pix=img.load()
    for y in range(430,1091):
        for x in range(W):
            r=((x-352)/475)**2+((y-754)/430)**2
            shade=min(1.0,r)
            a=round(244+5*shade)
            pix[x,y]=(a,a,round(a-1))
    d=ImageDraw.Draw(img)
    ellipse(d,(44,615,678,1060),(239,240,237))
    ellipse(d,(68,638,657,1037),(245,245,243))
    for x,y in [(90,825),(617,742),(475,1071),(223,568)]:
        ellipse(d,(x-4,y-4,x+4,y+4),(209,211,207))
    return img
def stroke(d,pts,color,width):
    d.line(pts,fill=color,width=width,joint='curve')
    r=width//2
    for x,y in pts:ellipse(d,(x-r,y-r,x+r,y+r),color)
def path(d,pts):
    shadow=[(x+4,y+12) for x,y in pts]
    stroke(d,shadow,(211,207,200),31)
    stroke(d,[(x,y+8) for x,y in pts],DARK,30)
    stroke(d,pts,ORANGE,29)
    stroke(d,[(x-1,y-3) for x,y in pts],LIGHT,7)
def platform(d,x,y,color='black',scale=1):
    rx=47*scale; ry=24*scale; height=48*scale
    top=(x,y-7*scale);left=(x-rx,y+ry-7*scale)
    right=(x+rx,y+ry-7*scale);bottom=(x,y+2*ry-7*scale)
    drop=height
    poly(d,[(left[0]+5,left[1]+9),(bottom[0]+6,bottom[1]+10),
            (right[0]+6,right[1]+9),(right[0]+6,right[1]+drop+11),
            (bottom[0]+6,bottom[1]+drop+10),(left[0]+5,left[1]+drop+10)],(221,222,217))
    if color=='black':topc,leftc,rightc=(45,46,50),(22,23,27),(31,32,36)
    else:topc,leftc,rightc=(252,252,250),(219,221,217),(236,237,233)
    poly(d,[left,bottom,(bottom[0],bottom[1]+drop),(left[0],left[1]+drop)],leftc)
    poly(d,[bottom,right,(right[0],right[1]+drop),(bottom[0],bottom[1]+drop)],rightc)
    poly(d,[top,left,bottom,right],topc)
    return (x,y+10*scale)
def pawn(d,x,y,color='black',scale=1):
    black=color=='black'
    base=(27,28,32) if black else (246,247,244)
    highlight=(56,57,61) if black else (255,255,253)
    dark=(14,15,17) if black else (211,214,209)
    def box(k):return tuple(round(v) for v in k)
    ellipse(d,box((x-25*scale,y-3*scale,x+25*scale,y+16*scale)),dark)
    poly(d,[(x-20*scale,y+3*scale),(x-17*scale,y-39*scale),
            (x+13*scale,y-39*scale),(x+22*scale,y+3*scale)],base)
    ellipse(d,box((x-20*scale,y-48*scale,x+19*scale,y-15*scale)),base)
    ellipse(d,box((x-19*scale,y-82*scale,x+17*scale,y-46*scale)),highlight)
    ellipse(d,box((x-15*scale,y-80*scale,x+13*scale,y-51*scale)),base)
    ellipse(d,box((x-9*scale,y-76*scale,x-4*scale,y-71*scale)),
            (99,99,100) if black else (255,255,255))
def station(d,key,color='black',scale=1):
    x,y=POINTS[key];platform(d,x,y,color,scale)
    pawn(d,x,y-15*scale,color,scale)
def parcel(d):
    x,y=POINTS['package'];platform(d,x,y,'white',.88)
    w=45;z=y-23
    poly(d,[(x,z-52),(x+w,z-31),(x,z-7),(x-w,z-31)],(235,204,166))
    poly(d,[(x-w,z-31),(x,z-7),(x,z+38),(x-w,z+15)],(198,147,100))
    poly(d,[(x,z-7),(x+w,z-31),(x+w,z+15),(x,z+38)],(223,174,124))
    poly(d,[(x-5,z-49),(x+7,z-43),(x+7,z+1),(x-5,z-6)],(250,230,193))
def bottle(d):
    x,y=POINTS['supplement']
    ellipse(d,(x-53,y+29,x+55,y+54),(218,221,218))
    poly(d,[(x-28,y+20),(x-31,y-43),(x-21,y-52),(x+21,y-52),
            (x+31,y-43),(x+28,y+20)],(237,240,237))
    ellipse(d,(x-30,y+12,x+30,y+31),(214,220,217))
    poly(d,[(x-32,y-38),(x+32,y-38),(x+30,y+7),(x-30,y+7)],(251,252,249))
    ellipse(d,(x-22,y-68,x+22,y-48),(215,221,219))
    poly(d,[(x-22,y-68),(x+22,y-68),(x+22,y-57),(x-22,y-57)],(246,247,245))
    ellipse(d,(x-21,y-74,x+21,y-64),(253,253,250))
    d.rounded_rectangle((x-22,y-24,x+22,y+10),radius=4,fill=(226,241,243))
    d.rectangle((x-4,y-19,x+4,y+5),fill=(99,159,169))
    d.rectangle((x-12,y-11,x+12,y-3),fill=(99,159,169))
def phone(d):
    x,y=POINTS['phone'];platform(d,x,y,'black',.85)
    poly(d,[(x-29,y-100),(x+23,y-92),(x+23,y-8),(x-29,y-17)],(31,33,36))
    poly(d,[(x-23,y-91),(x+17,y-85),(x+17,y-19),(x-23,y-25)],(250,251,248))
    d.line((x-15,y-77,x+8,y-73),fill=ORANGE,width=5)
    for q in range(3):
        cy=y-62+q*14
        d.rounded_rectangle((x-14,cy,x+11,cy+5),radius=2,fill=(201,212,210))
    d.line((x-28,y-97,x+23,y-90),fill=(83,85,88),width=2)
def accents(d,t):
    if ease(t*.9)<.1:return
    for x,y in [(192,575),(550,971),(262,1064),(621,780)]:
        d.line((x,y,x+22,y+11),fill=ORANGE,width=5)
        d.line((x+29,y+15,x+47,y+24),fill=INK,width=5)
    for x,y in [(90,758),(625,1009),(468,558)]:
        ellipse(d,(x-5,y-5,x+5,y+5),(224,226,222))
        ellipse(d,(x-2,y-2,x+2,y+2),(247,247,245))
def make_frame(t):
    im=bg();d=ImageDraw.Draw(im)
    # Connected tracks remain visible in every beat; no occluded SVG triangles.
    for p in PATHS:path(d,p)
    path_id=0 if t<4 else 2 if t<7 else 4 if t<11 else 5
    pts=PATHS[path_id];ratio=(t%3.8)/3.8
    edges=[math.hypot(x1-x0,y1-y0) for (x0,y0),(x1,y1) in zip(pts,pts[1:])]
    target=ratio*sum(edges)
    for i,length in enumerate(edges):
        if target<=length:
            q=target/length;x=lerp(pts[i][0],pts[i+1][0],q)
            y=lerp(pts[i][1],pts[i+1][1],q);break
        target-=length
    ellipse(d,(x-14,y-15,x+14,y+13),(255,254,251))
    accents(d,t)
    station(d,'sender','black',.98)
    station(d,'hub','black',.88)
    parcel(d);bottle(d)
    station(d,'traveler','black',.82)
    station(d,'mother','white',.84)
    phone(d)
    return im
def render():
    folder=ROOT/'frames';folder.mkdir(exist_ok=True)
    indices=sorted(set(min(15*FPS-1,round(t*FPS)) for t in TIMES)) if '--samples' in sys.argv else range(15*FPS)
    for i in indices:
        make_frame(i/FPS).save(folder/f'{i:04d}.png',optimize=True)
        if i%25==0:print('Rendered isometric frame',i,'/',15*FPS,flush=True)
if __name__=='__main__':render()
