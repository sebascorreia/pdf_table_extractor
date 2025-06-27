import os
import urllib.request

FONT_DIR = "fonts"
os.makedirs(FONT_DIR, exist_ok=True)

FONT_VARIANTS = {
    "regular": {
        "file": os.path.join(FONT_DIR, "DejaVuSans.ttf"),
        "url": "https://raw.githubusercontent.com/senotrusov/dejavu-fonts-ttf/master/ttf/DejaVuSans.ttf",
    },
    "bold": {
        "file": os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf"),
        "url": "https://raw.githubusercontent.com/senotrusov/dejavu-fonts-ttf/master/ttf/DejaVuSans-Bold.ttf",
    },
    "italic": {
        "file": os.path.join(FONT_DIR, "DejaVuSans-Oblique.ttf"),
        "url": "https://raw.githubusercontent.com/openstreetmap/potlatch2/master/fonts/fonts/DejaVuSans-Oblique.ttf",
    },
    "bold_italic": {
        "file": os.path.join(FONT_DIR, "DejaVuSans-BoldOblique.ttf"),
        "url": "https://raw.githubusercontent.com/senotrusov/dejavu-fonts-ttf/master/ttf/DejaVuSans-BoldOblique.ttf",
    },
}

def ensure_fonts_downloaded():
    for variant in FONT_VARIANTS.values():
        if not os.path.exists(variant["file"]):
            print(f"Downloading {os.path.basename(variant['file'])}...")
            urllib.request.urlretrieve(variant["url"], variant["file"])

def get_font_paths():
    ensure_fonts_downloaded()
    return {key: variant["file"] for key, variant in FONT_VARIANTS.items()}