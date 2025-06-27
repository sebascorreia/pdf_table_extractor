import pdfplumber
import numpy as np
import matplotlib.pyplot as plt
PDF_PATH = "data\PE1_4DP.pdf"
box1 = (38.67, 510.32,1188.7,1697.8)
boxelse = (44.02, 432.77, 1188.7, 1703.15)
columns = [175.07,766.13,846.36,926.6,982.76,1092.42]
finalboxes = [
    (49.37, 1521.28,496.01,1638.96),
    (768.8, 1523.96,1178.0,1638.96)
]
finalcolumns = [148.32, 274.02, 405.07, 985.44]
scale = 72/150

def scale_box(box):
    return tuple(round(x * scale, 2) for x in box)

def scale_list(lst):
    return [round(x * scale, 2) for x in lst]
with pdfplumber.open(PDF_PATH) as pdf:
    for i, page in enumerate(pdf.pages):
        if i ==0:
            bbox = box1
        else:
            bbox= boxelse
        im = page.to_image(resolution=72)
        bbox = scale_box(bbox)
        fig, ax = plt.subplots()
        ax.imshow(im.original)
        ax.set_title(f"Page {i + 1} — bbox + column check")
        plt.gca().invert_yaxis()

        # Draw bounding box
        x0, top, x1, bottom = bbox
        width = x1 - x0
        height = bottom - top
        rect = plt.Rectangle((x0, top), width, height,
                                linewidth=2, edgecolor='red', facecolor='none')
        ax.add_patch(rect)


        # Draw columns
        for x in scale_list(columns):
            ax.axvline(x=x, color='blue', linestyle='--', linewidth=1)
            ax.text(x, top - 10, f"{x:.1f}", rotation=90, fontsize=6, color='blue')
        
        if i == len(pdf.pages) -1:
            for box in finalboxes:
                box = scale_box(box)
                x0, top, x1, bottom = box
                width = x1 - x0
                height = bottom - top
                rect = plt.Rectangle((x0, top), width, height,
                                linewidth=2, edgecolor='red', facecolor='none')
                ax.add_patch(rect)
            for x in scale_list(finalcolumns):
                ax.axvline(x=x, color='green', linestyle='--', linewidth=1)
                ax.text(x, top - 10, f"{x:.1f}", rotation=90, fontsize=6, color='blue')
        
        plt.show()
