from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter, ImageOps
from pathlib import Path
import math, random, base64, json, textwrap

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'assets'
(OUT/'static').mkdir(parents=True,exist_ok=True)
NAVY=(9,17,32); INK=(16,29,48); PANEL=(21,36,58); EDGE=(40,67,93)
WHITE=(246,249,255); DIM=(158,177,201); MUTED=(107,135,166)
TEAL=(99,226,211); BLUE=(107,166,249); AMBER=(249,185,102); LILAC=(183,157,249)
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
MONO='/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
# Visually designed, original animated asset set for GitHub README.

def font(size,bold=False,mono=False):
 return ImageFont.truetype(MONO if mono else BOLD if bold else FONT, size)
def rgb_add(c,d):return tuple(max(0,min(255,c[i]+d[i])) for i in range(3))
def tint(c,k):return tuple(int(max(0,min(255,v*k))) for v in c)
def txt(d,xy,text,size=22,color=WHITE,bold=False,mono=False):d.text(xy,text,font=font(size,bold,mono),fill=color,stroke_width=0)
def rrect(d,box,r,fill,outline=None,width=1):d.rounded_rectangle(box,radius=r,fill=fill,outline=outline,width=width)
def grad(w,h,top=NAVY,bottom=(14,34,58)):
 im=Image.new('RGB',(w,h));d=ImageDraw.Draw(im)
 for y in range(h):
  t=y/max(1,h-1); c=tuple(int(top[k]*(1-t)+bottom[k]*t) for k in range(3));d.line([(0,y),(w,y)],fill=c)
 return im

def base(w,h,accent=TEAL,frame=0):
 im=grad(w,h);d=ImageDraw.Draw(im)
 for x in range(22,w,38):
  for y in range(20,h,38):
   d.point((x,y),fill=(30,49,70))
 d.rounded_rectangle((1,1,w-2,h-2),radius=16,outline=(40,68,91),width=2)
 d.rounded_rectangle((18,18,23,h-19),radius=2,fill=accent)
 for k in range(7):
  x=w-352+k*42
  d.line((x,32,x+14,32),fill=(48,74,94),width=2)
 return im,d

def icon(d,kind,cx,cy,scale=1,color=TEAL,t=0):
 S=lambda a:round(a*scale)
 if kind=='code':
  d.line([(cx-S(25),cy-S(17)),(cx-S(40),cy),(cx-S(25),cy+S(17))],fill=color,width=S(5),joint='curve')
  d.line([(cx+S(25),cy-S(17)),(cx+S(40),cy),(cx+S(25),cy+S(17))],fill=color,width=S(5),joint='curve')
  d.line((cx+S(11),cy-S(24),cx-S(10),cy+S(24)),fill=BLUE,width=S(5))
 elif kind=='stack':
  for j in range(3):
   yy=cy-S(23)+j*S(20)
   d.polygon([(cx,yy-S(13)),(cx+S(32),yy),(cx,yy+S(13)),(cx-S(32),yy)],outline=color if j==int(t*3)%3 else BLUE,width=S(3))
 elif kind=='terminal':
  rrect(d,(cx-S(43),cy-S(32),cx+S(43),cy+S(32)),S(8),(20,44,64),EDGE,2)
  d.line([(cx-S(26),cy-S(9)),(cx-S(15),cy),(cx-S(26),cy+S(9))],fill=color,width=S(4))
  d.line((cx-S(7),cy+S(10),cx+S(15),cy+S(10)),fill=BLUE,width=S(4))
 elif kind=='network':
  pts=[(cx-S(30),cy-S(15)),(cx+S(30),cy-S(26)),(cx+S(25),cy+S(25)),(cx-S(20),cy+S(29))]
  for j in range(4):d.line([pts[j],pts[(j+1)%4]],fill=EDGE,width=S(3))
  d.line([pts[0],pts[2]],fill=EDGE,width=S(3))
  for j,p in enumerate(pts):
   rad=S(8 if j==int(t*4)%4 else 6)
   d.ellipse((p[0]-rad,p[1]-rad,p[0]+rad,p[1]+rad),fill=color if j==int(t*4)%4 else BLUE)
 elif kind=='timeline':
  d.line((cx-S(43),cy,cx+S(43),cy),fill=EDGE,width=S(4))
  for j in range(4):
   x=cx-S(35)+j*S(23)
   rad=S(9) if j==int(t*4)%4 else S(6)
   d.ellipse((x-rad,cy-rad,x+rad,cy+rad),fill=color if j==int(t*4)%4 else BLUE)
 elif kind=='education':
  d.polygon([(cx-S(45),cy-S(15)),(cx,cy-S(38)),(cx+S(45),cy-S(15)),(cx,cy+S(8))],fill=(35,68,87),outline=color)
  d.polygon([(cx-S(27),cy-S(3)),(cx,cy+S(11)),(cx+S(27),cy-S(3)),(cx+S(27),cy+S(22)),(cx,cy+S(36)),(cx-S(27),cy+S(22))],fill=(35,68,87),outline=BLUE)
 elif kind=='camera':
  rrect(d,(cx-S(40),cy-S(24),cx+S(40),cy+S(27)),S(9),(30,52,75),color,3)
  d.ellipse((cx-S(16),cy-S(17),cx+S(16),cy+S(15)),outline=BLUE,width=S(4))
  d.rectangle((cx-S(30),cy-S(32),cx-S(5),cy-S(21)),fill=color)
 elif kind=='mail':
  rrect(d,(cx-S(45),cy-S(26),cx+S(45),cy+S(26)),S(7),(30,52,75),color,3)
  d.line([(cx-S(42),cy-S(22)),(cx,cy+S(9)),(cx+S(42),cy-S(22))],fill=BLUE,width=S(4))

def heading_gif(section,idx,title,subtitle,kind,accent=TEAL):
 w,h=1120,176;frames=[]
 for k in range(20):
  t=k/20;im,d=base(w,h,accent,k)
  txt(d,(47,29),f'{idx}  /  BILAL BAKESSOU',14,accent,bold=True,mono=True)
  txt(d,(47,64),title,40,WHITE,True)
  txt(d,(49,119),subtitle,16,DIM)
  # right visual zone
  rrect(d,(770,26,1084,150),14,(19,36,58),(43,75,96),2)
  icon(d,kind,847,89,0.92,accent,t)
  for j in range(8):
   yy=46+j*12; x1=911; x2=1050-(j%3)*20
   d.line((x1,yy,x2,yy),fill=(53,81,107),width=3)
   prog=(k*2.2+j*5)%100
   d.line((x1,yy,x1+(x2-x1)*prog/100,yy),fill=accent if j%3==0 else BLUE,width=3)
  # travelling signal stays inside strip
  xx=785+int((k/19)*275);d.ellipse((xx-3,139,xx+3,145),fill=accent)
  frames.append(im)
 save_gif(frames,OUT/'animated'/f'{section}.gif',dur=105)

def hero_gif():
 w,h=1120,346;frames=[]
 for k in range(26):
  t=k/26;im,d=base(w,h,TEAL,k)
  # subtle orbit background
  cx,cy=920,173
  for rad in (70,105,143):
   d.ellipse((cx-rad,cy-rad,cx+rad,cy+rad),outline=(34+rad//8,72+rad//8,94+rad//8),width=2)
  for j in range(9):
   a=(j/9+t*.5)*2*math.pi
   r=130 if j%2 else 90
   x=cx+math.cos(a)*r;y=cy+math.sin(a)*r
   color=TEAL if j%3==0 else BLUE
   d.ellipse((x-3,y-3,x+3,y+3),fill=color)
  # engineering illustration: nested code panel
  rrect(d,(798,101,1045,244),18,(20,39,59),(65,101,125),2)
  for a,c in [(813,(252,116,117)),(829,AMBER),(845,TEAL)]:d.ellipse((a,116,a+7,123),fill=c)
  txt(d,(824,139),'const build = {',18,BLUE,True,mono=True)
  txt(d,(846,169),'ideas: "real",',15,WHITE,mono=True)
  txt(d,(846,193),'quality: true',15,TEAL,mono=True)
  txt(d,(824,218),'}',18,BLUE,mono=True)
  # left content
  txt(d,(56,44),'FULL-STACK DEVELOPMENT  /  MOROCCO',17,TEAL,True,mono=True)
  txt(d,(54,94),'BILAL',78,WHITE,True)
  txt(d,(54,176),'BAKESSOU',78,WHITE,True)
  # typewriter / rotating tagline
  tagline='WEB APPLICATIONS  /  REST APIS  /  DATA'
  visible=max(3,int((k/25)*len(tagline)))
  txt(d,(58,273),tagline[:visible],19,DIM,mono=True)
  if k%6<4:
   x=58+d.textbbox((0,0),tagline[:visible],font=font(19,mono=True))[2]+3
   d.rectangle((x,277,x+9,294),fill=TEAL)
  d.line((57,318,746,318),fill=(58,89,108),width=2)
  frames.append(im)
 save_gif(frames,OUT/'animated'/'hero.gif',dur=90)

def save_gif(frames,path,dur=95):
 # shared palette improves stability and prevents per-frame quantization shimmer
 seed=frames[0].quantize(colors=128,method=Image.Quantize.MEDIANCUT)
 items=[f.quantize(palette=seed, dither=Image.Dither.NONE) for f in frames]
 items[0].save(path,save_all=True,append_images=items[1:],optimize=True,loop=0,duration=dur,disposal=2)
 print('GIF',path.name,path.stat().st_size)

PROJECTS=[
 ('pharmaclick','01','PharmaClick','ONLINE PHARMACY EXPERIENCE','React  /  JavaScript  /  Bootstrap',TEAL,'pharma'),
 ('streaming','02','Streaming Platform','REAL-TIME VIDEO & INTERACTION','Laravel  /  Vue.js  /  LiveKit  /  PostgreSQL',BLUE,'stream'),
 ('ecoshop','03','EcoShop API','E-COMMERCE BACKEND','Laravel  /  Sanctum  /  REST  /  Docker',AMBER,'api'),
 ('weather','04','Weather Risk Pipeline','DATA ENGINEERING & ANALYTICS','Python  /  Pandas  /  Airflow  /  PostgreSQL',LILAC,'weather'),
 ('easycoloc','05','EasyColoc','SHARED LIVING & EXPENSES','Laravel  /  Blade  /  Tailwind CSS',TEAL,'housing'),
 ('orm','06','Custom PHP ORM','DATABASE ABSTRACTION & CRUD','PHP  /  PDO  /  PostgreSQL  /  Docker',BLUE,'database'),
]

def draw_project_icon(d,kind,k,t,c):
 # right panel with diagrams or artistic UI metaphors, not invented screenshots
 x=758;y=30
 rrect(d,(x,y,1090,252),20,(21,37,59),(51,79,106),2)
 d.line((x+17,y+36,x+314,y+36),fill=(51,72,93),width=2)
 for i,col in enumerate(((254,119,110),AMBER,TEAL)):
  d.ellipse((x+20+i*17,y+16,x+28+i*17,y+24),fill=col)
 if kind=='pharma':
  # pills, search, checkout overview
  rrect(d,(x+20,y+56,x+291,y+91),13,(33,57,79))
  d.ellipse((x+34,y+67,x+46,y+79),outline=c,width=2)
  d.line((x+45,y+79,x+52,y+86),fill=c,width=2)
  for i in range(3):
   x0=x+23+i*92
   rrect(d,(x0,y+108,x0+80,y+188),9,(35,63,82))
   d.ellipse((x0+16,y+121,x0+64,y+154),fill=(52+i*9,93+i*4,105))
   d.line((x0+37,y+121,x0+44,y+154),fill=(224,250,247),width=3)
   d.rectangle((x0+17,y+165,x0+63,y+169),fill=c)
 elif kind=='stream':
  rrect(d,(x+21,y+52,x+200,y+179),10,(38,53,82))
  # play triangle / live progress
  d.polygon([(x+95,y+88),(x+95,y+140),(x+139,y+114)],fill=c)
  d.rectangle((x+35,y+160,x+172,y+164),fill=(55,79,98))
  d.rectangle((x+35,y+160,x+35+int(t*137),y+164),fill=c)
  for j in range(3):
   rrect(d,(x+220,y+55+j*48,x+299,y+94+j*48),8,(35,59,78))
   d.ellipse((x+228,y+67+j*48,x+241,y+80+j*48),fill=BLUE)
   d.line((x+249,y+70+j*48,x+290,y+70+j*48),fill=(145,172,192),width=3)
 elif kind=='api':
  lines=[('GET','/products'),('POST','/orders'),('AUTH','/login')]
  for i,(m,route) in enumerate(lines):
   rrect(d,(x+23,y+54+i*50,x+300,y+91+i*50),8,(30,55,76))
   rrect(d,(x+35,y+63+i*50,x+106,y+82+i*50),5,TEAL if i==0 else AMBER if i==1 else BLUE)
   txt(d,(x+46,y+64+i*50),m,12,NAVY,True,mono=True)
   txt(d,(x+121,y+63+i*50),route,15,WHITE,mono=True)
 elif kind=='weather':
  rrect(d,(x+20,y+54,x+305,y+191),11,(31,52,72))
  pts=[]
  for j in range(12):
   xx=x+36+j*23; yy=y+147-19*math.sin(j*.72)-j*2.2
   pts.append((xx,yy))
  for j in range(11):d.line((*pts[j],*pts[j+1]),fill=c,width=4)
  for pt in pts:d.ellipse((pt[0]-3,pt[1]-3,pt[0]+3,pt[1]+3),fill=WHITE)
  for j in range(4):d.line((x+35,y+80+j*31,x+288,y+80+j*31),fill=(58,74,92),width=1)
 elif kind=='housing':
  d.polygon([(x+70,y+114),(x+160,y+49),(x+253,y+114)],fill=(43,91,98),outline=c)
  rrect(d,(x+85,y+114,x+239,y+206),8,(34,65,81))
  rrect(d,(x+145,y+145,x+185,y+206),4,(95,156,164))
  for a in (100,195):rrect(d,(x+a,y+135,x+a+27,y+158),4,(120,182,179))
  d.ellipse((x+261,y+54,x+291,y+84),fill=AMBER)
  txt(d,(x+269,y+61),'$',12,NAVY,True)
 elif kind=='database':
  for j in range(3):
   cy=y+76+j*48
   d.ellipse((x+43,cy-15,x+141,cy+14),fill=(49,90,116),outline=c,width=3)
   d.rectangle((x+43,cy-3,x+141,cy+18),fill=(49,90,116))
   d.arc((x+43,cy-15,x+141,cy+14),0,180,fill=c,width=3)
  d.line((x+160,y+115,x+226,y+115),fill=c,width=3)
  d.polygon([(x+227,y+115),(x+211,y+106),(x+211,y+124)],fill=c)
  rrect(d,(x+240,y+84,x+291,y+150),8,(35,75,92),c,2)
  txt(d,(x+249,y+99),'ORM',13,WHITE,True,mono=True)
  txt(d,(x+249,y+125),'PHP',12,TEAL,True,mono=True)

def project_card(p):
 key,num,name,kicker,stack,accent,kind=p;w,h=1120,282
 im,d=base(w,h,accent)
 txt(d,(51,36),f'FEATURED WORK  /  {num}',16,accent,True,mono=True)
 txt(d,(49,85),name,42,WHITE,True)
 txt(d,(51,154),kicker,16,DIM,True,mono=True)
 rrect(d,(49,193,688,241),12,(26,45,66),(48,76,94),1)
 txt(d,(65,208),stack,16,WHITE,mono=True)
 draw_project_icon(d,kind,0,1,accent)
 im.save(OUT/'projects'/f'{key}.webp',format='WEBP',quality=90,method=6)
 print('PROJECT',key,(OUT/'projects'/f'{key}.webp').stat().st_size)

# Photos: retain authentic subjects, raise perceived contrast, crop professionally. Never retouch identity.
PHOTOS=[('robotics',str(ROOT/'assets/photos/source/robotics.jpg'),'ROBOTICS & INNOVATION','TECH EVENTS'),('outdoors',str(ROOT/'assets/photos/source/outdoors.jpg'),'BEYOND THE SCREEN','OUTDOORS'),('gitex',str(ROOT/'assets/photos/source/gitex.jpg'),'GITEX AFRICA 2026','COMMUNITY')]
def photo_crop(path, size=(416,465),centering=(.5,.45)):
 im=Image.open(path).convert('RGB')
 im=ImageOps.fit(im,size,method=Image.Resampling.LANCZOS,centering=centering)
 im=ImageEnhance.Contrast(im).enhance(1.055)
 im=ImageEnhance.Color(im).enhance(1.05)
 return im

def photo_gallery():
 w,h=1120,526
 im,d=base(w,h,TEAL)
 txt(d,(47,29),'BEYOND THE TERMINAL',29,WHITE,True)
 txt(d,(48,74),'A few moments from technology events and life beyond code.',16,DIM)
 sx=42;g=12;cw=337;ch=384;sy=118
 choices=[(0.50,.38),(0.50,.43),(0.52,.42)]
 for i,(key,path,cap,tag) in enumerate(PHOTOS):
  x=sx+i*(cw+g);picture=photo_crop(path,(cw,ch),choices[i])
  # subtle dark overlay on lower 90px for text legibility
  overlay=Image.new('RGBA',(cw,ch),(0,0,0,0));od=ImageDraw.Draw(overlay)
  for j in range(105):
   a=int(180*j/105);od.line((0,ch-105+j,cw,ch-105+j),fill=(5,13,25,a))
  picture=Image.alpha_composite(picture.convert('RGBA'),overlay).convert('RGB')
  mask=Image.new('L',(cw,ch),0);ImageDraw.Draw(mask).rounded_rectangle((0,0,cw-1,ch-1),radius=15,fill=255)
  im.paste(picture,(x,sy),mask)
  rrect(d,(x,sy,x+cw,sy+ch),15,None,(76,100,127),2)
  txt(d,(x+16,sy+ch-58),cap,17,WHITE,True)
  txt(d,(x+16,sy+ch-31),tag,11,TEAL,True,mono=True)
 im.save(OUT/'photos'/'moments.webp',format='WEBP',quality=88,method=6)
 print('GALLERY',(OUT/'photos'/'moments.webp').stat().st_size)
 for i,(key,path,cap,tag) in enumerate(PHOTOS):
  img=photo_crop(path,(700,900),choices[i]);img.save(OUT/'photos'/f'{key}.webp',format='WEBP',quality=86,method=6)
  print('PHOTO',key,(OUT/'photos'/f'{key}.webp').stat().st_size)

# Tech board retina-sharp / uses brand text initials rather than claiming official logos.
TECH=[
 ('FRONTEND',[('TS',(48,111,221),'TypeScript'),('JS',(242,208,72),'JavaScript'),('R',(81,201,244),'React'),('V',(73,190,136),'Vue.js'),('TW',(79,190,208),'Tailwind')]),
 ('BACKEND',[('PHP',(128,135,197),'PHP'),('L',(235,92,79),'Laravel'),('PY',(84,153,199),'Python'),('API',(88,218,180),'REST APIs'),('PDO',(206,161,105),'PDO')]),
 ('DATA & TOOLS',[('PG',(105,161,221),'PostgreSQL'),('SQL',(142,212,184),'MySQL'),('P',(129,165,211),'Pandas'),('D',(112,190,233),'Docker'),('G',(236,155,120),'Git')]),
]
def tech_board():
 w,h=1120,440;im,d=base(w,h,BLUE)
 txt(d,(48,30),'THE TOOLS BEHIND THE WORK',29,WHITE,True)
 txt(d,(48,75),'Selected technologies used across my public repositories.',16,DIM)
 for row,(label,skills) in enumerate(TECH):
  y=117+row*101
  txt(d,(48,y),label,13,BLUE,True,mono=True)
  for j,(mark,color,name) in enumerate(skills):
   x=47+j*211;Y=y+24
   rrect(d,(x,Y,x+198,Y+66),12,(23,43,63),(51,79,103),1)
   rrect(d,(x+10,Y+10,x+57,Y+56),11,color)
   bb=d.textbbox((0,0),mark,font=font(13,True));tw=bb[2]-bb[0]
   txt(d,(x+33-tw/2,Y+25),mark,13,NAVY,True)
   txt(d,(x+69,Y+23),name,15,WHITE,True)
 im.save(OUT/'tech-board.webp',format='WEBP',quality=92,method=6)
 print('TECH BOARD',(OUT/'tech-board.webp').stat().st_size)

if __name__=='__main__':
 hero_gif()
 for row in [
 ('about','01','ABOUT ME','Developer mindset, clean architecture, human-centred products.','code',TEAL),
 ('projects','02','SELECTED WORK','Frontend, backend, real-time apps and data engineering.','stack',BLUE),
 ('skills','03','TECH STACK','The tools and patterns behind the projects.','terminal',TEAL),
 ('experience','04','EXPERIENCE','Practical learning, delivery and real projects.','timeline',AMBER),
 ('education','05','LEARNING PATH','Continuous development through education and practice.','education',LILAC),
 ('community','06','BEYOND CODE','Technology events, curiosity and connections.','camera',TEAL),
 ('contact','07','LET US CONNECT','Open to junior roles, internships and collaboration.','mail',BLUE),
 ]:heading_gif(*row)
 for p in PROJECTS:project_card(p)
 photo_gallery();tech_board()
 for anim in (OUT/'animated').glob('*.gif'):
  frame=Image.open(anim).convert('RGB');frame.save(OUT/'static'/f'{anim.stem}.webp',format='WEBP',quality=93,method=6)
 print('OUTPUT',[(str(p.relative_to(ROOT)),p.stat().st_size) for p in sorted((OUT).rglob('*')) if p.is_file()])