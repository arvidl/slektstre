#!/usr/bin/env python3
"""
Script to combine all PDF files into a single book.
"""

import os
from pathlib import Path
import subprocess

def combine_pdfs():
    """Combine all PDF files into a single book."""
    
    # Check if pdftk is available
    try:
        subprocess.run(['pdftk', '--version'], capture_output=True, check=True)
        use_pdftk = True
    except (subprocess.CalledProcessError, FileNotFoundError):
        use_pdftk = False
        print("pdftk not found, trying with PyPDF2...")
    
    if use_pdftk:
        # Use pdftk to combine PDFs
        pdf_files = [
            "book_pdf/README.html",  # We'll convert this first
            "book_pdf/00_slektstraer_og_grafer.pdf",
            "book_pdf/01_introduksjon.pdf", 
            "book_pdf/02_bygg_tre_manuelt.pdf",
            "book_pdf/03_importer_data.pdf",
            "book_pdf/04_visualisering.pdf",
            "book_pdf/05_eksterne_databaser.pdf"
        ]
        
        # Convert HTML to PDF first
        subprocess.run(['wkhtmltopdf', 'book_pdf/README.html', 'book_pdf/README.pdf'], check=True)
        
        # Combine all PDFs
        cmd = ['pdftk'] + pdf_files + ['cat', 'output', 'book_pdf/Slektstre_med_NetworkX_Komplett_Bok.pdf']
        subprocess.run(cmd, check=True)
        
    else:
        # Use PyPDF2 as fallback
        try:
            import PyPDF2
        except ImportError:
            print("Installing PyPDF2...")
            subprocess.run(['pip', 'install', 'PyPDF2'], check=True)
            import PyPDF2
        
        # Check if README.pdf already exists
        if not os.path.exists('book_pdf/README.pdf'):
            print("README.pdf not found, skipping...")
            return
        
        # List of PDF files in order (with front matter)
        pdf_files = [
            "book_pdf/cover.pdf",
            "book_pdf/table_of_contents.pdf",
            "book_pdf/README.pdf",
            "book_pdf/00_slektstraer_og_grafer.pdf",
            "book_pdf/01_introduksjon.pdf", 
            "book_pdf/02_bygg_tre_manuelt.pdf",
            "book_pdf/03_importer_data.pdf",
            "book_pdf/04_visualisering.pdf",
            "book_pdf/05_eksterne_databaser.pdf",
            "book_pdf/index.pdf"
        ]
        
        # Create output PDF
        output_pdf = PyPDF2.PdfWriter()
        
        for pdf_file in pdf_files:
            if os.path.exists(pdf_file):
                with open(pdf_file, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        output_pdf.add_page(page)
                print(f"Added {pdf_file}")
            else:
                print(f"Warning: {pdf_file} not found")
        
        # Write combined PDF
        with open('book_pdf/Slektstre_med_NetworkX_Komplett_Bok.pdf', 'wb') as output_file:
            output_pdf.write(output_file)
        
        print("✅ Combined PDF created: book_pdf/Slektstre_med_NetworkX_Komplett_Bok.pdf")

if __name__ == "__main__":
    print("📚 Combining PDFs into a single book...")
    combine_pdfs()
    print("🎉 Book generation complete!")
