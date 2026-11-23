"""Advertio story film: original animated isometric miniatures.
The reference informs clean ivory lighting, extruded paths, rounded geometry and
limited accent color; four distinct visual scenes are independently animated.
"""
from __future__ import annotations
from pathlib import Path
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFilter
import math, os, sys

P=Path(__file__).resolve().parent
MODE=os.environ.get('ADVERTIO_RENDER_MODE','preview')
if MODE not in ('preview','final'):raise ValueError('render mode must be preview or final')
FPS=10 if MODE=='preview' else 30
N=15*FPS
W,H=720,1280
TIMES=[.5,1.6,3.3,4.4,6.2,7.5,9.5,11.4,13.1,14.7]
IVORY='#F8F8F5';INK='#263645';ORANGE='#F2753D';DARK_ORANGE='#C95529'
BLUE='#668EA5';PALE_BLUE='#C7DBE1';TEAL='#6EAFA4';PINK='#D79C9B'
BONE='#E8E8E4';WHITE='#FFFFFF';GOLD='#E8C49B'

def E(v):
    v=max(0.,min(1.,v));return v*v*(3-2*v)
def mix(a,b,v):return a+(b-a)*v
def poly(d,pts,fill):d.polygon([(round(x),round(y)) for x,y in pts],fill=fill)
def ell(d,xy,fill,outline=None,width=1):d.ellipse(tuple(round(v) for v in xy),fill=fill,outline=outline,width=width)
def rounded(d,xy,r,fill,outline=None,width=1):d.rounded_rectangle(tuple(round(v) for v in xy),radius=round(r),fill=fill,outline=outline,width=width)
def iso_slab(d,x,y,w,h,thick=20,top='#FFFFFF',left='#D8E1E1',right='#CBD5D7'):
    pts=[(x,y-h/2),(x+w/2,y),(x,y+h/2),(x-w/2,y)]
    a,b,c,dd=pts
    poly(d,[dd,c,(c[0],c[1]+thick),(dd[0],dd[1]+thick)],left)
    poly(d,[c,b,(b[0],b[1]+thick),(c[0],c[1]+thick)],right)
    poly(d,pts,top)
    return pts
def shadow(d,x,y,rx=100,ry=26):ell(d,(x-rx,y-ry,x+rx,y+ry),'#E0E4E3')
def rod(d,coords,width=17,color=ORANGE):
    d.line([(round(x+2),round(y+8)) for x,y in coords],fill='#E8E2DE',width=width+4,joint='curve')
    d.line([(round(x),round(y+5)) for x,y in coords],fill=DARK_ORANGE,width=width,joint='curve')
    d.line([(round(x),round(y)) for x,y in coords],fill=color,width=width,joint='curve')
    for x,y in coords:ell(d,(x-width/2,y-width/2,x+width/2,y+width/2),color)
def person(d,x,y,scale=1.,shirt=BLUE,hair=INK,skin='#DBAD8D',mood='neutral',wave=0.,legs=True):
    s=scale
    if legs:
        shadow(d,x,y+8*s,32*s,11*s)
        d.line((x-11*s,y-53*s,x-15*s,y-14*s),fill='#53606C',width=max(1,round(13*s)))
        d.line((x+12*s,y-52*s,x+14*s,y-14*s),fill='#53606C',width=max(1,round(13*s)))
        rounded(d,(x-26*s,y-16*s,x-10*s,y-5*s),5*s,'#3D4851')
        rounded(d,(x+7*s,y-16*s,x+25*s,y-5*s),5*s,'#3D4851')
    d.line((x-24*s,y-91*s,x-38*s,y-51*s),fill=shirt,width=max(1,round(13*s)))
    d.line((x+24*s,y-90*s,x+(37+12*wave)*s,y-(54+26*wave)*s),fill=shirt,width=max(1,round(13*s)))
    ell(d,(x-44*s,y-55*s,x-32*s,y-43*s),skin)
    ell(d,(x+(31+12*wave)*s,y-(61+26*wave)*s,x+(44+12*wave)*s,y-(47+26*wave)*s),skin)
    rounded(d,(x-28*s,y-102*s,x+28*s,y-49*s),18*s,shirt)
    rounded(d,(x-7*s,y-111*s,x+7*s,y-95*s),4*s,skin)
    ell(d,(x-30*s,y-163*s,x+30*s,y-107*s),skin)
    ell(d,(x-29*s,y-167*s,x+26*s,y-141*s),hair)
    ell(d,(x-30*s,y-158*s,x-19*s,y-121*s),hair)
    if mood in ('concerned','happy'):
        eyec='#283947'
        for dx in (-10,11):ell(d,(x+(dx-1.8)*s,y-135*s,x+(dx+1.8)*s,y-131*s),eyec)
        if mood=='happy':d.arc((x-10*s,y-130*s,x+12*s,y-117*s),0,170,fill='#8D514A',width=max(1,round(2*s)))
        else:d.arc((x-9*s,y-124*s,x+10*s,y-112*s),180,345,fill='#8D514A',width=max(1,round(2*s)))
def bottle(d,x,y,s=1.,lift=0):
    y-=lift;s=float(s)
    shadow(d,x,y+8*s,35*s,11*s)
    rounded(d,(x-34*s,y-79*s,x+34*s,y-10*s),13*s,'#E8F0F0',outline='#B9CBCB',width=max(1,round(2*s)))
    rounded(d,(x-31*s,y-60*s,x+31*s,y-22*s),8*s,WHITE)
    rounded(d,(x-9*s,y-54*s,x+9*s,y-30*s),2*s,'#B9D7D6')
    rounded(d,(x-3*s,y-59*s,x+3*s,y-24*s),1*s,TEAL)
    rounded(d,(x-15*s,y-46*s,x+15*s,y-37*s),1*s,TEAL)
    rounded(d,(x-27*s,y-92*s,x+27*s,y-73*s),6*s,'#D9E3E4')
    rounded(d,(x-21*s,y-98*s,x+21*s,y-90*s),4*s,WHITE)
def package(d,x,y,s=1.,open_lid=0.,ribbon=False):
    shadow(d,x,y+54*s,54*s,14*s)
    tw=66*s;ty=26*s;h=67*s
    a=(x,y-ty);b=(x+tw,y);c=(x,y+ty);dd=(x-tw,y)
    poly(d,[dd,c,(c[0],c[1]+h),(dd[0],dd[1]+h)],'#CEAA82')
    poly(d,[c,b,(b[0],b[1]+h),(c[0],c[1]+h)],'#B98760')
    poly(d,[a,dd,c,b],'#EBC9A1')
    if open_lid>0:
        lift=E(open_lid)*33*s
        poly(d,[(x,y-ty-lift),(x+tw,y-lift),(x,y+ty-lift),(x-tw,y-lift)],'#F3D9B5')
    if ribbon:rod(d,[(x-23*s,y-9*s),(x,y+ty),(x+22*s,y+9*s)],max(2,round(8*s)),'#FBF7EC')
def table(d,x,y,w=370,h=135):
    shadow(d,x+9,y+65,w*.52,33)
    iso_slab(d,x,y,w,h,31,'#F1F2EE','#E5E7E2','#D9DFDD')
    for side in (-1,1):
        px=x+side*w*.30
        rounded(d,(px-9,y+70,px+10,y+135),6,'#DDE0DB')
def suitcase(d,x,y,s=.8):
    shadow(d,x,y+15*s,32*s,10*s)
    rounded(d,(x-27*s,y-69*s,x+27*s,y+12*s),10*s,'#7EA6AC')
    rounded(d,(x-14*s,y-87*s,x+14*s,y-67*s),6*s,outline='#4B6B76',fill=WHITE,width=max(2,round(4*s)))
    d.line((x,y-62*s,x,y+4*s),fill='#B1D4D0',width=max(2,round(3*s)))
    for dx in (-16,16):ell(d,(x+(dx-5)*s,y+8*s,x+(dx+5)*s,y+18*s),'#33464F')
def phone(d,x,y,s=1.,scroll=0,matched=False):
    w,h=254*s,430*s
    shadow(d,x+10,y+h*.47,130*s,20*s)
    rounded(d,(x-w/2-8*s,y-h/2-9*s,x+w/2+8*s,y+h/2+9*s),30*s,'#263747')
    rounded(d,(x-w/2,y-h/2,x+w/2,y+h/2),24*s,WHITE)
    rounded(d,(x-30*s,y-h/2+8*s,x+30*s,y-h/2+16*s),5*s,'#263747')
    rounded(d,(x-w/2+10*s,y-h/2+36*s,x+w/2-10*s,y-h/2+95*s),12*s,TEAL)
    d.ellipse((x-84*s,y-h/2+58*s,x-74*s,y-h/2+68*s),fill=WHITE)
    d.line((x-70*s,y-h/2+63*s,x+73*s,y-h/2+63*s),fill=WHITE,width=max(2,round(3*s)))
    d.ellipse((x+74*s,y-h/2+58*s,x+84*s,y-h/2+68*s),fill=WHITE)
    for i in range(3):
        yy=y-h/2+(113+i*87-scroll)*s
        if yy<y-h/2+96*s or yy>y+h/2-70*s:continue
        highlight=matched and i==1
        rounded(d,(x-108*s,yy,x+109*s,yy+74*s),11*s,'#E3F2EF' if highlight else '#F2F4F2',outline='#8AC8B7' if highlight else '#E5E9E8',width=max(1,round(2*s)))
        ell(d,(x-96*s,yy+15*s,x-60*s,yy+51*s),'#B9D5E1' if i!=1 else '#C5D7CA')
        rounded(d,(x-47*s,yy+16*s,x+78*s,yy+22*s),3*s,'#94A6AD')
        rounded(d,(x-47*s,yy+31*s,x+31*s,yy+36*s),3*s,'#BBC8CA')
        rounded(d,(x+58*s,yy+51*s,x+93*s,yy+59*s),4*s,ORANGE if highlight else '#A0C8C4')
    rounded(d,(x-99*s,y+h/2-55*s,x+99*s,y+h/2-19*s),14*s,ORANGE)
def plane(d,x,y,s=1.,angle=0.):
    p=[(-37,0),(23,-8),(13,-27),(26,-21),(45,-2),(24,7),(18,26),(10,23),(13,7)]
    co=math.cos(angle);si=math.sin(angle)
    coords=[(x+(u*co-v*si)*s,y+(u*si+v*co)*s) for u,v in p]
    poly(d,coords,WHITE)
    d.line((x-18*s,y,x+24*s,y),fill='#6E9EAE',width=max(2,round(3*s)))
def draw_room(d,t):
    shadow(d,360,1000,287,36)
    iso_slab(d,355,896,560,206,42,'#F0F3F1','#DCE3E0','#D8DFDE')
    rounded(d,(110,587,260,672),18,'#EAF1F0')
    d.line((143,659,143,610,231,610),fill='#B8CDD0',width=6)
    ell(d,(181,586,232,613),'#C9DDE1')
    card_x=mix(900,432,E(t/.74)); card_y=581+8*math.sin(t*.9)
    shadow(d,card_x+4,815,122,18)
    rounded(d,(card_x-127,card_y-83,card_x+127,card_y+210),25,WHITE,outline='#C7D6D8',width=4)
    rounded(d,(card_x-117,card_y-72,card_x+117,card_y-15),15,'#E6F1F2')
    ell(d,(card_x-87,card_y-38,card_x-73,card_y-24),TEAL)
    rounded(d,(card_x-81,card_y+4,card_x+84,card_y+168),19,'#F6F7F2')
    person(d,card_x,card_y+164,.79,PINK,'#7A6362','#D2A18A',mood='concerned',legs=False)
    ell(d,(card_x+78,card_y-64,card_x+94,card_y-48),ORANGE)
    person(d,210,1017,1.28,BLUE,INK,'#D8A98E',mood='concerned',wave=.07*math.sin(2*t))
    bottle(d,326,955,.92,lift=11*math.sin(t*2.7))
    for j in range(4):
        rr=5+3*math.sin(t*2+j)
        x=370+j*13;y=803+j*7
        ell(d,(x-rr,y-rr,x+rr,y+rr),'#EFCBB7')
def draw_pack(d,t):
    u=t-3.8
    table(d,350,900,570,250)
    package(d,355,830,1.25,open_lid=max(.25,1-E((u-1)/1.9)))
    bby=mix(670,802,E((u-.2)/1.8))
    bottle(d,350,bby,1.0)
    d.arc((143,480,571,730),200,336,fill='#D3DFE0',width=4)
    rod(d,[(154,640),(214,621),(275,615),(335,632),(390,613),(463,586),(552,586)],9,'#E8B69B')
    prog=E((u-.3)/2.7)
    xs=154+398*prog
    py=640-60*prog+18*math.sin(prog*math.pi*1.5)
    plane(d,xs,py,.76,angle=-.12)
    iso_slab(d,145,672,119,55,12,'#D3E2E3','#C5D8D8','#BED0D2')
    iso_slab(d,565,635,122,55,12,'#D3E2E3','#C5D8D8','#BED0D2')
    if u>1.5:
        rounded(d,(297,813,413,819),3,'#F3C99D')
    rounded(d,(115,1040,250,1076),14,WHITE,outline='#DAE6E5',width=2)
    rounded(d,(476,1040,614,1076),14,WHITE,outline='#DAE6E5',width=2)
def draw_matching(d,t):
    u=t-7
    shadow(d,336,1050,255,32)
    iso_slab(d,341,995,500,225,30,'#F1F2F0','#DDE5E2','#D7E0DE')
    scale=1.04+0.025*math.sin(u*2)
    phone(d,330,745,scale,scroll=12*E((u-.3)/2),matched=u>1.7)
    person(d,560,1005,.92,'#E7AE80','#4A5861','#D7A98F',mood='happy',wave=E((u-1.9)/.6))
    suitcase(d,618,1000,.88)
    appear=E((u-1.65)/.52)
    if appear>0:
        xx=mix(690,515,appear); yy=548-8*math.sin(u*2)
        rounded(d,(xx-52,yy-34,xx+60,yy+32),21,WHITE,outline='#BAD9D4',width=3)
        ell(d,(xx-28,yy-5,xx-17,yy+6),TEAL)
        ell(d,(xx-5,yy-5,xx+6,yy+6),TEAL)
        ell(d,(xx+18,yy-5,xx+29,yy+6),TEAL)
        poly(d,[(xx+10,yy+27),(xx+2,yy+44),(xx-12,yy+28)],WHITE)
    if u>2.4:
        ell(d,(465,605,479,619),ORANGE)
        ell(d,(474,613,482,621),WHITE)
def draw_finale(d,t):
    u=t-11
    shadow(d,364,1010,292,34)
    iso_slab(d,359,908,584,207,44,'#F1F4F0','#D7E2DC','#D3DDDA')
    person(d,475,1000,1.19,PINK,'#686166','#D7AE91',mood='happy',wave=E((u-.4)/.75))
    p_x=mix(100,322,E((u-.2)/1.7));p_y=mix(950,916,E((u-.2)/1.7))
    package(d,p_x,p_y,.79,ribbon=True)
    if u>1.15:
        a=E((u-1.15)/.6)
        cx,cy=390,645
        ell(d,(cx-46*a,cy-46*a,cx+46*a,cy+46*a),'#D5EEE7')
        ell(d,(cx-30*a,cy-30*a,cx+30*a,cy+30*a),TEAL)
        d.line((cx-16*a,cy,cx-3*a,cy+13*a,cx+22*a,cy-15*a),fill=WHITE,width=max(1,round(7*a)),joint='curve')
        for j in range(9):
            ang=j*2.399+u*.6
            xx=390+108*math.cos(ang);yy=676+99*math.sin(ang)-(u-1.15)*16
            r=3+(j%3)*1.6
            ell(d,(xx-r,yy-r,xx+r,yy+r),ORANGE if j%3==0 else '#D4DAD4')
    for j in range(4):
        ex=125+j*20;ey=672+j*16
        ell(d,(ex-8,ey-8,ex+8,ey+8),('#D7E2E1' if j%2 else ORANGE))
@lru_cache(maxsize=1)
def bg():
    im=Image.new('RGB',(W,H),IVORY)
    wash=Image.new('RGBA',(W,H),(0,0,0,0))
    d=ImageDraw.Draw(wash)
    ell(d,(0,470,720,1140),(198,211,209,28))
    ell(d,(110,485,670,1050),(231,235,232,73))
    wash=wash.filter(ImageFilter.GaussianBlur(52))
    im=Image.alpha_composite(im.convert('RGBA'),wash).convert('RGB')
    return im
def make_frame(t):
    if t<0 or t>15:raise ValueError(t)
    im=bg().copy();d=ImageDraw.Draw(im)
    d.line((52,474,145,474),fill='#DADFDA',width=3)
    ell(d,(156,469,165,478),ORANGE)
    d.line((568,1097,654,1097),fill='#DADFDA',width=3)
    if t<3.8:draw_room(d,t)
    elif t<7:draw_pack(d,t)
    elif t<11:draw_matching(d,t)
    else:draw_finale(d,t)
    return im
def render():
    out=P/'frames';out.mkdir(exist_ok=True)
    idx=sorted(set(min(N-1,round(x*FPS)) for x in TIMES)) if '--samples' in sys.argv else range(N)
    for i in idx:
        make_frame(i/FPS).save(out/f'{i:04d}.png')
        if i%30==0:print(f'Rendered scene frame {i}/{N}',flush=True)
if __name__=='__main__':render()
