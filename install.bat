@echo off
setlocal
cd /d "%~dp0"
set "GAME_DIR=%CD%"

title JA2 r7609 Korean Patch Installer

if not exist "%GAME_DIR%\install.ps1" (
    echo [ERROR] install.ps1 was not found.
    echo Keep install.bat and install.ps1 in the same folder.
    echo.
    pause
    exit /b 1
)

if not exist "%GAME_DIR%\Patch\" (
    echo [ERROR] Patch folder was not found.
    echo Copy the full patch package into the JA2 installation folder first.
    echo.
    pause
    exit /b 1
)

if not exist "%GAME_DIR%\Ja2.ini" (
    echo [ERROR] Ja2.ini was not found in:
    echo %GAME_DIR%
    echo.
    echo Put this installer and the Patch folder directly in the
    echo Jagged Alliance 2 v1.13 r7609 installation folder, then run again.
    echo.
    pause
    exit /b 1
)

if not exist "%GAME_DIR%\ja2.exe" (
    echo [ERROR] ja2.exe was not found in:
    echo %GAME_DIR%
    echo.
    echo This does not look like the JA2 r7609 installation folder.
    echo.
    pause
    exit /b 1
)

echo JA2 r7609 Korean Patch
echo Install folder: %GAME_DIR%
echo.
echo Starting installation...
echo.

powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%GAME_DIR%\install.ps1" -GamePath "%GAME_DIR%"
set "EXITCODE=%ERRORLEVEL%"

echo.
if not "%EXITCODE%"=="0" (
    echo [ERROR] Installation failed. Error code: %EXITCODE%
    echo If the game is under Program Files, try right-clicking install.bat
    echo and choosing "Run as administrator".
    echo.
    pause
    exit /b %EXITCODE%
)

echo Installation completed successfully.
echo You can now launch ja2.exe.
echo.
pause
exit /b 0
