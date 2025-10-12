# Makefile for slektstre project

.PHONY: help install clean test book book-html book-pdf book-clean book-serve

help:
	@echo "🌳 Slektstre Project"
	@echo "==================="
	@echo "Available commands:"
	@echo "  make install      - Install dependencies"
	@echo "  make test         - Run tests"
	@echo "  make clean        - Clean temporary files"
	@echo ""
	@echo "📚 Book generation:"
	@echo "  make book         - Build both HTML and PDF versions"
	@echo "  make book-html    - Build HTML version only"
	@echo "  make book-pdf     - Build PDF version only"
	@echo "  make book-clean   - Clean book build files"
	@echo "  make book-serve   - Serve HTML book locally"

install:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt

test:
	@echo "🧪 Running tests..."
	python -m pytest tests/ -v

clean:
	@echo "🧹 Cleaning temporary files..."
	rm -rf __pycache__/
	rm -rf .ipynb_checkpoints/
	rm -rf src/__pycache__/
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete
	find . -name "*.pyd" -delete
	find . -name ".DS_Store" -delete

# Book generation commands (using nbconvert as fallback)
book: book-html book-pdf
	@echo "📚 Book generation complete!"
	@echo "📚 HTML version: _build/html/index.html"
	@echo "📚 PDF version: _build/latex/book.pdf"

book-html:
	@echo "🌐 Building HTML version with nbconvert..."
	@mkdir -p _build/html
	@jupyter nbconvert --to html notebooks/*.ipynb --output-dir=_build/html
	@echo "✅ HTML book built successfully!"

book-pdf:
	@echo "📄 Building PDF version..."
	@mkdir -p _build/latex
	@jupyter nbconvert --to pdf notebooks/*.ipynb --output-dir=_build/latex
	@echo "✅ PDF book built successfully!"

book-clean:
	@echo "🧹 Cleaning book build files..."
	rm -rf _build/
	rm -rf .jupyter_cache/
	@echo "✅ Book build files cleaned!"

book-serve:
	@echo "🌐 Serving HTML book locally..."
	@echo "📖 Open http://localhost:8000 in your browser"
	jupyter-book serve _build/html --port 8000