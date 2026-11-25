#!/usr/bin/env python3
"""The World in One Image — Wednesday 25 November 2026.

Draws a one-page newspaper front page that sums up the day's world news
in a single 1024x1024 PNG. No network, no clock, no randomness: running
this file twice writes byte-identical output.

Six stories, chosen from wire reports of 25 November 2026:
  1. Two tankers hit by mines in the Strait of Hormuz
  2. Nvidia shares slide ~7% as lawmakers question Trump's role in
     bringing back CEO Jensen Huang
  3. COP31 climate talks collapse in Antalya
  4. Ukraine hits a Russian warship off Libya
  5. Pakistan's first astronaut reaches China's space station
  6. Huawei convicted in a US trade-secrets case

Layout: masthead, one wide lead panel, a row of three panels, a row of
two panels, and a footer strip. Every picture on the page is drawn here
with Pillow primitives — no external images.
"""

import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

PAGE = 1024
MARGIN = 30
PAPER = (246, 241, 227)      # warm newsprint
INK = (23, 19, 12)           # near-black
TEAL = (15, 76, 70)          # deep teal, lead panel
TEAL_DARK = (9, 52, 48)
TEAL_MID = (38, 110, 102)
SEA = (18, 92, 86)
RUST = (178, 58, 42)         # rust red, accents
GOLD = (201, 154, 46)        # ochre gold, kickers
CREAM = (253, 252, 247)      # paper white
SAND = (232, 222, 196)       # panel fill
SKY = (220, 232, 228)
SMOKE = (120, 116, 104)

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")


def serif_bold(size):
    return ImageFont.truetype(str(FONT_DIR / "DejaVuSerif-Bold.ttf"), size)


def serif(size):
    return ImageFont.truetype(str(FONT_DIR / "DejaVuSerif.ttf"), size)


def sans(size):
    return ImageFont.truetype(str(FONT_DIR / "DejaVuSans.ttf"), size)


def sans_bold(size):
    return ImageFont.truetype(str(FONT_DIR / "DejaVuSans-Bold.ttf"), size)


def wrap_lines(draw, text, font, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_wrapped(draw, x, y, text, font, max_width, fill, leading=None):
    """Draw wrapped text; returns the y just below the last line."""
    if leading is None:
        leading = int(font.size * 1.28)
    for line in wrap_lines(draw, text, font, max_width):
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def spaced(text):
    """Letterspace a short kicker for a masthead feel."""
    return " ".join(list(text.replace(" ", "  ")))


def starburst(draw, cx, cy, outer, inner, fill, points=10):
    """A jagged blast star centred on (cx, cy)."""
    import math

    verts = []
    for i in range(points * 2):
        angle = math.pi * i / points - math.pi / 2
        radius = outer if i % 2 == 0 else inner
        verts.append((cx + radius * math.cos(angle),
                      cy + radius * math.sin(angle)))
    draw.polygon(verts, fill=fill)


def paint_hormuz_scene(draw, x, y, w, h):
    """Night sea in the strait: two tankers, mine blasts, smoke."""
    draw.rectangle([x, y, x + w, y + h], fill=TEAL_DARK)
    # sky glow
    draw.rectangle([x, y, x + w, y + int(h * 0.42)], fill=(24, 68, 64))
    draw.ellipse([x + w - 70, y + 14, x + w - 26, y + 58],
                 fill=(233, 214, 150))
    # sea
    sea_top = y + int(h * 0.55)
    draw.rectangle([x, sea_top, x + w, y + h], fill=SEA)
    for k in range(4):
        wy = sea_top + 14 + k * 16
        draw.arc([x + 8, wy - 8, x + w - 8, wy + 8], start=200, end=340,
                 fill=TEAL_MID, width=3)
    # tanker one (left, larger)
    hx, hy, hw, hh = x + 16, sea_top - 26, 150, 30
    draw.rectangle([hx, hy, hx + hw, hy + hh], fill=(30, 28, 24))
    draw.rectangle([hx + 96, hy - 22, hx + 138, hy], fill=(245, 240, 224))
    draw.rectangle([hx + 20, hy - 30, hx + 34, hy], fill=RUST)
    draw.rectangle([hx + 4, hy + hh, hx + hw - 4, hy + hh + 6],
                   fill=(30, 28, 24))
    # tanker two (right, smaller, behind the blast)
    hx2, hy2, hw2, hh2 = x + w - 150, sea_top - 18, 118, 24
    draw.rectangle([hx2, hy2, hx2 + hw2, hy2 + hh2], fill=(44, 40, 34))
    draw.rectangle([hx2 + 76, hy2 - 16, hx2 + 106, hy2],
                   fill=(245, 240, 224))
    # blasts
    starburst(draw, x + 58, sea_top - 52, 34, 14, (232, 126, 38))
    starburst(draw, x + 58, sea_top - 52, 18, 8, (246, 196, 90))
    starburst(draw, x + w - 96, sea_top - 44, 26, 11, (232, 126, 38))
    starburst(draw, x + w - 96, sea_top - 44, 13, 6, (246, 196, 90))
    # drifting mines
    for mx, my in ((x + w - 46, sea_top + 34), (x + 150, sea_top + 44)):
        draw.ellipse([mx - 7, my - 7, mx + 7, my + 7], fill=(20, 18, 14))
        for dx, dy in ((-9, 0), (9, 0), (0, -9), (0, 9),
                       (-6, -6), (6, -6), (-6, 6), (6, 6)):
            draw.line([mx, my, mx + dx, my + dy], fill=(20, 18, 14),
                      width=2)
    # smoke puffs
    for sx, sy, sr in ((x + 52, sea_top - 78, 9),
                       (x + 72, sea_top - 92, 12),
                       (x + w - 104, sea_top - 70, 8)):
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=SMOKE)


def paint_falling_chart(draw, x, y, w, h):
    """A share-price line falling off a cliff, in rust."""
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    draw.line([x + 10, y + h - 12, x + w - 10, y + h - 12],
              fill=INK, width=2)
    draw.line([x + 10, y + 10, x + 10, y + h - 12], fill=INK, width=2)
    pts = [(x + 16, y + 22), (x + 44, y + 30), (x + 70, y + 26),
           (x + 96, y + 44), (x + 122, y + 52), (x + 150, y + 78),
           (x + 176, y + 88), (x + w - 16, y + h - 22)]
    draw.line(pts, fill=RUST, width=5, joint="curve")
    ex, ey = pts[-1]
    draw.polygon([(ex, ey), (ex - 12, ey - 2), (ex - 2, ey - 12)],
                 fill=RUST)
    draw.text((x + 16, y + 6), "-7%", font=sans_bold(20), fill=RUST)


def paint_cracked_globe(draw, x, y, w, h):
    """A globe split by a rust crack: talks that fell apart."""
    cx, cy, r = x + w // 2, y + h // 2, min(w, h) // 2 - 8
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(186, 214, 205),
                 outline=TEAL, width=3)
    draw.arc([cx - r, cy - r, cx + r, cy + r], start=300, end=60,
             fill=TEAL, width=2)
    draw.arc([cx - r // 2, cy - r, cx + r // 2, cy + r], start=90,
             end=270, fill=TEAL, width=2)
    draw.line([cx - r, cy, cx + r, cy], fill=TEAL, width=2)
    crack = [(cx - 6, cy - r + 4), (cx + 10, cy - r // 2),
             (cx - 12, cy - 4), (cx + 8, cy + r // 3),
             (cx - 4, cy + r - 6)]
    draw.line(crack, fill=RUST, width=4, joint="curve")
    draw.ellipse([cx - r - 4, cy - r - 4, cx - r + 10, cy - r + 10],
                 fill=RUST)
    draw.ellipse([cx - 10, cy + r - 10, cx + 4, cy + r + 4], fill=RUST)


def paint_warship(draw, x, y, w, h):
    """A grey warship under a blast, off the Libyan coast."""
    draw.rectangle([x, y, x + w, y + h], fill=(210, 220, 214))
    sea_top = y + int(h * 0.62)
    draw.rectangle([x, sea_top, x + w, y + h], fill=(96, 140, 150))
    draw.line([x + 8, sea_top + 10, x + w - 8, sea_top + 10],
              fill=(70, 110, 120), width=2)
    hx, hy = x + 22, sea_top - 24
    draw.polygon([(hx, hy + 22), (hx + 14, hy), (hx + w - 44, hy),
                  (hx + w - 22, hy + 22)], fill=(74, 78, 82))
    draw.rectangle([hx + 60, hy - 20, hx + 120, hy], fill=(90, 94, 98))
    draw.line([hx + 90, hy - 44, hx + 90, hy - 20], fill=(74, 78, 82),
              width=4)
    draw.line([hx + 90, hy - 44, hx + 116, hy - 36], fill=(74, 78, 82),
              width=3)
    starburst(draw, x + w - 52, hy - 30, 24, 10, (232, 126, 38))
    starburst(draw, x + w - 52, hy - 30, 12, 6, (246, 196, 90))


def paint_rocket(draw, x, y, w, h):
    """A rocket climbing past a ringed planet toward a station."""
    draw.rectangle([x, y, x + w, y + h], fill=(16, 24, 44))
    for sx, sy in ((x + 14, y + 16), (x + w - 20, y + 30),
                   (x + 30, y + h - 18), (x + w - 34, y + h - 26),
                   (x + w // 2, y + 12)):
        draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=CREAM)
    # ringed planet
    px, py, pr = x + 26, y + h - 34, 16
    draw.ellipse([px - pr, py - pr, px + pr, py + pr], fill=GOLD)
    draw.arc([px - pr - 10, py - 6, px + pr + 10, py + 6], start=195,
             end=345, fill=CREAM, width=3)
    # rocket body
    rx, ry = x + w // 2 - 14, y + 18
    draw.polygon([(rx, ry + 26), (rx + 14, ry), (rx + 28, ry + 26)],
                 fill=RUST)
    draw.rectangle([rx, ry + 26, rx + 28, ry + 66], fill=CREAM)
    draw.rectangle([rx + 8, ry + 40, rx + 20, ry + 52], fill=TEAL)
    draw.polygon([(rx - 8, ry + 66), (rx, ry + 48), (rx, ry + 66)],
                 fill=RUST)
    draw.polygon([(rx + 28, ry + 66), (rx + 28, ry + 48),
                  (rx + 36, ry + 66)], fill=RUST)
    starburst(draw, rx + 14, ry + 82, 14, 6, (246, 196, 90))
    starburst(draw, rx + 14, ry + 82, 7, 3, (232, 126, 38))


def paint_chip(draw, x, y, w, h):
    """A silicon chip under a judge's gavel: the verdict."""
    draw.rectangle([x, y, x + w, y + h], fill=SAND)
    cx, cy = x + w // 2 - 18, y + h // 2
    side = 74
    for k in range(4):
        px = cx - side // 2 + k * 24
        draw.line([px, cy - side // 2 - 12, px, cy - side // 2],
                  fill=INK, width=3)
        draw.line([px, cy + side // 2, px, cy + side // 2 + 12],
                  fill=INK, width=3)
        py = cy - side // 2 + k * 24
        draw.line([cx - side // 2 - 12, py, cx - side // 2, py],
                  fill=INK, width=3)
        draw.line([cx + side // 2, py, cx + side // 2 + 12, py],
                  fill=INK, width=3)
    draw.rectangle([cx - side // 2, cy - side // 2,
                    cx + side // 2, cy + side // 2],
                   fill=INK)
    draw.rectangle([cx - 18, cy - 18, cx + 18, cy + 18], fill=GOLD)
    draw.text((cx - 9, cy - 11), "AI", font=sans_bold(18), fill=INK)
    # gavel head, top right
    gx, gy = x + w - 58, y + 16
    draw.rounded_rectangle([gx, gy, gx + 44, gy + 16], radius=4,
                           fill=RUST)
    draw.line([gx + 22, gy + 16, gx + 34, gy + 44], fill=INK, width=5)


def draw_masthead(draw):
    """Kicker, date in big serif, and a double rule."""
    y = 26
    kick = spaced("THE WORLD IN ONE IMAGE")
    font_kick = sans_bold(19)
    kw = draw.textlength(kick, font=font_kick)
    draw.text(((PAGE - kw) / 2, y), kick, font=font_kick, fill=RUST)
    y += 30
    date_font = serif_bold(52)
    date = "Wednesday, 25 November 2026"
    dw = draw.textlength(date, font=date_font)
    draw.text(((PAGE - dw) / 2, y), date, font=date_font, fill=INK)
    y += 68
    draw.line([MARGIN, y, PAGE - MARGIN, y], fill=INK, width=3)
    draw.line([MARGIN, y + 6, PAGE - MARGIN, y + 6], fill=INK, width=1)
    return y + 16


def draw_lead(draw, y):
    """Full-width lead panel: Hormuz, dark teal, scene on the right."""
    h = 268
    draw.rounded_rectangle([MARGIN, y, PAGE - MARGIN, y + h], radius=12,
                           fill=TEAL)
    text_x = MARGIN + 26
    text_w = 520
    chip_y = y + 22
    draw.rounded_rectangle([text_x, chip_y, text_x + 208, chip_y + 28],
                           radius=14, fill=GOLD)
    draw.text((text_x + 14, chip_y + 5), "01 · MIDDLE EAST",
              font=sans_bold(16), fill=INK)
    hy = chip_y + 44
    hy = draw_wrapped(draw, text_x, hy, "MINES IN THE STRAIT OF HORMUZ",
                      serif_bold(40), text_w, CREAM, leading=46)
    hy += 8
    draw_wrapped(draw, text_x, hy,
                 "Two tankers are hit by mines in the Strait of Hormuz, "
                 "Iran's Revolutionary Guards say, as shipping and oil "
                 "markets brace for escalation.",
                 sans(19), text_w, (226, 236, 230), leading=26)
    paint_hormuz_scene(draw, MARGIN + 578, y + 18, 360, h - 36)
    return y + h + 14


def draw_triplet(draw, y, stories):
    """Three equal panels in a row; each has a picture, kicker,
    headline and two or three lines of body text."""
    h = 246
    gap = 12
    w = (PAGE - 2 * MARGIN - 2 * gap) // 3
    for i, story in enumerate(stories):
        x = MARGIN + i * (w + gap)
        draw.rounded_rectangle([x, y, x + w, y + h], radius=10,
                               fill=CREAM, outline=(198, 188, 164),
                               width=1)
        story["paint"](draw, x + 12, y + 12, w - 24, 84)
        ty = y + 108
        draw.text((x + 14, ty), story["kicker"], font=sans_bold(14),
                  fill=RUST)
        ty += 22
        ty = draw_wrapped(draw, x + 14, ty, story["headline"],
                          serif_bold(23), w - 28, INK, leading=27)
        draw_wrapped(draw, x + 14, ty + 4, story["body"], sans(15),
                     w - 28, (58, 52, 42), leading=20)
    return y + h + 14


def draw_pair(draw, y, stories):
    """Two wide panels; picture on the left, text on the right."""
    h = 218
    gap = 12
    w = (PAGE - 2 * MARGIN - gap) // 2
    for i, story in enumerate(stories):
        x = MARGIN + i * (w + gap)
        draw.rounded_rectangle([x, y, x + w, y + h], radius=10,
                               fill=CREAM, outline=(198, 188, 164),
                               width=1)
        story["paint"](draw, x + 14, y + 14, 150, h - 28)
        tx = x + 180
        tw = w - 196
        ty = y + 20
        draw.text((tx, ty), story["kicker"], font=sans_bold(14),
                  fill=RUST)
        ty += 24
        ty = draw_wrapped(draw, tx, ty, story["headline"],
                          serif_bold(25), tw, INK, leading=29)
        draw_wrapped(draw, tx, ty + 6, story["body"], sans(16), tw,
                     (58, 52, 42), leading=21)
    return y + h + 14


def draw_footer(draw, y):
    """Thin rule and one centred line naming the day again."""
    draw.line([MARGIN, y, PAGE - MARGIN, y], fill=INK, width=2)
    line = ("Six stories from Wednesday 25 November 2026  ·  "
            "Drawn from wire reports of the day")
    font = sans(15)
    lw = draw.textlength(line, font=font)
    draw.text(((PAGE - lw) / 2, y + 10), line, font=font,
              fill=(58, 52, 42))


def build_front_page():
    """Compose the whole page and return the image."""
    img = Image.new("RGB", (PAGE, PAGE), PAPER)
    draw = ImageDraw.Draw(img)
    y = draw_masthead(draw)
    y = draw_lead(draw, y)
    y = draw_triplet(draw, y, [
        {"kicker": "02 · MARKETS", "paint": paint_falling_chart,
         "headline": "NVIDIA SLIDES 7%",
         "body": "Shares fall as lawmakers question Trump's role in "
                 "restoring CEO Jensen Huang."},
        {"kicker": "03 · CLIMATE", "paint": paint_cracked_globe,
         "headline": "CLIMATE TALKS COLLAPSE",
         "body": "COP31 in Antalya ends without a deal as oil states "
                 "block any fossil-fuel phase-out."},
        {"kicker": "04 · WAR", "paint": paint_warship,
         "headline": "UKRAINE HITS SHIP OFF LIBYA",
         "body": "Kyiv strikes a Russian warship off Libya, widening "
                 "a war once fought in the Black Sea."},
    ])
    y = draw_pair(draw, y, [
        {"kicker": "05 · SPACE", "paint": paint_rocket,
         "headline": "PAKISTAN'S FIRST ASTRONAUT",
         "body": "Pakistan's first astronaut reaches China's space "
                 "station — a first for the country."},
        {"kicker": "06 · JUSTICE", "paint": paint_chip,
         "headline": "HUAWEI CONVICTED IN US COURT",
         "body": "Huawei is convicted in the US of stealing trade "
                 "secrets in a sanctions case."},
    ])
    draw_footer(draw, y)
    return img


def main():
    out = Path(os.environ.get("MAKEFUN_OUTPUT", "/output/entry.png"))
    out.parent.mkdir(parents=True, exist_ok=True)
    img = build_front_page()
    img.save(out, format="PNG")
    print(f"wrote {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
