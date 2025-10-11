#!/usr/bin/env python3
"""
Script to convert audio files to multiple formats for web compatibility.
Converts M4A files to MP3 for maximum browser compatibility.
"""

import os
import subprocess
import sys
from pathlib import Path

def check_ffmpeg():
    """Check if ffmpeg is available."""
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ ffmpeg not found. Please install ffmpeg first:")
        print("   brew install ffmpeg  # macOS")
        print("   apt install ffmpeg  # Ubuntu/Debian")
        return False

def convert_audio(input_file, output_dir="podcast"):
    """Convert M4A file to MP3."""
    if not check_ffmpeg():
        return False
    
    input_path = Path(input_file)
    if not input_path.exists():
        print(f"❌ Input file not found: {input_file}")
        return False
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate output filename
    output_file = input_path.stem + ".mp3"
    output_path = Path(output_dir) / output_file
    
    print(f"🔄 Converting {input_file} to {output_path}")
    
    try:
        subprocess.run([
            'ffmpeg', 
            '-i', str(input_path),
            '-codec:a', 'libmp3lame',
            '-b:a', '128k',
            '-y',  # Overwrite output file
            str(output_path)
        ], check=True)
        
        print(f"✅ Successfully converted to {output_path}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error converting audio: {e}")
        return False

def main():
    """Main function."""
    if len(sys.argv) != 2:
        print("Usage: python convert_audio.py <input_file.m4a>")
        print("Example: python convert_audio.py podcast/episode.m4a")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    if convert_audio(input_file):
        print("🎉 Audio conversion complete!")
    else:
        print("❌ Audio conversion failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
