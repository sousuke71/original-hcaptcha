@echo off
REM WindowsでGUIアプリのexeを作るビルドスクリプト
python -m pip install --upgrade pip
python -m pip install pyinstaller
pyinstaller --onefile --windowed --name yoshimoto_shiritori_app yoshimoto_shiritori_app.py

echo.
echo Build complete. dist\yoshimoto_shiritori_app.exe を確認してください。
pause
