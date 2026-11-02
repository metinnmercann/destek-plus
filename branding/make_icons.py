#!/usr/bin/env python3
"""Destek+ ikonlarını üretir. Çalıştır: python3 branding/make_icons.py (repo kökünden)."""
from PIL import Image, ImageDraw

C1, C2 = (16, 185, 129), (13, 110, 253)  # yeşil -> mavi


def glyph(d, s, color, w):
    # monitör çerçevesi + ayak + ortada "+"
    m = s * 0.20
    top, bot = s * 0.24, s * 0.66
    d.rounded_rectangle([m, top, s - m, bot], radius=s * 0.06, outline=color, width=w)
    d.rectangle([s * 0.46, bot, s * 0.54, s * 0.75], fill=color)
    d.rounded_rectangle([s * 0.34, s * 0.74, s * 0.66, s * 0.79], radius=s * 0.02, fill=color)
    cx, cy, a, t = s / 2, (top + bot) / 2, s * 0.11, w * 0.55
    d.rounded_rectangle([cx - a, cy - t, cx + a, cy + t], radius=t * 0.6, fill=color)
    d.rounded_rectangle([cx - t, cy - a, cx + t, cy + a], radius=t * 0.6, fill=color)


def app_icon(size=1024, pad=0.0):
    S = size * 4
    grad = Image.new("RGBA", (S, S))
    gd = ImageDraw.Draw(grad)
    for i in range(S):
        k = i / (S - 1)
        gd.line([(0, i), (S, i)], fill=tuple(int(C1[j] + (C2[j] - C1[j]) * k) for j in range(3)) + (255,))
    mask = Image.new("L", (S, S), 0)
    p = S * pad
    ImageDraw.Draw(mask).rounded_rectangle([p, p, S - p, S - p], radius=(S - 2 * p) * 0.22, fill=255)
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    img.paste(grad, (0, 0), mask)
    g = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    inner = int(S - 2 * p)
    gl = Image.new("RGBA", (inner, inner), (0, 0, 0, 0))
    glyph(ImageDraw.Draw(gl), inner, (255, 255, 255, 255), int(inner * 0.055))
    g.paste(gl, (int(p), int(p)), gl)
    img = Image.alpha_composite(img, g)
    return img.resize((size, size), Image.LANCZOS)


def tray(size, color):
    S = size * 4
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    glyph(ImageDraw.Draw(img), S, color, int(S * 0.09))
    return img.resize((size, size), Image.LANCZOS)


# Ana ikon: branding/icon.svg'den 1024px olarak çizilmiş branding/icon-master.png
big = Image.open("branding/icon-master.png").convert("RGBA").resize((1024, 1024), Image.LANCZOS)
mac = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))  # macOS ikonları kenar boşluklu
mac.paste(big.resize((824, 824), Image.LANCZOS), (100, 100))
big.save("res/icon.png")
mac.save("res/mac-icon.png")
for n, s in [("32x32", 32), ("64x64", 64), ("128x128", 128), ("128x128@2x", 256)]:
    big.resize((s, s), Image.LANCZOS).save(f"res/{n}.png")
big.save("res/icon.ico", sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
big.save("flutter/windows/runner/resources/app_icon.ico", sizes=[(16, 16), (32, 32), (48, 48), (256, 256)])
big.save("res/tray-icon.ico", sizes=[(16, 16), (32, 32)])
mac.save("flutter/macos/Runner/AppIcon.icns")
tray(60, (255, 255, 255, 255)).save("res/mac-tray-dark-x2.png")
tray(48, (0, 0, 0, 255)).save("res/mac-tray-light-x2.png")
big.resize((512, 512), Image.LANCZOS).save("flutter/assets/icon.png") if __import__("os").path.exists("flutter/assets/icon.png") else None

SVG = open("branding/icon.svg").read()
for f in ["flutter/assets/icon.svg", "res/logo.svg", "res/scalable.svg"]:
    open(f, "w").write(SVG)
print("ok")
