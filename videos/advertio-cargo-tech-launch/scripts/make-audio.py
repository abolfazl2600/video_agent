"""Original deterministic, royalty-free 20-second synth bed for Advertio Cargo."""
import math, wave, struct
from pathlib import Path
SR=32000
DURATION=20
OUT=Path(__file__).resolve().parents[1]/'public'/'audio'/'original-tech-bed.wav'
OUT.parent.mkdir(parents=True,exist_ok=True)
# Original ambient minor-seventh progression and rhythmic pulses, no sampled music.
notes=[(110,130.81,164.81),(130.81,164.81,196),(98,123.47,146.83),(110,138.59,174.61)]
data=bytearray()
for i in range(SR*DURATION):
    t=i/SR
    chord=notes[min(3,int(t//5))]
    beat=t%0.5
    soft_attack=1-math.exp(-min(t,20-t)*9)
    tone=sum(math.sin(2*math.pi*hz*t+0.14*math.sin(t*.9))*0.06 for hz in chord)
    deep=0.14*math.sin(2*math.pi*(chord[0]/2)*t)*math.exp(-beat*7)
    tick=0.027*math.sin(2*math.pi*(5000-4400*min(.08,beat)/.08)*t)*math.exp(-beat*37) if beat<.10 else 0
    shimmer=.018*math.sin(2*math.pi*880*t+2*math.sin(t*5))*math.sin(math.pi*min(1,beat*2))**2
    # Emphasize the five scene transitions with short cinematic sweeps.
    sweep=0.0
    for event in (0,3,7,12,16):
        u=t-event
        if 0<=u<.28:sweep+=.15*math.sin(2*math.pi*(310*u+620*u*u))*(1-u/.28)
    gain=soft_attack*min(1,(20-t)/1.2)*.75
    v=max(-.95,min(.95,(tone+deep+tick+shimmer+sweep)*gain))
    data+=struct.pack('<h',int(v*32767))
with wave.open(str(OUT),'wb') as wav:
    wav.setnchannels(1);wav.setsampwidth(2);wav.setframerate(SR);wav.writeframes(data)
print(f'Generated original score: {OUT}, {DURATION}s')
