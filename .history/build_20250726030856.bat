@echo off
REM Clean previous builds
rmdir /s /q build
rmdir /s /q dist
del /q *.spec

REM Build with PyInstaller (no console, with icon)
pyinstaller --onefile --windowed --icon=icon.ico directory_analyzer.py

echo.
echo Build finished. The EXE is in the dist folder.
pause 