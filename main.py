"""make.fun entry: Sum up 25 November 2026's world news in one image.

A self-contained Python program (standard library only, no network) that
draws a one-page newspaper front page for Wednesday 25 November 2026 and
writes it as a PNG to the output directory. The picture is drawn pixel by
pixel with an embedded 5x7 bitmap font, so both grading runs produce
exactly the same bytes.

The day's stories, as first reported on 25 November 2026:
  * Tankers hit by explosions in the Strait of Hormuz (Tehran).
  * Houthi attack hits Riyadh's tallest skyscraper again, 11 injured;
    Saudi air defences destroy four drones over Ras Tanura.
  * Russia and Ukraine report 3 dead, 15 injured in overnight strikes
    on Kyiv, Kharkiv, Zaporizhzhia and Samara; Chancellor Merz says
    Europeans will show Russia its limits.
  * Israeli strike in Gaza City kills the Hamas security chief and his
    family; a storm threatens 1.76 million people sheltering in tents.
  * China's Shenzhou-24 launches with the first Pakistani astronaut,
    the first foreign astronaut aboard China's space station.
  * Australia signs a treaty with Solomon Islands, edging China out
    of a Pacific foothold.
Ticker: landmine casualties near 7,000 in 2025, a five-year high;
hostages freed in Cartagena, Colombia; Hanoi explosion kills six.
"""

import os
import struct
import zlib
from pathlib import Path

WIDTH = 1024
HEIGHT = 1024

PAPER = (247, 243, 233)
INK = (24, 28, 38)
NAVY = (18, 38, 74)
RED = (166, 32, 40)
GOLD = (198, 148, 42)
BODY = (52, 56, 66)
PANEL = (255, 253, 247)
LINE = (178, 170, 152)
CREAM = (250, 248, 240)
SUB = (205, 212, 226)

# A classic 5x7 bitmap font: seven rows of five pixels per glyph.
FONT = {
    "A": (".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "B": ("####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."),
    "C": (".###.", "#...#", "#....", "#....", "#....", "#...#", ".###."),
    "D": ("####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."),
    "E": ("#####", "#....", "#....", "####.", "#....", "#....", "#####"),
    "F": ("#####", "#....", "#....", "####.", "#....", "#....", "#...."),
    "G": (".###.", "#...#", "#....", "#.###", "#...#", "#...#", ".###."),
    "H": ("#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "I": (".###.", "..#..", "..#..", "..#..", "..#..", "..#..", ".###."),
    "J": ("..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."),
    "K": ("#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"),
    "L": ("#....", "#....", "#....", "#....", "#....", "#....", "#####"),
    "M": ("#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"),
    "N": ("#...#", "#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#"),
    "O": (".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "P": ("####.", "#...#", "#...#", "####.", "#....", "#....", "#...."),
    "Q": (".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"),
    "R": ("####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"),
    "S": (".####", "#....", "#....", ".###.", "....#", "....#", "####."),
    "T": ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."),
    "U": ("#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "V": ("#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."),
    "W": ("#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"),
    "X": ("#...#", ".#.#.", "..#..", "..#..", "..#..", ".#.#.", "#...#"),
    "Y": ("#...#", ".#.#.", ".#.#.", "..#..", "..#..", "..#..", "..#.."),
    "Z": ("#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"),
    "0": (".###.", "#...#", "#..##", "#.#.#", "##..#", "#...#", ".###."),
    "1": ("..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."),
    "2": (".###.", "#...#", "....#", "...#.", "..#..", ".#...", "#####"),
    "3": (".###.", "#...#", "....#", "..##.", "....#", "#...#", ".###."),
    "4": ("...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."),
    "5": ("#####", "#....", "####.", "....#", "....#", "#...#", ".###."),
    "6": (".###.", "#...#", "#....", "####.", "#...#", "#...#", ".###."),
    "7": ("#####", "....#", "...#.", "..#..", "..#..", "..#..", "..#.."),
    "8": (".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."),
    "9": (".###.", "#...#", "#...#", ".####", "....#", "#...#", ".###."),
    " ": (".....", ".....", ".....", ".....", ".....", ".....", "....."),
    ".": (".....", ".....", ".....", ".....", ".....", ".##..", ".##.."),
    ",": (".....", ".....", ".....", ".....", ".##..", ".##..", ".#..."),
    "'": ("..#..", "..#..", ".#...", ".....", ".....", ".....", "....."),
    "-": (".....", ".....", ".....", "#####", ".....", ".....", "....."),
    ":": (".....", ".##..", ".##..", ".....", ".##..", ".##..", "....."),
    ";": (".....", ".##..", ".##..", ".....", ".##..", ".##..", ".#..."),
    "!": ("..#..", "..#..", "..#..", "..#..", "..#..", ".....", "..#.."),
    "?": (".###.", "#...#", "....#", "..##.", "..#..", ".....", "..#.."),
    "(": ("...#.", "..#..", "..#..", "..#..", "..#..", "..#..", "...#."),
    ")": (".#...", "..#..", "..#..", "..#..", "..#..", "..#..", ".#..."),
}


class Canvas:
    """A tiny RGB pixel buffer with rectangle and bitmap-text drawing."""

    def __init__(self, width, height, colour):
        self.width = width
        self.height = height
        self.pixels = bytearray(bytes(colour) * width * height)

    def rect(self, x0, y0, x1, y1, colour):
        x0, y0 = max(0, x0), max(0, y0)
        x1, y1 = min(self.width, x1), min(self.height, y1)
        if x1 <= x0 or y1 <= y0:
            return
        row = bytes(colour) * (x1 - x0)
        for y in range(y0, y1):
            start = (y * self.width + x0) * 3
            self.pixels[start:start + len(row)] = row

    def outline(self, x0, y0, x1, y1, colour, width=2):
        self.rect(x0, y0, x1, y0 + width, colour)
        self.rect(x0, y1 - width, x1, y1, colour)
        self.rect(x0, y0, x0 + width, y1, colour)
        self.rect(x1 - width, y0, x1, y1, colour)

    def text(self, x, y, string, scale, colour, bold=False):
        cursor = x
        for ch in string.upper():
            glyph = FONT.get(ch, FONT[" "])
            for row_i, row in enumerate(glyph):
                for col_i, mark in enumerate(row):
                    if mark == "#":
                        self.rect(cursor + col_i * scale, y + row_i * scale,
                                  cursor + (col_i + 1) * scale,
                                  y + (row_i + 1) * scale, colour)
                        if bold:
                            self.rect(cursor + col_i * scale + scale // 2,
                                      y + row_i * scale,
                                      cursor + (col_i + 1) * scale + scale // 2,
                                      y + (row_i + 1) * scale, colour)
            cursor += 6 * scale
        return cursor

    def text_width(self, string, scale):
        return len(string) * 6 * scale - scale

    def wrap(self, string, scale, max_width):
        words, lines, current = string.split(), [], ""
        for word in words:
            trial = f"{current} {word}".strip()
            if self.text_width(trial, scale) <= max_width:
                current = trial
            else:
                lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines


def png_bytes(canvas):
    """Encode the canvas as a PNG using only zlib and struct."""
    raw = bytearray()
    stride = canvas.width * 3
    for y in range(canvas.height):
        raw.append(0)
        start = y * stride
        raw.extend(canvas.pixels[start:start + stride])

    def chunk(kind, data):
        return (struct.pack(">I", len(data)) + kind + data
                + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF))

    header = struct.pack(">IIBBBBB", canvas.width, canvas.height, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header)
            + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
            + chunk(b"IEND", b""))


STORIES = [
    ("MIDDLE EAST - HORMUZ",
     "TANKERS HIT BY BLASTS IN HORMUZ STRAIT",
     "TEHRAN SAYS TANKERS HIT BY EXPLOSIONS, RAISING FEARS FOR OIL SHIPPING.",
     RED),
    ("MIDDLE EAST - RIYADH",
     "HOUTHI HIT RIYADH TALLEST TOWER AGAIN",
     "11 INJURED IN RIYADH. SAUDI DEFENCES DOWN FOUR DRONES OVER RAS TANURA.",
     RED),
    ("EUROPE - UKRAINE WAR",
     "STRIKES KILL 3, INJURE 15 IN UKRAINE WAR",
     "KYIV, KHARKIV, ZAPORIZHZHIA, SAMARA HIT. MERZ: SHOW RUSSIA ITS LIMITS.",
     NAVY),
    ("GAZA",
     "GAZA CHIEF KILLED, STORM THREATENS TENTS",
     "ISRAELI STRIKE KILLS HAMAS CHIEF AND FAMILY. 1.76M IN TENTS AT RISK.",
     NAVY),
    ("SCIENCE - SPACE",
     "SHENZHOU-24: FIRST PAKISTANI ASTRONAUT",
     "PAKISTAN'S FIRST ASTRONAUT FLIES TO CHINA'S SPACE STATION ABOARD.",
     GOLD),
    ("PACIFIC",
     "AUSTRALIA SIGNS SOLOMON ISLANDS TREATY",
     "CANBERRA DEAL WITH HONIARA EDGES CHINA OUT OF A PACIFIC FOOTHOLD.",
     GOLD),
]

TICKER = ("LANDMINE TOLL NEAR 7,000 IN 2025, FIVE-YEAR HIGH - HOSTAGES FREED "
          "IN CARTAGENA - HANOI BLAST KILLS SIX")


def draw_front_page():
    page = Canvas(WIDTH, HEIGHT, PAPER)

    # Masthead.
    page.rect(0, 0, WIDTH, 150, NAVY)
    title = "THE WORLD IN ONE DAY"
    page.text((WIDTH - page.text_width(title, 8)) // 2, 14, title, 8, CREAM)
    date = "WEDNESDAY 25 NOVEMBER 2026"
    page.text((WIDTH - page.text_width(date, 5)) // 2, 78, date, 5, GOLD)
    sub = "THE DAY'S WORLD NEWS, SUMMED UP IN A SINGLE PICTURE"
    page.text((WIDTH - page.text_width(sub, 3)) // 2, 118, sub, 3, SUB)

    # Six story panels in two columns and three rows.
    top, panel_h, gap = 164, 240, 10
    for index, (kicker, headline, body, accent) in enumerate(STORIES):
        col, row = index % 2, index // 2
        x0 = 30 + col * (482 + gap)
        y0 = top + row * (panel_h + gap)
        x1, y1 = x0 + 482, y0 + panel_h
        page.rect(x0, y0, x1, y1, PANEL)
        page.outline(x0, y0, x1, y1, LINE, 2)
        page.rect(x0, y0, x0 + 10, y1, accent)
        page.text(x0 + 26, y0 + 14, kicker, 3, accent, bold=True)
        y = y0 + 46
        for line in page.wrap(headline, 3, x1 - x0 - 48):
            page.text(x0 + 26, y, line, 3, INK, bold=True)
            y += 30
        y += 8
        for line in page.wrap(body, 3, x1 - x0 - 48):
            page.text(x0 + 26, y, line, 3, BODY)
            y += 29

    # Ticker along the bottom.
    ticker_y = top + 3 * (panel_h + gap) + 6
    page.rect(0, ticker_y, WIDTH, HEIGHT, INK)
    page.text(34, ticker_y + 12, "ALSO TODAY", 3, GOLD)
    y = ticker_y + 44
    for line in page.wrap(TICKER, 3, WIDTH - 68):
        page.text(34, y, line, 3, CREAM)
        y += 29
    return page


def main():
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "entry.png").write_bytes(png_bytes(draw_front_page()))


if __name__ == "__main__":
    main()
