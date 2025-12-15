"""Extract schools from PDF"""
import pdfplumber
import re

pdf_path = "../LIST_OF_REACREDITTED_AND_NON_REACREDITED_TSS_AND_VTC__2024-2025.pdf"

try:
    with pdfplumber.open(pdf_path) as pdf:
        print(f"Total pages: {len(pdf.pages)}")
        
        for i, page in enumerate(pdf.pages[:5]):
            print(f"\n=== Page {i+1} ===")
            text = page.extract_text()
            if text:
                print(text[:1000])
            
            # Try extracting tables
            tables = page.extract_tables()
            if tables:
                print(f"\nFound {len(tables)} tables on page {i+1}")
                for j, table in enumerate(tables):
                    print(f"\nTable {j+1}:")
                    for row in table[:5]:
                        print(row)
except Exception as e:
    print(f"Error: {e}")
