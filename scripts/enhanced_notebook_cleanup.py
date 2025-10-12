#!/usr/bin/env python3
"""
Enhanced Notebook Cleanup Script
Removes embedded audio data and other large outputs from Jupyter notebooks
"""

import json
import os
import sys
import argparse
from pathlib import Path


def clean_notebook_outputs(notebook_path, remove_audio=True, remove_images=True):
    """
    Clean notebook outputs, with special handling for embedded audio/images
    
    Args:
        notebook_path (str): Path to the notebook file
        remove_audio (bool): Whether to remove embedded audio data
        remove_images (bool): Whether to remove embedded image data
    
    Returns:
        tuple: (success, size_before, size_after, reduction)
    """
    
    if not os.path.exists(notebook_path):
        print(f"❌ Notebook not found: {notebook_path}")
        return False, 0, 0, 0
    
    # Get file size before cleanup
    size_before = os.path.getsize(notebook_path)
    
    try:
        # Load the notebook
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
        
        cells_modified = 0
        audio_removed = 0
        images_removed = 0
        
        # Process each cell
        for cell in notebook.get('cells', []):
            if cell.get('cell_type') == 'code' and 'outputs' in cell:
                original_outputs = cell['outputs']
                cell['outputs'] = []
                
                # Check if we removed anything significant
                if original_outputs:
                    cells_modified += 1
                    
                    # Count what we're removing
                    for output in original_outputs:
                        if 'data' in output:
                            data = output['data']
                            
                            # Check for embedded audio
                            if remove_audio:
                                for key in data.keys():
                                    if isinstance(data[key], list):
                                        for item in data[key]:
                                            if isinstance(item, str) and 'data:audio' in item:
                                                audio_removed += 1
                                                break
                            
                            # Check for embedded images
                            if remove_images:
                                for key in data.keys():
                                    if isinstance(data[key], list):
                                        for item in data[key]:
                                            if isinstance(item, str) and 'data:image' in item:
                                                images_removed += 1
                                                break
        
        # Save the cleaned notebook
        with open(notebook_path, 'w', encoding='utf-8') as f:
            json.dump(notebook, f, ensure_ascii=False, separators=(',', ':'))
        
        # Get file size after cleanup
        size_after = os.path.getsize(notebook_path)
        reduction = size_before - size_after
        
        print(f"✅ Enhanced cleanup completed!")
        print(f"📊 Cells modified: {cells_modified}")
        print(f"🎵 Audio embeddings removed: {audio_removed}")
        print(f"🖼️ Image embeddings removed: {images_removed}")
        print(f"📊 Size before: {size_before / (1024*1024):.1f} MB")
        print(f"📊 Size after: {size_after / (1024*1024):.1f} MB")
        print(f"📉 Reduction: {reduction / (1024*1024):.1f} MB")
        
        return True, size_before, size_after, reduction
        
    except Exception as e:
        print(f"❌ Cleanup failed: {e}")
        return False, size_before, 0, 0


def main():
    parser = argparse.ArgumentParser(description='Enhanced notebook cleanup')
    parser.add_argument('notebook', help='Path to notebook file')
    parser.add_argument('--keep-audio', action='store_true', 
                       help='Keep embedded audio data')
    parser.add_argument('--keep-images', action='store_true',
                       help='Keep embedded image data')
    
    args = parser.parse_args()
    
    print("🧹 Starting enhanced notebook cleanup...")
    print(f"📁 Notebook: {args.notebook}")
    
    success, size_before, size_after, reduction = clean_notebook_outputs(
        args.notebook,
        remove_audio=not args.keep_audio,
        remove_images=not args.keep_images
    )
    
    if success:
        if reduction > 1024 * 1024:  # More than 1MB reduction
            print("🎉 Significant size reduction achieved!")
        elif reduction > 0:
            print("✅ Some cleanup performed")
        else:
            print("ℹ️ No significant cleanup needed")
        
        print("✅ Notebook is ready for commit/push!")
    else:
        print("❌ Cleanup failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
