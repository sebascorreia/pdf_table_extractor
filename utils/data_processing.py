import csv

def unwrap(row):
    return [cell[2:-1] if cell.startswith('="') and cell.endswith('"') else cell for cell in row]
def clean_extracted_table(input_csv, output_csv):
    cleaned_rows = []
    
    previous_row = None
    with open(input_csv, newline='', encoding="utf-8") as infile:
        
        reader = csv.reader(infile)
        
        for i, row in enumerate(reader):
            #Add header row
            if i==0:
                cleaned_rows.append(unwrap(row))
                continue
            if i ==1:
                previous_row= unwrap(row)
                continue
            #skip empty or accounted for rows
            if not any(cell.strip() for cell in row):
                continue
            # Remove wrapping ="" quotes
            unwrapped_row = unwrap(row)

            # Check all columns except the ones that can be null
            has_blank = False
            for indx, cell in enumerate(unwrapped_row):
                if not cell.strip() and indx !=4 :
                    has_blank = True
            if has_blank:
                # Merge into previous row
                for indx, cell in enumerate(unwrapped_row):
                    if cell.strip():
                        previous_row[indx]+= " " + cell
            else:
                cleaned_rows.append(previous_row)
                previous_row = unwrapped_row

    if previous_row:
        cleaned_rows.append(previous_row)

    # Rewrap all cells for Excel compatibility
    with open(output_csv, "w", newline='', encoding="utf-8") as outfile:
        writer = csv.writer(outfile)
        for row in cleaned_rows:
            safe_row = [f'="{cell.strip()}"' if cell.strip() else '' for cell in row]
            writer.writerow(safe_row)