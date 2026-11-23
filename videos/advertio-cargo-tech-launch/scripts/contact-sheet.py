from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
files=sorted((ROOT/'out'/'stills').glob('*.jpg'))
assert len(files)==10,(len(files),files)
width,height=672,378
margin,gap,label=24,14,43
canvas=Image.new('RGB',(5*width+4*gap+2*margin,2*(height+label)+gap+2*margin),(250,253,255))
draw=ImageDraw.Draw(canvas)
for index,file in enumerate(files):
 x=margin+(index%5)*(width+gap)
 y=margin+(index//5)*(height+label+gap)
 with Image.open(file) as img:
  canvas.paste(img.convert('RGB').resize((width,height),Image.Resampling.LANCZOS),(x,y))
 draw.text((x+6,y+height+8),file.stem,fill=(19,55,100))
out=ROOT/'out'/'quick-preview-contact-sheet.jpg'
canvas.save(out,quality=90)
print('Contact sheet:',out)
