#!/bin/bash
# Script for generating PDF book from slektstre repository

echo "🌳 Slektstre Book Generator"
echo "=========================="

# Check if we're in the right directory
if [ ! -f "README.md" ]; then
    echo "❌ Please run this script from the slektstre repository root"
    exit 1
fi

# Install dependencies if needed
echo "📦 Installing dependencies..."
pip install -r requirements-book.txt

# Check if LaTeX is installed
if ! command -v xelatex &> /dev/null; then
    echo "⚠️  LaTeX not found. Please install LaTeX:"
    echo "   macOS: brew install --cask mactex"
    echo "   Ubuntu: sudo apt-get install texlive-full"
    echo "   Windows: Install MiKTeX or TeX Live"
    exit 1
fi

# Generate the book
echo "📚 Generating PDF book..."
jupyter-book build . --builder pdfhtml

if [ $? -eq 0 ]; then
    echo "✅ PDF generated successfully!"
    echo "📄 Book location: _build/pdf/"
    echo "📖 Main PDF: _build/pdf/slektstre-med-networkx-en-komplett-guide.pdf"
else
    echo "❌ PDF generation failed"
    exit 1
fi
