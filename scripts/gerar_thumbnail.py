"""
Monta thumbnail de gameplay a partir de:
  - um print marcante da gameplay (fundo)
  - uma foto normal sua (o fundo é removido automaticamente via rembg)
  - um texto curto de impacto (até ~3 palavras)

Gera dois arquivos: thumbnail-youtube.png (1280x720) e thumbnail-tiktok.png (1080x1920).

Uso:
  python gerar_thumbnail.py <print.jpg> <foto.jpg> "TEXTO AQUI" <pasta_saida>
"""

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

YOUTUBE_SIZE = (1280, 720)
TIKTOK_SIZE = (1080, 1920)

FONT_CANDIDATES = [
    "impact.ttf",
    "impactmt.ttf",
    r"C:\Windows\Fonts\impact.ttf",
    r"C:\Windows\Fonts\arialbd.ttf",
    "arialbd.ttf",
]


def load_font(size: int) -> ImageFont.FreeTypeFont:
    for name in FONT_CANDIDATES:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def remove_background(foto_path: Path) -> Image.Image:
    from rembg import remove

    with open(foto_path, "rb") as f:
        data = f.read()
    result = remove(data)
    from io import BytesIO

    return Image.open(BytesIO(result)).convert("RGBA")


def cover_crop(img: Image.Image, size) -> Image.Image:
    return ImageOps.fit(img, size, method=Image.LANCZOS, centering=(0.5, 0.4))


def draw_impact_text(canvas: Image.Image, text: str, center_xy, max_width: int, base_size: int):
    draw = ImageDraw.Draw(canvas)
    text = text.upper()
    size = base_size
    font = load_font(size)
    while draw.textlength(text, font=font) > max_width and size > 30:
        size -= 4
        font = load_font(size)

    x, y = center_xy
    stroke_w = max(4, size // 14)
    draw.text(
        (x, y), text, font=font, fill="white",
        stroke_width=stroke_w, stroke_fill="black", anchor="mm",
    )


def montar_youtube(print_img: Image.Image, foto_cutout: Image.Image, texto: str) -> Image.Image:
    canvas = cover_crop(print_img.convert("RGB"), YOUTUBE_SIZE).convert("RGBA")

    foto_h = int(YOUTUBE_SIZE[1] * 0.95)
    ratio = foto_h / foto_cutout.height
    foto_w = int(foto_cutout.width * ratio)
    foto_resized = foto_cutout.resize((foto_w, foto_h), Image.LANCZOS)

    pos_x = YOUTUBE_SIZE[0] - foto_w + int(foto_w * 0.08)
    pos_y = YOUTUBE_SIZE[1] - foto_h
    canvas.paste(foto_resized, (pos_x, pos_y), foto_resized)

    draw_impact_text(
        canvas, texto,
        center_xy=(YOUTUBE_SIZE[0] * 0.32, YOUTUBE_SIZE[1] * 0.22),
        max_width=YOUTUBE_SIZE[0] * 0.55,
        base_size=120,
    )
    return canvas.convert("RGB")


def montar_tiktok(print_img: Image.Image, foto_cutout: Image.Image, texto: str) -> Image.Image:
    canvas = cover_crop(print_img.convert("RGB"), TIKTOK_SIZE).convert("RGBA")

    foto_h = int(TIKTOK_SIZE[1] * 0.62)
    ratio = foto_h / foto_cutout.height
    foto_w = int(foto_cutout.width * ratio)
    foto_resized = foto_cutout.resize((foto_w, foto_h), Image.LANCZOS)

    pos_x = (TIKTOK_SIZE[0] - foto_w) // 2
    pos_y = TIKTOK_SIZE[1] - foto_h
    canvas.paste(foto_resized, (pos_x, pos_y), foto_resized)

    draw_impact_text(
        canvas, texto,
        center_xy=(TIKTOK_SIZE[0] * 0.5, TIKTOK_SIZE[1] * 0.18),
        max_width=TIKTOK_SIZE[0] * 0.85,
        base_size=110,
    )
    return canvas.convert("RGB")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("print_path", type=Path)
    parser.add_argument("foto_path", type=Path)
    parser.add_argument("texto")
    parser.add_argument("saida_dir", type=Path)
    args = parser.parse_args()

    for p in (args.print_path, args.foto_path):
        if not p.exists():
            sys.exit(f"Arquivo não encontrado: {p}")

    print("Removendo fundo da foto...")
    foto_cutout = remove_background(args.foto_path)

    print_img = Image.open(args.print_path)

    args.saida_dir.mkdir(parents=True, exist_ok=True)

    yt = montar_youtube(print_img, foto_cutout, args.texto)
    yt_path = args.saida_dir / "thumbnail-youtube.png"
    yt.save(yt_path, quality=95)

    tk = montar_tiktok(print_img, foto_cutout, args.texto)
    tk_path = args.saida_dir / "thumbnail-tiktok.png"
    tk.save(tk_path, quality=95)

    print(f"Pronto:\n  {yt_path}\n  {tk_path}")


if __name__ == "__main__":
    main()
