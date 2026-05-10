@echo off
REM Windowsでexeを作るためのビルドスクリプト
python -m pip install --upgrade pip
python -m pip install pyinstaller
pyinstaller --onefile --name yoshimoto_shiritori yoshimoto_shiritori_game.py

echo.
echo Build complete. dist\yoshimoto_shiritori.exe を確認してください。
pause
