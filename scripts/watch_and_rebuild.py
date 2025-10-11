#!/usr/bin/env python3
"""
File watcher script for automatic book rebuilding when notebooks or README change.
"""

import os
import time
import subprocess
import sys
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class BookRebuildHandler(FileSystemEventHandler):
    """Handler for file changes that trigger book rebuild."""
    
    def __init__(self):
        self.last_rebuild = 0
        self.rebuild_delay = 2  # Wait 2 seconds before rebuilding
        
    def on_modified(self, event):
        """Handle file modification events."""
        if event.is_directory:
            return
            
        # Only watch specific file types
        if not (event.src_path.endswith('.ipynb') or 
                event.src_path.endswith('.md') or
                event.src_path.endswith('.py')):
            return
            
        # Avoid rebuilding too frequently
        current_time = time.time()
        if current_time - self.last_rebuild < self.rebuild_delay:
            return
            
        print(f"\n🔄 Detected change in: {event.src_path}")
        self.rebuild_book()
        self.last_rebuild = current_time
    
    def rebuild_book(self):
        """Rebuild the book."""
        try:
            print("📚 Rebuilding book...")
            
            # Convert notebooks to PDF
            result = subprocess.run([
                "jupyter", "nbconvert", "--to", "webpdf", 
                "notebooks/*.ipynb", "--output-dir=book_pdf"
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"❌ Error converting notebooks: {result.stderr}")
                return
            
            # Convert README to PDF
            readme_result = subprocess.run([
                "python", "-c", 
                """
import subprocess
import os
subprocess.run([
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '--headless', '--disable-gpu',
    '--print-to-pdf=book_pdf/README.pdf',
    '--print-to-pdf-no-header',
    'file://' + os.path.abspath('book_pdf/README.html')
])
                """
            ], capture_output=True, text=True)
            
            # Combine PDFs
            combine_result = subprocess.run([
                "python", "scripts/combine_pdfs.py"
            ], capture_output=True, text=True)
            
            if combine_result.returncode == 0:
                print("✅ Book rebuilt successfully!")
            else:
                print(f"❌ Error combining PDFs: {combine_result.stderr}")
                
        except Exception as e:
            print(f"❌ Error rebuilding book: {e}")

def main():
    """Main function to start the file watcher."""
    print("🌳 Slektstre Book Watcher")
    print("=" * 40)
    print("Watching for changes in notebooks/, README.md, and src/")
    print("Press Ctrl+C to stop")
    print()
    
    # Check if we're in the right directory
    if not os.path.exists("README.md"):
        print("❌ Please run this script from the slektstre repository root")
        sys.exit(1)
    
    # Check if watchdog is installed
    try:
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler
    except ImportError:
        print("❌ watchdog not installed. Install with: pip install watchdog")
        sys.exit(1)
    
    # Set up file watcher
    event_handler = BookRebuildHandler()
    observer = Observer()
    
    # Watch relevant directories
    observer.schedule(event_handler, "notebooks/", recursive=True)
    observer.schedule(event_handler, ".", recursive=False)  # For README.md
    observer.schedule(event_handler, "src/", recursive=True)
    
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping file watcher...")
        observer.stop()
    
    observer.join()
    print("👋 File watcher stopped")

if __name__ == "__main__":
    main()
