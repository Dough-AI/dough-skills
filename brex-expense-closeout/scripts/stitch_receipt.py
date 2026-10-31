#!/usr/bin/env python3
"""Turn a receipt PDF into one tall PNG that Drive's preview link serves whole.

Usage: stitch_receipt.py <input.pdf> <output.png> [--pages 1,2,5]
Renders each page, drops near-blank pages (the Google Doc conversion of an
email leaves many), trims white margins, and stacks what is left. --pages keeps
only the listed pages (1-based), before blank-page removal.

Drive's thumbnail link caps the long side at 16000 px, so the image is scaled
to fit; a warning is printed if that makes it narrower than 800 px (text may
be hard to read - split the receipt into two images instead).

Needs: pip install pypdfium2 pillow
"""
import argparse
import sys

try:
    import pypdfium2 as pdfium
    from PIL import Image, ImageChops, ImageOps
except ImportError:
    print("error: needs pypdfium2 and pillow - run: python -m pip install --user pypdfium2 pillow")
    sys.exit(1)

MAX_SIDE = 16000
WIDTH = 1240          # A4 at 150 dpi
MIN_READABLE = 800
BLANK_INK = 0.0002    # under this share of non-white pixels a page is blank (one text line is ~0.0018)
DPI = 150


def render(page):
    return page.render(scale=DPI / 72).to_pil().convert("RGB")


def ink_box(img):
    gray = ImageOps.grayscale(img).point(lambda p: 255 if p > 240 else 0)
    inverted = ImageChops.invert(gray)
    bbox = inverted.getbbox()
    if not bbox:
        return None, 0.0
    ink = sum(1 for p in inverted.getdata() if p) / (img.width * img.height)
    return bbox, ink


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("png")
    ap.add_argument("--pages", help="comma-separated 1-based page numbers to keep")
    args = ap.parse_args()

    try:
        doc = pdfium.PdfDocument(args.pdf)
    except Exception as e:
        print(f"error: cannot open {args.pdf}: {e}")
        sys.exit(1)
    page_count = len(doc)
    wanted = range(1, page_count + 1)
    if args.pages:
        try:
            wanted = [int(p) for p in args.pages.split(",")]
        except ValueError:
            print("error: --pages takes comma-separated page numbers, e.g. 1,2,5")
            sys.exit(1)
        bad = [n for n in wanted if not 1 <= n <= page_count]
        if bad:
            print(f"error: no page {bad[0]} - the PDF has {page_count} pages")
            sys.exit(1)

    parts = []
    for n in wanted:
        img = render(doc[n - 1])
        bbox, ink = ink_box(img)
        if bbox is None or ink < BLANK_INK:
            print(f"page {n}: blank, dropped")
            continue
        # keep full width so columns line up; trim only top and bottom
        parts.append(img.crop((0, max(bbox[1] - 20, 0), img.width, min(bbox[3] + 20, img.height))))
        print(f"page {n}: kept")

    if not parts:
        print("error: every page is blank")
        sys.exit(1)

    parts = [p.resize((WIDTH, round(p.height * WIDTH / p.width))) for p in parts]
    out = Image.new("RGB", (WIDTH, sum(p.height for p in parts)), "white")
    y = 0
    for p in parts:
        out.paste(p, (0, y))
        y += p.height

    if out.height > MAX_SIDE:
        scale = MAX_SIDE / out.height
        out = out.resize((round(out.width * scale), MAX_SIDE))
        if out.width < MIN_READABLE:
            print(f"warning: scaled to {out.width} px wide to fit 16000 px; split into two images")

    out.save(args.png, optimize=True)
    print(f"wrote {args.png} ({out.width}x{out.height}, {len(parts)} pages)")


if __name__ == "__main__":
    main()
