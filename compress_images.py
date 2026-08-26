from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent / "static" / "img"


def compress() -> None:
    for png in ROOT.glob("*.png"):
        image = Image.open(png).convert("RGB")
        max_width = 1920 if "hero" in png.name or "terminada" in png.name else 1400
        if image.width > max_width:
            ratio = max_width / image.width
            image = image.resize((max_width, int(image.height * ratio)), Image.Resampling.LANCZOS)
        dest = png.with_suffix(".jpg")
        image.save(dest, "JPEG", quality=82, optimize=True, progressive=True)
        png.unlink()
        print(f"{dest.name}: {dest.stat().st_size // 1024} KB")


if __name__ == "__main__":
    compress()
