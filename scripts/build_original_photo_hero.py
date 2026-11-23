from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math

ROOT=Path(__file__).resolve().parents[1]
ASSET=ROOT/'assets'
(ASSET/'animated').mkdir(parents=True,exist_ok=True)
(ASSET/'static').mkdir(parents=True,exist_ok=True)
PHOTOS=[
 ('WORKSHOP',ASSET/'photos/original/classroom.jpg', (0.38,0.32)),
 ('TECH EVENT',ASSET/'photos/original/robot.jpeg', (0.47,0.40)),
 ('GITEX AFRICA',ASSET/'photos/original/gitex.jpeg', (0.53,0.45)),
 ('CREATIVITY',ASSET/'photos/original/campus.jpg',(0.72,0.42)),
]
W,H=1200,460
PHOTO_X=708; PHOTO_W=W-PHOTO_X
BOLD='/usr/share/fonts/truetype/lato/Lato-Heavy.ttf'
REG='/usr/share/fonts/truetype/lato/Lato-Regular.ttf'
SEM='/usr/share/fonts/truetype/lato/Lato-Semibold.ttf'
def font(path,size): return ImageFont.truetype(path,size)
FB=font(BOLD,72); FS=font(SEM,24); FR=font(REG,23); FCH=font(SEM,22); FNOTE=font(SEM,15)

def cover_original(path,out_size,focus):
    # Only crop and resize original photography. Never generatively alter pixels or retouch faces.
    im=Image.open(path).convert('RGB')
    iw,ih=im.size; ow,oh=out_size
    target_ratio=ow/oh
    if iw/ih > target_ratio:
        cw=int(round(ih*target_ratio)); ch=ih
    else:
        cw=iw; ch=int(round(iw/target_ratio))
    cx,cy=focus[0]*iw,focus[1]*ih
    x=max(0,min(iw-cw,int(cx-cw/2))); y=max(0,min(ih-ch,int(cy-ch/2)))
    crop=im.crop((x,y,x+cw,y+ch))
    return crop.resize(out_size, Image.Resampling.LANCZOS)

# Exact same background in each frame; only the photo and tiny decorative pulse change.
def make_frame(index,pulse):
    im=Image.new('RGB',(W,H),(8,16,29));px=im.load()
    for y in range(H):
      for x in range(PHOTO_X):
       a=x/PHOTO_X; b=y/H
       px[x,y]=(int(5+12*a+4*b),int(15+18*a+3*b),int(30+25*a+4*b))
    d=ImageDraw.Draw(im)
    for gx in range(28,PHOTO_X,52):
       d.line([(gx,0),(gx,H)],fill=(23,47,65),width=1)
    for gy in range(0,H,46):
       d.line([(0,gy),(PHOTO_X,gy)],fill=(19,42,62),width=1)
    # photo is pasted without filters, overlays, gradients, or inpainting
    photo=cover_original(PHOTOS[index][1],(PHOTO_W,H),PHOTOS[index][2]); im.paste(photo,(PHOTO_X,0));d=ImageDraw.Draw(im)
    # a fixed border outside the subject photo (no alteration of photograph)
    d.rectangle([PHOTO_X-2,0,PHOTO_X,H],fill=(49,198,206))
    d.line([(PHOTO_X,0),(PHOTO_X,H)],fill=(67,172,196),width=2)
    # decorative original backdrop + restrained glow, only in graphics area
    d.rounded_rectangle((55,39,103,86),radius=12,outline=(44,211,216),width=2,fill=(9,29,45))
    d.text((64,49),'</>',font=font(SEM,20),fill=(102,234,231))
    d.text((58,95),'BILAL',font=FB,fill=(247,249,255),stroke_width=0)
    # gradient text (only the lettering is gradient)
    mask=Image.new('L',(W,H),0); md=ImageDraw.Draw(mask); md.text((54,170),'BAKESSOU',font=FB,fill=255)
    grad=Image.new('RGB',(W,H));p=grad.load()
    for x in range(55,600):
      t=max(0,min(1,(x-55)/460));a=(67,215,216);b=(192,112,237)
      col=tuple(int(a[k]*(1-t)+b[k]*t) for k in range(3))
      for yy in range(166,260):p[x,yy]=col
    im.paste(grad,(0,0),mask);d=ImageDraw.Draw(im)
    d.rounded_rectangle((56,266,479,314),radius=14,outline=(49,206,221),width=2,fill=(8,27,45))
    d.text((75,276),'FULL-STACK WEB DEVELOPER',font=FS,fill=(242,248,255))
    d.rounded_rectangle((56,338,60,366),radius=2,fill=(47,213,207))
    d.text((76,339),'Building web products, APIs & data workflows',font=font(REG,20),fill=(233,240,246))
    badges=[('React',(88,203,222)),('TypeScript',(88,161,246)),('Laravel',(217,93,106)),('Python',(234,190,93)),('SQL',(169,143,238))]
    cursor=56
    for text,color in badges:
      tw=d.textbbox((0,0),text,font=font(SEM,17))[2]
      bw=tw+36
      d.rounded_rectangle((cursor,386,cursor+bw,426),radius=12,outline=color,width=2,fill=(11,25,42))
      d.ellipse((cursor+11,402,cursor+20,411),fill=color)
      d.text((cursor+25,396),text,font=font(SEM,17),fill=(239,245,254))
      cursor+=bw+12
    # decorative long wave across left-only bottom edge; photo remains untouched
    points=[]
    for x in range(0,PHOTO_X):
       y=453-5*math.sin(math.pi*x/PHOTO_X)+1.5*math.sin(x/58+0.2*pulse)
       points.append((x,y))
    d.line(points,fill=(30+8*pulse,191+8*pulse,203+7*pulse),width=3)
    d.ellipse((671,28,683,40),fill=(38+10*pulse,193+8*pulse,207+5*pulse))
    return im

frames=[make_frame(i,p) for i in range(4) for p in range(2)]
# Save a screenshot-safe PNG preview from exact original composition.
frames[0].save(ASSET/'static/hero-original-photos.webp',format='WEBP',quality=92,method=6)
# Store as animated webp with excellent photographic color, alongside a broadly-compatible GIF.
frames[0].save(ASSET/'animated/hero-original-photos.webp',save_all=True,append_images=frames[1:],duration=[1900]*8,loop=0,quality=92,method=6)
# For high-fidelity photography on GitHub, the animated WebP above is preferred to indexed-color GIF.
# To export a .gif locally, use frames[0].save('hero.gif',save_all=True,append_images=frames[1:],duration=[1900]*8,loop=0).
print('Wrote animated WebP and static fallback using unmodified photo crops.')