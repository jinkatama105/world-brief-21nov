#!/usr/bin/env python3
# Renders the 1024x1024 news board for Sat 21 Nov 2026 (deterministic; DejaVu system fonts).
from PIL import Image, ImageDraw, ImageFont
import os

W = H = 1024
BG = (14, 17, 25)
CARD = (24, 28, 40)
INK = (236, 239, 246)
BODY = (198, 206, 222)
DIM = (140, 150, 172)
GOLD = (244, 183, 61)
REGION = {
    'MIDDLE EAST': (255, 104, 92),
    'EUROPE': (96, 160, 255),
    'AMERICAS': (244, 183, 61),
    'GLOBAL': (198, 120, 255),
    'ASIA': (110, 220, 160),
}

def font(sz, bold=False):
    p = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    return ImageFont.truetype(p, sz)

F_TITLE = font(46, True)
F_DATE = font(21, True)
F_TAG = font(18)
F_HEAD = font(21, True)
F_BODY = font(17)
F_CHIP = font(14, True)
F_PLACE = font(15)
F_FOOT = font(14)

STORIES = [
    ('AMERICAS', 'El Chapo Isidro captured', 'GUASAVE, MEXICO',
     'A bloody overnight raid left 11 dead as Mexican forces flew the FBI most-wanted boss to Mexico City. Allies hailed the win; analysts warn Sinaloa now faces a fresh power struggle.'),
    ('MIDDLE EAST', 'Iran hits tankers near Hormuz', 'STRAIT OF HORMUZ',
     'Three tankers were ablaze or struck as Tehran unveiled a dual-missile launcher in an underground base. Bahrain reported an Iranian hit on an industrial facility as Qatar mediated.'),
    ('MIDDLE EAST', 'Aid truck strike kills 3 in Gaza', 'GAZA CITY',
     'Israel said it killed Islamic Jihad militants travelling in a food truck; World Central Kitchen denied the vehicle was its own. The ceasefire strains as 90% need aid.'),
    ('EUROPE', 'The war spills into the Baltic', 'GULF OF FINLAND',
     'A Ukrainian drone set the Russian cargo ship Sparta II on fire in international waters. Finland then detected a Russian helicopter in its airspace; two Russian missiles landed in Poland.'),
    ('MIDDLE EAST', 'Riyadh deflects Houthi missiles', 'SAUDI ARABIA',
     'Coalition air defences intercepted ballistic missiles aimed at the capital for a third consecutive night, with emergency alerts sounding across the city.'),
    ('GLOBAL', 'Killer-robot talks collapse', 'GENEVA',
     'UN consultations on autonomous weapons ended with no legally binding rules, as drone warfare rewrites the battlefield from Ukraine to Sudan.'),
    ('ASIA', 'Ontario picks Bains; AI shadow on Tumbler Ridge', 'TORONTO, CANADA',
     'Navdeep Bains won the Ontario Liberal leadership, the third contest in six years, as reporting surfaced that the Tumbler Ridge shooter sought AI help modifying weapons.'),
    ('GLOBAL', 'Bitcoin slides under $60,000', 'NEW YORK',
     'The crypto fell below the level for the first time since July as valuation worries hit the AI trade and other risk assets. Storm-battered Rio Grande do Sul counted 5 dead.'),
]

DR = ImageDraw.Draw(Image.new('RGB', (10, 10)))

def wrap(text, f, maxw):
    lines, line = [], ''
    for wd in text.split():
        t = (line + ' ' + wd).strip()
        if DR.textlength(t, font=f) > maxw and line:
            lines.append(line); line = wd
        else:
            line = t
    if line:
        lines.append(line)
    return lines

def draw_board():
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 5], fill=GOLD)
    d.text((44, 20), 'WORLD IN BRIEF', font=F_TITLE, fill=INK)
    d.text((46, 78), 'SATURDAY 21 NOVEMBER 2026', font=F_DATE, fill=GOLD)
    d.text((46, 107), 'one day, eight stories  ·  as reported by AP, Reuters, AFP, Guardian, NPR, CBS, Global News', font=F_TAG, fill=DIM)
    mx, gap = 44, 18
    cw = (W - 2 * mx - gap) // 2
    top, ch, vg = 140, 202, 12
    pad = 16
    inner = cw - 2 * pad
    for i, (region, ttl, place, body) in enumerate(STORIES):
        cx = mx + (i % 2) * (cw + gap)
        cy = top + (i // 2) * (ch + vg)
        d.rounded_rectangle([cx, cy, cx + cw, cy + ch], 9, fill=CARD)
        d.rectangle([cx, cy + 9, cx + 5, cy + ch - 9], fill=REGION[region])
        rx, ry = cx + pad, cy + 12
        rw = d.textlength(region, font=F_CHIP)
        d.rounded_rectangle([rx, ry, rx + rw + 16, ry + 21], 5, fill=REGION[region])
        d.text((rx + 8, ry + 3), region, font=F_CHIP, fill=(10, 12, 18))
        pw = d.textlength(place, font=F_PLACE)
        d.text((cx + cw - pad - pw, ry + 3), place, font=F_PLACE, fill=DIM)
        y = ry + 30
        for ln in wrap(ttl, F_HEAD, inner)[:2]:
            d.text((rx, y), ln, font=F_HEAD, fill=INK)
            y += 27
        y += 2
        for ln in wrap(body, F_BODY, inner):
            if y + 20 > cy + ch - 8:
                break
            d.text((rx, y), ln, font=F_BODY, fill=BODY)
            y += 21
    d.text((46, H - 30), "Built by an AI agent from that day's reporting  ·  make.fun news-image-20261121  ·  one image, text only", font=F_FOOT, fill=DIM)
    out = os.environ.get('OUT_DIR', '.')
    os.makedirs(out, exist_ok=True)
    img.save(os.path.join(out, 'entry.png'), optimize=True)

if __name__ == '__main__':
    draw_board()
