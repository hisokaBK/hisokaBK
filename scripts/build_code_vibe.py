"""Build the profile's local GIF and PNG assets. Run from the repository root."""
from PIL import Image, ImageDraw, ImageFont, ImageOps
from pathlib import Path
import re, math
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets'/'code-vibe'
OUT.mkdir(parents=True,exist_ok=True)
BG='#0d1117'; PANEL='#151e2b'; BAR='#1c2939'; LINE='#30485b'; TEXT='#eef4fc'; BLUE='#91c9e9'; MUTED='#829fb2'; CYAN='#82d5e6'
def font(n,bold=False,mono=False):
    return ImageFont.truetype('DejaVuSansMono.ttf' if mono else 'DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf',n)
def txt(d,xy,s,size=32,color=TEXT,bold=False,mono=False,anchor=None):
    d.text(xy,s,font=font(size,bold,mono),fill=color,anchor=anchor)
def canvas(w,h): return Image.new('RGB',(w,h),BG)
def photo(im,path,box,r=24):
    x,y,w,h=box
    ph=ImageOps.fit(ImageOps.exif_transpose(Image.open(ROOT/path)).convert('RGB'),(w,h),Image.Resampling.LANCZOS)
    mask=Image.new('L',(w,h)); ImageDraw.Draw(mask).rounded_rectangle((0,0,w-1,h-1),radius=r,fill=255)
    ImageDraw.Draw(im).rounded_rectangle((x-5,y-5,x+w+4,y+h+4),radius=r+5,outline=LINE,width=3)
    im.paste(ph,(x,y),mask)
def gif(name,frames,durations):
    # A shared palette ensures the photograph and other fixed pixels remain stable.
    palette=frames[-1].quantize(colors=256,method=Image.Quantize.MEDIANCUT)
    fs=[f.quantize(palette=palette,dither=Image.Dither.NONE) for f in frames]
    fs[0].save(OUT/(name+'.gif'),save_all=True,append_images=fs[1:],duration=durations,loop=0,optimize=True,disposal=1)
    frames[-1].save(OUT/(name+'.png'),optimize=True)
def hero():
    im=canvas(1600,860);d=ImageDraw.Draw(im)
    for y in range(0,860,44):
        for x in range(0,1600,44):
            if x>980 or y>793:d.ellipse((x,y,x+2,y+2),fill='#233245')
    d.rounded_rectangle((19,19,1580,840),radius=28,outline=LINE,width=2)
    d.line((54,86,1546,86),fill=LINE,width=2)
    txt(d,(58,38),'<>',30,CYAN,mono=True);txt(d,(124,43),'PROFILE  /  BILAL BAKESSOU',20,MUTED,mono=True);txt(d,(1450,43),'01 / 01',19,MUTED,mono=True)
    d.rounded_rectangle((63,119,510,164),radius=22,fill=BAR,outline=LINE)
    d.ellipse((81,136,92,147),fill=CYAN);txt(d,(108,128),'WELCOME TO MY DIGITAL SPACE',20,BLUE,True)
    txt(d,(62,188),'BILAL',76,TEXT,True);x=62+d.textlength('BILAL',font=font(76,True))+21
    txt(d,(x,188),'BAKESSOU',76,BLUE,True)
    txt(d,(66,286),'Full-Stack Developer & Data Enthusiast',38,TEXT,True)
    txt(d,(68,352),'Turning ideas into digital experiences',32,'#b8c8d9')
    txt(d,(68,395),'through code, creativity and data.',32,'#b8c8d9')
    photo(im,'assets/photos/original/classroom.jpg',(1049,116,488,654))
    d=ImageDraw.Draw(im);ex,ey,er,eb=64,463,1008,803
    d.rounded_rectangle((ex,ey,er,eb),radius=18,fill=PANEL,outline=LINE,width=2)
    d.rounded_rectangle((ex+2,ey+2,er-2,ey+48),radius=16,fill=BAR)
    d.rectangle((ex+2,ey+28,er-2,ey+48),fill=BAR)
    for j,col in enumerate(['#7790aa','#86b5d0','#a0cddd']):d.ellipse((85+22*j,ey+18,95+22*j,ey+28),fill=col)
    txt(d,(172,ey+13),'developer.js',21,TEXT,mono=True);txt(d,(874,ey+13),'JAVASCRIPT',17,MUTED,mono=True)
    d.line((ex+2,ey+49,er-2,ey+49),fill=LINE)
    lines=['const developer = {','  name: "Bilal Bakessou",','  role: "Full-Stack Developer",','  focus: ["Web", "Data", "Innovation"],','  location: "Morocco",','  status: "Open to opportunities"','};']
    for i in range(7):txt(d,(88,ey+62+i*32),str(i+1),24,MUTED,mono=True)
    d.line((123,ey+63,123,ey+283),fill=LINE)
    txt(d,(83,ey+300),'UTF-8  ·  JavaScript',17,MUTED,mono=True);txt(d,(1048,790),'01  /  LEARNING BY BUILDING',19,MUTED,mono=True)
    tokens=[]
    for line in lines:
        arr=[]
        for m in re.finditer(r'"[^"\n]*"|\bconst\b|\bdeveloper\b|\b\w+(?=\s*:)|.',line):
            s=m.group();color='#b5dca7' if s.startswith('"') else '#c7a7f2' if s=='const' else CYAN if s=='developer' else BLUE if re.match(r'^\w+$',s) else TEXT
            arr.extend((ch,color) for ch in s)
        tokens.append(arr)
    length=sum(len(l)+1 for l in lines)-1; step=font(29,mono=True).getlength('M')
    def render(n,cursor):
        f=im.copy();dd=ImageDraw.Draw(f);rem=n;row=col=0
        for i,t in enumerate(tokens):
            count=min(max(rem,0),len(t))
            for j,(ch,color) in enumerate(t[:count]):txt(dd,(145+j*step,ey+60+i*32),ch,29,color,mono=True)
            row=i;col=count
            if rem<=len(t):break
            rem-=len(t)+1
        if cursor:
            cx=round(145+col*step);cy=ey+65+row*32
            dd.rectangle((cx,cy,cx+2,cy+25),fill=CYAN)
        return f
    # Quantize just the changing editor crop, instead of re-encoding the photo per frame.
    full=render(length,False);full.save(OUT/'hero.png',optimize=True)
    palette=full.quantize(colors=256,method=Image.Quantize.MEDIANCUT)
    base=im.quantize(palette=palette,dither=Image.Dither.FLOYDSTEINBERG)
    rect=(135,ey+55,er-10,ey+290);frames=[];dur=[]
    for n,cur,delay in [(0,True,350)]+[(n,True,90 if n%19==0 else 43) for n in range(1,length+1)]+[(length,j%2==0,500) for j in range(8)]:
        f=base.copy();f.paste(render(n,cur).crop(rect).quantize(palette=palette,dither=Image.Dither.NONE),rect[:2]);frames.append(f);dur.append(delay)
    frames[0].save(OUT/'hero.gif',save_all=True,append_images=frames[1:],duration=dur,loop=0,optimize=True,disposal=1)
def title(key,a,b,file):
    frames=[]
    for n in range(4):
        im=canvas(1200,115);d=ImageDraw.Draw(im)
        txt(d,(28,27),'//',43,BLUE,mono=True)
        txt(d,(104,26),a,43,TEXT,True)
        x=104+d.textlength(a,font=font(43,True))+13
        txt(d,(x,26),b+'.'*n,43,BLUE,True)
        txt(d,(1168,52),file,22,MUTED,mono=True,anchor='rm')
        frames.append(im)
    gif('title-'+key,frames,[320,320,320,2300])
def education_timeline(rows):
    # A downward arrow traces the reverse-chronological timeline.
    h=60+len(rows)*116; im=canvas(1200,h); d=ImageDraw.Draw(im)
    axis=57; ys=[48+i*116 for i in range(len(rows))]
    start=ys[0]-24; finish=ys[-1]+29
    d.line((axis,start,axis,finish),fill=LINE,width=3)
    for i,(head,desc) in enumerate(rows):
        y=ys[i]
        txt(d,(100,y-19),head,34,BLUE,True)
        txt(d,(100,y+28),desc,25,TEXT)
    frames=[]; durations=[]
    # Smooth travel, a brief pause at each milestone, then a final readable hold.
    stops=[start]+ys+[finish]
    for segment,(a,b) in enumerate(zip(stops,stops[1:])):
        count=max(3,round((b-a)/7))
        for step in range(count+1):
            if segment and not step: continue
            tip=round(a+(b-a)*step/count)
            f=im.copy(); dd=ImageDraw.Draw(f)
            if tip>start: dd.line((axis,start,axis,tip),fill=BLUE,width=3)
            for y in ys:
                reached=tip>=y
                dd.ellipse((axis-9,y-9,axis+9,y+9),fill=BG,outline=BLUE if reached else LINE,width=3)
                if reached: dd.ellipse((axis-4,y-4,axis+4,y+4),fill=BLUE)
            # Keep the arrowhead visible even as it crosses a milestone.
            dd.line((axis-9,tip-10,axis,tip,axis+9,tip-10),fill=BLUE,width=3,joint='curve')
            frames.append(f)
            durations.append(650 if step==count and b in ys else 65)
    durations[-1]=2800
    gif('education',frames,durations)

def info(key,rows,phot=None):
    h=max(230,60+len(rows)*104);im=canvas(1200,h);d=ImageDraw.Draw(im)
    if phot:photo(im,phot,(875,20,290,h-40));d=ImageDraw.Draw(im)
    for i,(head,desc) in enumerate(rows):
        y=28+104*i
        txt(d,(30,y),str(i+1).zfill(2),22,MUTED,mono=True)
        txt(d,(90,y-4),head,34,BLUE,True)
        txt(d,(90,y+43),desc,25,TEXT)
    frames=[]
    for p in (0,1,2,3):
        f=im.copy();dd=ImageDraw.Draw(f)
        dd.rectangle((30,h-13,112+p*24,h-10),fill=BLUE)
        frames.append(f)
    gif(key,frames,[450,450,450,2400])
projects=[
 ('pharmaclick','PharmaClick','Multilingual pharmacy storefront','React / JavaScript / CSS','PharmaClick','https://pharma-click.netlify.app/'),
 ('streaming','Streaming Platform','Live video, replay & audience interaction','Laravel / Vue.js / LiveKit / PostgreSQL','Streaming_Platform',None),
 ('weather','Weather Risk Pipeline','Data ingestion, cleaning & risk analysis','Python / Pandas / Airflow / PostgreSQL','pipeline-de-donnees',None),
]
def weather_visual(im,box):
    x,y,w,h=box; d=ImageDraw.Draw(im)
    d.rounded_rectangle((x,y,x+w,y+h),radius=18,fill=PANEL,outline=LINE,width=2)
    txt(d,(x+20,y+15),'WEATHER / DATA ENGINEERING',19,BLUE,mono=True)
    stages=[('01','INGEST','Weather API'),('02','TRANSFORM','Pandas'),('03','STORE','PostgreSQL'),('04','VISUALIZE','Streamlit')]
    for i,(n,label,tech) in enumerate(stages):
        yy=y+55+i*62
        d.rounded_rectangle((x+20,yy,x+w-20,yy+47),radius=9,fill=BG,outline=LINE,width=1)
        txt(d,(x+32,yy+12),n,17,MUTED,mono=True)
        txt(d,(x+76,yy+10),label,20,BLUE,True)
        txt(d,(x+w-34,yy+23),tech,18,TEXT,anchor='rm')
        if i<3:
            cx=x+w//2
            d.line((cx,yy+47,cx,yy+61),fill=CYAN,width=2)
            d.polygon([(cx-5,yy+55),(cx+5,yy+55),(cx,yy+62)],fill=CYAN)
    txt(d,(x+20,y+h-40),'ORCHESTRATION / APACHE AIRFLOW',17,MUTED,mono=True)
def project(p,i):
    key,name,desc,stack,repo,demo=p
    im=canvas(1200,420);d=ImageDraw.Draw(im)
    # Keep screenshots at their native aspect ratio; do not crop away the actual UI.
    if key=='weather':
        weather_visual(im,(30,25,500,370))
    else:
        path=ROOT/'assets'/'projects'/('pharmaclick-screenshot.webp' if key=='pharmaclick' else 'streaming-screenshot.webp')
        if not path.is_file():
            raise FileNotFoundError(path)
        ph=ImageOps.contain(Image.open(path).convert('RGB'),(490,350),Image.Resampling.LANCZOS)
        d.rounded_rectangle((30,25,530,395),radius=18,fill=PANEL,outline=LINE,width=2)
        im.paste(ph,(30+(500-ph.width)//2,25+(370-ph.height)//2))
    d=ImageDraw.Draw(im)
    txt(d,(570,31),f'PROJECT / {i:02d}',21,MUTED,mono=True)
    txt(d,(570,87),name,37,TEXT,True)
    # Fit text to right side with measured wrapping.
    def wrap(s,y,sz,color):
        line=''
        for word in s.split():
            cand=(line+' '+word).strip()
            if d.textlength(cand,font=font(sz))>580:
                txt(d,(570,y),line,sz,color);y+=sz+9;line=word
            else:line=cand
        txt(d,(570,y),line,sz,color)
    wrap(desc,151,29,TEXT);wrap(stack,256,24,BLUE)
    is_screen=key=='pharmaclick' or (key=='streaming' and (ROOT/'assets/projects/streaming-screenshot.webp').is_file())
    txt(d,(570,371),'APPLICATION SCREENSHOT' if is_screen else 'CONCEPTUAL PROJECT VISUAL',17,MUTED,mono=True)
    frames=[]
    for n in (1,2,3):
        f=im.copy();ImageDraw.Draw(f).rectangle((570,330,570+n*45,333),fill=BLUE);frames.append(f)
    gif('project-'+key,frames,[400,400,2400])
def button(key,label):
    im=canvas(360,88);d=ImageDraw.Draw(im)
    d.rounded_rectangle((3,3,356,84),radius=14,fill=PANEL,outline=LINE,width=2)
    txt(d,(25,43),'>',30,BLUE,True,True,anchor='lm')
    txt(d,(70,43),label,27,TEXT,True,anchor='lm')
    txt(d,(330,43),'↗',25,BLUE,anchor='rm')
    im.save(OUT/('button-'+key+'.png'),optimize=True)
if not (OUT/'hero.gif').is_file() or not (OUT/'hero.png').is_file():hero()
titles=[('about','Behind the','code','about.js'),('work','Selected','work','projects.tsx'),('stack','My','toolbox','stack.json'),('experience','Learning by','building','experience.js'),('education','My','journey','education.md'),('contact',"Let's",'connect','contact.js')]
for t in titles:title(*t)
info('about',[('Full-Stack & Data','Web interfaces, backend APIs and data workflows.'),('Developer mindset','Clean architecture and useful, maintainable software.'),('Open to opportunities','Junior roles, internships and collaborations.')], 'assets/photos/original/gitex.jpeg')
info('stack',[('Frontend','React · Vue.js · TypeScript · JavaScript · Tailwind · Bootstrap'),('Backend','PHP · Laravel · Node.js · Express.js · Python · REST APIs · MVC'),('Data','PostgreSQL · MySQL / MariaDB · MongoDB · Pandas · ETL'),('Tools','Git · GitHub · Docker · Postman · Linux · VS Code')])
info('experience',[('Logic Technologies MA','Web Development Intern · May – July 2026'),('Somavira','Data cleaning & structuring · March – April 2025')])
education_timeline([('YouCode (UM6P)','Full-Stack Web Development & Data · 2025 – 2026'),('OFPPT','Technicien Spécialisé en Développement Digital · Bac+2'),('Faculté des Sciences Moulay Ismaïl','University studies · Meknès'),('Baccalauréat SVT','2020')])
info('contact',[("Let's build something together",'Open to junior developer roles and meaningful projects.')])
# Remove stale generated profile cards and replaced button, not the source repositories.
for key in ('ecoshop','easycoloc','orm'):
    for suffix in ('.gif','.png'):
        (OUT/('project-'+key+suffix)).unlink(missing_ok=True)
(OUT/'button-github.png').unlink(missing_ok=True)
for i,p in enumerate(projects,1):project(p,i)
for k,l in [('portfolio','PORTFOLIO'),('linkedin','LINKEDIN'),('whatsapp','WHATSAPP'),('email','EMAIL'),('source','SOURCE CODE'),('demo','LIVE DEMO')]:button(k,l)
def pic(key,alt):
    return f'<picture><source media="(prefers-reduced-motion: reduce)" srcset="./assets/code-vibe/{key}.png" /><img src="./assets/code-vibe/{key}.gif" width="100%" alt="{alt}" /></picture>\n'
def btn(k,url,alt):
    return f'<a href="{url}"><img src="./assets/code-vibe/button-{k}.png" width="180" alt="{alt}" /></a>'
def row(items):return '<p align="center">'+' &nbsp; '.join(items)+'</p>\n'
readme=['<!-- Generated by scripts/build_code_vibe.py. Visual content uses local GIFs; accessible alternatives and independent PNG links are preserved. -->\n',pic('hero','Bilal Bakessou — Full-Stack Developer & Data Enthusiast, open to opportunities in Morocco.'),
 row([btn('portfolio','https://potfolio-bilal-bakessou.vercel.app/','Portfolio'),btn('linkedin','https://www.linkedin.com/in/bilal-bakessou-bs6/','LinkedIn'),btn('whatsapp','https://wa.me/212611470423','WhatsApp')])]
alts={'about':'Full-stack and data developer focused on clean architecture, APIs and data workflows.','stack':'Frontend: React, Vue, TypeScript, JavaScript, Tailwind, Bootstrap. Backend: PHP, Laravel, Node, Express, Python, REST, MVC. Data: PostgreSQL, MySQL, MongoDB, Pandas, ETL. Tools: Git, GitHub, Docker, Postman, Linux, VS Code.','experience':'Logic Technologies MA web development internship, May–July 2026; Somavira internship: data cleaning and structuring, March–April 2025.','education':'YouCode full-stack and data; OFPPT Bac+2; Faculté des Sciences Moulay Ismaïl; Baccalauréat SVT 2020.','contact':'Open to junior developer roles and meaningful projects.'}
for k,a,b,f in titles:
    readme.extend(['\n<br />\n',pic('title-'+k,a+' '+b+'...')])
    if k=='work':
        for p in projects:
            key,name,desc,stack,repo,demo=p
            visual='Application screenshot.' if key=='pharmaclick' or (key=='streaming' and (ROOT/'assets/projects/streaming-screenshot.webp').is_file()) else 'Conceptual project visual.'
            readme.append(pic('project-'+key,f'{name} — {desc}. Stack: {stack}. {visual}'))
            links=[btn('source','https://github.com/hisokaBK/'+repo,'Source code: '+name)]
            if demo:links.append(btn('demo',demo,'Live demo: '+name))
            readme.append(row(links))
    else:
        readme.append(pic(k,alts[k]))
        if k=='contact':readme.append(row([btn('email','mailto:bilalbakessou99@gmail.com','Email')]))
(ROOT/'README.md').write_text('\n'.join(readme),encoding='utf-8')
# Verify all generated images and relative references.
for p in OUT.iterdir():
    with Image.open(p) as im:
        assert im.width>0 and im.height>0
        if p.suffix=='.gif':assert im.n_frames>1,p
for p in re.findall(r'(?:src|srcset)="\./([^"]+)"',(ROOT/'README.md').read_text()):
    assert (ROOT/p).is_file(),p
print('Validated',len(list(OUT.iterdir())),'assets')
