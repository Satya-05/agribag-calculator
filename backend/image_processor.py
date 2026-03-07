from ocr_engine import extract_values_from_image

def process_page(image_path):
    try:
        # Extract all values using Gemini Vision
        col1, col2, col3, col4 = extract_values_from_image(image_path)
        
        print(f"Col 1 values: {col1}")
        print(f"Col 2 values: {col2}")
        print(f"Col 3 values: {col3}")
        print(f"Col 4 values: {col4}")
        
        # Calculate column sums
        col1_sum = round(sum(col1), 2)
        col2_sum = round(sum(col2), 2)
        col3_sum = round(sum(col3), 2)
        col4_sum = round(sum(col4), 2)
        total = round(col1_sum + col2_sum + col3_sum + col4_sum, 2)
        
        # Build display grid (15 rows x 4 cols)
        display_grid = []
        for row in range(15):
            display_grid.append([
                col1[row],
                col2[row],
                col3[row],
                col4[row]
            ])
        
        print(f"Column Sums: {[col1_sum, col2_sum, col3_sum, col4_sum]}")
        print(f"Total: {total}")
        
        return {
            "success": True,
            "grid": display_grid,
            "column_sums": [col1_sum, col2_sum, col3_sum, col4_sum],
            "total": total,
            "cells_detected": 60
        }
    
    except Exception as e:
        print(f"Error processing page: {e}")
        return {
            "success": False,
            "error": str(e),
            "grid": [],
            "column_sums": [0, 0, 0, 0],
            "total": 0
        }