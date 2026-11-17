from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageEnhance
from pathlib import Path
import math, subprocess, sys
P=Path(__file__).resolve().parent
W,H,FPS,COUNT=720,1280,30,450
PALE=(5,11,22)
FONT=P/'BYekan.ttf'
REF=P/'reference.jpg'
def clamp(n): return max(0.,min(1.,n))
def ease(n): n=clamp(n); return n*n*(3-2*n)
def font(sz): return ImageFont.truetype(str(FONT),sz)
def latin_font(sz):
    try: return ImageFont.truetype('DejaVuSansMono.ttf',sz)
    except OSError: return ImageFont.load_default(size=sz)
def photo_frame(t):
    source=Image.open(REF).convert('RGB')
    im=ImageOps.fit(source,(W,H),Image.Resampling.LANCZOS,centering=(.5,.5))
    sc=1+.035*ease(t/2.3)
    if sc>1:
        nw,nh=round(W*sc),round(H*sc)
        enlarged=im.resize((nw,nh),Image.Resampling.LANCZOS)
        dx=(nw-W)//2;dy=(nh-H)//2
        im=enlarged.crop((dx,dy,dx+W,dy+H))
    return im
def hud(im,t):
    alpha=ease((t-.22)/.65)
    if not alpha:return im
    l=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(l)
    cyan=(47,231,241,round(200*alpha)); muted=(38,155,192,round(85*alpha))
    d.rectangle([38,44,682,1238],outline=muted,width=2)
    for x,y,dx in [(38,44,115),(682,44,-115),(38,1238,115),(682,1238,-115)]:
        d.line([(x,y),(x+dx,y)],fill=cyan,width=4)
    for y in range(114,1200,32):
        d.line((40,y,46,y),fill=muted,width=2)
        d.line((674,y,680,y),fill=muted,width=2)
    d.text((58,62),'ADVERTIO / FLIGHT OS',font=latin_font(20),fill=(99,239,249,round(230*alpha)))
    d.text((642,62),'REC',font=latin_font(20),anchor='ra',fill=cyan)
    d.ellipse((651,69,663,81),fill=(49,237,226,round(230*alpha)))
    d.text((60,1186),'FLIGHT DATA // 09:16',font=latin_font(17),fill=cyan)
    d.text((660,1186),f'{t:05.2f} S',font=latin_font(18),anchor='ra',fill=cyan)
    yy=1000+round(80*math.sin(t*1.7))
    d.line((49,yy,72,yy),fill=(42,238,234,round(170*alpha)),width=3)
    d.line((648,yy,672,yy),fill=(42,238,234,round(170*alpha)),width=3)
    return Image.alpha_composite(im.convert('RGBA'),l)
def headline(im,t):
    texts=[(7.85,52,'وقتی می‌تونی از',149,(227,250,255)),(8.30,94,'فضای خالی',230,(52,237,241)),(8.85,110,'چمدونت',360,(255,255,255)),(9.55,59,'درآمد کسب کنی',510,(215,248,255))]
    layer=Image.new('RGBA',(W,H));d=ImageDraw.Draw(layer)
    for begin,sz,s,y,rgb in texts:
        a=ease((t-begin)/.78)
        if a<=0:continue
        yy=y+round(27*(1-a))
        if s=='چمدونت':
            d.rounded_rectangle((78,yy+2,642,yy+144),radius=12,fill=(9,50,68,round(210*a)),outline=(39,233,238,round(225*a)),width=3)
        d.text((360,yy+4),s,font=font(sz),anchor='mt',direction='rtl',language='fa',fill=(0,8,20,round(225*a)),stroke_width=4,stroke_fill=(0,8,20,round(225*a)))
        d.text((360,yy),s,font=font(sz),anchor='mt',direction='rtl',language='fa',fill=(*rgb,round(255*a)))
    if t>=12.85:
        a=ease((t-12.85)/.8)
        d.rounded_rectangle((176,976,544,1062),radius=12,fill=(7,39,56,round(220*a)),outline=(26,213,220,round(210*a)),width=3)
        d.text((360,991),'advertio.net',font=latin_font(45),anchor='mt',fill=(224,251,255,round(255*a)))
    return Image.alpha_composite(im.convert('RGBA'),layer)
def make_frame(i):
    t=i/FPS
    base=Image.open(P/'frames'/f'{i:04d}.png').convert('RGB')
    if t<2.6:
        ph=photo_frame(t)
        # First output frame is the reference photograph itself.
        fade=ease((t-1.25)/1.35)
        base=Image.blend(ph,base,fade)
    base=hud(base,t)
    base=headline(base,t)
    return base.convert('RGB')
def encode():
    output=P/'flight-dark-tech-tiktok.mp4'
    command=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-vf','scale=1080:1920:flags=lanczos','-c:v','libx264','-preset','medium','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',str(output)]
    with subprocess.Popen(command,stdin=subprocess.PIPE) as proc:
        for i in range(COUNT):
            proc.stdin.write(make_frame(i).tobytes())
        proc.stdin.close()
        if proc.wait()!=0:raise RuntimeError('FFmpeg failed')
    print(output)
if __name__=='__main__':
    if '--samples' in sys.argv:
        for i in [0,45,90,180,270,360,435]:
            make_frame(i).save(P/f'dark-tech-preview-{i:03d}.jpg',quality=88)
    else: encode()
