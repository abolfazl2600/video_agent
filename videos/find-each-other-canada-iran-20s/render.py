#!/usr/bin/env python3
"""Advertio / 20-second passenger cargo video from approved isometric image assets.

No synthesized Advertio logo is used; this video uses the uploaded visual panels,
transparent Persian typography, and font-independent raster layers.

ADVERTIO_RENDER_MODE=quick-preview (default): 540x960, 10fps, quick-preview.mp4
ADVERTIO_RENDER_MODE=preview:             540x960, 15fps, preview.mp4
ADVERTIO_RENDER_MODE=final:              1080x1920, 30fps, output.mp4

The final upscales the preview-source images and is intended only as a technical
export until full-resolution originals are supplied. Final is never automatic.
"""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

from PIL import Image, ImageOps

ROOT=Path(__file__).resolve().parent
FRAMES=ROOT/'assets'/'storyboard_frames'
TYPE=ROOT/'assets'/'typography'
MODE=os.environ.get('ADVERTIO_RENDER_MODE','quick-preview').strip().lower()
CONFIG={'quick-preview':(540,960,10,'quick-preview.mp4'),
        'preview':(540,960,15,'preview.mp4'),
        'final':(1080,1920,30,'output.mp4')}
if MODE not in CONFIG:
    raise ValueError('ADVERTIO_RENDER_MODE must be quick-preview, preview or final')
WIDTH,HEIGHT,FPS,OUTPUT=CONFIG[MODE]
SCENES=[
    {'dur':3, 'bg':'01_hook_canada.webp', 'zoom':1.075, 'layers':[
       ('01_narration_scene1.webp',.78,.11,0.0,2.65),
       ('02_distance_scene1.webp',.76,.78,1.0,2.95)]},
    {'dur':4, 'bg':'02_airport_traveler.webp', 'zoom':1.045, 'layers':[
       ('03_narration_scene2.webp',.78,.13,0.0,2.75),
       ('04_reveal_scene2.webp',.80,.76,1.45,3.95)]},
    {'dur':4, 'bg':'03_advertio_entry.webp', 'zoom':1.055, 'layers':[
       ('05_narration_scene3.webp',.79,.12,0.0,2.2),
       ('06_support_cta_scene3.webp',.79,.62,1.2,3.95)]},
    {'dur':5, 'bg':'04_connection_message.webp', 'zoom':1.050, 'layers':[
       ('07_message_scene4.webp',.82,.67,.65,4.85)]},
    {'dur':4, 'bg':'05_plane_cta.webp', 'zoom':1.065, 'layers':[
       ('08_cta_scene5.webp',.86,.21,.22,3.80),
       ('09_footer_scene5.webp',.80,.88,1.05,3.97)]}
]


def required_paths():
    for scene in SCENES:
        yield FRAMES/scene['bg']
        for name,*_ in scene['layers']:
            yield TYPE/name


def check():
    assert sum(s['dur'] for s in SCENES)==20, 'Expected 20-second storyboard'
    for p in required_paths():
        assert p.is_file() and p.stat().st_size>200, f'Missing {p}'
        with Image.open(p) as im:
            im.verify()
    assert shutil.which('ffmpeg') and shutil.which('ffprobe'), 'Install ffmpeg/ffprobe'
    print('Validated five storyboard scenes, nine WEBP layers and FFmpeg')


def ffmpeg(*args):
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y',*map(str,args)]
    print(' '.join(cmd[:9])+' ...',flush=True)
    subprocess.run(cmd,check=True)


def make_scene(scene,index,folder):
    duration=scene['dur']
    n=duration*FPS
    bg=FRAMES/scene['bg']
    args=['-loop','1','-i',str(bg)]
    for layer in scene['layers']:
        args.extend(['-loop','1','-i',str(TYPE/layer[0])])
    zoom=scene['zoom']
    # Gentle continuous push-in, kept orthographic in the underlying artwork.
    inc=(zoom-1)/max(1,n-1)
    chain=[f"[0:v]scale={int(WIDTH*1.16)//2*2}:-1,zoompan=z='min(zoom+{inc:.8f},{zoom:.4f})':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s={WIDTH}x{HEIGHT}:fps={FPS},format=yuv420p[base]"]
    prev='base'
    for i,(fname,scale,ypos,begin,end) in enumerate(scene['layers'],start=1):
        # WEBP typography layers maintain real transparency, animated as separate plates.
        layer=f't{i}'
        width=int(WIDTH*scale)//2*2
        fade_out=max(begin+.45,end-.28)
        chain.append(f"[{i}:v]scale={width}:-1,format=rgba,fade=t=in:st={begin:.2f}:d=0.30:alpha=1,fade=t=out:st={fade_out:.2f}:d=0.25:alpha=1[{layer}]")
        out=f'composed{i}'
        # y=... is a proportion of canvas height; center overlay around that location.
        chain.append(f"[{prev}][{layer}]overlay=(W-w)/2:{int(HEIGHT*ypos)}-h/2:enable='between(t,{begin:.2f},{end:.2f})'[{out}]")
        prev=out
    result=folder/f'scene{index}.mp4'
    ffmpeg(*args,'-filter_complex',';'.join(chain),'-map',f'[{prev}]',
           '-t',str(duration),'-r',str(FPS),'-an','-pix_fmt','yuv420p',
           '-c:v','libx264','-preset','veryfast' if MODE!='final' else 'medium',
           '-crf','26' if MODE=='quick-preview' else '20',
           '-movflags','+faststart',str(result))
    return result


def render():
    check()
    work=ROOT/'build'/MODE
    work.mkdir(parents=True,exist_ok=True)
    parts=[make_scene(s,i,work) for i,s in enumerate(SCENES,1)]
    listing=work/'concat.txt'
    listing.write_text(''.join("file '"+str(p.resolve())+"'\n" for p in parts))
    output=ROOT/OUTPUT
    ffmpeg('-f','concat','-safe','0','-i',listing,'-c','copy',output)
    info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries',
        'stream=width,height,avg_frame_rate:format=duration','-of','json',str(output)],text=True))
    assert abs(float(info['format']['duration'])-20)<.12, info
    assert output.stat().st_size>10000, output
    print('READY:',output,output.stat().st_size, 'bytes')


def samples():
    # Optional storyboard contact sheet from the current mode's MP4, not a replacement for MP4.
    file=ROOT/OUTPUT
    if not file.is_file(): render()
    frames=[]
    times=[.6,2.3,3.8,6.2,7.8,10.2,12.2,15.2,17.4,19.1]
    for i,t in enumerate(times):
        jpg=ROOT/f'frame-sample-{i:02d}.jpg'
        ffmpeg('-ss',str(t),'-i',file,'-frames:v','1',jpg)
        with Image.open(jpg) as im:
            frames.append(ImageOps.fit(im.convert('RGB'),(270,480)))
    result=Image.new('RGB',(5*270,2*480),'#06313e')
    for k,im in enumerate(frames):result.paste(im,((k%5)*270,(k//5)*480))
    result.save(ROOT/'quick-preview-contact-sheet.jpg',quality=86)
    print('Contact sheet and 10 sample frames generated')


if __name__=='__main__':
    if '--check' in sys.argv: check()
    elif '--samples' in sys.argv: samples()
    else:render()
