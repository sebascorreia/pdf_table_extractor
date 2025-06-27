import pymupdf
from utils.font_loader import get_font_paths

input_pdf = "data\PE1_4DP.pdf"
output_pdf = "output\cleaned.pdf"

font_paths = get_font_paths()
doc = pymupdf.open(input_pdf)
new_doc = pymupdf.open()

def detect_style(flags: int, fontname: str) -> str:
    fontname = fontname.lower()
    bold = (flags & 2) or "bold" in fontname
    italic = (flags & 1) or any(x in fontname for x in ("italic", "oblique"))
    if bold and italic:
        return "bold_italic"
    elif bold:
        return "bold"
    elif italic:
        return "italic"
    return "regular"

def get_color(span):
    return pymupdf.sRGB_to_pdf(span["color"])

for page_num in range(len(doc)):
    old_page = doc[page_num]
    new_page = new_doc.new_page(width=old_page.rect.width, height=old_page.rect.height)

    blocks = old_page.get_text("dict")["blocks"]

    for block in blocks:
        if "lines" not in block:
            continue
        for line in block["lines"]:
            spans = line["spans"]
            if not spans:
                continue
            # Skip entire line if watermark
            if any(span["text"] == "Sales Invoice" for span in spans):
                continue
            # Sort spans left to right
            spans.sort(key=lambda s: s["bbox"][0])

            # Build entire line as single string
            full_text = " ".join([s["text"].strip() for s in spans if s["text"].strip()])
            if not full_text:
                continue

            # Use the first span as reference for font, size, position
            ref = spans[0]
            x, y = ref["origin"]
            size = ref["size"]
            rotation = ref.get("rotation", 0)
            style = detect_style(ref["flags"], ref["font"])
            color = get_color(ref)

            new_page.insert_text(
                (x, y),
                full_text,
                fontsize = max(size - 1.5, 1),
                fontfile=font_paths[style],
                rotate=rotation,
                color=color,
                
            )

new_doc.save(output_pdf)
print(f"✅ Cleaned PDF saved to: {output_pdf}")