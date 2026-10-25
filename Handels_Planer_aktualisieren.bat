@echo off
REM SC Handels-Planer neu bauen (Preise live von star-head.de ziehen).
cd /d "%~dp0"
py handels_planer_bauen.py
if errorlevel 1 (
  echo.
  echo FEHLER beim Bauen - bitte Internetverbindung pruefen.
  pause
  exit /b 1
)
echo.
echo Fertig. SC_Handels_Planer.html wurde aktualisiert.
pause
