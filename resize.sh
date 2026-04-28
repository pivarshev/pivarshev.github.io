#!/bin/bash
#
# Image resize script
# Run this after adding new full-res images to artworks_full/
# It creates medium (~2000px) and small (~400px) versions.
#
# Usage:
#   cd /path/to/pivarshev.github.io
#   bash resize.sh
#
# Or resize just one folder:
#   bash resize.sh grids
#

FOLDER="$1"

if [ -n "$FOLDER" ]; then
    SEARCH="artworks_full/$FOLDER"
else
    SEARCH="artworks_full"
fi

echo "Resizing images from $SEARCH..."

find "$SEARCH" -type f -name "*.jpg" | while read fullpath; do
    # Get the relative path after artworks_full/
    relpath="${fullpath#artworks_full/}"

    # Medium version (~2000px) → artworks/
    medium="artworks/$relpath"
    mkdir -p "$(dirname "$medium")"
    if [ ! -f "$medium" ] || [ "$fullpath" -nt "$medium" ]; then
        cp "$fullpath" "$medium"
        sips --resampleHeightWidthMax 2000 "$medium" --out "$medium" >/dev/null 2>&1
        echo "  medium: $medium"
    fi

    # Small version (~400px) → artworks_small/
    small="artworks_small/$relpath"
    mkdir -p "$(dirname "$small")"
    if [ ! -f "$small" ] || [ "$fullpath" -nt "$small" ]; then
        cp "$fullpath" "$small"
        sips --resampleHeightWidthMax 400 "$small" --out "$small" >/dev/null 2>&1
        echo "  small:  $small"
    fi
done

echo ""
echo "Done. Three versions of each image:"
echo "  artworks_full/  → original (for zoom/download)"
echo "  artworks/       → medium ~2000px (upgrades after page loads)"
echo "  artworks_small/ → small ~400px (loads first, fast)"
