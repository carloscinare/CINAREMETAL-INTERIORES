"""Prepare smaller display images from the approved originals, without cropping."""
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "imagens"
OUT.mkdir(exist_ok=True)
products = json.loads((ROOT / "produtos.json").read_text())
sources = [(p["id"], p["source"]) for p in products]
sources.append(("portao-metal-madeira", "portao-metal-madeira-77cf45df.png"))
manifest = {}
for ident, source in sources:
    path = ROOT / source
    digest = hashlib.sha256(path.read_bytes()).hexdigest()[:8]
    with Image.open(path) as original:
        image = ImageOps.exif_transpose(original).convert("RGBA")
        widths = sorted(set([w for w in (320, 640, 960, 1280) if w < image.width] + [image.width]))
        variants = []
        for width in widths:
            height = round(image.height * width / image.width)
            resized = image.resize((width, height), Image.Resampling.LANCZOS)
            name = f"{ident}-{digest}-{width}.webp"
            resized.save(OUT / name, "WEBP", quality=90, method=6)
            variants.append({"width": width, "height": height, "path": "imagens/" + name})
        width = min(image.width, 1200)
        social = image.resize((width, round(image.height * width / image.width)), Image.Resampling.LANCZOS)
        background = Image.new("RGB", social.size, "#f7f4ef")
        background.paste(social, mask=social.getchannel("A"))
        name = f"{ident}-{digest}-partilha.jpg"
        background.save(OUT / name, "JPEG", quality=90, optimize=True)
        manifest[ident] = {
            "source": source,
            "width": image.width,
            "height": image.height,
            "variants": variants,
            "social": {"path": "imagens/" + name, "width": background.width, "height": background.height},
        }
(OUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
print(f"Prepared responsive images for {len(manifest)} approved models and projects")
