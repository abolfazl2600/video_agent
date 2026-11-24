#!/usr/bin/env python3
"""Premium camera-over-artwork film: original PNGs, 60 fps, subpixel optics."""
from pathlib import Path
import argparse
import math
import subprocess as sp
import cv2
import numpy as np

ROOT=Path(__file__).resolve().parent
W,H,FPS=1080,1920,60
DURS=[7.8,8.4,7.0,8.0,8.4,8.4]
TRANS=48
# Each key: time in shot, magnification, horizontal/vertical focal anchor, roll.
# Start/end are full posters so the travelling-camera cuts are spatially continuous.
PATHS=[
 [(0,1,0,0,0),(.15,1.12,0,-.70,0),(.29,1.035,0,-.15,0),(.53,1.025,.1,.05,0),(.78,1.40,-.62,.85,-.30),(.90,1.30,.58,.82,.18),(1,1,0,0,0)],
 [(0,1,0,0,0),(.18,1.045,.10,-.42,0),(.50,1.025,-.10,.05,0),(.69,1.20,.15,-.20,0),(.84,1.38,.75,.80,.24),(1,1,0,0,0)],
 [(0,1,0,0,0),(.18,1.06,0,-.45,0),(.43,1.035,0,0,0),(.66,1.44,-.73,.82,-.28),(.86,1.40,.75,.82,.22),(1,1,0,0,0)],
 [(0,1,0,0,0),(.20,1.06,0,-.48,0),(.52,1.025,.15,.12,0),(.71,1.22,.56,.24,0),(.85,1.36,-.55,.84,-.25),(1,1,0,0,0)],
 [(0,1,0,0,0),(.16,1.05,0,-.36,0),(.48,1.025,0,0,0),(.69,1.31,.08,.61,0),(.83,1.43,.65,.83,.20),(1,1,0,0,0)],
 [(0,1,0,0,0),(.18,1.06,0,-.50,0),(.48,1.025,0,0,0),(.67,1.37,-.58,.82,-.24),(.82,1.24,.34,.92,0),(.90,1.012,0,.2,0),(1,1,0,0,0)],
]
DIRECTIONS=['down','left','right','up','left']
def files():
    found={}
    for p in (ROOT/'assets').glob('*.png'):
        tail=p.stem.rsplit('-',1)[-1]
        if tail.isdecimal():
            k=int(tail)
            if k in found: raise ValueError(f'Duplicate slide {k}')
            found[k]=p
    if sorted(found)!=list(range(1,7)): raise ValueError(f'Expected slides 1–6, got {sorted(found)}')
    return [found[k] for k in range(1,7)]

def smooth(t):
    t=max(0.,min(1.,t))
    return t*t*t*(10+t*(-15+6*t))

def pose(keys,t):
    # Monotonic cubic Hermite interpolation with continuous first derivatives.
    # No rounded crop rectangles or duplicated/interpolated source frames.
    k=np.asarray(keys,dtype=np.float64)
    x=k[:,0]; y=k[:,1:]
    h=np.diff(x); delta=np.diff(y,axis=0)/h[:,None]
    slopes=np.zeros_like(y)
    for j in range(1,len(x)-1):
        a,b=delta[j-1],delta[j]
        for d in range(y.shape[1]):
            if a[d]*b[d]>0:
                w1=2*h[j]+h[j-1]; w2=h[j]+2*h[j-1]
                slopes[j,d]=(w1+w2)/(w1/a[d]+w2/b[d])
    i=max(0,min(len(x)-2,int(np.searchsorted(x,t,side='right')-1)))
    q=max(0.,min(1.,(t-x[i])/h[i])); q2=q*q;q3=q2*q
    return ((2*q3-3*q2+1)*y[i]+(q3-2*q2+q)*h[i]*slopes[i]+
            (-2*q3+3*q2)*y[i+1]+(q3-q2)*h[i]*slopes[i+1])

def read(p):
    im=cv2.imread(str(p),cv2.IMREAD_COLOR)
    if im is None: raise ValueError(p)
    # One high quality source resample, then a single fractional affine transform per frame.
    return cv2.resize(im,(2*W,2*H),interpolation=cv2.INTER_LANCZOS4)

def camera(im,v):
    z,u,vert,roll=map(float,v)
    sw,sh=2*W,2*H
    cx=sw*.5+(sw-sw/z)*.5*u
    cy=sh*.5+(sh-sh/z)*.5*vert
    M=cv2.getRotationMatrix2D((cx,cy),roll,z*.5)
    M[0,2]+=W*.5-cx;M[1,2]+=H*.5-cy
    return cv2.warpAffine(im,M,(W,H),flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_REPLICATE)

def travel(a,b,direction):
    horizontal=direction in ('left','right')
    forward=direction in ('left','up')
    first,second=(a,b) if forward else (b,a)
    gap=26
    cream=(231,240,247)
    if horizontal:
        spacer=np.full((H,gap,3),cream,np.uint8)
        canvas=np.concatenate((first,spacer,second),axis=1)
        span=W+gap
    else:
        spacer=np.full((gap,W,3),cream,np.uint8)
        canvas=np.concatenate((first,spacer,second),axis=0)
        span=H+gap
    def sample(t):
        v=span*(smooth(t) if forward else 1-smooth(t))
        dx,dy=(v,0) if horizontal else (0,v)
        M=np.array([[1.,0.,-dx],[0.,1.,-dy]],np.float64)
        return cv2.warpAffine(canvas,M,(W,H),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_REPLICATE)
    for i in range(TRANS):
        t=(i+1)/(TRANS+1)
        # Short simulated shutter exposure only while the camera travels.
        # Endpoints match the unblurred full poster and no text dissolves over text.
        dt=.25/(TRANS+1)
        mid=sample(t)
        if .09<t<.91:
            ends=cv2.addWeighted(sample(t-dt),.5,sample(t+dt),.5,0)
            mid=cv2.addWeighted(mid,.55,ends,.45,0)
        yield mid

def render(out):
    cv2.setNumThreads(2)
    out=out.resolve()
    out.parent.mkdir(parents=True,exist_ok=True)
    tmp=out.with_name(out.stem+'.part.mp4')
    images=[read(p) for p in files()]
    frames=0
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo',
         '-pixel_format','bgr24','-video_size',f'{W}x{H}','-framerate',str(FPS),
         '-i','-','-an','-c:v','libx264','-preset','veryfast','-crf','17',
         '-maxrate','12M','-bufsize','24M','-threads','4','-pix_fmt','yuv420p',
         '-r',str(FPS),'-fps_mode','cfr','-movflags','+faststart',str(tmp)]
    p=sp.Popen(cmd,stdin=sp.PIPE)
    try:
        for idx,(im,sec,keys) in enumerate(zip(images,DURS,PATHS)):
            n=round(sec*FPS)
            print(f'Camera shot {idx+1}: {n} original frames',flush=True)
            for f in range(n):
                frame=camera(im,pose(keys,f/(n-1)))
                p.stdin.write(frame.tobytes());frames+=1
            if idx<5:
                print('Spatial transition:',DIRECTIONS[idx],flush=True)
                a=camera(im,keys[-1][1:])
                b=camera(images[idx+1],PATHS[idx+1][0][1:])
                for frame in travel(a,b,DIRECTIONS[idx]):
                    p.stdin.write(frame.tobytes());frames+=1
        p.stdin.close()
        if p.wait(): raise RuntimeError('FFmpeg failed')
    except BaseException:
        if p.poll() is None: p.kill();p.wait()
        raise
    assert frames==3120,frames
    tmp.replace(out)
    print('Rendered',frames,'frames:',out,flush=True)

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--output',type=Path,default=ROOT/'renders'/'premium-camera-final.mp4')
    render(ap.parse_args().output)
