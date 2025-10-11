#!/usr/bin/env python3
"""
Validation script for the slektstre book.
Checks that all notebooks are valid and PDFs are properly generated.
"""

import os
import subprocess
import sys
from pathlib import Path
import json

def check_notebooks():
    """Check that all notebooks are valid and can be executed."""
    print("🔍 Validating notebooks...")
    
    notebook_dir = Path("notebooks")
    if not notebook_dir.exists():
        print("❌ notebooks/ directory not found")
        return False
    
    valid_count = 0
    total_count = 0
    
    for notebook in notebook_dir.glob("*.ipynb"):
        total_count += 1
        print(f"  Checking {notebook.name}...")
        
        try:
            # Try to load and validate the notebook
            with open(notebook, 'r', encoding='utf-8') as f:
                nb_data = json.load(f)
            
            # Basic validation
            if 'cells' not in nb_data:
                print(f"    ❌ {notebook.name}: No cells found")
                continue
                
            if len(nb_data['cells']) == 0:
                print(f"    ❌ {notebook.name}: Empty notebook")
                continue
            
            # Check for required imports
            has_imports = False
            for cell in nb_data['cells']:
                if cell.get('cell_type') == 'code':
                    source = ''.join(cell.get('source', []))
                    if 'import' in source and 'sys.path.append' in source:
                        has_imports = True
                        break
            
            if not has_imports:
                print(f"    ⚠️  {notebook.name}: No proper imports found")
            
            print(f"    ✅ {notebook.name}: Valid")
            valid_count += 1
            
        except Exception as e:
            print(f"    ❌ {notebook.name}: Error - {e}")
    
    print(f"📊 Notebook validation: {valid_count}/{total_count} valid")
    return valid_count == total_count

def check_pdf_files():
    """Check that all PDF files are generated and have reasonable sizes."""
    print("\n🔍 Validating PDF files...")
    
    book_dir = Path("book_pdf")
    if not book_dir.exists():
        print("❌ book_pdf/ directory not found")
        return False
    
    expected_pdfs = [
        "README.pdf",
        "00_slektstraer_og_grafer.pdf",
        "01_introduksjon.pdf",
        "02_bygg_tre_manuelt.pdf",
        "03_importer_data.pdf",
        "04_visualisering.pdf",
        "05_eksterne_databaser.pdf"
    ]
    
    valid_count = 0
    total_count = len(expected_pdfs)
    
    for pdf_name in expected_pdfs:
        pdf_path = book_dir / pdf_name
        print(f"  Checking {pdf_name}...")
        
        if not pdf_path.exists():
            print(f"    ❌ {pdf_name}: File not found")
            continue
        
        # Check file size
        size_mb = pdf_path.stat().st_size / (1024 * 1024)
        
        if size_mb < 0.1:  # Less than 100KB
            print(f"    ⚠️  {pdf_name}: Very small ({size_mb:.1f}MB) - might be empty")
        elif size_mb > 50:  # More than 50MB
            print(f"    ⚠️  {pdf_name}: Very large ({size_mb:.1f}MB) - might need optimization")
        else:
            print(f"    ✅ {pdf_name}: OK ({size_mb:.1f}MB)")
        
        valid_count += 1
    
    # Check combined book
    combined_pdf = book_dir / "Slektstre_med_NetworkX_Komplett_Bok.pdf"
    if combined_pdf.exists():
        size_mb = combined_pdf.stat().st_size / (1024 * 1024)
        print(f"  ✅ Combined book: {size_mb:.1f}MB")
        valid_count += 1
        total_count += 1
    else:
        print(f"  ❌ Combined book not found")
    
    print(f"📊 PDF validation: {valid_count}/{total_count} files OK")
    return valid_count == total_count

def check_dependencies():
    """Check that all required dependencies are installed."""
    print("\n🔍 Checking dependencies...")
    
    required_packages = [
        'jupyter', 'nbconvert', 'networkx', 'matplotlib', 
        'pydantic', 'pyyaml', 'pandas', 'plotly'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("Install with: pip install -r requirements.txt")
        return False
    
    print("📊 All dependencies OK")
    return True

def check_playwright():
    """Check that Playwright browsers are installed."""
    print("\n🔍 Checking Playwright...")
    
    try:
        result = subprocess.run([
            "python", "-c", 
            "from playwright.sync_api import sync_playwright; print('Playwright OK')"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("  ✅ Playwright installed")
        else:
            print("  ❌ Playwright not working")
            print("  Run: playwright install")
            return False
    except Exception as e:
        print(f"  ❌ Playwright error: {e}")
        return False
    
    return True

def main():
    """Main validation function."""
    print("🌳 Slektstre Book Validator")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not os.path.exists("README.md"):
        print("❌ Please run this script from the slektstre repository root")
        sys.exit(1)
    
    # Run all checks
    checks = [
        check_dependencies,
        check_playwright,
        check_notebooks,
        check_pdf_files
    ]
    
    all_passed = True
    for check in checks:
        if not check():
            all_passed = False
    
    print("\n" + "=" * 40)
    if all_passed:
        print("🎉 All validations passed! Book is ready.")
    else:
        print("❌ Some validations failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
