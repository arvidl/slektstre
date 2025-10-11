#!/usr/bin/env python3
"""
Script for generating a complete PDF book from the slektstre repository.
This script combines README.md and all notebooks into a single PDF.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import jupyter_book
        import sphinx
        print("✅ Jupyter Book and Sphinx are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install with: pip install -r requirements-book.txt")
        return False

def create_front_matter():
    """Create front matter (cover, TOC, index)."""
    print("📄 Creating front matter...")
    
    try:
        result = subprocess.run([
            "python", "scripts/create_front_matter.py"
        ], check=True, capture_output=True, text=True)
        
        print("✅ Front matter created successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creating front matter: {e}")
        print(f"Error output: {e.stderr}")
        return False

def convert_notebooks():
    """Convert individual notebooks to PDF."""
    print("📓 Converting notebooks to PDF...")
    
    notebooks = [
        "README.md",
        "notebooks/00_slektstraer_og_grafer.ipynb",
        "notebooks/01_introduksjon.ipynb",
        "notebooks/02_bygg_tre_manuelt.ipynb",
        "notebooks/03_importer_data.ipynb",
        "notebooks/04_visualisering.ipynb",
        "notebooks/05_eksterne_databaser.ipynb"
    ]
    
    # Create book_pdf directory
    os.makedirs("book_pdf", exist_ok=True)
    
    success = True
    for notebook in notebooks:
        try:
            if notebook.endswith('.md'):
                # Convert markdown to HTML first, then to PDF
                html_file = f"book_pdf/{Path(notebook).stem}.html"
                pdf_file = f"book_pdf/{Path(notebook).stem}.pdf"
                
                # Convert to HTML
                subprocess.run([
                    "pandoc", notebook, "-o", html_file, "--standalone"
                ], check=True)
                
                # Convert HTML to PDF using Chrome
                subprocess.run([
                    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                    "--headless",
                    "--disable-gpu",
                    f"--print-to-pdf={pdf_file}",
                    "--print-to-pdf-no-header",
                    f"file://{os.path.abspath(html_file)}"
                ], check=True)
                
            else:
                # Convert notebook to PDF
                pdf_file = f"book_pdf/{Path(notebook).stem}.pdf"
                subprocess.run([
                    "jupyter", "nbconvert", "--to", "webpdf", notebook, 
                    "--output-dir", "book_pdf", "--output", f"{Path(notebook).stem}.pdf"
                ], check=True)
            
            print(f"✅ Converted {notebook}")
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error converting {notebook}: {e}")
            success = False
    
    return success

def combine_pdfs():
    """Combine all PDFs into a single book."""
    print("📚 Combining PDFs into single book...")
    
    try:
        result = subprocess.run([
            "python", "scripts/combine_pdfs.py"
        ], check=True, capture_output=True, text=True)
        
        print("✅ PDFs combined successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error combining PDFs: {e}")
        print(f"Error output: {e.stderr}")
        return False

def generate_pdf():
    """Generate complete PDF book."""
    print("📚 Generating complete PDF book...")
    
    # Step 1: Create front matter
    if not create_front_matter():
        return False
    
    # Step 2: Convert notebooks
    if not convert_notebooks():
        return False
    
    # Step 3: Combine PDFs
    if not combine_pdfs():
        return False
    
    print("✅ Complete PDF book generated successfully!")
    print(f"📄 Book location: book_pdf/Slektstre_med_NetworkX_Komplett_Bok.pdf")
    return True

def main():
    """Main function."""
    print("🌳 Slektstre Book Generator")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not os.path.exists("README.md"):
        print("❌ Please run this script from the slektstre repository root")
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Generate PDF
    if generate_pdf():
        print("\n🎉 Book generation complete!")
        print("📖 The PDF book should be available in _build/pdf/")
    else:
        print("\n❌ Book generation failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
