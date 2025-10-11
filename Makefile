# Makefile for generating the slektstre book

.PHONY: help install build clean book pdf watch validate

help:
	@echo "🌳 Slektstre Book Generator"
	@echo "=========================="
	@echo "Available commands:"
	@echo "  make install    - Install dependencies"
	@echo "  make build      - Build HTML book"
	@echo "  make pdf        - Generate PDF book"
	@echo "  make book       - Generate both HTML and PDF"
	@echo "  make watch      - Watch for changes and auto-rebuild"
	@echo "  make validate   - Validate book and notebooks"
	@echo "  make clean      - Clean build files"

install:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt

install-book:
	@echo "📦 Installing book generation dependencies only..."
	pip install -r requirements-book.txt

build:
	@echo "📚 Building HTML book..."
	jupyter-book build . --builder html

pdf:
	@echo "📚 Generating PDF book..."
	jupyter-book build . --builder pdfhtml

book: build pdf
	@echo "📚 Building complete book with front matter..."
	@python scripts/generate_book.py

watch:
	@echo "👀 Starting file watcher..."
	python scripts/watch_and_rebuild.py

validate:
	@echo "🔍 Validating book..."
	python scripts/validate_book.py

clean:
	@echo "🧹 Cleaning build files..."
	rm -rf _build/
	rm -rf .jupyter_cache/
	rm -rf book_pdf/

# Default target
all: book
