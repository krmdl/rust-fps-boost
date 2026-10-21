@echo off
setlocal
title Rust FPS Boost
cd /d "%~dp0"

if not exist "%~dp0tools\apply.ps1" (
  echo Could not find tools\apply.ps1 next to this file.
  echo Extract the whole ZIP first ^(right-click the ZIP ^> Extract All^), then run install.bat from the extracted folder.
  pause & exit /b 1
)

echo.
echo   Rust FPS Boost
echo   --------------
echo   1. Install (detects your graphics card and suggests settings)
echo   2. Preview only (shows what would change, writes nothing)
echo   3. Undo last install
echo   4. Restore my original config (from before the first install)
echo   5. Exit
echo.
choice /c 12345 /n /m "Choose 1-5: "
set "PS=powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0tools\apply.ps1""
if errorlevel 5 exit /b 0
if errorlevel 4 (%PS% -Restore -Original & goto end)
if errorlevel 3 (%PS% -Restore & goto end)
if errorlevel 2 (%PS% -DryRun & goto end)
%PS%

:end
echo.
pause
