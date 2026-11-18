import os, struct, sys, zlib

W = 1024
H = 1024
PAPER = (250, 243, 228)
INK = (22, 20, 18)
RED = (178, 34, 28)
GREY = (110, 104, 92)
LIGHT = (228, 218, 196)
BLUE = (52, 84, 120)
GREEN = (46, 110, 62)
GOLD = (176, 132, 32)

buf = bytearray(PAPER[0] for _ in range(W * H * 3))
for i in range(W * H):
    buf[i * 3] = PAPER[0]
    buf[i * 3 + 1] = PAPER[1]
    buf[i * 3 + 2] = PAPER[2]


def px(x, y, c):
    if 0 <= x < W and 0 <= y < H:
        o = (y * W + x) * 3
        buf[o] = c[0]
        buf[o + 1] = c[1]
        buf[o + 2] = c[2]


def rect(x, y, w, h, c):
    for yy in range(y, y + h):
        for xx in range(x, x + w):
            px(xx, yy, c)


def hline(x, y, w, c, t=1):
    rect(x, y, w, t, c)


def vline(x, y, h, c, t=1):
    rect(x, y, t, h, c)


def border(x, y, w, h, c, t=1):
    hline(x, y, w, c, t)
    hline(x, y + h - t, w, c, t)
    vline(x, y, h, c, t)
    vline(x + w - t, y, h, c, t)


def disc(cx, cy, r, c):
    for yy in range(cy - r, cy + r + 1):
        for xx in range(cx - r, cx + r + 1):
            if (xx - cx) * (xx - cx) + (yy - cy) * (yy - cy) <= r * r:
                px(xx, yy, c)


def circle(cx, cy, r, c):
    for a in range(360):
        import math
        xx = int(cx + r * math.cos(a * 3.14159265 / 180.0))
        yy = int(cy + r * math.sin(a * 3.14159265 / 180.0))
        px(xx, yy, c)
        px(xx + 1, yy, c)


def poly(points, c):
    ys = [p[1] for p in points]
    for yy in range(min(ys), max(ys) + 1):
        xs = []
        n = len(points)
        for i in range(n):
            x1, y1 = points[i]
            x2, y2 = points[(i + 1) % n]
            if (y1 <= yy < y2) or (y2 <= yy < y1):
                xs.append(x1 + (yy - y1) * (x2 - x1) / (y2 - y1))
        xs.sort()
        for k in range(0, len(xs) - 1, 2):
            for xx in range(int(xs[k]), int(xs[k + 1]) + 1):
                px(xx, yy, c)


def tri(x1, y1, x2, y2, x3, y3, c):
    poly([(x1, y1), (x2, y2), (x3, y3)], c)


# 5x7 bitmap font, each glyph is 7 rows of 5 bits as strings.
F = {}
def _g(ch, rows):
    F[ch] = rows
_g('A', ['01110','10001','10001','11111','10001','10001','10001'])
_g('B', ['11110','10001','10001','11110','10001','10001','11110'])
_g('C', ['01110','10001','10000','10000','10000','10001','01110'])
_g('D', ['11110','10001','10001','10001','10001','10001','11110'])
_g('E', ['11111','10000','10000','11110','10000','10000','11111'])
_g('F', ['11111','10000','10000','11110','10000','10000','10000'])
_g('G', ['01110','10001','10000','10111','10001','10001','01111'])
_g('H', ['10001','10001','10001','11111','10001','10001','10001'])
_g('I', ['01110','00100','00100','00100','00100','00100','01110'])
_g('J', ['00111','00010','00010','00010','00010','10010','01100'])
_g('K', ['10001','10010','10100','11000','10100','10010','10001'])
_g('L', ['10000','10000','10000','10000','10000','10000','11111'])
_g('M', ['10001','11011','10101','10101','10001','10001','10001'])
_g('N', ['10001','11001','10101','10011','10001','10001','10001'])
_g('O', ['01110','10001','10001','10001','10001','10001','01110'])
_g('P', ['11110','10001','10001','11110','10000','10000','10000'])
_g('Q', ['01110','10001','10001','10001','10101','10010','01101'])
_g('R', ['11110','10001','10001','11110','10100','10010','10001'])
_g('S', ['01111','10000','10000','01110','00001','00001','11110'])
_g('T', ['11111','00100','00100','00100','00100','00100','00100'])
_g('U', ['10001','10001','10001','10001','10001','10001','01110'])
_g('V', ['10001','10001','10001','10001','10001','01010','00100'])
_g('W', ['10001','10001','10001','10101','10101','10101','01010'])
_g('X', ['10001','10001','01010','00100','01010','10001','10001'])
_g('Y', ['10001','10001','01010','00100','00100','00100','00100'])
_g('Z', ['11111','00001','00010','00100','01000','10000','11111'])
_g('a', ['00000','00000','01110','00001','01111','10001','01111'])
_g('b', ['10000','10000','10110','11001','10001','10001','11110'])
_g('c', ['00000','00000','01110','10000','10000','10001','01110'])
_g('d', ['00001','00001','01101','10011','10001','10001','01111'])
_g('e', ['00000','00000','01110','10001','11111','10000','01110'])
_g('f', ['00110','01001','01000','11110','01000','01000','01000'])
_g('g', ['00000','01111','10001','10001','01111','00001','01110'])
_g('h', ['10000','10000','10110','11001','10001','10001','10001'])
_g('i', ['00100','00000','01100','00100','00100','00100','01110'])
_g('j', ['00010','00000','00110','00010','00010','10010','01100'])
_g('k', ['10000','10000','10010','10100','11000','10100','10010'])
_g('l', ['01100','00100','00100','00100','00100','00100','01110'])
_g('m', ['00000','00000','11010','10101','10101','10101','10101'])
_g('n', ['00000','00000','10110','11001','10001','10001','10001'])
_g('o', ['00000','00000','01110','10001','10001','10001','01110'])
_g('p', ['00000','00000','10110','11001','10001','11110','10000'])
_g('q', ['00000','00000','01101','10011','10001','01111','00001'])
_g('r', ['00000','00000','10110','11001','10000','10000','10000'])
_g('s', ['00000','00000','01111','10000','01110','00001','11110'])
_g('t', ['01000','01000','11110','01000','01000','01001','00110'])
_g('u', ['00000','00000','10001','10001','10001','10011','01101'])
_g('v', ['00000','00000','10001','10001','10001','01010','00100'])
_g('w', ['00000','00000','10001','10101','10101','10101','01010'])
_g('x', ['00000','00000','10001','01010','00100','01010','10001'])
_g('y', ['00000','00000','10001','10001','01111','00001','01110'])
_g('z', ['00000','00000','11111','00010','00100','01000','11111'])
_g('0', ['01110','10001','10011','10101','11001','10001','01110'])
_g('1', ['00100','01100','00100','00100','00100','00100','01110'])
_g('2', ['01110','10001','00001','00110','01000','10000','11111'])
_g('3', ['11111','00010','00100','00010','00001','10001','01110'])
_g('4', ['00010','00110','01010','10010','11111','00010','00010'])
_g('5', ['11111','10000','11110','00001','00001','10001','01110'])
_g('6', ['00110','01000','10000','11110','10001','10001','01110'])
_g('7', ['11111','00001','00010','00100','01000','01000','01000'])
_g('8', ['01110','10001','10001','01110','10001','10001','01110'])
_g('9', ['01110','10001','10001','01111','00001','00010','01100'])
_g(' ', ['00000','00000','00000','00000','00000','00000','00000'])
_g('.', ['00000','00000','00000','00000','00000','01100','01100'])
_g(',', ['00000','00000','00000','00000','01100','00100','01000'])
_g("'", ['00100','00100','01000','00000','00000','00000','00000'])
_g('-', ['00000','00000','00000','01110','00000','00000','00000'])
_g(':', ['00000','01100','01100','00000','01100','01100','00000'])
_g(';', ['00000','01100','01100','00000','01100','00100','01000'])
_g('&', ['01100','10010','10100','01000','10101','10010','01101'])
_g('(', ['00010','00100','01000','01000','01000','00100','00010'])
_g(')', ['01000','00100','00010','00010','00010','00100','01000'])
_g('!', ['00100','00100','00100','00100','00100','00000','00100'])
_g('?', ['01110','10001','00001','00110','00100','00000','00100'])
_g('%', ['11001','11010','00010','00100','01000','01011','10011'])
_g('$', ['00100','01111','10100','01110','00101','11110','00100'])
_g('/', ['00001','00010','00010','00100','01000','01000','10000'])
_g('+', ['00000','00100','00100','11111','00100','00100','00000'])
_g('=', ['00000','00000','11111','00000','11111','00000','00000'])
_g('"', ['01010','01010','00000','00000','00000','00000','00000'])
_g('#', ['01010','01010','11111','01010','11111','01010','01010'])
_g('*', ['00000','10101','01110','11111','01110','10101','00000'])
_g('_', ['00000','00000','00000','00000','00000','00000','11111'])
_g('<', ['00010','00100','01000','10000','01000','00100','00010'])
_g('>', ['01000','00100','00010','00001','00010','00100','01000'])


def text_w(s, sc):
    return len(s) * 6 * sc


def draw_text(x, y, s, c, sc=1):
    cx = x
    for ch in s:
        g = F.get(ch)
        if g is None:
            g = F[' ']
        for r in range(7):
            row = g[r]
            for cc in range(5):
                if row[cc] == '1':
                    rect(cx + cc * sc, y + r * sc, sc, sc, c)
        cx += 6 * sc
    return cx


def text_cx(cx, y, s, c, sc=1):
    draw_text(cx - text_w(s, sc) // 2, y, s, c, sc)


def wrap(s, maxw, sc):
    words = s.split(' ')
    lines = []
    cur = ''
    for wd in words:
        t = wd if not cur else cur + ' ' + wd
        if text_w(t, sc) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def chunk_png():
    raw = bytearray()
    for y in range(H):
        raw.append(0)
        raw.extend(buf[y * W * 3:(y + 1) * W * 3])
    comp = zlib.compress(bytes(raw), 6)

    def chunk(typ, data):
        out = struct.pack('>I', len(data)) + typ + data
        out += struct.pack('>I', zlib.crc32(typ + data) & 0xffffffff)
        return out
    ihdr = struct.pack('>IIBBBBB', W, H, 8, 2, 0, 0, 0)
    return (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', ihdr)
            + chunk(b'IDAT', comp) + chunk(b'IEND', b''))


STORIES = [
    ("MIDDLE EAST", "ME", [
        "US jets hit Qeshm island as Hormuz standoff escalates",
        "Fourth tanker struck by a mine in the Strait of Hormuz",
        "Oman rescues 24 sailors from a stricken tanker crew",
        "Iran fires drones at US targets in Bahrain",
        "Houthis launch drones at a Saudi oil pipeline",
        "Riyadh names a new anti-Houthi coalition commander",
        "West presses Israel to open Gaza crossings",
        "Winter rain floods Gaza shelters, UN warns",
        "Israeli jets strike southern Lebanon",
        "Settler kills Palestinian woman near Jericho",
        "Houthis advance as Yemeni army pulls back",
        "Dubai airport traffic falls 28.1 percent",
        "93,000 tents sent to Gaza as winter bites",
        "8,600 aid trucks enter Gaza",
    ]),
    ("EUROPE", "EU", [
        "Ukraine hits the Kerch bridge again",
        "Russia strikes a bridge in Kyiv",
        "Russian missile cuts heat and water in Kyiv",
        "Zaporizhzhia attack kills 26 people",
        "Russia says it downed 300-plus drones",
        "Depardieu pleads guilty in court",
        "Germany thrash Netherlands 5-0",
        "Britain sanctions eight companies",
    ]),
    ("ASIA-PACIFIC", "AP", [
        "Trump, Xi and Putin meet in Shenzhen",
        "Putin arrives in Shenzhen for summit",
        "Xi urges free trade at the summit",
        "Modi joins the ASEAN-India summit",
        "Quad unveils a minerals pact",
        "Japan scrambles jets over intrusions",
        "India face Pakistan in U19 Asia Cup final",
        "Pakistan cuts petrol prices",
        "Eco summit adopts Vision 2035",
        "US loses its measles-free status",
        "Apple sign-in and App Store hit by outage",
        "Rocket failure destroys Amazon satellites",
        "Rosary thrown at Pope Leo",
    ]),
    ("AMERICAS", "AM", [
        "US tightens AI chip export rules",
        "Trump weighs CNN dirty bomb report",
        "Wall Street falls sharply",
        "Tech shares slide on Wall Street",
        "Nvidia in focus as markets wobble",
    ]),
    ("AFRICA", "AF", [
        "Ebola in Congo out of control, 5,505 dead",
        "Seventeen die in two South Africa shootings",
        "Guinea arrests 1,200 in gold mine raids",
    ]),
    ("OCEANIA", "OC", [
        "Australia sanctions Israeli settlers",
        "Qantas flight diverted mid-journey",
        "New Zealand lists 98 visa-free nations",
        "Pacific Forum tests maritime security plan",
    ]),
    ("CLIMATE", "CL", [
        "COP31 draft calls for faster fossil fuel exit",
    ]),
]

PICS = [
    "Tanker mine blast", "Drones over Bahrain", "Kerch bridge hit",
    "Germany 5-0 win", "Rocket failure", "AI chip curbs",
    "Ebola in Congo", "Qantas diverted", "COP31 draft",
    "Asia Cup final", "Depardieu guilty", "Bitcoin under $65k",
]


def draw_icon(i, x, y, w, h):
    cx = x + w // 2
    cy = y + h // 2
    rect(x, y, w, h, (238, 231, 210))
    border(x, y, w, h, INK, 1)
    if i == 0:  # tanker
        rect(cx - 45, cy - 5, 90, 16, INK)
        rect(cx - 30, cy - 20, 30, 15, INK)
        rect(cx + 5, cy - 28, 8, 8, RED)
        for k in range(4):
            hline(cx - 50 + k * 26, cy + 22, 18, BLUE, 2)
        tri(cx + 30, cy - 34, cx + 44, cy - 20, cx + 30, cy - 12, GOLD)
    elif i == 1:  # drone
        rect(cx - 22, cy - 6, 44, 12, INK)
        disc(cx - 26, cy - 10, 7, GREY)
        disc(cx + 26, cy - 10, 7, GREY)
        disc(cx - 26, cy + 10, 7, GREY)
        disc(cx + 26, cy + 10, 7, GREY)
        disc(cx, cy, 4, RED)
    elif i == 2:  # bridge
        hline(cx - 48, cy - 8, 96, INK, 4)
        vline(cx - 48, cy - 8, 26, INK, 3)
        vline(cx + 45, cy - 8, 26, INK, 3)
        for k in range(5):
            vline(cx - 32 + k * 16, cy - 8, 14, GREY, 2)
        tri(cx - 20, cy + 18, cx, cy + 2, cx + 20, cy + 18, BLUE)
    elif i == 3:  # football
        disc(cx, cy, 24, (255, 255, 255))
        circle(cx, cy, 24, INK)
        poly([(cx, cy - 9), (cx + 9, cy - 3), (cx + 6, cy + 8), (cx - 6, cy + 8), (cx - 9, cy - 3)], INK)
    elif i == 4:  # rocket
        tri(cx - 14, cy - 30, cx, cy - 44, cx + 14, cy - 30, RED)
        rect(cx - 14, cy - 30, 28, 34, INK)
        disc(cx, cy - 12, 6, (255, 255, 255))
        tri(cx - 20, cy + 4, cx - 8, cy + 4, cx - 16, cy + 20, RED)
        tri(cx + 8, cy + 4, cx + 20, cy + 4, cx + 16, cy + 20, RED)
        tri(cx - 6, cy + 4, cx, cy + 26, cx + 6, cy + 4, GOLD)
    elif i == 5:  # chip
        rect(cx - 22, cy - 22, 44, 44, INK)
        rect(cx - 12, cy - 12, 24, 24, GOLD)
        for k in range(4):
            hline(cx - 32, cy - 14 + k * 10, 10, INK, 2)
            hline(cx + 22, cy - 14 + k * 10, 10, INK, 2)
            vline(cx - 14 + k * 10, cy - 32, 10, INK, 2)
            vline(cx - 14 + k * 10, cy + 22, 10, INK, 2)
    elif i == 6:  # virus
        disc(cx, cy, 18, RED)
        for a in range(0, 360, 45):
            import math
            dx = int(24 * math.cos(a * 3.14159 / 180))
            dy = int(24 * math.sin(a * 3.14159 / 180))
            disc(cx + dx, cy + dy, 4, RED)
        disc(cx - 6, cy - 5, 3, (255, 255, 255))
        disc(cx + 6, cy + 5, 3, (255, 255, 255))
    elif i == 7:  # plane
        tri(cx - 44, cy, cx + 10, cy - 12, cx + 10, cy + 4, INK)
        tri(cx + 10, cy - 12, cx + 44, cy - 2, cx + 10, cy + 4, INK)
        tri(cx - 6, cy + 4, cx + 6, cy + 4, cx, cy + 22, RED)
        tri(cx - 6, cy - 4, cx + 6, cy - 4, cx, cy - 20, INK)
    elif i == 8:  # leaf
        poly([(cx - 22, cy + 18), (cx - 18, cy - 18), (cx + 20, cy - 14), (cx + 22, cy + 16)], GREEN)
        vline(cx, cy - 16, 34, INK, 2)
        hline(cx - 40, cy + 24, 80, BLUE, 2)
    elif i == 9:  # cricket bat and ball
        rect(cx - 30, cy - 24, 10, 40, (150, 110, 60))
        rect(cx - 28, cy + 16, 6, 18, INK)
        disc(cx + 22, cy + 10, 12, RED)
        disc(cx + 22, cy + 10, 5, (255, 255, 255))
    elif i == 10:  # gavel
        rect(cx - 30, cy - 14, 44, 12, INK)
        rect(cx - 8, cy - 2, 8, 30, (150, 110, 60))
        hline(cx - 34, cy + 28, 68, INK, 3)
    else:  # coin
        disc(cx, cy - 2, 24, GOLD)
        circle(cx, cy - 2, 24, INK)
        draw_text(cx - 6, cy - 12, "$", INK, 2)


def main():
    rect(0, 0, W, H, PAPER)
    border(8, 8, W - 16, H - 16, INK, 2)
    # Masthead
    text_cx(512, 20, "THE WORLD TODAY", INK, 6)
    hline(20, 66, 984, INK, 3)
    text_cx(512, 74, "TUESDAY 17 NOVEMBER 2026  -  48 STORIES  -  SIX CONTINENTS - ONE FRONT PAGE", RED, 2)
    hline(20, 98, 984, INK, 1)
    # Lead story, left
    lx, lw = 20, 540
    draw_text(lx, 110, "LEAD STORY", RED, 2)
    hl = wrap("US STRIKES QESHM ISLAND AS HORMUZ STANDOFF ESCALATES", lw, 3)
    yy = 134
    for ln in hl:
        draw_text(lx, yy, ln, INK, 3)
        yy += 24
    deck = wrap("US jets hit Qeshm as the Hormuz standoff deepened. A fourth tanker was mined and Oman saved 24 sailors. Iran fired drones at US targets in Bahrain as 93,000 tents reached Gaza.", lw, 2)
    yy += 6
    for ln in deck:
        draw_text(lx, yy, ln, INK, 2)
        yy += 17
    draw_text(lx, yy + 4, "Markets slid as bitcoin fell below $65,000.", GREY, 1)
    # Map, right
    mx, mw = 572, 432
    draw_text(mx, 110, "WHERE THE NEWS HAPPENED", INK, 2)
    my, mh = 132, 128
    rect(mx, my, mw, mh, (214, 226, 232))
    border(mx, my, mw, mh, INK, 1)
    poly([(mx + 28, my + 22), (mx + 88, my + 16), (mx + 118, my + 32), (mx + 98, my + 58), (mx + 58, my + 62), (mx + 28, my + 46)], (190, 186, 160))
    poly([(mx + 108, my + 72), (mx + 138, my + 66), (mx + 148, my + 96), (mx + 128, my + 116), (mx + 112, my + 96)], (190, 186, 160))
    poly([(mx + 188, my + 16), (mx + 218, my + 12), (mx + 228, my + 32), (mx + 208, my + 42), (mx + 188, my + 36)], (190, 186, 160))
    poly([(mx + 198, my + 46), (mx + 238, my + 42), (mx + 252, my + 66), (mx + 238, my + 100), (mx + 212, my + 96), (mx + 198, my + 70)], (190, 186, 160))
    poly([(mx + 232, my + 12), (mx + 330, my + 8), (mx + 388, my + 22), (mx + 378, my + 56), (mx + 328, my + 72), (mx + 258, my + 56), (mx + 232, my + 36)], (190, 186, 160))
    poly([(mx + 328, my + 86), (mx + 368, my + 82), (mx + 378, my + 100), (mx + 348, my + 112), (mx + 324, my + 102)], (190, 186, 160))
    draw_text(mx + 30, my + 30, "N AMERICA", INK, 1)
    draw_text(mx + 188, my + 20, "EUROPE", INK, 1)
    draw_text(mx + 280, my + 30, "ASIA", INK, 1)
    draw_text(mx + 205, my + 66, "AFRICA", INK, 1)
    draw_text(mx + 330, my + 90, "OCEANIA", INK, 1)
    disc(mx + 300, my + 48, 5, RED)
    disc(mx + 214, my + 26, 4, RED)
    disc(mx + 222, my + 44, 4, RED)
    draw_text(mx, 266, "Red dots: Qeshm, Kyiv and Gaza - the day's flashpoints.", GREY, 1)
    hline(20, 292, 984, INK, 2)
    # Pictures
    draw_text(20, 302, "12 STORIES IN PICTURES", INK, 3)
    hline(20, 324, 984, INK, 1)
    pw, gap = 156, 10
    for r in range(2):
        for c in range(6):
            i = r * 6 + c
            x = 20 + c * (pw + gap)
            y = 332 + r * 76
            draw_icon(i, x, y, pw, 58)
            cap = PICS[i]
            draw_text(x + (pw - text_w(cap, 1)) // 2, y + 62, cap, INK, 1)
    hline(20, 486, 984, INK, 2)
    # Full list
    draw_text(20, 496, "ALL 48 STORIES - BY REGION", INK, 3)
    hline(20, 518, 984, INK, 1)
    # split: col1 first 24 stories, col2 rest
    flat = []
    for name, tag, items in STORIES:
        flat.append(("H", name, tag))
        for it in items:
            flat.append(("S", it, tag))
    col1 = flat[:27]
    col2 = flat[27:]
    n = 0
    for col, x0 in ((col1, 20), (col2, 520)):
        yy = 526
        for kind, txt, tag in col:
            if kind == "H":
                rect(x0, yy, 484, 15, LIGHT)
                draw_text(x0 + 4, yy + 4, txt, RED, 1)
                yy += 16
            else:
                n += 1
                draw_text(x0, yy + 4, "%02d" % n, INK, 1)
                draw_text(x0 + 20, yy + 4, tag, RED, 1)
                draw_text(x0 + 42, yy + 4, txt, INK, 1)
                yy += 16
    hline(20, 1006, 984, INK, 1)
    os.makedirs("/output", exist_ok=True)
    data = chunk_png()
    with open("/output/entry.png", "wb") as f:
        f.write(data)
    print("wrote /output/entry.png", len(data), "stories", n)


if __name__ == "__main__":
    main()
