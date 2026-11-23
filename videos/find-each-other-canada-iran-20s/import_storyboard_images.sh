#!/usr/bin/env bash
# Import the approved, separately delivered storyboard frames into this project.
# This deliberately DOES NOT create a video or run GitHub Actions.
set -euo pipefail
SRC="${1:?Usage: bash import_storyboard_images.sh /path/to/storyboard_frames}"
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="$PROJECT_DIR/assets/storyboard_frames"
mkdir -p "$TARGET"
for name in \
  01_hook_canada.png \
  02_airport_traveler.png \
  03_advertio_entry.png \
  04_connection_message.png \
  05_plane_cta.png; do
  if [[ ! -s "$SRC/$name" ]]; then echo "Missing source: $SRC/$name" >&2; exit 1; fi
  cp "$SRC/$name" "$TARGET/$name"
  echo "Imported: $name"
done
echo "All five images imported. Review before git add/commit."
