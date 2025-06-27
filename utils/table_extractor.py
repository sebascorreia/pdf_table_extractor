import pdfplumber
import numpy as np
import csv
from utils.data_processing import clean_extracted_table
PDF_PATH = "output\cleaned.pdf"
scale = 72 / 150

# Define bounding boxes and columns (scaled to PDF space)
box1 = tuple(round(x * scale, 2) for x in (38.67, 510.32, 1188.7, 1697.8))
boxelse = tuple(round(x * scale, 2) for x in (44.02, 432.77, 1188.7, 1703.15))
columns = [round(x * scale, 2) for x in [175.07, 766.13, 846.36, 926.6, 982.76, 1092.42]]

def group_words_by_rows(words, y_tolerance=3):
    rows = []
    for word in sorted(words, key=lambda w: w['top']):
        inserted = False
        for row in rows:
            if abs(row[0]['top'] - word['top']) < y_tolerance:
                row.append(word)
                inserted = True
                break
        if not inserted:
            rows.append([word])
    return rows

def assign_to_columns(row_words, column_edges):
    cells = [''] * (len(column_edges) + 1)
    for word in row_words:
        x = word['x0']
        for i, edge in enumerate(column_edges):
            if x < edge:
                cells[i] += word['text'] + ' '
                break
        else:
            cells[-1] += word['text'] + ' '
    return [cell.strip() for cell in cells]

all_rows = []

with pdfplumber.open(PDF_PATH) as pdf:
    for i, page in enumerate(pdf.pages):
        bbox = box1 if i == 0 else boxelse
        cropped = page.within_bbox(bbox)
        words = cropped.extract_words()

        rows = group_words_by_rows(words)
        for j,row_words in enumerate(rows):
            row = assign_to_columns(row_words, columns)
            if i == 0 and j== 0:
                all_rows.append(row)
            else:    
                row = [f'="{cell}"' if cell else '' for cell in row]
                all_rows.append(row)

# Write CSV
with open("output\extracted_table_manual.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(all_rows)

print("✅ Extracted and saved to extracted_table_manual.csv (with preserved Item Codes)")
clean_extracted_table("output\extracted_table_manual.csv", "output\clean_extracted_table.csv")
print("Cleaned")