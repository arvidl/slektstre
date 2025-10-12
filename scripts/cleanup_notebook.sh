#!/bin/bash
# Enhanced Notebook Cleanup Script
# Usage: ./cleanup_notebook.sh [notebook_path]

set -e

# Default notebook path
NOTEBOOK_PATH="${1:-notebooks/00_slektstraer_og_grafer.ipynb}"

echo "🧹 Starting enhanced notebook cleanup..."
echo "📁 Notebook: $NOTEBOOK_PATH"

# Check if notebook exists
if [ ! -f "$NOTEBOOK_PATH" ]; then
    echo "❌ Notebook not found: $NOTEBOOK_PATH"
    exit 1
fi

# Get size before cleanup
SIZE_BEFORE=$(stat -c%s "$NOTEBOOK_PATH")
echo "📊 Size before cleanup: $(echo "scale=1; $SIZE_BEFORE / 1024 / 1024" | bc) MB"

# Run the enhanced cleanup script
python scripts/enhanced_notebook_cleanup.py "$NOTEBOOK_PATH"

# Get size after cleanup
SIZE_AFTER=$(stat -c%s "$NOTEBOOK_PATH")
REDUCTION=$((SIZE_BEFORE - SIZE_AFTER))

echo ""
echo "📊 Final size: $(echo "scale=1; $SIZE_AFTER / 1024 / 1024" | bc) MB"
echo "📉 Total reduction: $(echo "scale=1; $REDUCTION / 1024 / 1024" | bc) MB"

if [ $REDUCTION -gt 1048576 ]; then  # More than 1MB
    echo "🎉 Significant size reduction achieved!"
elif [ $REDUCTION -gt 0 ]; then
    echo "✅ Some cleanup performed"
else
    echo "ℹ️ No significant cleanup needed"
fi

echo "✅ Notebook is ready for commit/push!"
