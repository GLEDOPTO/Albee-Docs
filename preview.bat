@echo off
cd /d "%~dp0"
echo Starting local preview server...
start /b "" python -m http.server 8123 --bind 127.0.0.1
timeout /t 2 >nul
start "" http://127.0.0.1:8123/
echo.
echo Preview is running at: http://127.0.0.1:8123/
echo English version:       http://127.0.0.1:8123/en/
echo.
echo Close this window to stop the server.
pause >nul
