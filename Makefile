# Makefile for slektstre project

.PHONY: help install clean test

help:
	@echo "🌳 Slektstre Project"
	@echo "==================="
	@echo "Available commands:"
	@echo "  make install    - Install dependencies"
	@echo "  make test       - Run tests"
	@echo "  make clean      - Clean temporary files"

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