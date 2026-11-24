#!/usr/bin/env python3
"""Artisans cinematic edition: original slides, bespoke paper transitions, no new copy."""
import argparse
import math
from pathlib import Path
import subprocess as sp
import tempfile
import cv2
import numpy as np

ROOT = Path(__file__).resolve().parent
W, H, FPS = 1080, 1920, 30
HOLDS = [7, 8, 6, 7, 8, 9]
MOVES = [(1.0,1.04,.48,.52),(1.035,1.005,.57,.48),(1.0,1.045,.43,.59),
         (1.035,1.0,.53,.46),(1.0,1.04,.55,.58),(1.035,1.0,.5,.5)]
ENC = ['-an','-c:v','libx264','-preset','veryfast','-crf','18','-threads','3',
       '-pix_fmt','yuv420p','-r',str(FPS),'-video_track_timescale','15360']
BASE = ['ffmpeg','-hide_banner','-loglevel','error','-y']
BLUE = (199,85,0)
NAVY = (63,36,8)
PALE = (186,151,111)

def sources():
    files = {}
    for p in (ROOT/'assets').glob('*.png'):
        tail = p.stem.rsplit('-',1)[-1]
        if tail.isdecimal():
            k = int(tail)
            if k in files: raise ValueError(f'Duplicate slide {k}')
            files[k] = p
    assert sorted(files) == list(range(1,7)), files
    return [files[i] for i in range(1,7)]

def ease(p):
    return p*p*(3-2*p)

def shot(src, out, seconds, move):
    a,b,x,y = move
    n = seconds*FPS
    e = f'(0.5-0.5*cos(PI*on/{n-1}))'
    z = f'{a}+({b-a})*{e}'
    # The anchor also drifts gently; maximum crop remains under 4.5%.
    ax = f'({x}+0.07*sin(PI*on/{n-1}))'
    ay = f'({y}-0.06*sin(PI*on/{n-1}))'
    vf = ('scale=2160:3840:force_original_aspect_ratio=decrease:flags=lanczos,'
          'pad=2160:3840:(ow-iw)/2:(oh-ih)/2:color=0xF7F0E7,'
          f"zoompan=z='{z}':x='(iw-iw/zoom)*{ax}':y='(ih-ih/zoom)*{ay}':"
          f'd={n}:s={W}x{H}:fps={FPS},setsar=1,format=yuv420p')
    sp.run(BASE+['-threads','2','-i',str(src),'-filter_threads','2','-vf',vf,
                '-frames:v',str(n)]+ENC+[str(out)],check=True)

def edge(clip, last=False):
    cap = cv2.VideoCapture(str(clip))
    if last:
        cap.set(cv2.CAP_PROP_POS_FRAMES,int(cap.get(cv2.CAP_PROP_FRAME_COUNT))-1)
    ok, frame = cap.read()
    cap.release()
    assert ok and frame.shape == (H,W,3), clip
    return frame

def poly(im, pts, color=BLUE, width=4, closed=False):
    cv2.polylines(im,[np.array(pts,np.int32)],closed,color,width,cv2.LINE_AA)

def icon(kind):
    """Original small line-art accents, not a brand mark; only used on transition paper."""
    im=np.zeros((240,240,4),np.uint8)
    ink=(BLUE[0],BLUE[1],BLUE[2],255)
    muted=(PALE[0],PALE[1],PALE[2],230)
    def line(pts,c=ink,w=4,closed=False): poly(im,pts,c,w,closed)
    def circle(p,r,c=ink,w=4): cv2.circle(im,p,r,c,w,cv2.LINE_AA)
    if kind==0: # air route / folded paper airplane
        for x,y in [(36,170),(49,162),(63,152),(77,143)]:
            circle((x,y),2,muted,2)
        line([(66,113),(187,66),(148,178),(115,136),(66,113)],ink,4)
        line([(115,136),(187,66)],ink,4)
        line([(115,136),(107,163),(130,151)],ink,4)
    elif kind==1: # Persian textile-inspired simple diamond and stitching
        line([(120,51),(186,120),(120,189),(54,120)],ink,4,True)
        line([(120,80),(158,120),(120,160),(82,120)],muted,4,True)
        circle((120,120),8,ink,3)
        for x,y in [(43,120),(197,120),(120,40),(120,200)]:
            circle((x,y),2,muted,2)
    elif kind==2: # payment / engraved coin
        circle((120,120),58,ink,4)
        circle((120,120),47,muted,2)
        line([(137,99),(106,99),(98,107),(106,119),(132,122),(140,133),(132,143),(101,143)],ink,4)
        line([(120,86),(120,155)],ink,3)
    elif kind==3: # shop browser window
        line([(53,70),(187,70),(187,164),(53,164)],ink,4,True)
        line([(53,92),(187,92)],ink,3)
        for x in [64,75,86]: circle((x,81),2,muted,2)
        line([(86,107),(155,107),(155,147),(86,147)],muted,3,True)
        line([(93,139),(108,122),(120,132),(133,116),(149,139)],ink,3)
    else: # parcel and share arrow
        line([(71,113),(120,85),(169,113),(120,141)],ink,4,True)
        line([(71,113),(71,165),(120,191),(169,165),(169,113)],ink,4)
        line([(120,141),(120,191)],ink,4)
        line([(96,99),(145,127)],muted,4)
        line([(137,73),(160,50),(183,73)],ink,4)
        line([(160,50),(160,90)],ink,4)
    return im

def transition(left,right,out,kind):
    # Feathered masks travel in different directions; a cream paper layer
    # briefly separates the two compositions so Persian typography never doubles.
    y,x=np.mgrid[0:H,0:W].astype(np.float32)
    x/=W-1; y/=H-1
    fields=[.78*x+.22*(1-y),
            .72*y+.20*x+.08*np.sin(2*np.pi*x),
            np.sqrt((x-.5)**2+(y-.5)**2),
            .85*(1-x)+.15*y,
            .86*(1-y)+.14*x]
    f=fields[kind]
    f=(f-f.min())/(f.max()-f.min())
    shade=(2.3*np.cos((x+.25*y)*np.pi)+1.7*np.sin(y*np.pi)).astype(np.float32)
    paper=np.clip(np.array([231,240,247],np.float32)[None,None,:]+shade[:,:,None],0,255).astype(np.uint8)
    im=icon(kind)
    ic=im[:,:,:3].astype(np.float32)
    ia=im[:,:,3].astype(np.float32)/255
    proc=sp.Popen(BASE+['-f','rawvideo','-pixel_format','bgr24','-video_size',f'{W}x{H}',
                        '-framerate',str(FPS),'-i','-']+ENC+[str(out)],stdin=sp.PIPE)
    try:
        for k in range(FPS):
            p=k/(FPS-1)
            if p<=.5:
                q=ease(p*2)
                field=f
                scene=left
            else:
                q=1-ease((p-.5)*2)
                field=1-f
                scene=right
            feather=.13
            alpha=np.clip((q*(1+2*feather)-feather-field)/feather+.5,0,1)
            alpha=alpha*alpha*(3-2*alpha)
            a=alpha[:,:,None]
            frame=np.rint(scene*(1-a)+paper*a).astype(np.uint8)
            # Icon visible exclusively on the paper region, never over the text.
            opacity=math.sin(math.pi*p)**2
            dx=int(18*math.sin((p-.5)*math.pi))
            dy=int(-9*math.sin(p*math.pi))
            x0=W//2-120+dx; y0=H//2-120+dy
            region=frame[y0:y0+240,x0:x0+240]
            m=(ia*opacity*alpha[y0:y0+240,x0:x0+240])[:,:,None]
            region[:]=np.rint(region*(1-m)+ic*m).astype(np.uint8)
            proc.stdin.write(frame.tobytes())
    finally:
        proc.stdin.close()
    if proc.wait(): raise RuntimeError('Transition encoder failed')

def render(out):
    out=out.resolve()
    out.parent.mkdir(parents=True,exist_ok=True)
    src=sources()
    cv2.setNumThreads(2)
    with tempfile.TemporaryDirectory(prefix='artisans-cinematic-') as d:
        tmp=Path(d)
        clips=[]
        for i,(p,sec,move) in enumerate(zip(src,HOLDS,MOVES)):
            path=tmp/f'shot-{i}.mp4'
            print('Shot',i+1,p.name,flush=True)
            shot(p,path,sec,move)
            clips.append(path)
        sequence=[]
        for i,clip in enumerate(clips):
            sequence.append(clip)
            if i<5:
                tr=tmp/f'transition-{i}.mp4'
                print('Transition',i+1,flush=True)
                transition(edge(clip,True),edge(clips[i+1]),tr,i)
                sequence.append(tr)
        playlist=tmp/'concat.txt'
        playlist.write_text(''.join("file '"+str(p)+"'\n" for p in sequence))
        sp.run(BASE+['-f','concat','-safe','0','-i',str(playlist),'-c','copy',
                     '-movflags','+faststart',str(out)],check=True)

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--output',type=Path,default=ROOT/'renders'/'cinematic-final.mp4')
    render(ap.parse_args().output)
