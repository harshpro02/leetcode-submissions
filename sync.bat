@echo off
REM Double-click this to pull today's accepted submissions and push them.
cd /d "%~dp0"
python pull_submissions.py --push
echo.
pause
