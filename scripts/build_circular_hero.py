#!/usr/bin/env python3
"""Render circular-photo GitHub profile assets from exact original image files.

SOURCE PHOTOS ARE NEVER CHANGED. The code only resizes / crops copies, masks
those copies to circles, and draws graphics outside their pixels. No AI edits,
face retouching, color filters, or inpainting are applied to the photographs.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets'
ANIM = OUT / 'animated'
STATIC = OUT / 'static'
CIRCLES = OUT / 'photos' / 'circles'
for p in (ANIM, STATIC, CIRCLES):
    p.mkdir(parents=True, exist_ok=True)

# Values choose crop location only; source pixels stay intact.
PHOTO_SPECS = [
    ('classroom', 'classroom.jpg', (0.34, 0.38, 0.73)),
    ('robot', 'robot.jpeg', (0.48, 0.40, 0.86)),
    ('gitex', 'gitex.jpeg', (0.51, 0.48, 1.00)),
    ('campus', 'campus.jpg', (0.76, 0.38, 0.65)),
]
SRC = OUT / 'photos' / 'original'
W, H = 1200, 460
TEAL = (53, 223, 222)
VIOLET = (184, 129, 252)
FG = (244, 247, 253)
PALE = (177, 197, 221)
POSITIONS = [(779, 111), (1033, 111), (779, 325), (1033, 325)]
R = 86

def pick_font(size, bold=False):
    candidates = [
        '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
        '/usr/share/fonts/truetype/lato/Lato-Heavy.ttf' if bold else '/usr/share/fonts/truetype/lato/Lato-Regular.ttf',
    ]
    for name in candidates:
        if Path(name).exists():
            return ImageFont.truetype(name, size)
    return ImageFont.load_default()

FONT_NAME = pick_font(66, True)
FONT_ROLE = pick_font(21, True)
FONT_BODY = pick_font(18)
FONT_CHIP = pick_font(15, True)
FONT_LABEL = pick_font(13, True)

def cropped_photo(source, focus, px):
    """Crop/resize only. No photo content is edited beyond resampling."""
    im = Image.open(source).convert('RGB')
    iw, ih = im.size
    cx, cy, factor = focus
    side = min(iw, ih) * factor
    xc = cx * iw
    yc = cy * ih
    left = max(0, min(iw - side, xc - side / 2))
    top = max(0, min(ih - side, yc - side / 2))
    return im.crop((int(left), int(top), int(left + side), int(top + side))).resize((px, px), Image.Resampling.LANCZOS)

def mask_photo(source, focus, size):
    # The alpha mask only controls which original pixels are visible.
    photo = cropped_photo(source, focus, size)
    mask = Image.new('L', (size, size), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size - 1, size - 1), fill=255)
    result = photo.convert('RGBA')
    result.putalpha(mask)
    return result

def linear_gradient_name(canvas):
    text = 'BAKESSOU'
    m = Image.new('L', canvas.size, 0)
    md = ImageDraw.Draw(m)
    md.text((47, 154), text, font=FONT_NAME, fill=255)
    ink = Image.new('RGBA', canvas.size)
    ip = ink.load()
    for x in range(42, 485):
        t = min(1, max(0, (x-47) / 390))
        c = tuple(round(TEAL[j] * (1 - t) + VIOLET[j] * t) for j in range(3))
        for y in range(147, 235):
            ip[x, y] = (*c, 255)
    canvas.paste(ink, (0, 0), m)

def background():
    image = Image.new('RGBA', (W, H), (7, 17, 33, 255))
    p = image.load()
    for y in range(H):
        for x in range(W):
            u = x / W
            glow = math.exp(-(((x-900)/360)**2 + ((y-224)/260)**2))
            p[x, y] = (round(7+5*u+4*glow), round(16+10*u+11*glow), round(30+14*u+18*glow), 255)
    d = ImageDraw.Draw(image)
    for gx in range(18, W, 42):
        d.line((gx, 0, gx, H), fill=(26, 49, 77, 120), width=1)
    for gy in range(16, H, 42):
        d.line((0, gy, W, gy), fill=(26, 49, 77, 120), width=1)
    d.rounded_rectangle((28, 27, 78, 75), radius=13, fill=(12, 37, 56), outline=TEAL, width=2)
    d.text((34, 40), '</>', font=pick_font(16, True), fill=TEAL)
    d.text((48, 94), 'BILAL', font=FONT_NAME, fill=FG)
    linear_gradient_name(image)
    d = ImageDraw.Draw(image)
    d.rounded_rectangle((46, 250, 505, 292), radius=12, outline=(45, 209, 214), width=2, fill=(10, 31, 49))
    d.text((62, 259), 'FULL-STACK WEB DEVELOPER', font=FONT_ROLE, fill=FG)
    d.rounded_rectangle((47, 321, 53, 344), radius=3, fill=TEAL)
    d.text((67, 322), 'Web products  /  APIs  /  Data workflows', font=FONT_BODY, fill=(225, 235, 248))
    chips = [('React', (83, 216, 228)), ('TypeScript', (94, 161, 255)), ('Laravel', (243, 116, 131)), ('Python', (252, 202, 105)), ('SQL', (183, 144, 251))]
    x = 47
    for title, accent in chips:
        bbox = d.textbbox((0, 0), title, font=FONT_CHIP)
        width = bbox[2] - bbox[0] + 34
        d.rounded_rectangle((x, 378, x+width, 413), radius=11, outline=accent, width=2, fill=(12, 28, 49))
        d.ellipse((x+10, 392, x+18, 400), fill=accent)
        d.text((x+23, 385), title, font=FONT_CHIP, fill=FG)
        x += width + 10
    # Graphic strokes never tint or repaint the source photos.
    d.line([(12, 448), (160, 438), (338, 446), (533, 444), (645, 446)], fill=(55, 199, 216), width=3)
    d.line([(632, 14), (632, 445)], fill=(38, 78, 103), width=2)
    # Delicate orbital connectors behind circles.
    d.line([(779, 111), (1033, 111), (1033, 325), (779, 325), (779, 111)], fill=(44, 91, 115), width=2)
    d.line([(779, 111), (1033, 325)], fill=(30, 66, 97), width=1)
    d.line([(779, 325), (1033, 111)], fill=(30, 66, 97), width=1)
    return image

def draw_circle(base, i, active, pulse=0):
    label, fname, focus = PHOTO_SPECS[i]
    x, y = POSITIONS[i]
    r = R
    d = ImageDraw.Draw(base)
    # Shadow and bezel entirely outside the photo circle.
    d.ellipse((x-r-12, y-r-9, x+r+12, y+r+15), fill=(3, 10, 19, 255))
    active_color = TEAL if i in (0,3) else VIOLET
    stroke = active_color if active else (72, 106, 136)
    if active:
        for s, alpha in [(13,55),(9,95),(5,155)]:
            d.ellipse((x-r-s, y-r-s, x+r+s, y+r+s), outline=(*stroke, alpha), width=2)
    d.ellipse((x-r-5, y-r-5, x+r+5, y+r+5), fill=(13, 31, 49), outline=stroke, width=4 if active else 3)
    photo = mask_photo(SRC/fname, focus, 2*r)
    base.alpha_composite(photo,(x-r,y-r))
    # little factual labels are outside photographs
    label_width=d.textbbox((0,0),label.upper(),font=FONT_LABEL)[2]
    label_x=x-(label_width+24)//2
    label_y=y+r+6
    d.rounded_rectangle((label_x,label_y,label_x+label_width+24,label_y+25),radius=12,fill=(9,25,45),outline=stroke,width=1)
    d.text((label_x+12,label_y+5),label.upper(),font=FONT_LABEL,fill=(233,246,254))

def render(active=0, pulse=0):
    im=background()
    for i in range(4):
        draw_circle(im,i,i==active,pulse)
    return im

def make_thumbnails():
    for name, fname, focus in PHOTO_SPECS:
        size=230
        canvas=Image.new('RGBA',(size,size),(0,0,0,0))
        d=ImageDraw.Draw(canvas)
        d.ellipse((5,5,225,225),fill=(12,32,53,255),outline=(61,212,224,255),width=5)
        ring=mask_photo(SRC/fname,focus,210)
        canvas.alpha_composite(ring,(10,10))
        canvas.save(CIRCLES/(name+'.webp'),'WEBP',quality=94,method=6)

if __name__ == '__main__':
    make_thumbnails()
    frames=[render(i, j) for i in range(4) for j in range(2)]
    frames[0].convert('RGB').save(STATIC/'hero-circles.webp','WEBP',quality=90,method=6)
    frames[0].save(ANIM/'hero-circles.webp',save_all=True,append_images=frames[1:],duration=[1800]*8,loop=0,quality=88,method=6)
    # GIF is optional backup but WebP is better for exact colors in original photographs.
    print('Circular-photo assets ready. Original source photographs are unchanged.')