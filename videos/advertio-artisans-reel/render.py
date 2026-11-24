#!/usr/bin/env python3
"""Render six supplied slides, with camera motion and dissolve transitions only."""
import subprocess as sp
from pathlib import Path
import argparse
import re

ROOT=Path(__file__).resolve().parent
DURATIONS=[7,9,7,8,9,10]
FPS=30
TRANS=0.6
MOVES=[(1.0,1.035,.5,.5),(1.035,1.0,.52,.5),(1.0,1.04,.5,.55),(1.025,1.0,.48,.48),(1.0,1.035,.5,.55),(1.025,1.0,.5,.5)]

def render(out):
    args=['ffmpeg','-hide_banner','-loglevel','error','-y','-filter_complex_threads','2']
    filters=[]
    slides={}
    for p in (ROOT/'assets').glob('ChatGPT Image *.png'):
        m=re.search(r'-(\d+)\.png
    for i,(d,(a,b,x,y)) in enumerate(zip(DURATIONS,MOVES)):
        p=slides[i+1]
        if not p.is_file(): raise FileNotFoundError(p)
        args += ['-i',str(p)]
        frames=d*FPS
        ease=f'(0.5-0.5*cos(PI*on/{frames-1}))'
        z=f'{a}+({b-a})*{ease}'
        filters.append(f"[{i}:v]scale=2160:3840:force_original_aspect_ratio=decrease:flags=lanczos,pad=2160:3840:(ow-iw)/2:(oh-ih)/2:color=0xF7F0E7,zoompan=z='{z}':x='(iw-iw/zoom)*{x}':y='(ih-ih/zoom)*{y}':d={frames}:s=1080x1920:fps={FPS},setsar=1,format=yuv420p,settb=1/{FPS}[v{i}]")
    total=DURATIONS[0];prev='v0'
    for i in range(1,len(DURATIONS)):
        nxt=f'm{i}'
        filters.append(f'[{prev}][v{i}]xfade=transition=fade:duration={TRANS}:offset={total-TRANS:.3f}[{nxt}]')
        total+=DURATIONS[i]-TRANS;prev=nxt
    out.parent.mkdir(parents=True,exist_ok=True)
    args += ['-filter_complex',';'.join(filters),'-map',f'[{prev}]','-an','-c:v','libx264','-preset','veryfast','-crf','18','-threads','4','-pix_fmt','yuv420p','-movflags','+faststart','-r',str(FPS),str(out)]
    sp.run(args,check=True)

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--output',type=Path,default=ROOT/'renders'/'final.mp4')
    render(ap.parse_args().output)
, p.name)
        if m:
            idx=int(m.group(1))
            if idx in slides: raise ValueError(f'Duplicate slide {idx}')
            slides[idx]=p
    if set(slides)!=set(range(1,7)):
        raise ValueError(f'Expected exactly slides 1–6; found {sorted(slides)}')
    for i,(d,(a,b,x,y)) in enumerate(zip(DURATIONS,MOVES)):
        p=ROOT/'assets'/f'slide-{i+1:02}.png'
        if not p.is_file(): raise FileNotFoundError(p)
        args += ['-i',str(p)]
        frames=d*FPS
        ease=f'(0.5-0.5*cos(PI*on/{frames-1}))'
        z=f'{a}+({b-a})*{ease}'
        filters.append(f"[{i}:v]scale=2160:3840:flags=lanczos,zoompan=z='{z}':x='(iw-iw/zoom)*{x}':y='(ih-ih/zoom)*{y}':d={frames}:s=1080x1920:fps={FPS},setsar=1,format=yuv420p,settb=1/{FPS}[v{i}]")
    total=DURATIONS[0];prev='v0'
    for i in range(1,len(DURATIONS)):
        nxt=f'm{i}'
        filters.append(f'[{prev}][v{i}]xfade=transition=fade:duration={TRANS}:offset={total-TRANS:.3f}[{nxt}]')
        total+=DURATIONS[i]-TRANS;prev=nxt
    out.parent.mkdir(parents=True,exist_ok=True)
    args += ['-filter_complex',';'.join(filters),'-map',f'[{prev}]','-an','-c:v','libx264','-preset','veryfast','-crf','18','-threads','4','-pix_fmt','yuv420p','-movflags','+faststart','-r',str(FPS),str(out)]
    sp.run(args,check=True)

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--output',type=Path,default=ROOT/'renders'/'final.mp4')
    render(ap.parse_args().output)
