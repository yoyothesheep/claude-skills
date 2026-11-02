#!/usr/bin/env python3
"""Pull the color palette out of a design, for the brand pass.

Usage:
  python3 extract_palette.py <page.html> [--top N]   colors from :root variables, else all CSS colors by use
  python3 extract_palette.py <screenshot.png> [--top N]   dominant colors from the pixels (needs Pillow)
  python3 extract_palette.py --contrast <fg> <bg>   WCAG contrast ratio (AA: 4.5 body, 3 large text)
"""
import re
import sys
from collections import Counter
from pathlib import Path

HEX = re.compile(r"#(?:[0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b")
RGB = re.compile(r"rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)")
VAR = re.compile(r"(--[\w-]+)\s*:\s*(#(?:[0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b|rgba?\([^)]*\))")


def to_hex(c):
    c = c.strip()
    m = RGB.match(c)
    if m:
        return "#%02x%02x%02x" % tuple(int(x) for x in m.groups())
    c = c.lower()
    return "#" + "".join(ch * 2 for ch in c[1:]) if len(c) == 4 else c


def luminance(hex_color):
    r, g, b = (int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5))
    lin = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in (r, g, b)]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def contrast(a, b):
    la, lb = sorted((luminance(to_hex(a)), luminance(to_hex(b))), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def from_html(path, top):
    css = path.read_text(errors="ignore")
    variables = {name: to_hex(val) for name, val in VAR.findall(css)}
    if variables:
        for name, val in variables.items():
            print(f"{val}  {name}")
        return
    counts = Counter(to_hex(c) for c in HEX.findall(css))
    counts.update(to_hex(m.group(0)) for m in RGB.finditer(css))
    for val, n in counts.most_common(top):
        print(f"{val}  used {n}x")


def from_image(path, top):
    from PIL import Image
    img = Image.open(path).convert("RGB")
    img.thumbnail((400, 400))
    pal = img.quantize(colors=top).convert("RGB")
    for n, rgb in sorted(pal.getcolors(), reverse=True):
        print("#%02x%02x%02x  %.0f%%" % (*rgb, 100 * n / (pal.width * pal.height)))


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    if args[0] == "--contrast" and len(args) == 3:
        ratio = contrast(args[1], args[2])
        verdict = "AA" if ratio >= 4.5 else "AA large only" if ratio >= 3 else "FAIL"
        print(f"{ratio:.2f}:1  {verdict}")
        return
    top = int(args[args.index("--top") + 1]) if "--top" in args else 12
    path = Path(args[0])
    (from_image if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"} else from_html)(path, top)


if __name__ == "__main__":
    main()
