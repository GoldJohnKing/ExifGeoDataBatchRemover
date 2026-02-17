#!/bin/bash
# WSL中编译Windows exe脚本
# 通过调用Windows上的Python/uv来生成exe

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WIN_PATH="$(wslpath -w "$SCRIPT_DIR")"

echo "Building EXIF Geo Data Batch Remover for Windows..."
echo "Project path: $WIN_PATH"
echo

# 使用Windows的uv创建venv并打包
cmd.exe /c "cd /d $WIN_PATH && uv venv .venv-win && .venv-win\\Scripts\\activate && uv pip install piexif pyinstaller && pyinstaller --onefile --console --name ExifGeoDataBatchRemover src\\exif_geo_remover.py"

echo
echo "Build complete!"
echo "Output: $SCRIPT_DIR/dist/ExifGeoDataBatchRemover.exe"
