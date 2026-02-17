@echo off
echo Building EXIF Geo Data Batch Remover...
echo.

REM 激活虚拟环境
call .venv\Scripts\activate.bat

REM 使用PyInstaller打包
pyinstaller --onefile --console --name "ExifGeoDataBatchRemover" src\exif_geo_remover.py

echo.
echo Build complete! Output: dist\ExifGeoDataBatchRemover.exe
pause
